#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

from carpyncho import cql


# =============================================================================
# CONSTANTS
# =============================================================================

CQL_LIB_PATH = os.path.abspath(os.path.dirname(cql.__file__))

EXPRESSION_PY_PATH = os.path.join(CQL_LIB_PATH, "expressions.py")

with codecs.open(EXPRESSION_PY_PATH, encoding="utf8") as fp:
    EXPRESSIONS_PY = "\n".join(
        line.rstrip()
        for line in fp.readlines()
        if line.strip() and line.strip()[0] != "#")

NAMESPACES_PY = "\n".join(
    "{} = {}('{}', {})".format(k, cql.NS.__name__, k, ns.get_ns_attrs())
    for k, ns in cql.NAMESPACES.items())

CQL_EXEC_NAMESPACE_PY = "{{{}}}".format(", ".join(
    "'{}': {}".format(k, k) for k in cql.NAMESPACES.keys()
))


DEFAULT_CQL_QUERY = "search(ra, dec, radius).filter(...)"


# =============================================================================
# FUNCTIONS
# =============================================================================

def cql(request):
    return {
        "EXPRESSIONS_PY": EXPRESSIONS_PY,
        "NAMESPACES_PY": NAMESPACES_PY,
        "CQL_EXEC_NAMESPACE_PY": CQL_EXEC_NAMESPACE_PY,
        "DEFAULT_CQL_QUERY": DEFAULT_CQL_QUERY}
