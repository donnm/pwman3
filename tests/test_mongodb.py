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
# Copyright (C) 2015 Oz Nahum Tiram <nahumoz@gmail.com>
# ============================================================================

import unittest
from .test_crypto_engine import give_key, DummyCallback
import pymongo
from pwman.data.drivers.mongodb import MongoDB
# use pwmantest

# db.createUser(
#    {
#      user: "tester",
#      pwd: "12345678",
#       roles: [{ role: "dbAdmin", db: "pwmantest" },
#               { role: "readWrite", db: "pwmantest" },]
#    })
from pwman.util.crypto_engine import CryptoEngine


class TestMongoDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        u = u"mongodb://tester:12345678@localhost:27017/pwmantest"
        cls.db = MongoDB(u)
        cls.db._open()

    @classmethod
    def tearDownClass(cls):
        coll = cls.db._db['crypto']
        coll.drop()
        cls.db._db['counters'].drop()
        cls.db._db['nodes'].drop()
        cls.db.close()

    def test_1_con(self):
        self.assertIsInstance(self.db._con, pymongo.Connection)

    @unittest.skip("MongoDB creates collections on the fly")
    def test_2_create_collections(self):
        pass

    def test_3_load_key(self):
        self.db.savekey('SECRET$6$KEY')
        secretkey = self.db.loadkey()
        self.assertEqual(secretkey, u'SECRET$6$KEY')

    @unittest.skip("")
    def test_4_save_crypto(self):
        self.db.save_crypto_info("TOP", "SECRET")
        secretkey = self.db.loadkey()
        self.assertEqual(secretkey, 'TOP$6$SECRET')
        row = self.db.fetch_crypto_info()
        self.assertEqual(row, ('TOP', 'SECRET'))

    def test_5_add_node(self):
        innode = [u"TBONE", u"S3K43T", u"example.org", u"some note",
                  [u"bartag", u"footag"]]
        self.db.add_node(innode)
        outnode = self.db.getnodes([1])[0]
        self.assertEqual(innode[:-1] + [t for t in innode[-1]], outnode[1:])

    def test_6_list_nodes(self):
        ret = self.db.listnodes()
        self.assertEqual(ret, [1])
        ret = self.db.listnodes("footag")
        self.assertEqual(ret, [1])

    def test_6a_list_tags(self):
        ret = self.db.listtags()
        self.assertListEqual(ret, ['bartag', 'footag'])

    def test_6b_get_nodes(self):
        ret = self.db.getnodes([1])
        retb = self.db.getnodes([])
        self.assertListEqual(ret, retb)

    @unittest.skip("tags are created in situ in mongodb")
    def test_7_get_or_create_tag(self):
        pass

    @unittest.skip("tags are removed with their node")
    def test_7a_clean_orphans(self):
        pass

    def test_8_remove_node(self):
        self.db.removenodes([1])
        n = self.db.listnodes()
        self.assertEqual(len(n), 0)

    @unittest.skip("No schema migration with mongodb")
    def test_9_check_db_version(self):
        pass


if __name__ == '__main__':

    ce = CryptoEngine.get()
    ce.callback = DummyCallback()
    ce.changepassword(reader=give_key)
    unittest.main(verbosity=2, failfast=True)
