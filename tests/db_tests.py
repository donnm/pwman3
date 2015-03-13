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
# Copyright (C) 2013 Oz Nahum <nahumoz@gmail.com>
# ============================================================================

from pwman.data import factory
#from pwman.data.drivers.sqlite import DatabaseException
from pwman.util.config import get_pass_conf
#from pwman.util.generator import leetlist
from pwman.util.crypto_engine import CryptoEngine
from pwman.ui import get_ui_platform
from pwman.ui.tools import CMDLoop, CliMenuItem
# from pwman import (parser_options, get_conf_options, get_conf, set_umask)
from pwman.data.database import __DB_FORMAT__
import sys
import unittest
if sys.version_info.major > 2:
    from io import StringIO
else:
    from StringIO import StringIO
import os
import os.path

dummyfile = """
[Encryption]

[Readline]

[Global]
xsel = /usr/bin/xsel
colors = yes
umask = 0100
cls_timeout = 5

[Database]
"""


#def node_factory(username, password, url, notes, tags=None):
#    node = NewNode()
#    node.username = username
#    node.password = password
#    node.url = url
#    node.notes = notes
#    tags = [TagNew(tn) for tn in tags]
#    node.tags = tags
#
#    return node

_saveconfig = False

PwmanCliNew, OSX = get_ui_platform(sys.platform)


from .test_tools import (SetupTester)  # DummyCallback2,
                         #  DummyCallback3, DummyCallback4)

testdb = os.path.join(os.path.dirname(__file__), "test.pwman.db")


#class DBTests(unittest.TestCase):
#
#    """test everything related to db"""
#
#    def setUp(self):
#        "test that the right db instance was created"
#        dbver = __DB_FORMAT__
#        self.dbtype = 'SQLite'
#        self.db = factory.create(self.dbtype, dbver, testdb)
#        self.tester = SetupTester(dbver, testdb)
#        self.tester.create()
#
#    def test_1_db_created(self):
#        "test that the right db instance was created"
#        self.assertIn(self.dbtype, self.db.__class__.__name__)
#
#    def test_2_db_opened(self):
#        "db was successfuly opened"
#        # it will have a file name associated
#        self.assertTrue(hasattr(self.db, '_filename'))
#
#    def test_3_create_node(self):
#        "test that a node can be successfuly created"
#        # this method does not test do_new
#        # which is a UI method, rather we test
#        # _db.addnodes
#        username = u'tester'
#        password = u'Password'
#        url = u'example.org'
#        notes = u'some notes'
#        node = NewNode()
#        node.username = username
#        node.password = password
#        node.url = url
#        node.notes = notes
#        # node = NewNode(username, password, url, notes)
#        tags = [TagNew(tn) for tn in ['testing1', 'testing2']]
#        node.tags = tags
#        self.db.open()
#        self.db.addnodes([node])
#        idx_created = node._id
#        new_node = self.db.getnodes([idx_created])[0]
#
#        for key, attr in {'password': password, 'username': username,
#                          'url': url, 'notes': notes}.items():
#            self.assertEqual(attr, getattr(new_node, key).decode())
#        self.db.close()
#
#    def test_4_tags(self):
#        enc = CryptoEngine.get()
#        got_tags = self.tester.cli._tags(enc)
#        self.assertEqual(2, len(got_tags))
#
#    def test_5_change_pass(self):
#        enc = CryptoEngine.get()
#        enc.callback = DummyCallback2()
#        self.tester.cli._db.changepassword()
#
#    @unittest.skip("This is broken as long as changepassword isn't working.")
#    def test_6_db_change_pass(self):
#        "fuck yeah, we change the password and the new dummy works"
#        enc = CryptoEngine.get()
#        enc.callback = DummyCallback3()
#        self.tester.cli._db.changepassword()
#        self.tester.cli.do_forget('')
#        enc.callback = DummyCallback4()
#        # TODO: this is broken!
#        self.tester.cli.do_ls('')
#
#    def test_7_db_list_tags(self):
#        # tags are return as ecrypted strings
#        tags = self.tester.cli._db.listtags()
#        self.assertEqual(2, len(tags))
#        self.tester.cli.do_filter('testing1')
#        tags = self.tester.cli._db.listtags()
#        self.assertEqual(2, len(tags))
#        self.tester.cli.do_ls('')
#
#    def test_8_db_remove_node(self):
#        node = self.tester.cli._db.getnodes([1])
#        self.tester.cli._db.removenodes(node)
#        # create the removed node again
#        node = NewNode()
#        node.username = 'tester'
#        node.password = 'Password'
#        node.url = 'example.org'
#        node.notes = 'some notes'
#        tags = [TagNew(tn) for tn in ['testing1', 'testing2']]
#        node.tags = tags
#        self.db.open()
#        self.db.addnodes([node])
#
#    def test_9_sqlite_init(self):
#        db = SQLiteDatabaseNewForm("test")
#        self.assertEqual("test", db._filename)


