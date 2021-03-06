#
#    Copyright (c) 2010 Brian E. Granger
#
#    This file is part of pyzmq.
#
#    pyzmq is free software; you can redistribute it and/or modify it under
#    the terms of the Lesser GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    pyzmq is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    Lesser GNU General Public License for more details.
#
#    You should have received a copy of the Lesser GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import sys

from unittest import TestCase

import zmq

#-----------------------------------------------------------------------------
# Utilities
#-----------------------------------------------------------------------------


class BaseZMQTestCase(TestCase):

    def setUp(self):
        self.context = zmq.Context()
        self.sockets = []
    
    def tearDown(self):
        while self.sockets:
            sock = self.sockets.pop()
            sock.close()
        del self.context
            

    def create_bound_pair(self, type1, type2, interface='tcp://127.0.0.1'):
        """Create a bound socket pair using a random port."""
        s1 = zmq.Socket(self.context, type1)
        port = s1.bind_to_random_port(interface)
        s2 = zmq.Socket(self.context, type2)
        s2.connect('%s:%s' % (interface, port))
        self.sockets.extend([s1,s2])
        return s1, s2

    def ping_pong(self, s1, s2, msg):
        s1.send(msg)
        msg2 = s2.recv()
        s2.send(msg2)
        msg3 = s1.recv()
        return msg3

    def ping_pong_json(self, s1, s2, o):
        s1.send_json(o)
        o2 = s2.recv_json()
        s2.send_json(o2)
        o3 = s1.recv_json()
        return o3

    def ping_pong_pyobj(self, s1, s2, o):
        s1.send_pyobj(o)
        o2 = s2.recv_pyobj()
        s2.send_pyobj(o2)
        o3 = s1.recv_pyobj()
        return o3

    def assertRaisesErrno(self, errno, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except zmq.ZMQError:
            e = sys.exc_info()[1]
            self.assertEqual(e.errno, errno, "wrong error raised, expected '%s' \
got '%s'" % (zmq.ZMQError(errno), zmq.ZMQError(e.errno)))
        else:
            self.fail("Function did not raise any error")
        


class PollZMQTestCase(BaseZMQTestCase):
    pass

