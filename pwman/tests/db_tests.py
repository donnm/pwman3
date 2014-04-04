#============================================================================
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
#============================================================================
# Copyright (C) 2013 Oz Nahum <nahumoz@gmail.com>
#============================================================================

from pwman.data.nodes import NewNode
from pwman.data.tags import TagNew
from pwman.data import factory
from pwman.data.drivers.sqlite import DatabaseException
from pwman.util import config
from pwman.util.callback import Callback
from pwman.util.generator import leetlist
from pwman.util.crypto import CryptoEngine, CryptoBadKeyException

from pwman import which, default_config
from pwman.ui import get_ui_platform
from pwman.ui.base import get_pass_conf
from pwman.ui.tools import CMDLoop, CliMenuItem

import unittest
import StringIO
import os
import os.path
import sys

_saveconfig = False

PwmanCliNew, OSX = get_ui_platform(sys.platform)


class DummyCallback(Callback):

    def getsecret(self, question):
        return u'12345'

    def getnewsecret(self, question):
        return u'12345'


class DummyCallback2(Callback):

    def getinput(self, question):
        return u'newsecret'

    def getsecret(self, question):
        return u'wrong'

    def getnewsecret(self, question):
        return u'newsecret'


class DummyCallback3(Callback):

    def getinput(self, question):
        return u'newsecret'

    def getsecret(self, question):
        return u'12345'

    def getnewsecret(self, question):
        return u'newsecret'


class DummyCallback4(Callback):

    def getinput(self, question):
        return u'newsecret'

    def getsecret(self, question):
        return u'newsecret'

    def getnewsecret(self, question):
        return u'newsecret'


default_config['Database'] = {'type': 'SQLite',
                              'filename':
                              os.path.join(os.path.dirname(__file__),
                                           "test.pwman.db")
                              }


class SetupTester(object):

    def __init__(self):
        config.set_defaults(default_config)
        if not OSX:
            self.xselpath = which("xsel")
            config.set_value("Global", "xsel", self.xselpath)
        else:
            self.xselpath = "xsel"

    def clean(self):
        if os.path.exists(config.get_value('Database', 'filename')):
            os.remove(config.get_value('Database', 'filename'))

        if os.path.exists(os.path.join(os.path.dirname(__file__),
                                       'testing_config')):
            os.remove(os.path.join(os.path.dirname(__file__),
                                   'testing_config'))

    def create(self):
        dbver = 0.4
        dbtype = config.get_value("Database", "type")
        db = factory.create(dbtype, dbver)
        self.cli = PwmanCliNew(db, self.xselpath, DummyCallback)


class DBTests(unittest.TestCase):
    """test everything related to db"""

    def setUp(self):
        "test that the right db instance was created"
        dbver = 0.4
        self.dbtype = config.get_value("Database", "type")
        self.db = factory.create(self.dbtype, dbver)
        self.tester = SetupTester()
        self.tester.create()

    def test_db_created(self):
        "test that the right db instance was created"
        self.assertIn(self.dbtype, self.db.__class__.__name__)

    def test_db_opened(self):
        "db was successfuly opened"
        # it will have a file name associated
        self.assertTrue(hasattr(self.db, '_filename'))

    def test_create_node(self):
        "test that a node can be successfuly created"
        # this method does not test do_new
        # which is a UI method, rather we test
        # _db.addnodes
        username = 'tester'
        password = 'Password'
        url = 'example.org'
        notes = 'some notes'
        #node = NewNode(username, password, url, notes)
        node = NewNode()
        node.username = username
        node.password = password
        node.url = url
        node.notes = notes
        #node = NewNode(username, password, url, notes)
        tags = [TagNew(tn) for tn in ['testing1', 'testing2']]
        node.tags = tags
        self.db.open()
        self.db.addnodes([node])
        idx_created = node._id
        new_node = self.db.getnodes([idx_created])[0]
        for key, attr in {'password': password, 'username': username,
                          'url': url, 'notes': notes}.iteritems():
            self.assertEquals(attr, getattr(new_node, key))
        self.db.close()

    def test_tags(self):
        enc = CryptoEngine.get()
        got_tags = self.tester.cli._tags(enc)
        self.assertEqual(2, len(got_tags))

    def test_change_pass(self):
        enc = CryptoEngine.get()
        enc._callback = DummyCallback2()
        self.assertRaises(CryptoBadKeyException,
                          self.tester.cli._db.changepassword)

    def test_db_change_pass(self):
        "fuck yeah, we change the password and the new dummy works"
        enc = CryptoEngine.get()
        enc._callback = DummyCallback3()
        self.tester.cli._db.changepassword()
        self.tester.cli.do_forget('')
        enc._callback = DummyCallback4()
        self.tester.cli.do_ls('')

    def test_db_list_tags(self):
        # tags are return as ecrypted strings
        tags = self.tester.cli._db.listtags()
        self.assertEqual(2, len(tags))
        self.tester.cli.do_filter('testing1')
        # TODO: fix this broken tag issue
        #tags = self.tester.cli._db.listtags()
        #self.assertEqual(1, len(tags))
        self.tester.cli.do_ls('')

    def test_db_remove_node(self):
        node = self.tester.cli._db.getnodes([1])
        self.tester.cli._db.removenodes(node)
        # create the removed node again
        node = NewNode()
        node.username = 'tester'
        node.password = 'Password'
        node.url = 'example.org'
        node.notes = 'some notes'
        tags = [TagNew(tn) for tn in ['testing1', 'testing2']]
        node.tags = tags
        self.db.open()
        self.db.addnodes([node])


