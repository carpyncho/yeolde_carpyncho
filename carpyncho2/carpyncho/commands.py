#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created at 2015-12-07T20:41:54.110455 by corral 0.0.1


# =============================================================================
# DOCS
# =============================================================================

"""Command line commands for carpyncho

"""


# =============================================================================
# IMPORTS
# =============================================================================

import sys
import os
import shutil
import argparse
from pprint import pprint

from texttable import Texttable

from sqlalchemy.engine import url

from sqlalchemy_utils import database_exists, create_database, drop_database

from corral import cli, conf, db, core

from carpyncho import bin, cql
from carpyncho .libs import tiles2hdf5
from carpyncho.models import Tile, Pawprint, PawprintXTile


# =============================================================================
# COMMANDS
# =============================================================================

if conf.settings.DEBUG:

    class FreshLoad(cli.BaseCommand):
        """Reset the database and run the loader class (only in debug)"""

        def setup(self):
            self.conn = conf.settings.CONNECTION

            urlo = url.make_url(self.conn)
            self.backend = urlo.get_backend_name()
            self.db = urlo.database

        def recreate_pg(self):
            if database_exists(self.conn):
                drop_database(self.conn)
            create_database(self.conn)

        def recreate_sqlite(self):
            try:
                os.remove(self.db)
            except OSError:
                pass

        def handle(self):
            if self.backend == "postgresql":
                self.recreate_pg()
            elif self.backend == "sqlite":
                self.recreate_sqlite()

            try:
                shutil.rmtree("_input_data")
            except OSError:
                pass

            try:
                shutil.rmtree("_data")
            except OSError:
                pass

            if not os.path.isdir("example_data"):
                if not os.path.exists("example_data.tar.bz2"):
                    os.system(
                        "wget "
                        "--output-document=example_data.tar.bz2 "
                        "https://db.tt/0ZWM6dPr")
                os.system("tar jxf example_data.tar.bz2")

            shutil.copytree("example_data", "_input_data")
            os.system("python in_corral.py createdb --noinput")
            os.system("python in_corral.py load")


class Paths(cli.BaseCommand):
    """Show the paths of carpyncho"""

    def handle(self):
        table = Texttable(max_width=0)
        table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
        table.header(("Propuse", "Path"))
        table.add_row(("Binary Extensions", conf.settings.BIN_PATH))
        table.add_row(("Input Data", conf.settings.INPUT_PATH))
        table.add_row(("Storage", conf.settings.DATA_PATH))
        print(table.draw())


class BuildBin(cli.BaseCommand):
    """Build the bin executables needed to run carpyncho"""

    def handle(self):
        core.logger.info("Building bin extensions...")
        bin.build()
        core.logger.info("Done")


class LSTile(cli.BaseCommand):
    """List all registered tiles"""

    def _bool(self, e):
        return e.lower() not in ("0", "", "false")

    def setup(self):
        choices = "True 1 true 0 false False".split()
        self.parser.add_argument(
            "-r", "--ready", dest="ready", action="store", choices=choices,
            help="Show only the given ready status")
        self.parser.add_argument(
            "-st", "--status", dest="status", action="store",
            choices=Tile.statuses.enums, nargs="+",
            help="Show only the given status")

    def handle(self, ready, status):
        table = Texttable(max_width=0)
        table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
        table.header(("Tile", "Status", "Size", "Readed", "Ready"))
        cnt = 0

        with db.session_scope() as session:
            query = session.query(
                Tile.name, Tile.status, Tile.data_size,
                Tile.data_readed, Tile.ready)
            if ready is not None:
                ready = self._bool(ready)
                query = query.filter(Tile.ready == ready)
            if status:
                query = query.filter(Tile.status.in_(status))
            map(table.add_row, query)
            cnt = query.count()
        print(table.draw())
        print("Count: {}".format(cnt))


class LSPawprint(cli.BaseCommand):
    """List all registered pawprints"""

    def setup(self):
        self.parser.add_argument(
            "-st", "--status", dest="status", action="store",
            choices=Pawprint.statuses.enums, nargs="+",
            help="Show only the given status")

    def handle(self, status):
        table = Texttable(max_width=0)
        table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
        table.header(("Pawprint", "Status", "MJD", "Size", "Readed"))
        cnt = 0

        with db.session_scope() as session:
            query = session.query(
                Pawprint.name, Pawprint.status, Pawprint.mjd,
                Pawprint.data_size, Pawprint.data_readed)
            if status:
                query = query.filter(Pawprint.status.in_(status))
            map(table.add_row, query)
            cnt = query.count()
        print(table.draw())
        print("Count: {}".format(cnt))


