import serializer

class lazy(object):
    def __init__(self, arg=None):
        self.arg = arg
    
    def __call__(self, func, *args, **kwargs):
        if callable(func) and self.arg is not None:
            def decorator(*args, **kwargs):
                result = func(*args, **kwargs)
                return serializer.XMLSerializer(result, self.arg)
            return decorator
        return serializer.XMLSerializer(
            self.arg(func, *args, **kwargs))
