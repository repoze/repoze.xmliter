# -*- coding: utf-8 -*-
import unittest

from repoze.xmliter import decorator
from repoze.xmliter import serializer
from repoze.xmliter import utils

import lxml.html
import lxml.etree

import sys
if sys.version_info > (3,):
    unicode = str
    
class TestIterator(unittest.TestCase):
    
    def create_tree(self):
        return lxml.html.fromstring(''.join(self.create_iterable()))
    
    def create_iterable(self, preamble="", body=""):
        return [preamble,
            "<html>",
                "<head>",
                    "<title>My homepage</title>",
                "</head>",
                "<body>",
                    "Hello, wörld!",
                    body,
                "</body>"
            "</html>",
        ]
    
    def test_html_serialization(self):
        """Test HTML serialization."""
        
        @decorator.lazy(serializer=lxml.html.tostring)
        def app(a, b, c=u""):
            tree = self.create_tree()
            tree.find('body').attrib['class'] = " ".join((a, b, c))
            return tree

        result = app("a", "b", c="c")

        self.assertEqual(
            lxml.html.tostring(result.tree),
            b"".join(result))

        # With Unicode encoding:
        self.assertEqual(
            lxml.html.tostring(result.tree, encoding='unicode'),
            u"".join(result.serialize(encoding=unicode)))
        
    def test_xml_serialization(self):
        """Test XML serialization."""
        
        @decorator.lazy
        def app(a, b, c=u""):
            tree = self.create_tree()
            tree.find('body').attrib['class'] = " ".join((a, b, c))
            return tree

        result = app("a", "b", c="c")

        self.assertEqual(
            lxml.etree.tostring(result.tree),
            b"".join(result))

        # With Unicode encoding:
        self.assertEqual(
            lxml.etree.tostring(result.tree, encoding='unicode'),
            u"".join(result.serialize(encoding=unicode)))

    def test_decorator_instancemethod(self):
        class test(object):
            @decorator.lazy
            def process(self, tree):
                return tree

            def __call__(self, tree):
                return self.process(tree)

        result = test()(self.create_tree())
        self.assertEqual(
            lxml.etree.tostring(result.tree),
            b"".join(result))

        self.assertEqual(
            lxml.etree.tostring(result.tree, encoding='unicode'),
            u"".join(result.serialize(encoding=unicode)))
    
    def test_getXMLSerializer(self):
        t = utils.getXMLSerializer(self.create_iterable())
        self.failUnless(isinstance(t, serializer.XMLSerializer))
        
        t2 = utils.getXMLSerializer(t)
        self.failUnless(t2 is t)
        
        self.assertEqual(
            b"<html><head><title>My homepage</title></head><body>Hello, w&#246;rld!</body></html>",
            b"".join(t2))

        self.assertEqual(
            u"<html><head><title>My homepage</title></head><body>Hello, wörld!</body></html>",
            u"".join(t2.serialize(encoding=unicode)))

    def test_length(self):
        t = utils.getXMLSerializer(self.create_iterable())
        self.failUnless(len(t) == 1)
        self.failUnless(len(list(t)) == 1)

    def test_getHTMLSerializer(self):
        t = utils.getHTMLSerializer(self.create_iterable(body='<img src="foo.png" />'), pretty_print=True)
        self.failUnless(isinstance(t, serializer.XMLSerializer))
        
        t2 = utils.getXMLSerializer(t)
        self.failUnless(t2 is t)
        
        self.assertEqual(
            b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">\n<html>\n<head><title>My homepage</title></head>\n<body>Hello, w&#246;rld!<img src="foo.png">\n</body>\n</html>\n',
            b"".join(t2))

        self.assertEqual(
            u'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">\n<html>\n<head><title>My homepage</title></head>\n<body>Hello, wörld!<img src="foo.png">\n</body>\n</html>\n',
            u"".join(t2.serialize(encoding=unicode)))
    
    def test_getHTMLSerializer_doctype_xhtml_serializes_to_xhtml(self):
        t = utils.getHTMLSerializer(self.create_iterable(preamble='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n', body='<img src="foo.png" />'), pretty_print=True)
        self.failUnless(isinstance(t, serializer.XMLSerializer))
        
        t2 = utils.getXMLSerializer(t)
        self.failUnless(t2 is t)
        
        self.assertEqual(
            b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=ASCII" />\n    <title>My homepage</title>\n  </head>\n  <body>Hello, w&#246;rld!<img src="foo.png" /></body>\n</html>\n',
            b"".join(t2))

        self.assertEqual(
            u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n    <title>My homepage</title>\n  </head>\n  <body>Hello, wörld!<img src="foo.png" /></body>\n</html>\n',
            u"".join(t2.serialize(encoding=unicode)))

    def test_xsl(self):
        t = utils.getHTMLSerializer(self.create_iterable(body='<br>'))
        transform = lxml.etree.XSLT(lxml.etree.XML(b'''
            <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                <xsl:output method="xml" indent="no" omit-xml-declaration="yes"
                    media-type="text/html" encoding="UTF-8"
                    doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN"
                    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"
                    />
                <xsl:template match="@*|node()">
                  <xsl:copy>
                    <xsl:apply-templates select="@*|node()"/>
                  </xsl:copy>
                </xsl:template>
            </xsl:stylesheet>
            '''))
        t.tree = transform(t.tree)
        self.failUnless('<br />' in str(t))

    def test_replace_doctype(self):
        t = utils.getHTMLSerializer(self.create_iterable(preamble='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n', body='<img src="foo.png" />'), pretty_print=True, doctype="<!DOCTYPE html>")
        self.failUnless(isinstance(t, serializer.XMLSerializer))

        t2 = utils.getXMLSerializer(t)
        self.failUnless(t2 is t)
        
        self.assertEqual(
            b'<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=ASCII" />\n    <title>My homepage</title>\n  </head>\n  <body>Hello, w&#246;rld!<img src="foo.png" /></body>\n</html>\n',
            b"".join(t2))

        self.assertEqual(
            u'<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n    <title>My homepage</title>\n  </head>\n  <body>Hello, wörld!<img src="foo.png" /></body>\n</html>\n',
            u"".join(t2.serialize(encoding=unicode)))

    def test_replace_doctype_blank(self):
        t = utils.getHTMLSerializer(self.create_iterable(preamble='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n', body='<img src="foo.png" />'), pretty_print=True, doctype="")
        self.failUnless(isinstance(t, serializer.XMLSerializer))

        t2 = utils.getXMLSerializer(t)
        self.failUnless(t2 is t)
        
        self.assertEqual(
            b'<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=ASCII" />\n    <title>My homepage</title>\n  </head>\n  <body>Hello, w&#246;rld!<img src="foo.png" /></body>\n</html>\n',
            b"".join(t2))

        self.assertEqual(
            u'<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n    <title>My homepage</title>\n  </head>\n  <body>Hello, wörld!<img src="foo.png" /></body>\n</html>\n',
            u"".join(t2.serialize(encoding=unicode)))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
