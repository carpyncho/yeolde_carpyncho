#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect
import time
import string
import multiprocessing as mp
try:
    import cPickle as pickle
except ImportError:
    import pickle


import six

import tables as tb

import bottle as bt

import requests


# =============================================================================
# CONSTANTS
# =============================================================================

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 6699

TPL_URL = string.Template("http://${host}:${port}")


# =============================================================================
# EXCEPTIONS
# =============================================================================

class ConfigurationError(ValueError): pass

class ServerNotRunning(ValueError): pass


# =============================================================================
# DATA SERVER
# =============================================================================

class TablesServer(mp.Process):

    def __init__(self, h5file, app=None, group=None, name="TablesServer", **kwargs):
        if not isinstance(h5file, tb.File):
            msg = "'h5file' must be an instance of 'tables.File'. Found: {}"
            raise TypeError(msg.format(type(h5file)))
        if app and not isinstance(app, bt.Bottle):
            msg = "'app' must be an instance of 'bottle.Bottle'. Found: {}"
            raise TypeError(msg.format(type(app)))
        super(TablesServer, self).__init__(group=group, name=name)

        self._h5file = h5file
        self._h5file.flush()

        self._kwargs = kwargs
        self._kwargs.setdefault("host", DEFAULT_HOST)
        self._kwargs.setdefault("port", DEFAULT_PORT)

        self._app = app or bt.Bottle()
        self.connect(self._app)

        self._node_buff = {}

    # =========================================================================
    # MAGIC
    # =========================================================================
    def __repr__(self):
        return "<TablesServer '{}'>".format(self._h5file.filename)


    # =========================================================================
    # PROPERTIES
    # =========================================================================
    @property
    def h5file(self):
        return self._h5file

    @property
    def kwargs(self):
        return dict(self._kwargs)

    @property
    def app(self):
        return self._app

    # =========================================================================
    # FUNCTIONS
    # =========================================================================
    def run(self):
        bt.run(self._app, **self._kwargs)

    def serialize(self, data):
        try:
            return dumps(data)
        except Exception as err:
            bt.response.status = 500
            return dumps(err)

    def get_node(self, key):
        if key not in self._node_buff:
            self._node_buff[key] = self._h5file.get_node(*key)
        return self._node_buff[key]

    # =========================================================================
    # ROUTES
    # =========================================================================
    def connect(self, app):

        # POST
        @app.route("/node_append", method="POST")
        def node_append():
            key = (
                bt.request.forms["where"],
                bt.request.forms.get("name"),
                bt.request.forms.get("classname"))
            node = self.get_node(key)
            rows = pickle.load(bt.request.files["rows"].file)
            return self.serialize(node.append(rows))

        @app.route("/node_flush", method="POST")
        def node_flush():
            key = (
                bt.request.forms["where"],
                bt.request.forms.get("name"),
                bt.request.forms.get("classname"))
            node = self.get_node(key)
            return self.serialize(node.flush())

        @app.route("/flush", method="POST")
        def file_flush():
            self.h5file.flush()

        # GET
        @app.route("/has_node", method="GET")
        def has_node():
            path = bt.request.forms["path"]
            status = path in self.h5file
            return self.serialize(status)

        @app.route("/ping", method="GET")
        def ping():
            return six.b(self._h5file.filename)


# =============================================================================
# NODE PROXY
# =============================================================================

class _NodeProxy(object):

    def __init__(self, where, name, classname, rh5):
        self._where = where
        self._name = name
        self._classname = classname
        self._rh5 = rh5

    def __repr__(self):
        return "<_NodeProxy (where={}, name={}, classname={}) {}>".format(
            self._where, self._name, self._classname, self._rh5.url)

    def __setitem__(self, k, v):
        self.add_to_current_row(k, v)

    @property
    def where(self):
        return self._where
    @property
    def name(self):
        return self._name
    @property
    def classname(self):
        return self._classname

    @property
    def rh5(self):
        return self._rh5

    def append(self, rows):
        data = {
            "where": self._where, "name": self._name,
            "classname": self._classname}
        files = {"rows": dumps(rows)}
        self._rh5.post("node_append", data=data, files=files)

    def flush(self):
        data = {
            "where": self._where, "name": self._name,
            "classname": self._classname}
        self._rh5.post("node_flush", data=data)


# =============================================================================
# THE FILE PROXY
# =============================================================================

class MPTablesFile(object):

    def __init__(self, url):
        self._url = url
        self._node_buff = {}

    # =========================================================================
    # MAGIC
    # =========================================================================
    def __enter__(self):
        """Enter a context and return self."""
        return self

    def __exit__(self, *exc_info):
        return False

    def __contains__(self, k):
        return self.has_node(k)

    def __repr__(self):
        mem = hex(id(self))
        return "<MPTablesFile '{}' at {}>".format(self._url, mem)

    # =========================================================================
    # PROPERTIES
    # =========================================================================
    @property
    def url(self):
        return self._url

    # =========================================================================
    # FUNCTIONS
    # =========================================================================
    def deserialize_response(self, response):
        content = response.content
        if content:
            data = loads(content)
            if isinstance(data, Exception):
                raise data
            return data

    def post(self, url, deserialize=True, *args, **kwargs):
        full_url = "/".join((self.url, url))
        response = requests.post(url=full_url, *args, **kwargs)
        return (
            self.deserialize_response(response)
            if deserialize else response.content)

    def get(self, url, deserialize=True, *args, **kwargs):
        full_url = "/".join((self.url, url))
        response = requests.get(url=full_url, *args, **kwargs)
        return (
            self.deserialize_response(response)
            if deserialize else response.content)

    # =========================================================================
    # API POST
    # =========================================================================
    def ping(self):
        response = self.get("ping", deserialize=False)
        return six.text_type(response)

    def has_node(self, nodename):
        status = self.get("has_node", data={"path": nodename})
        return status

    def get_node(self, where, name=None, classname=None):
        key = (where, name, classname)
        if key not in self._node_buff:
            self._node_buff[key] = _NodeProxy(
                where=where, name=name, classname=classname, rh5=self)
        return self._node_buff[key]

    def flush(self):
        self.post("flush")


# =============================================================================
# FUNCTIONS
# =============================================================================

def server_to_url(server, url_template=TPL_URL):
    host = server.kwargs["host"]
    port = server.kwargs["port"]
    url = url_template.substitute(host=host, port=port)
    return url


def connect(conn, *args, **kwargs):
    if isinstance(conn, TablesServer):
        conn = server_to_url(conn)
    return MPTablesFile(conn)


def dumps(data, *args, **kwargs):
    return pickle.dumps(
        data, protocol=pickle.HIGHEST_PROTOCOL, *args, **kwargs)


def loads(stream, *args, **kwargs):
    return pickle.loads(stream, *args, **kwargs)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
