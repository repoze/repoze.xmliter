Overview
========

This package provides a wrapper for ``lxml`` trees which serializes to
string on iteration, but otherwise makes the tree available in an
attribute.

The primary for this is WSGI middleware which may avoid
needless XML parsing and serialization.

Usage
-----

It's recommend to use the `lazy` decorator on your application method.

  >>> from repoze.xmliter import lazy
  
  >>> @lazy
  ... def application(environ, start_response)
  ...     return some_lxml_tree

You may provide a parser function:

  >>> @lazy(parser=lxml.etree.fromstring)
  ... def application(environ, start_response)
  ...     return some_lxml_tree
  
The decorator ensures that the return-value is iterable yielding a
string, but it also exposes the XML tree to middlewares.

Middleware should use `isinstance` to test if the result is an XML
iterable:

  >>> from repoze.xmliter.serializer import XMLSerializer
  >>> isinstance(result, XMLSerializer)

In this case, the middleware can simply access the `tree` attribute of
the result.
