"""
Gamification Database Models

Tables:
- user_xp: Track user experience points and levels
- user_achievements: Track unlocked achievements
- user_streaks: Track daily check-in streaks
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, 
    ForeignKey, Text, JSON, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
import enum

from .base import Base


class AchievementCategory(enum.Enum):
    """Achievement categories"""
    DISCOVERY = "discovery"
    GROWING = "growing"
    HARVEST = "harvest"
    COMMUNITY = "community"
    LEARNING = "learning"
    STREAKS = "streaks"


class UserXP(Base):
    """
    Track user experience points and level progression.
    
    XP is earned through:
    - Daily check-ins
    - Using AI features
    - Completing achievements
    - Community participation
    """
    __tablename__ = "user_xp"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    total_xp = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="xp_record")
    xp_history = relationship("XPTransaction", back_populates="user_xp", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<UserXP(user_id={self.user_id}, level={self.level}, xp={self.total_xp})>"


class XPTransaction(Base):
    """
    Log of all XP transactions for auditing and analytics.
    """
    __tablename__ = "xp_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_xp_id = Column(Integer, ForeignKey("user_xp.id"), nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    source = Column(String(100), nullable=False)  # e.g., "daily_checkin", "achievement:first_plant"
    description = Column(String(255), nullable=True)
    extra_data = Column(JSON, nullable=True)  # Additional context (renamed from metadata)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    user_xp = relationship("UserXP", back_populates="xp_history")
    
    def __repr__(self):
        return f"<XPTransaction(user_xp_id={self.user_xp_id}, amount={self.amount}, source={self.source})>"


class UserAchievement(Base):
    """
    Track which achievements users have unlocked.
    """
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    achievement_id = Column(String(50), nullable=False, index=True)  # e.g., "first_plant", "streak_7"
    
    # Achievement metadata
    category = Column(SQLEnum(AchievementCategory), nullable=False)
    xp_awarded = Column(Integer, default=0, nullable=False)
    nft_unlocked = Column(String(100), nullable=True)  # NFT collection ID if applicable
    
    # Progress tracking (for incremental achievements)
    progress = Column(Float, default=1.0, nullable=False)  # 0.0 to 1.0
    is_complete = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    unlocked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="achievements")
    
    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement={self.achievement_id})>"


class UserStreak(Base):
    """
    Track daily check-in streaks.
    """
    __tablename__ = "user_streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    
    # Streak data
    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    total_checkins = Column(Integer, default=0, nullable=False)
    
    # Last check-in timestamp
    last_checkin = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="streak_record")
    checkin_history = relationship("CheckInLog", back_populates="streak", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<UserStreak(user_id={self.user_id}, current={self.current_streak}, longest={self.longest_streak})>"


class CheckInLog(Base):
    """
    Log of all daily check-ins for history and analytics.
    """
    __tablename__ = "checkin_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    streak_id = Column(Integer, ForeignKey("user_streaks.id"), nullable=False, index=True)
    
    # Check-in data
    checkin_date = Column(DateTime, nullable=False)
    plants_checked = Column(Integer, default=0)
    photos_uploaded = Column(Integer, default=0)
    environment_logged = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    
    # XP earned for this check-in
    base_xp = Column(Integer, default=10)
    bonus_xp = Column(Integer, default=0)
    streak_bonus = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    streak = relationship("UserStreak", back_populates="checkin_history")
    
    def __repr__(self):
        return f"<CheckInLog(streak_id={self.streak_id}, date={self.checkin_date})>"


class AgentMetrics(Base):
    """
    Track agent performance metrics for EvoAgentX learning.
    """
    __tablename__ = "agent_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # Execution metrics
    total_executions = Column(Integer, default=0, nullable=False)
    successful_executions = Column(Integer, default=0, nullable=False)
    
    # Feedback metrics
    user_feedback_positive = Column(Integer, default=0, nullable=False)
    user_feedback_negative = Column(Integer, default=0, nullable=False)
    
    # Performance metrics
    avg_confidence = Column(Float, default=0.0, nullable=False)
    outcome_accuracy = Column(Float, default=0.0, nullable=False)
    avg_execution_time_ms = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<AgentMetrics(agent_id={self.agent_id}, executions={self.total_executions})>"
