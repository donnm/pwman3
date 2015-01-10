# ============================================================================
# This file is part of Pwman3.
#
# Pwman3 is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2
# as published by the Free Software Foundation;
#
# Pwman3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pwman3; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ============================================================================
# Copyright (C) 2013-2014 Oz Nahum Tiram <nahumoz@gmail.com>
# ============================================================================

import sys
import unittest
import os
import os.path
from pwman.data import factory
from pwman.data.drivers.sqlite import DatabaseException, SQLite
from pwman.ui import get_ui_platform
from pwman.data.database import __DB_FORMAT__
from .test_tools import (SetupTester)

PwmanCliNew, OSX = get_ui_platform(sys.platform)
testdb = os.path.join(os.path.dirname(__file__), "test.pwman.db")
_saveconfig = False


class TestFactory(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        SetupTester().clean()

    def setUp(self):
        "test that the right db instance was created"
        self.dbtype = 'SQLite'
        self.db = factory.create(self.dbtype, __DB_FORMAT__, testdb)
        self.tester = SetupTester(__DB_FORMAT__, testdb)
        self.tester.create()

    def test_factory_check_db_ver(self):
        self.assertEqual(factory.check_db_version('SQLite', testdb), 0.6)

    def test_factory_check_db_file(self):
        factory.create('SQLite', version='0.3', filename='baz.db')
        self.assertEqual(factory.check_db_version('SQLite', 'baz.db'), 0.3)
        os.unlink('baz.db')

    def test_factory_create(self):
        db = factory.create('SQLite', filename='foo.db')
        db._open()
        self.assertTrue(os.path.exists('foo.db'))
        db.close()
        os.unlink('foo.db')
        self.assertIsInstance(db, SQLite)
        self.assertRaises(DatabaseException, factory.create, 'UNKNOWN')


if __name__ == '__main__':
    # make sure we use local pwman
    sys.path.insert(0, os.getcwd())
    # check if old DB exists, if so remove it.
    # excuted only once when invoked upon import or
    # upon run
    SetupTester().clean()
    unittest.main(verbosity=1, failfast=True)
