#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created at 2015-12-07T20:41:54.110455 by corral 0.0.1


# =============================================================================
# DOCS
# =============================================================================

"""carpyncho database models

"""

# =============================================================================
# IMPORTS
# =============================================================================

import os
import shutil

import numpy as np

from corral import db
from corral.conf import settings

from astropy.coordinates import SkyCoord


# =============================================================================
# TILE
# =============================================================================

class Tile(db.Model):
    """Represent a VVV tile. Can has 3 states:

    - `raw`: The tile is discovery and only a path to the original path
      is added
    - `measures`: The tile know how many sources they has and the serialized
      version of the file is loaded.
    - `loaded`: All the sources of the tile are created on *MasterSource* table

    """

    __tablename__ = "Tile"

    statuses = db.Enum("raw", "measured", "loaded", name="tile_statuses")

    ready = db.Column(db.Boolean, default=False)

    id = db.Column(db.Integer, db.Sequence('tile_id_seq'), primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True, unique=True)
    _filename = db.Column("filename", db.Text)

    data = db.Column(db.PickleType, nullable=True)
    data_size = db.Column(db.Integer, nullable=True)
    data_readed = db.Column(db.Integer, nullable=True)

    status = db.Column(statuses, default="raw")

    def __repr__(self):
        return "<Tile '{}'>".format(self.name)

    def file_path(self):
        if self._filename:
            return os.path.join(
                settings.STORED_TILES_DIR, self._filename)

    def store_file(self, fpath):
        self._filename = os.path.basename(fpath)
        shutil.copyfile(fpath, self.file_path())


# =============================================================================
# MASTER SOURCE
# =============================================================================

class MasterSource(db.Model):

    __tablename__ = "MasterSource"
    __table_args__ = (
        db.UniqueConstraint('tile_id', 'order', name='_tile_order_uc'),
    )

    id = db.Column(
        db.Integer, db.Sequence('master_src_id_seq'), primary_key=True)

    tile_id = db.Column(db.Integer, db.ForeignKey('Tile.id'), nullable=False)
    tile = db.relationship("Tile", backref=db.backref("sources"))

    order = db.Column(db.Integer, nullable=False)

    ra_h = db.Column(db.Float, nullable=False)
    dec_h = db.Column(db.Float, nullable=False)

    ra_j = db.Column(db.Float, nullable=False)
    dec_j = db.Column(db.Float, nullable=False)

    ra_k = db.Column(db.Float, nullable=False)
    dec_k = db.Column(db.Float, nullable=False)

    x = db.Column(db.Float, nullable=True)
    y = db.Column(db.Float, nullable=True)
    z = db.Column(db.Float, nullable=True)

    type = db.Column(db.String(255))

    @classmethod
    def conesearch(cls, ra, dec, radius):
        x, y, z = SkyCoord(
            ra=ra, dec=dec, unit="deg", frame="icrs"
        ).represent_as("cartesian").xyz.value
        cos_r = np.cos(radius)
        query = (cls.x * x + cls.y * y + cls.z * z) >= cos_r
        return query

    def __repr__(self):
        return u"<MasterSource '{}[{}]'>".format(self.tile, self.order)


# =============================================================================
# CLASSIFICATIONS
# =============================================================================

