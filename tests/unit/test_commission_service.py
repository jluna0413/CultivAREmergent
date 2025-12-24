import pytest
from app.services.commission_service import CommissionService
from app.models_async.breeders import MarketplaceBreeder

class TestCommissionService:
    
    def test_starter_tier(self):
        breeder = MarketplaceBreeder(current_tier="Starter", fee_override=None, active_buffs=None)
        rate = CommissionService.calculate_commission_from_model(breeder)
        assert rate == 0.25

    def test_mover_tier(self):
        breeder = MarketplaceBreeder(current_tier="Mover", fee_override=None, active_buffs=None)
        rate = CommissionService.calculate_commission_from_model(breeder)
        assert rate == 0.20

    def test_shaker_tier(self):
        breeder = MarketplaceBreeder(current_tier="Shaker", fee_override=None, active_buffs=None)
        rate = CommissionService.calculate_commission_from_model(breeder)
        assert rate == 0.15
        
    def test_market_maker_tier(self):
        breeder = MarketplaceBreeder(current_tier="Market Maker", fee_override=None, active_buffs=None)
        rate = CommissionService.calculate_commission_from_model(breeder)
        assert rate == 0.10

    def test_fee_override(self):
        # Override takes precedence (e.g. 5% = 500 bps)
        breeder = MarketplaceBreeder(current_tier="Starter", fee_override=500, active_buffs=None)
        rate = CommissionService.calculate_commission_from_model(breeder)
        assert rate == 0.05

    def test_active_buff(self):
        # Starter (25%) with 1% reduction buff
        buffs = '[{"name": "Early Bird", "reduction": 1.0}]'
        breeder = MarketplaceBreeder(current_tier="Starter", fee_override=None, active_buffs=buffs)
        rate = CommissionService.calculate_commission_from_model(breeder)
        assert rate == 0.24

    def test_fee_floor(self):
        # Ensure it doesn't drop below floor (5%)
        # Starter (25%) with huge reduction (30%) -> Should cap at 5%
        buffs = '[{"name": "Super Buff", "reduction": 30.0}]'
        breeder = MarketplaceBreeder(current_tier="Starter", fee_override=None, active_buffs=buffs)
        rate = CommissionService.calculate_commission_from_model(breeder)
        assert rate == 0.05
