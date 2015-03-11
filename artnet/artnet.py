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
from .node import *
from .port import *
from .dmx import *
from . import _an

class Artnet(object):

    (SRV, NODE, MSRV, ROUTE, BACKUP, RAW) = (0, 1, 2, 3, 4, 5)

    _num_ports = 0

    def __init__(self, type=SRV, ip=None):
        self._ip = ip
        self._node = _an.artnet_new(ip, 0)
        self.type = type
        self.subnet = 0
        self._CHANDLER = \
            CFUNCTYPE(c_int, c_void_p, c_void_p, c_void_p)
        self._handlers = {}
        self._ports = []

    def __del__(self):
        if self._node != None:
            _an.artnet_destroy(self._node)

    @property
    def handle(self):
        return self._node

    def start(self):
        ret = _an.artnet_start(self._node)

    def stop(self):
        ret = _an.artnet_stop(self._node)

    def read(self, timeout=0):
        ret = _an.artnet_read(self._node, timeout)

    def fileno(self):
        return _an.artnet_get_sd(self._node)

    TTM_DEFAULT = 0xFF
    TTM_PRIVATE = 0xFE
    TTM_AUTO = 0xFD

    def send_poll(self, ip=None, ttm=TTM_DEFAULT):
        return _an.artnet_send_poll(self._node, ip, ttm)

    @property
    def ip(self):
        return self._ip

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
        _an.artnet_set_node_type(self._node, value)

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
        _an.artnet_set_short_name(self._node, value)

    @property
    def long_name(self):
        return self._name
    @long_name.setter
    def long_name(self, value):
        self._name = value
        _an.artnet_set_long_name(self._node, value)

    @property
    def broadcast_limit(self):
        return self._bcast_limit
    @broadcast_limit.setter
    def broadcast_limit(self, value):
        self._bcast_limit = value
        _an.artnet_set_bcast_limit(self._node, value)

    @property
    def subnet(self):
        return self._subnet
    @broadcast_limit.setter
    def subnet(self, value):
        self._subnet = value
        _an.artnet_set_subnet_addr(self._node, value)

    HANDLER_RECV = 0
    HANDLER_SEND = 1
    HANDLER_POLL = 2
    HANDLER_REPLY = 3
    HANDLER_DMX = 4
    HANDLER_ADDRESS = 5
    HANDLER_INPUT = 6
    HANDLER_TOD_REQUEST = 7
    HANDLER_TOD_DATA = 8
    HANDLER_TOD_CONTROL = 9
    HANDLER_RDM = 10
    HANDLER_IPPROG = 11
    HANDLER_FIRMWARE = 12
    HANDLER_FIRMWARE_REPLY = 13

    def _handler(self, node, pp, data):
        h = self._handlers[data]
        return h['cb'](self, h['data'])

    def set_handler(self, handler, cb, data=None):
        ccb = self._CHANDLER(self._handler)
        self._handlers[handler] = {
            'cb' : cb,
            'data' : data,
            'ccb' : ccb
        }
        _an.artnet_set_handler(self._node, handler, ccb, handler)

    def nodes(self):
        return Nodes(self._node)

    _port_cfg = {
        Port.INPUT   : 0x40,
        Port.OUTPUT  : 0x80,
        Port.DMX     : 0x00,
        Port.MIDI    : 0x01,
        Port.AVAB    : 0x02,
        Port.CMX     : 0x03,
        Port.ADB     : 0x04,
        Port.ARTNET  : 0x05
    }

    def add_port(self, port):
        id = self._num_ports
        self._num_ports = self._num_ports + 1

        _an.artnet_set_port_type(self._node, id, \
            self._port_cfg[port.direction], \
            self._port_cfg[port.data_type])

        dir = 1 if port.direction == Port.INPUT else 2
        _an.artnet_set_port_addr(self._node, id, dir, \
            port.address)

        self._ports.append(port)
        port.set_context(self)
        return id

    def ports(self):
        return filter(lambda x: x != None, self._ports)

class ArtnetController(Artnet):

    def __init__(self, name = 'py-artnet', long_name = ''):
        super(ArtnetController, self).__init__(Artnet.SRV)
        self.name = name
        self.long_name = long_name
        self.set_handler(self.HANDLER_POLL, self._handler_poll)
        self.set_handler(self.HANDLER_REPLY, self._handler_reply)
        self.start()

    def _handler_reply(self, artnet, data):
        return 0

    def _handler_poll(self, artnet, data):
        _an.artnet_send_poll_reply(self._node)
        return 0

    def discover(self):
        self.send_poll()

    def run(self):
        self.read()