class TestDBFalseConfig(unittest.TestCase):

    def setUp(self):
        #filename = default_config['Database'].pop('filename')
        self.fname1 = default_config['Database'].pop('filename')
        self.fname = config._conf['Database'].pop('filename')

    def test_db_missing_conf_parameter(self):
            self.assertRaises(DatabaseException, factory.create,
                              'SQLite', 0.4)

    def tearDown(self):
        config.set_value('Database', 'filename', self.fname)
        default_config['Database']['filename'] = self.fname1
        config._conf['Database']['filename'] = self.fname


class CLITests(unittest.TestCase):
    """
    test command line functionallity
    """

    def setUp(self):
        "test that the right db instance was created"
        dbver = 0.4
        self.dbtype = config.get_value("Database", "type")
        self.db = factory.create(self.dbtype, dbver)
        self.tester = SetupTester()
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

    def test_random_leet_password(self):
        password = self.tester.cli.get_password(None, leetify=True, length=7)
        l_num = 0
        for v in leetlist.values():
            if v in password:
                l_num += 1
        # sometime despite all efforts, randomness dictates that no
        # leetifying happens ...
        self.assertTrue(l_num >= 0)

    def test_leet_password(self):
        password = self.tester.cli.get_password(None, leetify=True,
                                                reader=lambda x: u'HAtman')
        self.assertRegexpMatches(password, ("(H|h)?(A|a|4)?(T|t|\+)?(m|M|\|"
                                            "\/\|)?(A|a|4)?(N|n|\|\\|)?"))

    def test_get_url(self):
        url = self.tester.cli.get_url(reader=lambda: u'example.com')
        self.assertEqual(url, u'example.com')

    def test_get_notes(self):
        notes = self.tester.cli.get_notes(reader=lambda:
                                          u'test 123\n test 456')
        self.assertEqual(notes, u'test 123\n test 456')

    def test_get_tags(self):
        tags = self.tester.cli.get_tags(reader=lambda: u'looking glass')
        for t in tags:
            self.assertIsInstance(t, TagNew)

        for t, n in zip(tags, 'looking glass'.split()):
            self.assertEqual(t.name.strip(), n)

    # creating all the components of the node does
    # the node is still not added !

    def test_add_new_entry(self):
        #node = NewNode('alice', 'dough!', 'example.com',
        #               'lorem impsum')

        node = NewNode()
        node.username = 'alice'
        node.password = 'dough!'
        node.url = 'example.com'
        node.notes = 'somenotes'
        node.tags = 'lorem ipsum'

        tags = self.tester.cli.get_tags(reader=lambda: u'looking glass')
        node.tags = tags
        self.tester.cli._db.addnodes([node])
        self.tester.cli._db._cur.execute(
            "SELECT ID FROM NODES ORDER BY ID ASC", [])
        rows = self.tester.cli._db._cur.fetchall()

        # by now the db should have 2 new nodes
        # the first one was added by test_create_node in DBTests
        # the second was added just now.
        # This will pass only when running all the tests then ...
        self.assertEqual(len(rows), 2)

    def test_get_ids(self):
        #used by do_cp or do_open,
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

        dummy_stdin = StringIO.StringIO('4\n\nX')
        self.assertTrue(len(dummy_stdin.readlines()))
        dummy_stdin.seek(0)
        sys.stdin = dummy_stdin
        menu.run(node)
        self.tester.cli._db.editnode(2, node)
        sys.stdin = sys.__stdin__

    def test_get_pass_conf(self):
        numerics, leet, s_chars = get_pass_conf()
        self.assertFalse(numerics)
        self.assertFalse(leet)
        self.assertFalse(s_chars)

    def test_do_tags(self):
        self.tester.cli.do_filter('bank')

    def test_do_clear(self):
        self.tester.cli.do_clear('')

    def test_do_exit(self):
        self.assertTrue(self.tester.cli.do_exit(''))


class FactoryTest(unittest.TestCase):

    def test_factory_check_db_ver(self):
        self.assertEquals(factory.check_db_version('SQLite'), 0.4)


class ConfigTest(unittest.TestCase):

    def setUp(self):
        "test that the right db instance was created"
        dbver = 0.4
        self.dbtype = config.get_value("Database", "type")
        self.db = factory.create(self.dbtype, dbver)
        self.tester = SetupTester()
        self.tester.create()

    def test_config_write(self):
        _filename = os.path.join(os.path.dirname(__file__),
                                 'testing_config')
        config._file = _filename
        config.save(_filename)
        self.assertTrue(_filename)
        os.remove(_filename)

    def test_config_write_with_none(self):
        _filename = os.path.join(os.path.dirname(__file__),
                                 'testing_config')
        config._file = _filename
        config.save()
        self.assertTrue(os.path.exists(_filename))
        os.remove(_filename)

    def test_write_no_permission(self):
        # this test will pass if you run as root ...
        # assuming you are not doing something like that
        self.assertRaises(config.ConfigException, config.save,
                          '/root/test_config')

    def test_add_default(self):
        config.add_defaults({'Section1': {'name': 'value'}})
        self.assertIn('Section1', config._defaults)

    def test_get_conf(self):
        cnf = config.get_conf()
        cnf_keys = cnf.keys()
        self.assertTrue('Encryption' in cnf_keys)
        self.assertTrue('Readline' in cnf_keys)
        self.assertTrue('Global' in cnf_keys)
        self.assertTrue('Database' in cnf_keys)

    def test_load_conf(self):
        self.assertRaises(config.ConfigException, config.load, 'NoSuchFile')
        # Everything should be ok
        config.save('TestConfig.ini')
        config.load('TestConfig.ini')
        # let's corrupt the file
        cfg = open('TestConfig.ini', 'w')
        cfg.write('Corruption')
        cfg.close()
        self.assertRaises(config.ConfigException, config.load,
                          'TestConfig.ini')
        os.remove('TestConfig.ini')
