
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class UserGeneticsBase(BaseModel):
    name: str
    genetics_type: str = "mother" # seed, clone, pollen, mother
    description: Optional[str] = None
    cultivar_id: Optional[int] = None
    
    # Metadata
    lineage_string: Optional[str] = None
    generation: Optional[int] = None
    thc_percentage: Optional[float] = None
    cbd_percentage: Optional[float] = None
    indica_percentage: Optional[float] = None
    sativa_percentage: Optional[float] = None
    dominant_terpenes: Optional[List[str]] = None
    flower_time_days: Optional[int] = None

class UserGeneticsCreate(UserGeneticsBase):
    pass

class UserGeneticsResponse(UserGeneticsBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
