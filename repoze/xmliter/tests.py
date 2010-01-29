import unittest

from repoze.xmliter import decorator
from repoze.xmliter import serializer
from repoze.xmliter import utils

import lxml.html
import lxml.etree

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
                    "Hello, world!",
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
            "".join(result))

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
            "".join(result))

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
            "".join(result))
    
    def test_getXMLSerializer(self):
        t = utils.getXMLSerializer(self.create_iterable())
        self.failUnless(isinstance(t, serializer.XMLSerializer))
        
        t2 = utils.getXMLSerializer(t)
        self.failUnless(t2 is t)
        
        self.assertEqual(
            "<html><head><title>My homepage</title></head><body>Hello, world!</body></html>",
            "".join(t2))

    def test_getHTMLSerializer(self):
        t = utils.getHTMLSerializer(self.create_iterable(body='<img src="foo.png" />'))
        self.failUnless(isinstance(t, serializer.XMLSerializer))
        
        t2 = utils.getXMLSerializer(t)
        self.failUnless(t2 is t)
        
        self.assertEqual(
            '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">\n<html>\n<head><title>My homepage</title></head>\n<body>Hello, world!<img src="foo.png">\n</body>\n</html>\n',
            "".join(t2))
    
    def test_getHTMLSerializer_doctype_xhtml_serializes_to_xhtml(self):
        t = utils.getHTMLSerializer(self.create_iterable(preamble='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n', body='<img src="foo.png" />'))
        self.failUnless(isinstance(t, serializer.XMLSerializer))
        
        t2 = utils.getXMLSerializer(t)
        self.failUnless(t2 is t)
        
        self.assertEqual(
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=ASCII" />\n    <title>My homepage</title>\n  </head>\n  <body>Hello, world!<img src="foo.png" /></body>\n</html>\n',
            "".join(t2))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
