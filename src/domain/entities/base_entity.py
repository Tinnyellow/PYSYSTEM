"""
Domain entities for the Sales Management System.
"""

from abc import ABC
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import uuid


@dataclass
class BaseEntity(ABC):
    """Base entity class with common properties."""
    
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize entity with ID and timestamps if not provided."""
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
