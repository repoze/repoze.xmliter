import serializer

def lazy(function=None, parser=None):
    if function is not None:
        def decorator(*args, **kwargs):
            result = function(*args, **kwargs)
            if parser is None:
                return serializer.XMLSerializer(result)
            return serializer.XMLSerializer(result, parser)
    else:
        def decorator(function):
            return lazy(function=function, parser=parser)
    
    return decorator