class Classification(db.Model):

    __tablename__ = "Classification"

    id = db.Column(
        db.Integer, db.Sequence('classification_id_seq'), primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return "<Classification '{}'>".format(self.name)


class ClassificationXMasterSource(db.Model):

    __tablename__ = "ClassificationXMasterSource"
    __table_args__ = (
        db.UniqueConstraint('classification_id', 'master_src_id',
                            name='_classification_master_src_uc'),
    )

    id = db.Column(db.Integer, db.Sequence('cxms_id_seq'), primary_key=True)

    classification_id = db.Column(
        db.Integer, db.ForeignKey('Classification.id'), nullable=False)
    classification = db.relationship(
        "Classification", backref=db.backref("cxms"))

    master_src_id = db.Column(
        db.Integer, db.ForeignKey('MasterSource.id'), nullable=False)
    master_src = db.relationship(
        "MasterSource", backref=db.backref("cxms"))

    extra_data = db.Column(db.JSONType)

    def __repr__(self):
        string = "<CXMS '{}: {}'>"
        return string.format(self.classification.name, str(self.master_src))


# =============================================================================
# LIGHT CURVE
# =============================================================================

class LightCurve(db.Model):

    __tablename__ = "LightCurve"

    id = db.Column(
        db.Integer, db.Sequence('lightcurve_id_seq'), primary_key=True)

    source_id = db.Column(
        db.Integer, db.ForeignKey('MasterSource.id'),
        nullable=False, unique=True)
    source = db.relationship(
        "MasterSource", backref=db.backref("lightcurve"), uselist=False)

    obs_number = db.Column(db.Integer)
    pdm_period = db.Column(db.Float, nullable=True)
    ls_period = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return "<LightCurve '{}'>".format(repr(self.source))


# =============================================================================
# PAWPRINT
# =============================================================================

class Pawprint(db.Model):

    __tablename__ = "Pawprint"

    statuses = db.Enum("raw", "measured", "loaded", name="pawprint_statuses")

    id = db.Column(
        db.Integer, db.Sequence('pawprint_id_seq'), primary_key=True)

    name = db.Column(db.String(255), nullable=False, unique=True)
    mjd = db.Column(db.Float, nullable=True)

    data = db.Column(db.PickleType, nullable=True)
    data_size = db.Column(db.Integer, nullable=True)
    data_readed = db.Column(db.Integer, nullable=True)

    _filename = db.Column("filename", db.Text)

    status = db.Column(statuses, default="raw")

    def __repr__(self):
        return "<Pawprint '{}'>".format(repr(self.name))

    def file_path(self):
        if self._filename:
            yearmonth = self._filename[1:7]
            day = self._filename[7:9]
            return os.path.join(
                settings.STORED_PAWPRINT_DIR, yearmonth, day, self._filename)

    def store_file(self, fpath):
        self._filename = os.path.basename(fpath)
        file_path = self.file_path()
        file_dir = os.path.dirname(file_path)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        shutil.copyfile(fpath, file_path)


class PawprintXTile(db.Model):

    __tablename__ = "PawprintXTile"
    __table_args__ = (
        db.UniqueConstraint('pawprint_id', 'tile_id',
                            name='_pawprint_tile_uc'),
    )

    statuses = db.Enum(
        "raw", "pending", "sync", name="pawprint_x_tile_statuses")

    id = db.Column(db.Integer, db.Sequence('pxt_id_seq'), primary_key=True)

    pawprint_id = db.Column(
        db.Integer, db.ForeignKey('Pawprint.id'), nullable=False)
    pawprint = db.relationship(
        "Pawprint", backref=db.backref("pxts"))

    tile_id = db.Column(db.Integer, db.ForeignKey('Tile.id'), nullable=False)
    tile = db.relationship("Tile", backref=db.backref("pxts"))

    status = db.Column(statuses, default="raw")

    def __repr__(self):
        string = "<PXT '{}: {}'>"
        return string.format(self.tile.name, self.pawprint.name)


class PawprintSource(db.Model):

    __tablename__ = "PawprintSource"
    __table_args__ = (
        db.UniqueConstraint('pawprint_id', 'order', name='_pawprint_order_uc'),
    )

    id = db.Column(
        db.Integer, db.Sequence('pawprint_src_id_seq'), primary_key=True)

    pawprint_id = db.Column(
        db.Integer, db.ForeignKey('Pawprint.id'), nullable=False)
    pawprint = db.relationship(
        "Pawprint", backref=db.backref("pxt"))

    order = db.Column(db.Integer, nullable=False)

    ra_deg = db.Column(db.Float)
    ra_h = db.Column(db.Float)
    ra_m = db.Column(db.Float)
    ra_s = db.Column(db.Float)
    dec_deg = db.Column(db.Float)
    dec_d = db.Column(db.Float)
    dec_m = db.Column(db.Float)
    dec_s = db.Column(db.Float)
    pwp_x = db.Column(db.Float)
    pwp_y = db.Column(db.Float)
    mag = db.Column(db.Float)
    mag_err = db.Column(db.Float)
    chip_nro = db.Column(db.Float)
    stel_cls = db.Column(db.Float)
    elip = db.Column(db.Float)
    pos_ang = db.Column(db.Float)

    hjd = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return u"<PawprintSource '{}[{}]'>".format(self.pawprint, self.order)


# =============================================================================
# CLASS MATCH
# =============================================================================

class Match(db.Model):

    __tablename__ = "Match"
    __table_args__ = (
        db.UniqueConstraint('pawprint_src_id', 'master_src_id', 'tile_id',
                            name='_match_uc'),
    )

    id = db.Column(db.Integer, db.Sequence('match_id_seq'), primary_key=True)

    band = db.Column(
        db.Enum("k", "j", "h", name="match, bands"), index=True)

    tile_id = db.Column(
        db.Integer, db.ForeignKey('Tile.id'), index=True, nullable=False)
    tile = db.relationship(
        "Tile", backref=db.backref("matches"), lazy="joined")
    master_src_id = db.Column(
        db.Integer, db.ForeignKey('MasterSource.id'),
        index=True, nullable=False)
    master_src = db.relationship(
        "MasterSource", backref=db.backref("matches"), lazy="joined")
    master_src_order = db.Column(db.Integer)
    master_src_ra = db.Column(db.Float)
    master_src_dec = db.Column(db.Float)

    pawprint_id = db.Column(
        db.Integer, db.ForeignKey('Pawprint.id'), index=True, nullable=False)
    pawprint = db.relationship(
        "Pawprint", backref=db.backref("matches"), lazy="joined")
    pawprint_src_id = db.Column(
        db.Integer, db.ForeignKey('PawprintSource.id'),
        index=True, nullable=False)
    pawprint_src = db.relationship(
        "PawprintSource", backref=db.backref("matches"), lazy="joined")
    pawprint_src_order = db.Column(db.Integer)
    pawprint_src_ra = db.Column(db.Float)
    pawprint_src_dec = db.Column(db.Float)
    pawprint_src_mag = db.Column(db.Float)
    pawprint_src_mag_err = db.Column(db.Float)
    pawprint_src_hjd = db.Column(db.Float, nullable=True)
    pawprint_src_chip_nro = db.Column(db.Float)
    pawprint_src_stel_cls = db.Column(db.Float)
    pawprint_src_elip = db.Column(db.Float)
    pawprint_src_pos_ang = db.Column(db.Float)

    tile_id = db.Column(
        db.Integer, db.ForeignKey('Tile.id'), index=True, nullable=False)
    tile = db.relationship(
        "Tile", backref=db.backref("matches"), lazy="joined")

    def __repr__(self):
        return u"<Match '{}->{}'>".format(self.master_src, self.pawprint_src)
