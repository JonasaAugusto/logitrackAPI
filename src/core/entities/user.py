from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class UserEntity:
    username: str
    email: str
    password_hash: str
    is_active: bool = True
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
