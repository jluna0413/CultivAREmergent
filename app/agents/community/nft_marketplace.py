"""
NFT Marketplace Agent

Manages NFT-linked genetics, Founder NFT perks, and Algorand marketplace operations.

Part of Community Agents.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import logging

from pydantic import BaseModel, Field

from ..base import (
    AgentRole,
    AgentContext,
    AgentResult,
    BaseAgent,
    AgentRegistry,
)
from ...gamification import gamification_engine

logger = logging.getLogger(__name__)


class NFTTier(str, Enum):
    """NFT collection tiers"""
    FOUNDER = "founder"
    GENESIS = "genesis"
    PREMIUM = "premium"
    STANDARD = "standard"


class NFTType(str, Enum):
    """Types of NFTs in the ecosystem"""
    FOUNDER_PASS = "founder_pass"
    GENETICS_CERTIFICATE = "genetics_certificate"
    GROW_BADGE = "grow_badge"
    ACHIEVEMENT_TROPHY = "achievement_trophy"
    BREEDER_VERIFIED = "breeder_verified"


class FounderPerks(BaseModel):
    """Perks for Founder NFT holders"""
    marketplace_discount: float = Field(default=0.15, description="15% discount")
    exclusive_drops_access: bool = True
    priority_auction_bidding: bool = True
    verified_badge: bool = True
    governance_voting: bool = True
    monthly_seed_airdrops: bool = True
    private_discord_access: bool = True
    early_feature_access: bool = True


class NFTAsset(BaseModel):
    """NFT asset on Algorand"""
    asset_id: int
    name: str
    tier: NFTTier
    nft_type: NFTType
    owner_address: str
    metadata_uri: str
    created_at: datetime
    traits: Dict[str, Any] = Field(default_factory=dict)


class NFTMarketplaceAgent(BaseAgent):
    """
    NFT marketplace and Algorand integration agent.
    
    Capabilities:
    - Founder NFT verification and perks
    - Genetics NFT minting
    - Marketplace NFT listings
    - Auction house integration
    - NFT-gated access control
    
    Integrates with:
    - Algorand blockchain (via algorand_server.py)
    - Marketplace models
    - Gamification (achievement NFTs)
    """
    
    def __init__(self):
        super().__init__(
            agent_id="nft_marketplace",
            name="NFT Marketplace",
            role=AgentRole.COMMUNITY,
            description="NFT-linked genetics and Algorand marketplace operations",
        )
        
        # Register MCP tools
        self.register_tool(
            "verify_founder",
            self.verify_founder_status,
            "Verify if user holds Founder NFT"
        )
        self.register_tool(
            "get_perks",
            self.get_founder_perks,
            "Get perks for NFT tier"
        )
        self.register_tool(
            "mint_genetics_nft",
            self.mint_genetics_certificate,
            "Mint genetics certificate NFT"
        )
        self.register_tool(
            "list_user_nfts",
            self.list_user_nfts,
            "List all NFTs owned by user"
        )
        self.register_tool(
            "check_access",
            self.check_nft_gated_access,
            "Check if user has access to NFT-gated feature"
        )
        
        # Mock NFT database (would connect to Algorand indexer)
        self._nft_holdings: Dict[str, List[Dict]] = {}
        self._founder_addresses = set()  # Addresses that hold Founder NFTs
        
    async def execute(self, context: AgentContext, **kwargs) -> AgentResult:
        """Execute NFT marketplace operation"""
        action = kwargs.get("action", "verify")
        
        try:
            if action == "verify":
                result = await self.verify_founder_status(
                    wallet_address=kwargs.get("wallet_address"),
                    user_id=context.user_id,
                )
            elif action == "perks":
                result = await self.get_founder_perks(
                    nft_tier=kwargs.get("nft_tier", "founder"),
                )
            elif action == "mint":
                result = await self.mint_genetics_certificate(
                    strain_name=kwargs.get("strain_name"),
                    breeder=kwargs.get("breeder"),
                    owner_address=kwargs.get("owner_address"),
                    metadata=kwargs.get("metadata", {}),
                )
            elif action == "list":
                result = await self.list_user_nfts(
                    wallet_address=kwargs.get("wallet_address"),
                )
            elif action == "access":
                result = await self.check_nft_gated_access(
                    wallet_address=kwargs.get("wallet_address"),
                    feature=kwargs.get("feature", "exclusive_drops"),
                )
            else:
                result = {"error": f"Unknown action: {action}"}
                
            # Award XP for NFT interactions
            if context.user_id:
                gamification_engine.award_xp(
                    context.user_id, 10, "nft_interaction"
                )
                
            return AgentResult(
                success=True,
                agent_id=self.agent_id,
                output=result,
                confidence=0.95,
                xp_reward=10,
                next_actions=["view_marketplace", "mint_nft", "claim_perks"],
            )
            
        except Exception as e:
            logger.error(f"NFTMarketplace error: {e}")
            return AgentResult(
                success=False,
                agent_id=self.agent_id,
                output=None,
                error=str(e),
            )
    
    async def verify_founder_status(
        self,
        wallet_address: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Verify if user holds a Founder NFT.
        
        In production, queries Algorand indexer for NFT holdings.
        """
        if not wallet_address:
            return {
                "verified": False,
                "reason": "No wallet address provided",
                "help": "Connect your Algorand wallet to verify Founder status",
            }
            
        # Mock verification (would query Algorand)
        is_founder = wallet_address in self._founder_addresses or wallet_address.startswith("FOUNDER")
        
        if is_founder:
            return {
                "verified": True,
                "tier": NFTTier.FOUNDER.value,
                "wallet_address": wallet_address,
                "perks": FounderPerks().dict(),
                "badge": "🏆 Verified Founder",
                "since": "2024-01-01",
            }
        else:
            return {
                "verified": False,
                "tier": None,
                "wallet_address": wallet_address,
                "message": "No Founder NFT found in this wallet",
                "how_to_get": [
                    "Purchase from secondary marketplace",
                    "Wait for next Founder drop",
                    "Win in community events",
                ],
            }
    
    async def get_founder_perks(self, nft_tier: str = "founder") -> Dict[str, Any]:
        """Get perks for a specific NFT tier"""
        perks_by_tier = {
            NFTTier.FOUNDER.value: {
                "tier_name": "Founder",
                "tier_emoji": "🏆",
                "perks": FounderPerks().dict(),
                "exclusive_features": [
                    "Access to Founder-only strain drops",
                    "15% discount on all marketplace purchases",
                    "Priority bidding in auctions",
                    "Monthly seed airdrops",
                    "Private Discord channel",
                    "Governance voting rights",
                    "Early access to new features",
                ],
            },
            NFTTier.GENESIS.value: {
                "tier_name": "Genesis",
                "tier_emoji": "💎",
                "perks": {
                    "marketplace_discount": 0.10,
                    "exclusive_drops_access": True,
                    "priority_auction_bidding": False,
                    "verified_badge": True,
                },
                "exclusive_features": [
                    "Access to Genesis strain drops",
                    "10% discount on marketplace",
                    "Genesis holder badge",
                ],
            },
            NFTTier.PREMIUM.value: {
                "tier_name": "Premium",
                "tier_emoji": "⭐",
                "perks": {
                    "marketplace_discount": 0.05,
                    "exclusive_drops_access": False,
                    "verified_badge": True,
                },
                "exclusive_features": [
                    "5% discount on marketplace",
                    "Premium holder badge",
                ],
            },
        }
        
        tier_perks = perks_by_tier.get(nft_tier.lower(), perks_by_tier[NFTTier.FOUNDER.value])
        
        return {
            **tier_perks,
            "comparison": {
                "founder_vs_genesis": "Founders get priority bidding and governance",
                "genesis_vs_premium": "Genesis gets exclusive drops access",
            },
        }
    
    async def mint_genetics_certificate(
        self,
        strain_name: str,
        breeder: str,
        owner_address: str,
        metadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Mint a genetics certificate NFT on Algorand.
        
        Creates an immutable record of strain provenance.
        """
        if not strain_name or not breeder or not owner_address:
            return {"error": "strain_name, breeder, and owner_address required"}
            
        # Generate mock asset ID (would be actual Algorand ASA)
        mock_asset_id = hash(f"{strain_name}{breeder}{datetime.utcnow().timestamp()}") % 1000000000
        
        nft_data = {
            "asset_id": abs(mock_asset_id),
            "name": f"Genetics: {strain_name}",
            "unit_name": "GENE",
            "nft_type": NFTType.GENETICS_CERTIFICATE.value,
            "tier": NFTTier.STANDARD.value,
            "owner": owner_address,
            "metadata": {
                "strain_name": strain_name,
                "breeder": breeder,
                "minted_at": datetime.utcnow().isoformat(),
                "verified": True,
                **(metadata or {}),
            },
            "ipfs_uri": f"ipfs://Qm...{abs(mock_asset_id) % 10000}",  # Mock IPFS
        }
        
        # Store in mock holdings
        if owner_address not in self._nft_holdings:
            self._nft_holdings[owner_address] = []
        self._nft_holdings[owner_address].append(nft_data)
        
        return {
            "success": True,
            "message": f"Genetics certificate minted for {strain_name}",
            "nft": nft_data,
            "transaction": {
                "type": "asset_create",
                "status": "confirmed",
                "tx_id": f"TX{abs(mock_asset_id) % 100000}",
            },
            "next_steps": [
                "View in your wallet",
                "Trade on secondary marketplace",
                "Use for provenance verification",
            ],
        }
    
    async def list_user_nfts(self, wallet_address: str) -> Dict[str, Any]:
        """List all NFTs owned by a wallet"""
        if not wallet_address:
            return {"error": "wallet_address required"}
            
        holdings = self._nft_holdings.get(wallet_address, [])
        
        # Check if founder
        is_founder = await self.verify_founder_status(wallet_address)
        
        # Mock additional NFTs for demonstration
        if wallet_address.startswith("FOUNDER"):
            holdings.append({
                "asset_id": 1,
                "name": "CultivAR Founder Pass #001",
                "nft_type": NFTType.FOUNDER_PASS.value,
                "tier": NFTTier.FOUNDER.value,
            })
            
        return {
            "wallet_address": wallet_address,
            "total_nfts": len(holdings),
            "is_founder": is_founder.get("verified", False),
            "nfts": holdings,
            "categories": {
                "founder_passes": len([n for n in holdings if n.get("nft_type") == NFTType.FOUNDER_PASS.value]),
                "genetics_certificates": len([n for n in holdings if n.get("nft_type") == NFTType.GENETICS_CERTIFICATE.value]),
                "grow_badges": len([n for n in holdings if n.get("nft_type") == NFTType.GROW_BADGE.value]),
                "achievements": len([n for n in holdings if n.get("nft_type") == NFTType.ACHIEVEMENT_TROPHY.value]),
            },
        }
    
    async def check_nft_gated_access(
        self,
        wallet_address: str,
        feature: str,
    ) -> Dict[str, Any]:
        """Check if user has access to an NFT-gated feature"""
        if not wallet_address:
            return {"has_access": False, "reason": "No wallet connected"}
            
        # Define feature requirements
        feature_requirements = {
            "exclusive_drops": [NFTTier.FOUNDER, NFTTier.GENESIS],
            "priority_bidding": [NFTTier.FOUNDER],
            "governance_voting": [NFTTier.FOUNDER],
            "monthly_airdrops": [NFTTier.FOUNDER],
            "private_discord": [NFTTier.FOUNDER],
            "marketplace_discount": [NFTTier.FOUNDER, NFTTier.GENESIS, NFTTier.PREMIUM],
        }
        
        required_tiers = feature_requirements.get(feature, [])
        
        # Check user's tier
        verification = await self.verify_founder_status(wallet_address)
        user_tier = verification.get("tier")
        
        has_access = user_tier in [t.value for t in required_tiers] if user_tier else False
        
        return {
            "feature": feature,
            "has_access": has_access,
            "user_tier": user_tier,
            "required_tiers": [t.value for t in required_tiers],
            "message": "Access granted ✅" if has_access else "NFT required for access",
            "upgrade_path": None if has_access else {
                "required": required_tiers[0].value if required_tiers else "any",
                "how_to_get": "Purchase from marketplace or win in events",
            },
        }
    
    def add_founder_address(self, address: str):
        """Register a founder address (admin function)"""
        self._founder_addresses.add(address)


# Register agent
AgentRegistry.register(NFTMarketplaceAgent())
