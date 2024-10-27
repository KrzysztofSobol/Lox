from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Credential:
    id: Optional[int]
    website_id: int
    username: str
    encrypted_password: bytes
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime