#!/usr/bin/env python
# Copyright (C) 2013 Fredrik Lindberg <fli@shapeshifter.se>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

from __future__ import print_function

from artnet import ArtnetController, DmxPort
from select import select
from optparse import OptionParser

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

parser = OptionParser(usage="%prog [options] channel value [channel value [...]]")
parser.add_option("-p", "--port", dest="port", default=0,
                  help="Set port address")
(opts, args) = parser.parse_args()

if len(args) % 2:
    parser.error("Channel and values should be specified in pairs")

ac = ArtnetController("pyartnet-setdmx")
dp = DmxPort(opts.port, DmxPort.INPUT)
ac.add_port(dp)

print("Using port {}".format(dp))

for channel, value in pairwise(args):
    dp.set(int(channel), int(value))
    print("Channel " + channel + ", set to " + value)
dp.send()
