from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    password_hash: str
    salt: str
    wrapped_encryption_key: str
    created_at: datetime
    updated_at: datetime