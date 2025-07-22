# tests/test_cache.py
from cache.schema_cache import SchemaCache

class TestSchemaCache:
    def test_cache_get_set(self):
        cache = SchemaCache()
        schema = {"type": "object"}
        
        cache.set_schema("travel", schema)
        retrieved = cache.get_schema("travel")
        
        assert retrieved == schema
    
    def test_cache_miss(self):
        cache = SchemaCache()
        result = cache.get_schema("nonexistent")
        assert result is None
    
    def test_cache_performance(self):
        cache = SchemaCache()
        schema = {"type": "object"}
        
        # Test that cache is faster than regenerating
        import time
        
        # First call (cache miss)
        start = time.time()
        cache.set_schema("travel", schema)
        cache.get_schema("travel")
        first_call_time = time.time() - start
        
        # Second call (cache hit)
        start = time.time()
        cache.get_schema("travel")
        second_call_time = time.time() - start
        
        assert second_call_time < first_call_time
