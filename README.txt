Overview
========

This package provides a wrapper for ``lxml`` trees which serializes to
string on iteration, but otherwise makes the tree available in an
attribute.

The primary for this is WSGI middleware which may avoid
needless XML parsing and serialization.

Usage
-----

It's recommend to use the `lazy` decorator on your application method. This
allows you to return an lxml tree object, which is then automatically turned
into an XMLSerializer.

  >>> from repoze.xmliter import lazy
  
  >>> @lazy
  ... def application(environ, start_response)
  ...     return some_lxml_tree

You may provide a serializer function, which will be used when the
XMLSerializer is eventually iterated over (i.e. when the response is rendered):

  >>> @lazy(serializer=lxml.html.tostring)
  ... def application(environ, start_response)
  ...     return some_lxml_tree

Middleware can use `isinstance` to test if the result is an XML
iterable:

  >>> from repoze.xmliter.serializer import XMLSerializer
  >>> isinstance(result, XMLSerializer)

In this case, the middleware can simply access the `tree` attribute of
the result.

There are two convenience methods which can be used to parse a WSGI iterable
of strings and build an XMLSerializer object, but avoids re-building the
serializer if the input iterable is already an instance of XMLSerializer:

  >>> from repoze.xmliter.utils import getXMLSerializer
  >>> result = getXMLSerializer(result)

Or, if you are parsing HTML:

  >>> from repoze.xmliter.utils import getHTMLSerializer
  >>> result = getHTMLSerializer(result)

If `result` is not an XMLSerializer, it will be parsed using a feed parser,
turned into an lxml tree, and wrapped up in an XMLSerializer, which is
returned.
