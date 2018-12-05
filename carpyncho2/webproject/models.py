#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import hashlib

from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.fields.json import JSONField


class Profile(models.Model):

    user = models.OneToOneField(User, related_name="profile")
    affiliation = models.CharField(max_length=500, help_text="")
    note = models.TextField(help_text="Why do you want a Capyncho user? (or any other commentary)")

    def __unicode__(self):
        return u"{}".format(self.user)


class CQLAst(models.Model):
    class Meta:
        verbose_name = "CQL AST"
        verbose_name_plural = "CQL ASTs"

    _ast = models.TextField(db_column="ast", default="null")
    hash = models.CharField(max_length=255, unique=True)

    @classmethod
    def get_register(cls, ast_str):
        ast_hash = hashlib.sha256(ast_str).hexdigest()
        try:
            obj = CQLAst.objects.get(hash=ast_hash)
        except CQLAst.DoesNotExist:
            obj = CQLAst(hash=ast_hash)
            obj.ast = json.loads(ast_str)
            obj.save()
        return obj

    @property
    def ast(self):
        return json.loads(self._ast)

    @ast.setter
    def ast(self, v):
        self._ast = json.dumps(v)

    def __unicode__(self):
        return u"'{}'".format(self.ast)


class CQLQuery(models.Model):
    class Meta:
        verbose_name = "CQL Query"
        verbose_name_plural = "CQL Queries"

    query = models.TextField()
    hash = models.CharField(max_length=255)
    ast = models.ForeignKey(CQLAst)
    users = models.ManyToManyField(User, related_name="cql_queries")
    counter = models.PositiveIntegerField(default=0)

    @classmethod
    def get_register(cls, cql, ast, user):
        cql_hash = hashlib.sha256(cql).hexdigest()
        try:
            obj = CQLQuery.objects.get(hash=cql_hash)
        except CQLQuery.DoesNotExist:
            obj = CQLQuery(hash=cql_hash)
            obj.query = cql
            obj.ast = ast
            obj.save()
        obj.counter += 1
        obj.users.add(user)
        return obj

    def __unicode__(self):
        return u"'{}'".format(self.query)
