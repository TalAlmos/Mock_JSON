class SchemaCache:
    def __init__(self):
        self._cache = {}

    def set_schema(self, key, schema):
        self._cache[key] = schema

    def get_schema(self, key):
        return self._cache.get(key) 