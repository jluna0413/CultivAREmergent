"""
Blueprints package for the CultivAR application - ASYNC VERSION.

This package contains all Flask blueprints that have been converted to use
async patterns with async handlers and async SQLAlchemy operations.

Converted Blueprints:
- admin.py: Admin dashboard and user management (async patterns)
- auth.py: Authentication and user sessions (async patterns)
- breeders.py: Breeder management (async patterns)
- clones.py: Clone management system (async patterns)
- cultivars.py: Cultivar management interface (async patterns) - PRIMARY
- dashboard.py: Main application dashboard (async patterns)
- diagnostics.py: System diagnostics and monitoring (async patterns)
- market.py: Market/seed bank interface (async patterns)
- marketing.py: Marketing, blog, and waitlist (async patterns)
- newsletter.py: Newsletter subscription management (async patterns)
- social.py: Social/community features (async patterns)

All blueprints now use async route handlers and async SQLAlchemy patterns
for database operations.

NOTE: This is a cultivars-first migration. The legacy 'strains' terminology
is maintained through backward compatibility aliases.
"""

# Avoid importing blueprints at package import time to prevent circular imports.
# Consumers should import specific blueprint modules directly, e.g.:
#   from app.blueprints.auth import auth_bp
# or use the get_blueprint function below for dynamic access.

def get_blueprint(name):
    """Lazily import and return a blueprint object by its exported name.

    Example:
        bp = get_blueprint('auth_bp')
    """
    mapping = {
        'admin_bp': 'app.blueprints.admin',
        'auth_bp': 'app.blueprints.auth',
        'breeders_bp': 'app.blueprints.breeders',
        'clones_bp': 'app.blueprints.clones',
        'cultivars_bp': 'app.blueprints.cultivars',
        'diagnostics_bp': 'app.blueprints.diagnostics',
        'market_bp': 'app.blueprints.market',
        'marketing_bp': 'app.blueprints.marketing',
        'news_letter_bp': 'app.blueprints.newsletter',
        'social_bp': 'app.blueprints.social',
        # strains_bp is a legacy alias that points to the cultivars module
        'strains_bp': 'app.blueprints.cultivars',
    }
    module_name = mapping.get(name)
    if not module_name:
        raise KeyError(f'Unknown blueprint name: {name}')
    module = __import__(module_name, fromlist=['*'])
    return getattr(module, name)

# Provide __all__ as the canonical blueprint names. Prefer direct imports from modules.
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