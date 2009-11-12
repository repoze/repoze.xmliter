from repoze.xmliter.serializer import XMLSerializer

def lazy(function=None, serializer=None):
    if function is not None:
        def decorator(*args, **kwargs):
            result = function(*args, **kwargs)
            if serializer is None:
                return XMLSerializer(result)
            return XMLSerializer(result, serializer)
    else:
        def decorator(function):
            return lazy(function=function, serializer=serializer)
    
    return decorator
