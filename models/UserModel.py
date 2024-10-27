from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    password_hash: str
    encryption_key: bytes
    created_at: datetime
    updated_at: datetime