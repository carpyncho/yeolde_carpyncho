#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# IMPORTS
# =============================================================================

import six

# =============================================================================
# OPERATIONS
# =============================================================================

OP_EQ = "=="
OP_NE = "!="
OP_LE = "<="
OP_LT = "<"
OP_GT = ">"
OP_GE = ">="
OP_AND = "&"
OP_OR = "|"
OP_INVERT = "~"
OP_LIKE = "like"
OP_ILIKE = "ilike"
OP_BELONGS = "belongs"


OPERATIONS = (
    OP_EQ, OP_NE, OP_LE, OP_LT, OP_GT, OP_GE, OP_AND,
    OP_OR, OP_INVERT, OP_LIKE, OP_ILIKE, OP_BELONGS)


OP = "OP"
LEFT = "LEFT"
RIGHT = "RIGHT"


OP_FUNCTIONS = {
    OP_EQ: lambda r, l: r == l,
    OP_NE: lambda r, l: r != l,
    OP_LE: lambda r, l: r <= l,
    OP_LT: lambda r, l: r < l,
    OP_GT: lambda r, l: r > l,
    OP_GE: lambda r, l: r >= l,
    OP_AND: lambda r, l: r & l,
    OP_OR: lambda r, l: r | l,
    OP_INVERT: lambda r, l: ~r,
    OP_LIKE: lambda r, l: r.like(l),
    OP_ILIKE: lambda r, l: r.ilike(l),
    OP_BELONGS: lambda r, l: r.in_(l),
}


DOWNLOAD_FORMATS = ["csv"]


# =============================================================================
# EXPRESSION CLASS
# =============================================================================

class Expression(object):

    def __init__(self, prev, op=None, v=None):
        if op is not None and op not in OPERATIONS:
            msg = "Invalid operation '{} {} {}'".format(name, op, v)
            raise ValueError(msg)
        self.prev = prev
        self.op = op
        self.v = v

    def compile(self):
        l, o, r = self.prev, self.op, self.v
        if o is None:
            return l
        data = {}
        return {
            LEFT: l.compile() if isinstance(l, Expression) else l, OP: o,
            RIGHT: r.compile() if isinstance(r, Expression) else r}

    def _chain(self, op, v=None):
        return Expression(self, op, v)

    def _not_between_expressions(self, op, v):
        if isinstance(self.prev, Expression) or isinstance(v, Expression):
            msg = "'{}' are no allowed in between expressions".format(op)
            raise TypeError(msg)

    def _only_between_expressions(self, op, v):
        between = (
            isinstance(self.prev, Expression) and isinstance(v, Expression))
        if not between:
            msg = "'{}' are allowed only in between expressions".format(op)
            raise TypeError(msg)

    def _only_strings(self, op, v):
        if not isinstance(v, str):
            msg = "'{}' only support strings".format(op)
            raise ValueError(msg)

    def __str__(self):
        prev = self.prev
        if isinstance(prev, str):
            return prev
        elif isinstance(prev.prev, Expression):
            prev = "({})".format(self.prev)
        if self.op and self.v:
            return "{} {} {}".format(prev, self.op, self.v)
        elif self.op:
            return "{}{}".format(self.op, prev)

    def __repr__(self):
        return "<Expression := '{}'>".format(self)

    def __and__(self, v):
        self._only_between_expressions(OP_AND, v)
        return self._chain(OP_AND, v)

    def __or__(self, v):
        self._only_between_expressions(OP_OR, v)
        return self._chain(OP_OR, v)

    def __invert__(self):
        return self._chain(OP_INVERT)

    def __eq__(self, v):
        self._not_between_expressions(OP_EQ, v)
        return self._chain(OP_EQ, v)

    def __ne__(self, v):
        self._not_between_expressions(OP_NE, v)
        return self._chain(OP_NE, v)

    def __le__(self, v):
        self._not_between_expressions(OP_LE, v)
        return self._chain(OP_LE, v)

    def __lt__(self, v):
        self._not_between_expressions(OP_LT, v)
        return self._chain(OP_LT, v)

    def __gt__(self, v):
        self._not_between_expressions(OP_GT, v)
        return self._chain(OP_GT, v)

    def __ge__(self, v):
        self._not_between_expressions(OP_GE, v)
        return self._chain(OP_GE, v)

    def like(self, v):
        self._not_between_expressions(OP_LIKE, v)
        self._only_strings(OP_LIKE, v)
        return self._chain(OP_LIKE, v)

    def ilike(self, v):
        self._not_between_expressions(OP_ILIKE, v)
        self._only_strings(OP_ILIKE, v)
        return self._chain(OP_ILIKE, v)

    def belongs(self, v):
        self._not_between_expressions(OP_BELONGS, v)
        if not hasattr(v, "__iter__"):
            msg = "'{}' operator need some kind of iterable".format(OP_BELONGS)
            raise ValueError(msg)
        return self._chain(OP_BELONGS, v)


# =============================================================================
# NAME SPACES
# =============================================================================

