from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Website:
    id: Optional[int]
    user_id: int
    name: str
    url: str
    created_at: datetime
    updated_at: datetime