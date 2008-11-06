import lxml.etree

class XMLSerializer(object):
    def __init__(self, tree, serializer=lxml.etree.tostring):
        self.tree = tree
        self.serializer = serializer
        
    def __iter__(self):
        return iter(str(self),)

    def __str__(self):
        return self.serializer(self.tree)

    def __unicode__(self):
        return self.serializer(self.tree, encoding=unicode)
