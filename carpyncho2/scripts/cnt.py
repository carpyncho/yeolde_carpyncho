#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corral import db
from carpyncho.models import Match, MasterSource


with db.session_scope() as session:
    query = session.query(
        db.func.count(Match.id)
    ).filter(Match.tile_id.is_(None))
    print query.all()