class LSSync(cli.BaseCommand):
    """List the status of every pawprint and thir tile"""

    def setup(self):
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument(
            '-s', '--synced', dest='filter',
            action='store_const', const="synced", default="all",
            help='display only the synced pawprints')
        group.add_argument(
            '-u', '--unsynced', dest='filter',
            action='store_const', const="unsynced",
            help='display only the unsynced pawprints')

    def handle(self, filter):
        table = Texttable(max_width=0)
        table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
        table.header(("Tile", "Pawprint", "Status"))

        with db.session_scope() as session:
            query = session.query(PawprintXTile)
            if filter == "synced":
                query = query.filter(PawprintXTile.status == "sync")
            elif filter == "unsynced":
                query = query.filter(PawprintXTile.status != "sync")

            for pxt in query:
                table.add_row([pxt.tile.name, pxt.pawprint.name, pxt.status])
            print(table.draw())


class CQL(cli.BaseCommand):
    """Execute a Carpyncho Query Language and return the result list of sources

    """

    MAX_ROWS = 100

    def setup(self):
        self.parser.add_argument(
            'cql_query', action="store", help='The CQL query')
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument(
            '--ast', dest='print_ast', default=False, action="store_true",
            help='Print the Abstract syntax tree of the given CQL query')
        group.add_argument(
            '--sql', dest='print_sql', default=False, action="store_true",
            help='Print the SQL equivalent of the CQL')

    def handle(self, cql_query, print_ast, print_sql):
        cql_query_object = cql.from_string(cql_query, cql.NAMESPACES)
        ast = cql_query_object.compile()

        if print_ast:
            pprint(ast)
            print("")
            return

        with db.session_scope() as session:
            result = cql.eval(ast, session)

            if print_sql:
                print(
                    "DOWNLOAD '{}':\n\t{}".format(result.fmt(), result.query)
                    if isinstance(result, cql.Writer) else
                    result[0])
                print("")
                return

            # DOWNLOAD
            if isinstance(result, cql.Writer):
                result.dump(sys.stdout)
                return

            # NORMAL QUERY
            sqla_query, column_names = result

            table = Texttable(max_width=0)
            table.set_deco(
                Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
            count = sqla_query.count()

            if  sqla_query.count() > self.MAX_ROWS:
                sqla_query = sqla_query.limit(self.MAX_ROWS)
                count = self.MAX_ROWS

            table.header(column_names)
            for idx, row in enumerate(sqla_query):
                table.add_row(row)

            print(table.draw())
            print("ROWCOUNT = {}".format(count))


class Django(cli.BaseCommand):
    """Send the remaining parameters to the django project of the webpage"""

    def setup(self):
        self.parser.add_argument(
            'arguments', nargs=argparse.REMAINDER,
            help="Django arguments (see 'python in_corrral.py django help')")

    def handle(self, arguments):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webproject.settings")
        from django.core.management import execute_from_command_line
        execute_from_command_line(["corral"] + arguments)


class DumpTiles(cli.BaseCommand):
    """Dump a given list of tiles into a hdf5 file"""

    def setup(self):
        self.parser.add_argument(
            "tiles", nargs="+", help="list of tile names to be dumped")
        self.parser.add_argument(
            "-o", "--output", help="hdf5 file path",
            required=True, dest="output")
        self.parser.add_argument(
            "-a", "--append", dest="append",
            help="append to existing file", action="store_true")
        self.parser.add_argument(
            "-p", "--procs", dest="procs", type=int, default=1,
            help="how many process you need to run", action="store")
        self.parser.add_argument(
            "-sync", "--sync", dest="sync",
            help="execute all process as a sequence", action="store_true")

    def handle(self, tiles, output, append, procs, sync):
        mode = "r+" if append else "w"
        if os.path.exists(output) and mode == "w":
            raise OSError("File '{}' already exists".format(output))
        with db.session_scope() as session:
            procs = tiles2hdf5.dump(session, tiles, output, mode, procs, sync)
            if not sync:
                for proc in procs:
                    proc.join()
                exitcodes = [proc.exitcode for proc in procs]
                status = sum(exitcodes)
                if status:
                    sys.exit(status)
