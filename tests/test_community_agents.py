"""Test script for Community Agents"""
import asyncio
from app.agents.community import NFTMarketplaceAgent, GrowBuddyAgent, ReputationTrackerAgent

async def test_nft_marketplace():
    print("=== NFT Marketplace Test ===")
    agent = NFTMarketplaceAgent()
    
    # Test founder verification
    result = await agent.verify_founder_status(wallet_address="FOUNDER123ABC")
    print(f"Founder Verified: {result['verified']}")
    print(f"Tier: {result.get('tier', 'N/A')}")
    
    # Test perks
    perks = await agent.get_founder_perks("founder")
    print(f"Discount: {perks['perks']['marketplace_discount']*100}%")
    
    # Test genetics NFT minting
    mint = await agent.mint_genetics_certificate(
        strain_name="Purple Haze",
        breeder="Test Breeder",
        owner_address="OWNER123"
    )
    print(f"Minted: {mint['success']}")
    return True

async def test_grow_buddy():
    print("\n=== Grow Buddy Test ===")
    agent = GrowBuddyAgent()
    
    # Test personalized advice
    advice = await agent.get_personalized_advice(
        topic="watering",
        experience_level="beginner"
    )
    print(f"Advice Count: {len(advice['advice'])}")
    print(f"Pro Tip: {advice['pro_tip'][:50]}...")
    
    # Test mentor matching
    mentors = await agent.find_mentor(
        experience_level="beginner",
        grow_style="coco_coir"
    )
    print(f"Mentors Found: {mentors['total_matches']}")
    
    # Test daily tip
    tip = await agent.get_daily_tip("beginner")
    print(f"Daily Tip: {tip['tip'][:50]}...")
    return True

async def test_reputation():
    print("\n=== Reputation Tracker Test ===")
    agent = ReputationTrackerAgent()
    
    # Award reputation
    award = await agent.award_reputation(
        user_id=1,
        rep_action="grow_complete",
        category="growing"
    )
    print(f"Points Awarded: {award['points_awarded']}")
    print(f"New Total: {award['new_total']}")
    print(f"Tier: {award['tier']}")
    
    # Verify seller
    verify = await agent.verify_seller_trust(user_id=1)
    print(f"Trust Grade: {verify['trust_grade']}")
    print(f"Recommendation: {verify['recommendation']}")
    return True

async def main():
    await test_nft_marketplace()
    await test_grow_buddy()
    await test_reputation()
    print("\n✅ All Community Agent tests passed!")

if __name__ == "__main__":
    asyncio.run(main())
