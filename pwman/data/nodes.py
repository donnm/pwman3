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
# Copyright (C) 2012 Oz Nahum <nahumoz@gmail.com>
#============================================================================
#============================================================================
# Copyright (C) 2006 Ivan Kelly <ivan@ivankelly.net>
#============================================================================

from pwman.util.crypto import CryptoEngine


class NewNode(object):

    def __init__(self, username="", password="", url="", notes="", tags=""):
        """Initialise everything to null."""

        self._id = 0
        self._username = username
        self._password = password
        self._url = url
        self._notes = notes
        self._tags = tags

    def __setattribute__(self, name, value):

        if name in ['username']:
            enc = CryptoEngine.get()
            object.__setattr__(self, name, value)
            name = '_'+name
            object.__setattr__(self, name, enc.encrypt(value).strip())

    def __getattribute__(self, name):

        if name in ['username']:
            enc = CryptoEngine.get()
            return enc.decrypt(eval('self._'+name).strip())
        else:
            return object.__getattribute__(self, name)

    def dump_edit_to_db(self):
        dump = ""
        dump += "username:"+self._username+"##"
        dump += "password:"+self._password+"##"
        dump += "url:"+self._url+"##"
        dump += "notes:"+self._notes+"##"
        dump += "tags:"
        tagsloc = ""
        for tag in self._tags:
            if isinstance(tag, str):
                tagsloc += "tag:"+tag.strip()+"**endtag**"
            else:
                tagsloc += "tag:"+tag.get_name()+"**endtag**"
        dump += tagsloc
        dump = [dump]
        return dump

    def dump_to_db(self):
        enc = CryptoEngine.get()
        dump = ""
        dump += "username:"+enc.encrypt(self._username)+"##"
        dump += "password:"+enc.encrypt(self._password)+"##"
        dump += "url:"+enc.encrypt(self._url)+"##"
        dump += "notes:"+enc.encrypt(self._notes)+"##"
        dump += "tags:"
        tagsloc = ""
        for tag in self._tags:
            if isinstance(tag, str):
                tagsloc += "tag:"+tag.strip()+"**endtag**"
            else:
                tagsloc += "tag:"+tag.get_name()+"**endtag**"
        dump += tagsloc
        dump = [dump]
        return dump

    def set_tags(self, tags):
        """
        TODO: remove all references
        this method expects a list of tag instances.
        hence feed it with them.

        fixed! the method parse_node_string in
        SQLiteDatabase returns a dictionary,
        but a also, Tags instances..."""
        self._tags = []
        if tags:
            self._tags = [t for t in tags]

    def set_id(self, id):

        self._id = id

    #@property
    #def username(self):
    #    """Get the current username."""
    #    enc = CryptoEngine.get()
    #    return enc.decrypt(self._username).strip()

    @property
    def password(self):
        """Get the current password."""
        enc = CryptoEngine.get()
        return enc.decrypt(self._password).strip()

    #@username.setter
    #def username(self, value):
    #    """Set the Notes."""
    #    enc = CryptoEngine.get()
    #    self._username = enc.encrypt(value).strip()

    @password.setter
    def password(self, value):
        """Set the Notes."""
        enc = CryptoEngine.get()
        self._password = enc.encrypt(value).strip()

    @property
    def tags(self):
        return [tag for tag in self._tags]

    @tags.setter
    def tags(self, value):
        self._tags = [tag for tag in value]

    @property
    def url(self):
        """Get the current url."""
        enc = CryptoEngine.get()
        return enc.decrypt(self._url).strip()

    @url.setter
    def url(self, value):
        """Set the Notes."""
        enc = CryptoEngine.get()
        self._url = enc.encrypt(value).strip()

    @property
    def notes(self):
        """Get the current notes."""
        enc = CryptoEngine.get()
        return enc.decrypt(self._notes).strip()

    @notes.setter
    def notes(self, value):
        """Set the Notes."""
        enc = CryptoEngine.get()
        self._notes = enc.encrypt(value).strip()


class Node(object):
    def __init__(self, username="", password="", url="",
                 notes="", tags=[]):
        """Initialise everything to null."""
        self._id = 0

        enc = CryptoEngine.get()
        self._username = enc.encrypt(username)
        self._password = enc.encrypt(password)
        self._url = enc.encrypt(url)
        self._notes = enc.encrypt(notes)
        self._tags = []
        self.set_tags(tags)

    def get_tags(self):
        tags = []
        enc = CryptoEngine.get()
        for i in self._tags:
            tags.append(enc.decrypt(i))
        return tags

    def set_tags(self, tags):
        self._tags = []
        enc = CryptoEngine.get()
        for i in tags:
            self._tags.append(enc.encrypt(i))

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_username(self):
        """Return the username."""
        enc = CryptoEngine.get()
        return enc.decrypt(self._username)

    def set_username(self, username):
        """Set the username."""
        enc = CryptoEngine.get()
        self._username = enc.encrypt(username)

    def get_password(self):
        """Return the password."""
        enc = CryptoEngine.get()
        return enc.decrypt(self._password)

    def set_password(self, password):
        """Set the password."""
        enc = CryptoEngine.get()
        self._password = enc.encrypt(password)

    def get_url(self):
        """Return the URL."""
        enc = CryptoEngine.get()
        return enc.decrypt(self._url)

    def set_url(self, url):
        """Set the URL."""
        enc = CryptoEngine.get()
        self._url = enc.encrypt(url)

    def get_notes(self):
        """Return the Notes."""
        enc = CryptoEngine.get()
        return enc.decrypt(self._notes)

    def set_notes(self, notes):
        """Set the Notes."""
        enc = CryptoEngine.get()
        self._notes = enc.encrypt(notes)
