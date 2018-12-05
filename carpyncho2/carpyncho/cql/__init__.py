#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# IMPORTS
# =============================================================================

from collections import defaultdict

from corral import db

from ..models import Tile, MasterSource

from .io import Writer, create_writer
from .expressions import (
    NS, search, from_string, operator_function,
    is_ast_expression, is_search, is_export,
    OP, LEFT, RIGHT, OP_INVERT)


# =============================================================================
# CONSTANTS
# =============================================================================

MODEL_TO_NAMESPACE = {Tile: "tile", MasterSource: "source"}


EXPOSE = (
    Tile.id, Tile.name,
    MasterSource.id, MasterSource.type,
    MasterSource.ra_h, MasterSource.dec_h,
    MasterSource.ra_j, MasterSource.dec_j,
    MasterSource.ra_k, MasterSource.dec_k,
    MasterSource.x, MasterSource.y, MasterSource.z)


# =============================================================================
# AUTO CONSTANTS
# =============================================================================

def _make_namespaces():
    ns_conf, namespaces = defaultdict(list), {}
    attr_to_field, field_to_attr = {}, {}
    for exposed in EXPOSE:
        namespace = MODEL_TO_NAMESPACE[exposed.class_]
        ns_conf[namespace].append(exposed.key)

        field_name = "{}.{}".format(namespace, exposed.key)
        attr_to_field[field_name] = exposed
        field_to_attr[exposed] = field_name

    for name, attrs in ns_conf.items():
        ns = NS(name, attrs)
        namespaces[name] = ns

    return attr_to_field, field_to_attr, dict(ns_conf), namespaces


ATTR_TO_FIELD, FIELD_TO_ATTR, NS_CONF, NAMESPACES = _make_namespaces()


locals().update(NAMESPACES)

del _make_namespaces


# =============================================================================
# FUNCTIONS
# =============================================================================


def make_filter(flt):
    if is_ast_expression(flt):
        op = operator_function(flt[OP])
        left = make_filter(flt[LEFT])
        right = make_filter(flt[RIGHT])
        return op(left, right)
    else:
        try:
            return ATTR_TO_FIELD.get(flt, flt)
        except TypeError:
            return flt


def selected_columns(columns):
    if columns:
        return [ATTR_TO_FIELD[attr].label(attr) for attr in columns], columns
    fields, columns = [], []
    for field in EXPOSE:
        attr = FIELD_TO_ATTR[field]
        fields.append(field.label(attr))
        columns.append(attr)
    return fields, columns


def get_order(orderby):
    if orderby is not None:
        crits = []
        for ob in orderby:
            desc = False
            if is_ast_expression(ob):
                attr = ob[LEFT]
                desc = (ob[OP] == OP_INVERT)
            else:
                attr = ob
            crit = ATTR_TO_FIELD[attr]
            if desc:
                crit = db.desc(crit)
            crits.append(crit)
        return crits


def eval(ast, session):
    if is_export(ast):
        cql_ast, fmt = ast["query"], ast["fmt"]
        query, column_names = eval(cql_ast, session)
        return create_writer(fmt, query, column_names)

    elif is_search(ast):
        conesearch, filters, options = (
            ast["conesearch"], ast["filters"], ast["options"])

        queries = []
        if conesearch is not None:
            queries.append(MasterSource.conesearch(**conesearch))
        if filters is not None:
            queries.append(make_filter(filters))

        columns, column_names = selected_columns(options["columns"])

        orderby = get_order(options["orderby"])

        query = session.query(*columns).join(
            MasterSource.tile
        ).filter(db.and_(*queries))

        if orderby is not None:
            query = query.order_by(*orderby)
        if options["offset"] is not None:
            offset = int(options["offset"])
            query = query.offset(offset)
        if options["limit"] is not None:
            limit = int(options["limit"])
            query = query.limit(limit)

        return query, column_names
    else:
        raise ValueError("invalid ast")
