from lxml import etree, html
from repoze.xmliter.serializer import XMLSerializer

def getXMLSerializer(iterable, parser=etree.XMLParser, serializer=etree.tostring, pretty_print=False):
    """Turn the given iterable into an XMLSerializer. If it is already an
    XMLSerializer, return as-is. Otherwise, parse the input using with the
    given parser in feed-parser mode and initalize an XMLSerializer with the
    appropriate serializer function and pretty printing flag.
    """
    if isinstance(iterable, XMLSerializer):
        return iterable
    
    p = parser()
    for chunk in iterable:
        p.feed(chunk)
    root = p.close()
    
    return XMLSerializer(root.getroottree(), serializer, pretty_print)

def getHTMLSerializer(iterable, pretty_print=True):
    """Convenience method to create an XMLSerializer instance using the HTML
    parser and string serialization. Pretty print is enabled by default.
    """
    return getXMLSerializer(
                iterable,
                parser=html.HTMLParser,
                serializer=html.tostring,
                pretty_print=pretty_print
            )
