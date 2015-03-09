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

from artnet import ArtnetController
from select import select
from optparse import OptionParser
from time import time

parser = OptionParser(usage="%prog [options]")
parser.add_option("-t", dest="timeout", default=3,
                  help="Discovery timeout")
(opts, args) = parser.parse_args()

ac = ArtnetController("pyartnet-discover")
ac.discover()

start = time()
while (time() - start) < int(opts.timeout):
	readable, writeable, exception = select([ac], [], [], 1)
	if len(readable) > 0:
		ac.run()

for node in ac.nodes():
	print "IP: " + node.ip + " (" + node.mac + ")"
	print "Name: " + node.name,
	print ", version: " + str(node.version)
	print "Subnet: " + str(node.subnet)
	print "Ports: " + str(node.ports)
