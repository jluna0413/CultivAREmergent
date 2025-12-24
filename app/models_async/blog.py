"""
Asynchronous database models for blog-related data.
"""

from .base import Base
# Import BlogPost from marketing module to avoid duplication
from .marketing import BlogPost

# Alias for backward compatibility
Post = BlogPost
Category = BlogPost  # Alias for categories