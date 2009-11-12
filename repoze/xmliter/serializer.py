import lxml.etree

class XMLSerializer(object):
    
    def __init__(self, tree, serializer=lxml.etree.tostring, pretty_print=False):
        self.tree = tree
        self.serializer = serializer
        self.pretty_print = pretty_print
        
    def __iter__(self):
        return iter(str(self),)

    def __str__(self):
        return self.serializer(self.tree, pretty_print=self.pretty_print)

    def __unicode__(self):
        return self.serializer(self.tree, encoding=unicode, pretty_print=self.pretty_print)
