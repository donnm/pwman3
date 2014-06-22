import pwman.util.config as config
import os
from pwman.util.crypto import (CryptoEngine, CryptoException,
                               CryptoNoCallbackException, CryptoEngineOld)
# set cls_timout to negative number (e.g. -1) to disable
default_config = {'Global': {'umask': '0100', 'colors': 'yes',
                             'cls_timeout': '5'
                             },
                  'Database': {'type': 'SQLite',
                               'filename': os.path.join("tests", "pwman.db")},
                  'Encryption': {'algorithm': 'AES'},
                  'Readline': {'history': os.path.join("tests",
                                                       "history")}
                  }

config.set_defaults(default_config)
import unittest


class CryptoTest(unittest.TestCase):

    def test_no_algorithm(self):
        config.set_value('Encryption', 'algorithm', '')
        self.assertRaises((CryptoException,), CryptoEngine)

    def test_getcipher(self):
        crypto = CryptoEngine()
        self.assertRaises((CryptoNoCallbackException,), crypto._getcipher)

    def test_prepare_data(self):
        obj = 'dummy_data'
        self.assertTrue(True)

    def test_get(self):
        old_engine = CryptoEngine.get()
        self.assertIsInstance(old_engine, CryptoEngineOld)
        CryptoEngine._instance = None
        new_engine = CryptoEngine.get(dbver=0.5)
        self.assertIsInstance(new_engine, CryptoEngine)
        self.assertFalse(isinstance(new_engine, CryptoEngineOld))
        CryptoEngine._instance = None
        old_engine = CryptoEngine.get()
