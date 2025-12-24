"""
Database migration script for gamification tables.

Run this script to create the gamification tables:
    python scripts/migrate_gamification.py
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text


async def migrate():
    """Create gamification tables."""
    from app.models_async.base import async_engine
    
    # SQL statements to create tables
    statements = [
        """
        CREATE TABLE IF NOT EXISTS user_xp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            total_xp INTEGER NOT NULL DEFAULT 0,
            level INTEGER NOT NULL DEFAULT 1,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_user_xp_user_id ON user_xp(user_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS xp_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_xp_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            source VARCHAR(100) NOT NULL,
            description VARCHAR(255),
            extra_data JSON,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_xp_id) REFERENCES user_xp(id)
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_xp_transactions_user_xp_id ON xp_transactions(user_xp_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_id VARCHAR(50) NOT NULL,
            category VARCHAR(20) NOT NULL,
            xp_awarded INTEGER NOT NULL DEFAULT 0,
            nft_unlocked VARCHAR(100),
            progress FLOAT NOT NULL DEFAULT 1.0,
            is_complete BOOLEAN NOT NULL DEFAULT 1,
            unlocked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_user_achievements_user_id ON user_achievements(user_id)
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_user_achievements_achievement_id ON user_achievements(achievement_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS user_streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            current_streak INTEGER NOT NULL DEFAULT 0,
            longest_streak INTEGER NOT NULL DEFAULT 0,
            total_checkins INTEGER NOT NULL DEFAULT 0,
            last_checkin DATETIME,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_user_streaks_user_id ON user_streaks(user_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS checkin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            streak_id INTEGER NOT NULL,
            checkin_date DATETIME NOT NULL,
            plants_checked INTEGER DEFAULT 0,
            photos_uploaded INTEGER DEFAULT 0,
            environment_logged BOOLEAN DEFAULT 0,
            notes TEXT,
            base_xp INTEGER DEFAULT 10,
            bonus_xp INTEGER DEFAULT 0,
            streak_bonus INTEGER DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (streak_id) REFERENCES user_streaks(id)
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_checkin_logs_streak_id ON checkin_logs(streak_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS agent_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id VARCHAR(50) NOT NULL UNIQUE,
            total_executions INTEGER NOT NULL DEFAULT 0,
            successful_executions INTEGER NOT NULL DEFAULT 0,
            user_feedback_positive INTEGER NOT NULL DEFAULT 0,
            user_feedback_negative INTEGER NOT NULL DEFAULT 0,
            avg_confidence FLOAT NOT NULL DEFAULT 0.0,
            outcome_accuracy FLOAT NOT NULL DEFAULT 0.0,
            avg_execution_time_ms INTEGER NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_agent_metrics_agent_id ON agent_metrics(agent_id)
        """,
        # Marketplace tables (foundation for auction house)
        """
        CREATE TABLE IF NOT EXISTS marketplace_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER NOT NULL,
            seller_type VARCHAR(20) NOT NULL DEFAULT 'house',
            title VARCHAR(200) NOT NULL,
            description TEXT,
            listing_type VARCHAR(30) NOT NULL DEFAULT 'fixed_price',
            strain_name VARCHAR(100) NOT NULL,
            breeder_name VARCHAR(100),
            seed_count INTEGER DEFAULT 1,
            seed_type VARCHAR(50),
            price FLOAT,
            nft_asset_id VARCHAR(100),
            nft_required BOOLEAN DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            quantity_available INTEGER DEFAULT 1,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (seller_id) REFERENCES users(id)
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_marketplace_listings_seller_id ON marketplace_listings(seller_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS auctions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            listing_id INTEGER NOT NULL UNIQUE,
            starting_price FLOAT NOT NULL,
            reserve_price FLOAT,
            buy_now_price FLOAT,
            bid_increment FLOAT DEFAULT 1.00,
            current_bid FLOAT,
            current_bidder_id INTEGER,
            bid_count INTEGER DEFAULT 0,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL,
            extended_end_time DATETIME,
            status VARCHAR(20) NOT NULL DEFAULT 'draft',
            winner_id INTEGER,
            final_price FLOAT,
            allow_extensions BOOLEAN DEFAULT 1,
            extension_minutes INTEGER DEFAULT 5,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (listing_id) REFERENCES marketplace_listings(id),
            FOREIGN KEY (current_bidder_id) REFERENCES users(id),
            FOREIGN KEY (winner_id) REFERENCES users(id)
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_auctions_listing_id ON auctions(listing_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS auction_bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            auction_id INTEGER NOT NULL,
            bidder_id INTEGER NOT NULL,
            amount FLOAT NOT NULL,
            is_winning BOOLEAN DEFAULT 0,
            is_auto_bid BOOLEAN DEFAULT 0,
            ip_address VARCHAR(50),
            user_agent VARCHAR(255),
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (auction_id) REFERENCES auctions(id),
            FOREIGN KEY (bidder_id) REFERENCES users(id)
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_auction_bids_auction_id ON auction_bids(auction_id)
        """,
        """
        CREATE TABLE IF NOT EXISTS auction_watches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            auction_id INTEGER NOT NULL,
            notify_outbid BOOLEAN DEFAULT 1,
            notify_ending BOOLEAN DEFAULT 1,
            notify_ended BOOLEAN DEFAULT 1,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (auction_id) REFERENCES auctions(id)
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_auction_watches_user_id ON auction_watches(user_id)
        """,
    ]
    
    async with async_engine.begin() as conn:
        for stmt in statements:
            try:
                await conn.execute(text(stmt.strip()))
                print(f"✓ Executed: {stmt.split()[0:5]}...")
            except Exception as e:
                print(f"✗ Error: {e}")
                
    print("\n✅ Gamification tables migration complete!")


if __name__ == "__main__":
    asyncio.run(migrate())
