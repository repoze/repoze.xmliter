import lxml.etree

class XMLSerializer(object):
    
    def __init__(self, tree, serializer=lxml.etree.tostring, pretty_print=False):
        self.tree = tree
        self.serializer = serializer
        self.pretty_print = pretty_print
        
    def __iter__(self):
        return iter(str(self),)

    def __str__(self):
        # Defer to the xsl:output settings if appropriate
        if isinstance(self.tree, lxml.etree._XSLTResultTree):
            return str(self.tree)
        return self.serializer(self.tree, pretty_print=self.pretty_print)

    def __unicode__(self):
        if isinstance(self.tree, lxml.etree._XSLTResultTree):
            return unicode(self.tree)
        return self.serializer(self.tree, encoding=unicode, pretty_print=self.pretty_print)
