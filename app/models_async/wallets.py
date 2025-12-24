"""
Blockchain wallet integration models.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models_async.base import Base


class WalletProvider(enum.Enum):
    """Supported wallet providers"""
    PERA = "pera"  # Pera Wallet (Algorand)
    MYALGO = "myalgo"  # MyAlgo Wallet
    DEFLY = "defly"  # Defly Wallet
    INTERNAL = "internal"  # Platform-managed wallet


class UserWallet(Base):
    """
    User's Algorand wallets for NFT interactions.
    """
    __tablename__ = "user_wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Wallet details
    algorand_address = Column(String(58), unique=True, nullable=False, index=True)
    wallet_provider = Column(Enum(WalletProvider), nullable=False)
    wallet_name = Column(String(100))  # User-defined name
    
    # Status
    is_primary = Column(Boolean, default=False)  # Primary wallet for transactions
    is_verified = Column(Boolean, default=False)  # Verified ownership
    verified_at = Column(DateTime)
    
    # Security
    last_signature_at = Column(DateTime)  # Last time used for signing
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="wallets")
    transactions = relationship("WalletTransaction", back_populates="wallet")
    
    def __repr__(self):
        return f"<UserWallet(user_id={self.user_id}, address='{self.algorand_address[:8]}...')>"


class WalletTransactionType(enum.Enum):
    """Types of wallet transactions"""
    NFT_MINT = "nft_mint"
    NFT_TRANSFER = "nft_transfer"
    NFT_BURN = "nft_burn"
    PAYMENT = "payment"
    ESCROW_RELEASE = "escrow_release"
    ROYALTY_PAYMENT = "royalty_payment"


class WalletTransaction(Base):
    """
    Records all blockchain transactions for users.
    """
    __tablename__ = "wallet_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("user_wallets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Transaction details
    txn_hash = Column(String(64), unique=True, nullable=False, index=True)
    transaction_type = Column(Enum(WalletTransactionType), nullable=False, index=True)
    
    # Amounts
    amount_microalgos = Column(BigInteger)  # For payments
    asset_id = Column(BigInteger)  # For NFT transactions
    
    # Status
    is_confirmed = Column(Boolean, default=False, index=True)
    confirmed_at = Column(DateTime)
    block_number = Column(BigInteger)
    
    # Metadata
    note = Column(Text)  # Transaction note/memo
    reference_id = Column(Integer)  # Order ID, pack ID, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    wallet = relationship("UserWallet", back_populates="transactions")
    user = relationship("User")
    
    def __repr__(self):
        return f"<WalletTransaction(txn='{self.txn_hash[:8]}...', type={self.transaction_type.value})>"


class WalletOnboardingStatus(Base):
    """
    Tracks user's progress through wallet setup.
    """
    __tablename__ = "wallet_onboarding_status"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Onboarding steps
    has_viewed_tutorial = Column(Boolean, default=False)
    has_connected_wallet = Column(Boolean, default=False)
    has_verified_wallet = Column(Boolean, default=False)
    has_made_first_transaction = Column(Boolean, default=False)
    
    # Tutorial completion
    tutorial_step = Column(Integer, default=0)  # 0-5
    tutorial_completed_at = Column(DateTime)
    
    # Wallet connection
    wallet_connected_at = Column(DateTime)
    wallet_provider_chosen = Column(Enum(WalletProvider))
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<WalletOnboardingStatus(user_id={self.user_id}, completed={self.completed_at is not None})>"
