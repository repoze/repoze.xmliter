import lxml.etree
import re

import sys

doctype_re_b = re.compile(b"^<!DOCTYPE\\s[^>]+>\\s*", re.MULTILINE)
doctype_re_u = re.compile(u"^<!DOCTYPE\\s[^>]+>\\s*", re.MULTILINE)

class XMLSerializer(object):

    def __init__(self, tree, serializer=None, pretty_print=False, doctype=None):
        if serializer is None:
            serializer = lxml.etree.tostring
        self.tree = tree
        self.serializer = serializer
        self.pretty_print = pretty_print
        if doctype and not doctype.endswith('\n'):
            doctype = doctype + '\n'
        self.doctype = doctype

    def serialize(self, encoding=None):
        # Defer to the xsl:output settings if appropriate
        if isinstance(self.tree, lxml.etree._XSLTResultTree):
            if encoding is str:
                result = str(self.tree)
            else:
                result = bytes(self.tree)
        else:
            result = self.serializer(self.tree, encoding=encoding, pretty_print=self.pretty_print)
        if self.doctype is not None:
            if encoding is str:
                result = doctype_re_u.sub(self.doctype, result, 1)
            else:
                result = doctype_re_b.sub(self.doctype.encode(), result, 1)
        return result

    def __iter__(self):
        return iter((bytes(self),))

    def __str__(self):
        return self.serialize(str)

    def __bytes__(self):
        return self.serialize()

    def __len__(self):
        return 1
