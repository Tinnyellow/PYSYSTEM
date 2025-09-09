"""
Performance optimization utilities for PYSYSTEM.
Includes lazy loading, pagination, and batch processing capabilities.
"""

from typing import List, Dict, Any, Optional, Callable, Iterator, TypeVar, Generic
from dataclasses import dataclass
from functools import wraps
import time
from threading import Lock

T = TypeVar('T')


@dataclass
class PageResult(Generic[T]):
    """Result of a paginated query."""
    items: List[T]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool


class LazyLoader(Generic[T]):
    """Implements lazy loading for large datasets."""
    
    def __init__(self, 
                 load_func: Callable[[], List[T]], 
                 cache_ttl: int = 300):
        """
        Initialize lazy loader.
        
        Args:
            load_func: Function to load data
            cache_ttl: Cache time to live in seconds
        """
        self._load_func = load_func
        self._cache_ttl = cache_ttl
        self._data: Optional[List[T]] = None
        self._last_load_time: float = 0
        self._lock = Lock()
    
    @property
    def data(self) -> List[T]:
        """Get data, loading if necessary."""
        with self._lock:
            current_time = time.time()
            
            # Check if cache is expired or empty
            if (self._data is None or 
                current_time - self._last_load_time > self._cache_ttl):
                
                self._data = self._load_func()
                self._last_load_time = current_time
            
            return self._data or []
    
    def reload(self) -> List[T]:
        """Force reload of data."""
        with self._lock:
            self._data = self._load_func()
            self._last_load_time = time.time()
            return self._data or []
    
    def clear_cache(self) -> None:
        """Clear cached data."""
        with self._lock:
            self._data = None
            self._last_load_time = 0


class PaginationHelper:
    """Helper for implementing pagination in large datasets."""
    
    @staticmethod
    def paginate(items: List[T], 
                 page: int = 1, 
                 page_size: int = 50) -> PageResult[T]:
        """
        Paginate a list of items.
        
        Args:
            items: List of items to paginate
            page: Page number (1-based)
            page_size: Number of items per page
            
        Returns:
            PageResult with paginated data
        """
        if page < 1:
            page = 1
        
        total_count = len(items)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        paginated_items = items[start_idx:end_idx]
        
        return PageResult(
            items=paginated_items,
            total_count=total_count,
            page=page,
            page_size=page_size,
            has_next=end_idx < total_count,
            has_previous=page > 1
        )
    
    @staticmethod
    def get_page_info(total_items: int, 
                     page: int, 
                     page_size: int) -> Dict[str, Any]:
        """Get pagination information."""
        total_pages = (total_items + page_size - 1) // page_size
        
        return {
            'current_page': page,
            'total_pages': total_pages,
            'total_items': total_items,
            'items_per_page': page_size,
            'has_next': page < total_pages,
            'has_previous': page > 1,
            'start_item': (page - 1) * page_size + 1,
            'end_item': min(page * page_size, total_items)
        }


class BatchProcessor:
    """Process large datasets in batches for better performance."""
    
    @staticmethod
    def process_in_batches(items: List[T], 
                          batch_size: int,
                          processor: Callable[[List[T]], Any]) -> List[Any]:
        """
        Process items in batches.
        
        Args:
            items: Items to process
            batch_size: Size of each batch
            processor: Function to process each batch
            
        Returns:
            List of results from each batch
        """
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            result = processor(batch)
            results.append(result)
        
        return results
    
    @staticmethod
    def batch_iterator(items: List[T], batch_size: int) -> Iterator[List[T]]:
        """Create an iterator that yields batches."""
        for i in range(0, len(items), batch_size):
            yield items[i:i + batch_size]


class PerformanceMonitor:
    """Monitor performance metrics for optimization."""
    
    def __init__(self):
        self._metrics: Dict[str, List[float]] = {}
        self._lock = Lock()
    
    def time_function(self, func_name: str):
        """Decorator to time function execution."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    execution_time = time.time() - start_time
                    self.record_metric(func_name, execution_time)
            return wrapper
        return decorator
    
    def record_metric(self, metric_name: str, value: float) -> None:
        """Record a performance metric."""
        with self._lock:
            if metric_name not in self._metrics:
                self._metrics[metric_name] = []
            
            self._metrics[metric_name].append(value)
            
            # Keep only last 100 measurements
            if len(self._metrics[metric_name]) > 100:
                self._metrics[metric_name] = self._metrics[metric_name][-100:]
    
    def get_stats(self, metric_name: str) -> Dict[str, float]:
        """Get statistics for a metric."""
        with self._lock:
            values = self._metrics.get(metric_name, [])
            
            if not values:
                return {
                    'count': 0,
                    'avg': 0,
                    'min': 0,
                    'max': 0
                }
            
            return {
                'count': len(values),
                'avg': sum(values) / len(values),
                'min': min(values),
                'max': max(values)
            }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all metrics."""
        return {
            metric: self.get_stats(metric) 
            for metric in self._metrics.keys()
        }


class SearchOptimizer:
    """Optimize search operations with indexing and caching."""
    
    def __init__(self):
        self._indexes: Dict[str, Dict[str, List[int]]] = {}
        self._lock = Lock()
    
    def build_index(self, 
                   items: List[Dict[str, Any]], 
                   field_name: str) -> None:
        """Build search index for a field."""
        with self._lock:
            if field_name not in self._indexes:
                self._indexes[field_name] = {}
            
            index = self._indexes[field_name]
            index.clear()
            
            for idx, item in enumerate(items):
                field_value = str(item.get(field_name, '')).lower()
                
                # Index whole words
                words = field_value.split()
                for word in words:
                    if word not in index:
                        index[word] = []
                    index[word].append(idx)
                
                # Index partial matches
                for i in range(len(field_value)):
                    for j in range(i + 1, len(field_value) + 1):
                        substring = field_value[i:j]
                        if len(substring) >= 2:  # Minimum 2 characters
                            if substring not in index:
                                index[substring] = []
                            if idx not in index[substring]:
                                index[substring].append(idx)
    
    def search(self, 
              items: List[Dict[str, Any]], 
              field_name: str, 
              query: str) -> List[int]:
        """Search using pre-built index."""
        if not query or len(query) < 2:
            return list(range(len(items)))
        
        query = query.lower()
        
        with self._lock:
            if field_name not in self._indexes:
                # Fallback to linear search
                return self._linear_search(items, field_name, query)
            
            index = self._indexes[field_name]
            
            # Find exact matches first
            if query in index:
                return index[query]
            
            # Find partial matches
            matches = set()
            for key in index:
                if query in key:
                    matches.update(index[key])
            
            return list(matches)
    
    def _linear_search(self, 
                      items: List[Dict[str, Any]], 
                      field_name: str, 
                      query: str) -> List[int]:
        """Fallback linear search."""
        results = []
        query_lower = query.lower()
        
        for idx, item in enumerate(items):
            field_value = str(item.get(field_name, '')).lower()
            if query_lower in field_value:
                results.append(idx)
        
        return results
    
    def clear_indexes(self) -> None:
        """Clear all search indexes."""
        with self._lock:
            self._indexes.clear()


# Global instances
performance_monitor = PerformanceMonitor()
search_optimizer = SearchOptimizer()
