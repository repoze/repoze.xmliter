import unittest

from repoze.xmliter import decorator
from repoze.xmliter import serializer
from repoze.xmliter import utils

import lxml.html
import lxml.etree

class TestIterator(unittest.TestCase):
    
    def create_tree(self):
        return lxml.html.fromstring(''.join(self.create_iterable()))
    
    def create_iterable(self):
        return [
            "<html>",
                "<head>",
                    "<title>My homepage</title>",
                "</head>",
                "<body>",
                    "Hello, world!",
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
        t = utils.getHTMLSerializer(self.create_iterable())
        self.failUnless(isinstance(t, serializer.XMLSerializer))
        
        t2 = utils.getXMLSerializer(t)
        self.failUnless(t2 is t)
        
        self.assertEqual(
            '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">\n<html>\n<head><title>My homepage</title></head>\n<body>Hello, world!</body>\n</html>\n',
            "".join(t2))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
