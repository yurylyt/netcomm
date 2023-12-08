class HashWrapper:
    """
    Uses explicit property definition instead of __getattr__/__setattr__ approach for performance reasons

    """
    def __init__(self, data):
        self._data = data

    def _get(self, item):
        return self._data[item]

    def _set(self, key, value):
        self._data[key] = value

