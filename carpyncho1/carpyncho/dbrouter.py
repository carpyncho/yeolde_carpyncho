#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

class AppDBRouter(object):

    def _db_by_app_label(self, model):
        app_label = model._meta.app_label
        return app_label if app_label in settings.DATABASES else "default"

    def db_for_read(self, model, **hints):
        return self._db_by_app_label(model)

    def db_for_write(self, model, **hints):
        return self._db_by_app_label(model)

    def allow_migrate(self, db, model):
        db_sugested = self._db_by_app_label(model)
        return db_sugested == db
