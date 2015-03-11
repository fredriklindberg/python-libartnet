# This file is a part of python-libartnet
#
# Copyright (C) 2013 Fredrik Lindberg <fli@shapeshifter.se>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from ctypes import *
from socket import inet_ntoa
import struct
from . import _an

class Node(object):
    def __init__(self, ne):
        self.raw = ne

    @property
    def ip(self):
        return inet_ntoa(self.raw.ip)

    @property
    def mac(self):
        return "%02x:%02x:%02x:%02x:%02x:%02x" % \
            struct.unpack("BBBBBB", self.raw.mac)

    @property
    def version(self):
        return self.raw.version

    @property
    def name(self):
        return self.raw.shortname

    @property
    def long_name(self):
        return self.raw.longname

    @property
    def report(self):
        return self.raw.nodereport

    @property
    def subnet(self):
        return self.raw.subnet

    @property
    def ports(self):
        return self.raw.numbports


class NodeEntry(Structure):
    _fields_ = [
        ("ip", c_ubyte * 4),
        ("version", c_short),
        ("subnet", c_short),
        ("oem", c_short),
        ("ebea", c_ubyte),
        ("status", c_ubyte),
        ("etsaman", c_ubyte * 2),
        ("shortname", c_char * 18),
        ("longname", c_char * 64),
        ("nodereport", c_char * 64),
        ("numbports", c_short),
        ("porttypes", c_ubyte * 4),
        ("goodinput", c_ubyte * 4),
        ("goodoutput", c_ubyte * 4),
        ("swin", c_ubyte * 4),
        ("swout", c_ubyte * 4),
        ("swvideo", c_ubyte),
        ("swmacro", c_ubyte),
        ("swstyle", c_ubyte),
        ("mac", c_ubyte * 6),
    ]

class Nodes(object):
    def __init__(self, artnet):
        self._artnet = artnet
        self._nl = _an.artnet_get_nl(artnet)

    def __len__(self):
        return _an.artnet_nl_get_length(self._nl)

    def __iter__(self):
        self._entry = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self._entry == 0:
            self._entry = _an.artnet_nl_first(self._nl)
        else:
            self._entry = _an.artnet_nl_next(self._nl)

        if self._entry != 0:
            c_ne_p = POINTER(NodeEntry)
            nodeentry = cast(self._entry, c_ne_p).contents
            return Node(nodeentry)
        else:
            raise StopIteration
