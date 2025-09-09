"""
Base repository interface.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Base repository interface for CRUD operations."""
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """Save an entity."""
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[T]:
        """Find an entity by its ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """Find all entities."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an entity."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete an entity by its ID."""
        pass
    
    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        """Check if an entity exists."""
        pass