class CLITests(unittest.TestCase):

    """
    test command line functionallity
    """

    def setUp(self):
        "test that the right db instance was created"
        self.dbtype = 'SQLite'
        self.db = factory.create(self.dbtype, __DB_FORMAT__, testdb)
        self.tester = SetupTester(__DB_FORMAT__, testdb)
        self.tester.create()

    def test_input(self):
        name = self.tester.cli.get_username(reader=lambda: u'alice')
        self.assertEqual(name, u'alice')

    def test_password(self):
        password = self.tester.cli.get_password(None,
                                                reader=lambda x: u'hatman')
        self.assertEqual(password, u'hatman')

    def test_random_password(self):
        password = self.tester.cli.get_password(None, length=7)
        self.assertEqual(len(password), 7)

    #def test_random_leet_password(self):
    #    password = self.tester.cli.get_password(None, leetify=True, length=7)
    #    l_num = 0
    #    for v in leetlist.values():
    #        if v in password:
    #            l_num += 1
        # sometime despite all efforts, randomness dictates that no
        # leetifying happens ...
    #    self.assertTrue(l_num >= 0)

    def test_leet_password(self):
        password = self.tester.cli.get_password(None, leetify=True,
                                                reader=lambda x: u'HAtman')
        # python3 compatability
        if sys.version_info.major < 3:
            self.assertRegexpMatches(password,
                                     ("(H|h)?(A|a|4)?(T|t|\+)?(m|M|\|"
                                      "\/\|)?(A|a|4)?(N|n|\|\\|)?"))
        else:
            self.assertRegex(password, ("(H|h)?(A|a|4)?(T|t|\+)?(m|M|\|"
                                        "\/\|)?(A|a|4)?(N|n|\|\\|)?"))

    def test_get_url(self):
        url = self.tester.cli.get_url(reader=lambda: u'example.com')
        self.assertEqual(url, u'example.com')

    def test_get_notes(self):
        notes = self.tester.cli.get_notes(reader=lambda:
                                          u'test 123\n test 456')
        self.assertEqual(notes, u'test 123\n test 456')

    #def test_get_tags(self):
    #    tags = self.tester.cli.get_tags(reader=lambda: u'looking glass')
    #    for t in tags:
    #        self.assertIsInstance(t, TagNew)

    #    for t, n in zip(tags, u'looking glass'.split()):
    #        self.assertEqual(t.name.strip().decode(), n)

    # creating all the components of the node does
    # the node is still not added !

    #def test_add_new_entry(self):
    #    # node = NewNode('alice', 'dough!', 'example.com',
        #               'lorem impsum')
    #    node = NewNode()
    #    node.username = b'alice'
    #    node.password = b'dough!'
    #    node.url = b'example.com'
    #    node.notes = b'somenotes'
    #    node.tags = b'lorem ipsum'

    #    tags = self.tester.cli.get_tags(reader=lambda: u'looking glass')
    #    node.tags = tags
    #    self.tester.cli._db.addnodes([node])
    #    self.tester.cli._db._cur.execute(
    #        "SELECT ID FROM NODES ORDER BY ID ASC", [])
    #    rows = self.tester.cli._db._cur.fetchall()

        # by now the db should have 2 new nodes
        # the first one was added by test_create_node in DBTests
        # the second was added just now.
        # This will pass only when running all the tests then ...
    #    self.assertEqual(len(rows), 2)

    #    node = NewNode()
    #    node.username = b'alice'
    #    node.password = b'dough!'
    #    node.url = b'example.com'
    #    node.notes = b'somenotes'
    #    node.tags = b'lorem ipsum'

    #    tags = self.tester.cli.get_tags(reader=lambda: u'looking glass')
    #    node.tags = tags
    #    self.tester.cli._db.addnodes([node])

    def test_get_ids(self):
        # used by do_cp or do_open,
        # this spits many time could not understand your input
        self.assertEqual([1], self.tester.cli.get_ids('1'))
        self.assertListEqual([1, 2, 3, 4, 5], self.tester.cli.get_ids('1-5'))
        self.assertListEqual([], self.tester.cli.get_ids('5-1'))
        self.assertListEqual([], self.tester.cli.get_ids('5x-1'))
        self.assertListEqual([], self.tester.cli.get_ids('5x'))
        self.assertListEqual([], self.tester.cli.get_ids('5\\'))

    def test_edit(self):
        node = self.tester.cli._db.getnodes([2])[0]
        menu = CMDLoop()
        menu.add(CliMenuItem("Username", self.tester.cli.get_username,
                             node.username,
                             node.username))
        menu.add(CliMenuItem("Password", self.tester.cli.get_password,
                             node.password,
                             node.password))
        menu.add(CliMenuItem("Url", self.tester.cli.get_url,
                             node.url,
                             node.url))
        menunotes = CliMenuItem("Notes",
                                self.tester.cli.get_notes(reader=lambda:
                                                          u'bla bla'),
                                node.notes,
                                node.notes)
        menu.add(menunotes)
        menu.add(CliMenuItem("Tags", self.tester.cli.get_tags,
                             node.tags,
                             node.tags))

        dummy_stdin = StringIO('4\n\nX')

        class dummy_stdin(object):

            def __init__(self):
                self.idx = -1
                self.ans = ['4', 'some fucking notes', 'X']

            def __call__(self, msg):
                self.idx += 1
                return self.ans[self.idx]

        dstin = dummy_stdin()
        menu.run(node, reader=dstin)
        self.tester.cli._db.editnode(2, node)

    def test_get_pass_conf(self):
        numerics, leet, s_chars = get_pass_conf(self.tester.cli.config)
        self.assertFalse(numerics)
        self.assertFalse(leet)
        self.assertFalse(s_chars)

    def test_do_tags(self):
        self.tester.cli.do_filter('bank')

    def test_do_forget(self):
        self.tester.cli.do_forget('')

    def test_do_auth(self):
        crypto = CryptoEngine.get()
        rv = crypto.authenticate('12345')
        self.assertTrue(rv)
        self.assertFalse(crypto.authenticate('WRONG'))

    def test_do_clear(self):
        self.tester.cli.do_clear('')

    def test_do_exit(self):
        self.assertTrue(self.tester.cli.do_exit(''))


class FactoryTest(unittest.TestCase):

    def test_factory_check_db_ver(self):
        self.assertEqual(factory.check_db_version('SQLite', testdb), 0.5)

    def test_factory_check_db_file(self):
        factory.create('SQLite', version='0.3', filename='baz.db')
        self.assertEqual(factory.check_db_version('SQLite', 'baz.db'), 0.3)
        os.unlink('baz.db')

    #def test_factory_create(self):
    #    db = factory.create('SQLite', filename='foo.db')
    #    db._open()
    #    self.assertTrue(os.path.exists('foo.db'))
    #    db.close()
    #    os.unlink('foo.db')
    #    self.assertIsInstance(db, SQLiteDatabaseNewForm)
    #    self.assertRaises(DatabaseException, factory.create, 'UNKNOWN')


if __name__ == '__main__':
    # make sure we use local pwman
    sys.path.insert(0, os.getcwd())
    # check if old DB exists, if so remove it.
    # excuted only once when invoked upon import or
    # upon run
    SetupTester().clean()
    unittest.main(verbosity=1, failfast=True)