class NS(object):

    def __init__(self, namespace, attrs=None):
        self._ns = namespace
        self._attrs = attrs

    def __repr__(self):
        return "<NS: {}({})>".format(self._ns, self._attrs or "")

    def __getattr__(self, name):
        if self._attrs is not None and name not in self._attrs:
            msg = "{} has not attribute '{}'"
            raise AttributeError(msg.format(self._ns, name))
        full_name = ".".join([self._ns, name])
        return Expression(full_name)

    def get_ns_name(self):
        return self._ns

    def get_ns_attrs(self):
        return tuple(self._attrs)


# =============================================================================
# THE QUERY
# =============================================================================

class CarpynchoQuery(object):

    def __init__(self, ra, dec, radius, columns, offset, limit, orderby):

        if (ra, dec, radius) != (None, None, None):
            try:
                ra, dec, radius = float(ra), float(dec), float(radius)
            except TypeError:
                msg = ("'ra', 'dec' and 'radius' "
                       "must be all None or all numeric values")
                raise TypeError(msg)
            self._conesearch = {"ra": ra, "dec": dec, "radius": radius}
        else:
            self._conesearch = None

        if columns is not None:
            compiled_cols = []
            for col in columns:
                if not (isinstance(col, Expression) and
                        isinstance(col.prev, str)):
                    msg = (
                        "'cols' must be a list of namespace attributes, "
                        "found: '{}' of type {}").format(col, type(col))
                    raise TypeError(msg)
                compiled_col = col.compile()
                if isinstance(compiled_col, dict):
                    msg = "Not operation alloweds over columns selectors"
                    raise TypeError(msg)
                elif compiled_col in compiled_cols:
                    msg = "Duplicated column '{}'".format(compiled_col)
                    raise ValueError(msg)
                compiled_cols.append(compiled_col)
            columns = compiled_cols

        offset = None if offset is None else int(offset)
        limit = None if limit is None else int(limit)

        if orderby is not None:
            if not hasattr(orderby, "__iter__"):
                orderby = [orderby]
            new_orderby = []
            for ob in orderby:
                if not isinstance(ob, Expression):
                    msg = (
                        "'orderby' must be a single or a list "
                        "namespace attributes")
                    raise TypeError(msg)
                new_orderby.append(ob.compile())
            orderby = new_orderby

        self._options = {"columns": columns, "offset": offset, "limit": limit,
                         "orderby": orderby}
        self._filters = []

    def _add_expression(self, expr):
        if not isinstance(expr, Expression):
            raise TypeError(
                "'{}' is not a CarpynchoQuery Expression".format(expr))
        self._filters.append(expr)

    def filter(self, *exprs):
        if not exprs:
            raise ValueError("filter expected at least 1 argument, got 0")
        for expr in exprs:
            self._add_expression(expr)
        return self

    def is_search_empty(self):
        empty_cs = not self._conesearch
        empty_filters = not self._filters
        return empty_cs and empty_filters

    def compile(self):
        if self.is_search_empty():
            raise ValueError("The search is empty")
        filters = None
        for flt in self._filters:
            if filters is None:
                filters = flt.compile()
            else:
                filters = {OP: OP_AND, LEFT: filters, RIGHT: flt.compile()}
        return {
            "conesearch": self._conesearch,
            "options": self._options.copy(), "filters": filters}


class Export(object):

    def __init__(self, query, fmt):
        if not isinstance(query, CarpynchoQuery):
            raise TypeError("query must be an instance of CQLQuery")
        if fmt not in DOWNLOAD_FORMATS:
            raise ValueError(
                "'fmt' must be one of: {}".format(", ".join(DOWNLOAD_FORMATS)))
        self._query = query
        self._fmt = fmt

    def compile(self):
        return {"query": self._query.compile(), "fmt": self._fmt}



# =============================================================================
# FUNCTIONS
# =============================================================================

def operator_function(op):
    try:
        return OP_FUNCTIONS[op]
    except KeyError:
        raise ValueError("Invalid operator '{}'".format(op))


def is_ast_expression(obj):
    return (
        isinstance(obj, dict) and
        OP in obj and LEFT in obj and RIGHT in obj)


def is_search(obj):
    return (
        isinstance(obj, dict) and
        tuple(sorted(obj)) == ("conesearch", "filters", "options"))


def is_export(obj):
    return isinstance(obj, dict) and tuple(sorted(obj)) == ("fmt", "query")


def search(ra=None, dec=None, radius=None, columns=None,
           offset=None, limit=None, orderby=None):
    """Creates a query for the carpyncho database, you can specify"""
    query = CarpynchoQuery(ra, dec, radius, columns,
                           offset, limit, orderby)
    return query


def export(query, fmt):
    return Export(query, fmt)


def from_string(src, extra_namespace):
    ns = {"search": search, "export": export}
    ns.update(extra_namespace)
    result_var = "__query__"
    if any(fs in src for fs in ["__", "import", "eval", "exec"]):
        raise ValueError("Invalid query '{}'".format(src))

    lines = [l.rstrip() for l in src.splitlines() if l.strip()]
    lines[-1] = "{} = {}".format(result_var, lines[-1])

    wrapped_src = "\n".join(lines)
    six.exec_(wrapped_src, ns, ns)
    return ns[result_var]

