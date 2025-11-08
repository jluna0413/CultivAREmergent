"""LEGACY: Pydantic models for Cultivars domain - DEPRECATED.

This file is maintained for backward compatibility only. All new code should import
from models.cultivars instead of models.strains.

The actual implementation has been moved to app/fastapi_app/models/cultivars.py
"""

# DEPRECATED: Import everything from the new cultivars module
from .cultivars import (
    CultivarBase,
    CultivarCreate,
    CultivarUpdate,
    CultivarResponse,
    CultivarListResponse,
    CultivarFilters,
    CultivarStats,
)

# LEGACY: Backward compatibility aliases - use Cultivar* classes instead
StrainBase = CultivarBase
StrainCreate = CultivarCreate
StrainUpdate = CultivarUpdate
StrainResponse = CultivarResponse
StrainListResponse = CultivarListResponse
StrainFilters = CultivarFilters
StrainStats = CultivarStats

# DEPRECATION WARNING
import warnings

warnings.warn(
    "models.strains is deprecated. Use models.cultivars instead. "
    "The Cultivar* implementation is ready.",
    DeprecationWarning,
    stacklevel=2
)
