"""
Cultivar handlers for the CultivAR application.
Backward compatibility wrapper - all actual functionality is in cultivar_handlers.py

This file maintains legacy 'strain' terminology imports for existing code.
Use cultivar_handlers.py for new development.
"""

# Import everything from the primary implementation
from .cultivar_handlers import (
    get_cultivar,
    get_in_stock_cultivars, 
    get_out_of_stock_cultivars,
    add_cultivar,
    update_cultivar,
    delete_cultivar,
    # Backward compatibility aliases
    get_strain,
    get_in_stock_strains,
    get_out_of_stock_strains, 
    add_strain,
    update_strain,
    delete_strain
)

# Legacy import for direct module access
from .cultivar_handlers import *
