"""
Cache Manager for API responses and validation results.
Improves performance by caching frequently accessed data.
"""

import json
import time
from typing import Dict, Any, Optional
from pathlib import Path


class CacheManager:
    """Manages cache for API responses and validation results."""
    
    def __init__(self, cache_dir: str = "cache", ttl_seconds: int = 3600):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory to store cache files
            ttl_seconds: Time to live for cache entries (default 1 hour)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl_seconds = ttl_seconds
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
    
    def _get_cache_file(self, key: str) -> Path:
        """Get cache file path for given key."""
        safe_key = key.replace('/', '_').replace(':', '_')
        return self.cache_dir / f"{safe_key}.json"
    
    def _is_expired(self, timestamp: float) -> bool:
        """Check if cache entry is expired."""
        return time.time() - timestamp > self.ttl_seconds
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value by key.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        # Check memory cache first
        if key in self._memory_cache:
            entry = self._memory_cache[key]
            if not self._is_expired(entry['timestamp']):
                return entry['data']
            else:
                del self._memory_cache[key]
        
        # Check file cache
        cache_file = self._get_cache_file(key)
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    entry = json.load(f)
                    
                if not self._is_expired(entry['timestamp']):
                    # Load into memory cache
                    self._memory_cache[key] = entry
                    return entry['data']
                else:
                    # Remove expired file
                    cache_file.unlink()
            except (json.JSONDecodeError, KeyError, OSError):
                # Remove corrupted cache file
                if cache_file.exists():
                    cache_file.unlink()
        
        return None
    
    def set(self, key: str, value: Any) -> None:
        """
        Set cached value for key.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        entry = {
            'data': value,
            'timestamp': time.time()
        }
        
        # Store in memory cache
        self._memory_cache[key] = entry
        
        # Store in file cache
        cache_file = self._get_cache_file(key)
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(entry, f, ensure_ascii=False, indent=2)
        except OSError:
            # Failed to write to disk, but memory cache is still available
            pass
    
    def clear(self) -> None:
        """Clear all cache entries."""
        # Clear memory cache
        self._memory_cache.clear()
        
        # Clear file cache
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except OSError:
                pass
    
    def clear_expired(self) -> None:
        """Clear expired cache entries."""
        # Clear expired memory cache
        expired_keys = [
            key for key, entry in self._memory_cache.items()
            if self._is_expired(entry['timestamp'])
        ]
        for key in expired_keys:
            del self._memory_cache[key]
        
        # Clear expired file cache
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    entry = json.load(f)
                    
                if self._is_expired(entry['timestamp']):
                    cache_file.unlink()
            except (json.JSONDecodeError, KeyError, OSError):
                # Remove corrupted cache file
                cache_file.unlink()


# Global cache instance
cache_manager = CacheManager()
