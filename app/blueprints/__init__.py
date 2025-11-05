"""
Blueprints package for the CultivAR application - ASYNC VERSION.

This package contains all Flask blueprints that have been converted to use
async patterns with async handlers and async SQLAlchemy operations.

Converted Blueprints:
- admin.py: Admin dashboard and user management (async patterns)
- auth.py: Authentication and user sessions (async patterns) 
- breeders.py: Breeder management (async patterns)
- clones.py: Clone management system (async patterns)
- dashboard.py: Main application dashboard (async patterns)
- diagnostics.py: System diagnostics and monitoring (async patterns)
- market.py: Market/seed bank interface (async patterns)
- marketing.py: Marketing, blog, and waitlist (async patterns)
- newsletter.py: Newsletter subscription management (async patterns)
- social.py: Social/community features (async patterns)
- strains.py: Strain management interface (async patterns)

All blueprints now use async route handlers and async SQLAlchemy patterns
for database operations.
"""

# Import all blueprints to make them available
from . import (
    admin_bp,
    auth_bp,
    breeders_bp,
    clones_bp,
    cultivars_bp,
    diagnostics_bp,
    market_bp,
    marketing_bp,
    news_letter_bp,
    social_bp,
    strains_bp,
)

# Export blueprint instances
__all__ = [
    'admin_bp',
    'auth_bp',
    'breeders_bp',
    'clones_bp',
    'cultivars_bp',
    'diagnostics_bp',
    'market_bp',
    'marketing_bp',
    'news_letter_bp',
    'social_bp',
    'strains_bp',
]