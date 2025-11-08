"""
Strain management handlers for the CultivAR application - ASYNC VERSION.
Legacy backward compatibility wrapper for 'strain' terminology.
This module provides backward compatibility by delegating to the primary 'cultivar' handlers.
All new code should use 'cultivar' terminology from cultivar_handlers_async.py.
"""

# Import all functions from the primary cultivar handlers module
from .cultivar_handlers_async import (
    # Primary cultivar functions
    get_all_cultivars,
    get_cultivar_by_id, 
    create_cultivar,
    update_cultivar,
    delete_cultivar,
    get_in_stock_cultivars,
    get_out_of_stock_cultivars,
    search_cultivars,
    
    # Backward compatibility aliases (already defined in cultivar_handlers_async.py)
    get_all_strains,
    get_strain_by_id,
    create_strain,
    update_strain,
    delete_strain,
    get_in_stock_strains,
    get_out_of_stock_strains,
    search_strains
)

# Legacy import for direct module access
from .cultivar_handlers_async import *