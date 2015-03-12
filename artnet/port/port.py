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

class Port(object):

    INPUT   = "input"
    OUTPUT  = "output"
    DMX     = "DMX"
    MIDI    = "MIDI"
    AVAB    = "AVAB"
    CMX     = "CMX"
    ADB     = "ADB"
    ARTNET  = "ARTNET"

    _port_types = {
        INPUT   : 0x40,
        OUTPUT  : 0x80,
        DMX     : 0x00,
        MIDI    : 0x01,
        AVAB    : 0x02,
        CMX     : 0x03,
        ADB     : 0x04,
        ARTNET  : 0x05
    }

    _id = None
    _data_type = None
    _artnet = None

    def __init__(self, address = 0, direction = INPUT):
        if address < 0 or address >= 16:
            raise IndexError("Invalid port address")
        self._address = address

        if direction != self.INPUT and direction != self.OUTPUT:
            raise IndexError("Direction should be INPUT or OUTPUT")
        self._direction = direction

    def __str__(self):
        return self._data_type + " " + self._direction + \
            " @ " + str(self._address)

    def set_context(self, artnet):
        self._artnet = artnet
        self._id = 0
        for port in artnet.ports():
            if port == self:
                break
            self._id = self._id + 1

    @property
    def address(self):
        return self._address

    @property
    def direction(self):
        return self._direction

    @property
    def artnet_direction(self):
        return self._port_types[self._direction]

    @property
    def data_type(self):
        return self._data_type

    @property
    def artnet_data_type(self):
        return self._port_types[self._data_type]

    @property
    def data(self):
        return None

    def send(self):
        return None
