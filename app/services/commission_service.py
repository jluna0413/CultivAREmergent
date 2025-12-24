import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models_async.breeders import MarketplaceBreeder
from app.models_async.sales import SalesTransaction
from datetime import datetime, timedelta

class CommissionService:
    """
    Handles tiered commission calculations and breeder progression based on MONTHLY performance.
    Tiers: Starter, Mover, Shaker, Market Maker.
    """
    
    TIERS = {
        "Starter": {"fee": 25.0},
        "Mover": {"fee": 20.0, "sales_req": 10, "rating_req": 450}, # 4.5 * 100
        "Shaker": {"fee": 15.0, "sales_req": 50, "rating_req": 480}, # 4.8 * 100
        "Market Maker": {"fee": 10.0, "sales_req": 500, "rating_req": 500} # Manual/Top 1%
    }
    
    FEE_FLOOR = 5.0

    @staticmethod
    async def calculate_commission(db: AsyncSession, breeder_id: int) -> float:
        """
        Calculate the commission percentage (decimal) for a specific breeder.
        Considers Tier, Active Buffs, and Overrides.
        """
        stmt = select(MarketplaceBreeder).where(MarketplaceBreeder.id == breeder_id)
        result = await db.execute(stmt)
        breeder = result.scalar_one_or_none()
        
        if not breeder:
            return 0.25 # Default fallback (Starter)
            
        return CommissionService.calculate_commission_from_model(breeder)

    @staticmethod
    def calculate_commission_from_model(breeder: MarketplaceBreeder) -> float:
        """
        Sync helper to calc commission from loaded model.
        """
        # 1. Custom Override
        if breeder.fee_override is not None:
            return float(breeder.fee_override) / 10000.0 # basis points
            
        # 2. Base Tier Fee
        tier_data = CommissionService.TIERS.get(breeder.current_tier, CommissionService.TIERS["Starter"])
        base_fee = tier_data["fee"]
        
        # 3. Apply Buffs
        active_fee = base_fee
        if breeder.active_buffs:
            try:
                buffs = json.loads(breeder.active_buffs)
                for buff in buffs:
                    # Example buff: {"name": "Hot Streak", "reduction": 1.0, "expires": "..."}
                    active_fee -= buff.get("reduction", 0.0)
            except json.JSONDecodeError:
                pass 
        
    @staticmethod
    async def get_daily_sales_history(db: AsyncSession, breeder_user_id: int, days: int = 30) -> list[dict]:
        """
        Get daily sales volume for the last N days.
        Returns list of dicts: [{"date": "ISO", "amount": float, "count": int}]
        """
        now = datetime.utcnow()
        # To get exactly 'days' points ending with Today:
        # Start = Today - (days - 1)
        start_date = now - timedelta(days=days - 1)
        
        # Aggregate by day
        stmt = (
            select(
                func.date(SalesTransaction.created_at).label("day"),
                func.sum(SalesTransaction.total_amount).label("total"),
                func.count(SalesTransaction.id).label("count")
            )
            .where(
                SalesTransaction.seller_user_id == breeder_user_id,
                SalesTransaction.status == "COMPLETED", # Enum usage ideally
                SalesTransaction.created_at >= start_date
            )
            .group_by("day")
            .order_by("day")
        )
        
        result = await db.execute(stmt)
        rows = result.all()
        
        # Convert to dict lookup
        data_map = {str(row.day): {"amount": row.total, "count": row.count} for row in rows}
        
        # Fill missing days with 0
        history = []
        for i in range(days):
            d = (start_date + timedelta(days=i)).date()
            d_str = str(d)
            entry = data_map.get(d_str, {"amount": 0.0, "count": 0})
            history.append({
                "date": d_str,
                "amount": float(entry["amount"]),
                "count": entry["count"]
            })
            
        return history

    @staticmethod
    async def update_breeder_metrics(db: AsyncSession, breeder_id: int, new_sale_amount: int):
        """
        Update sales stats and check for Tier Promotion based on MONTHLY SALES.
        Note: Demotions would happen in a scheduled monthly job (not here).
        This function only handles mid-month promotions.
        """
        stmt = select(MarketplaceBreeder).where(MarketplaceBreeder.id == breeder_id)
        result = await db.execute(stmt)
        breeder = result.scalar_one_or_none()
        
        if not breeder:
            return

        # Update Stats
        breeder.total_sales += 1
        breeder.total_revenue += new_sale_amount
        breeder.month_sales += 1 # Track monthly progress
        
        # Check Progression
        current_tier = breeder.current_tier
        sales = breeder.month_sales # Use Monthly Sales
        rating = 500 # Mock rating
        
        new_tier = current_tier
        
        # Threshold Checks (Promotions Only)
        # Logic: Check highest tier first
        if sales >= 50 and rating >= 480:
             # Prevent skipping if we want sequential? No, jumping is fine.
             new_tier = "Shaker"
             # Market Maker (Top 1%) is manual or separate process, but Shaker is auto.
        elif sales >= 10 and rating >= 450:
             if current_tier == "Starter":
                 new_tier = "Mover"
        
        if new_tier != current_tier:
            # We assume promotions happen immediately, resets happen monthly
            # Check if this is an upgrade (we don't downgrade here to avoid flip-flopping)
            tier_ranks = ["Starter", "Mover", "Shaker", "Market Maker"]
            try:
                curr_rank = tier_ranks.index(current_tier)
                new_rank = tier_ranks.index(new_tier)
                if new_rank > curr_rank:
                     breeder.current_tier = new_tier
                     print(f"🎉 Breeder {breeder.breeder_name} promoted to {new_tier}!")
            except ValueError:
                pass # Unknown tier
            
        await db.commit()
