import decorator
import unittest

import lxml.html
import lxml.etree

class TestIterator(unittest.TestCase):
    def create_tree(self):
        return lxml.html.fromstring("""\
        <html>
          <head>
            <title>My homepage</title>
          </head>
          <body>
            Hello, world!
          </body>
        </html>""")
        
    def test_html_serialization(self):
        """Test HTML serialization."""
        
        @decorator.lazy(parser=lxml.html.tostring)
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

    def test_decorator(self):
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

