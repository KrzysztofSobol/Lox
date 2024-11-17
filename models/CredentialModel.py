from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Credential:
    id: Optional[int]
    website_id: int
    username: str
    password: str
    saved_link: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime