# This file is part of eventmq.
#
# eventmq is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# eventmq is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with eventmq.  If not, see <http://www.gnu.org/licenses/>.
"""
:mod:`messages` -- Client Messaging
===================================
"""
from json import dumps as serialize

from .. import conf
from ..utils.messages import send_emqp_message


def send_request(socket, message, reply_requested=False, guarantee=False,
                 retry_count=0, queue=None):
    """
    Send a REQUEST command.

    Default headers are always all disabled by default. If they are included in
    the headers then they have been enabled.
    """
    headers = []

    if reply_requested:
        headers.append('reply-requested')

    if guarantee:
        headers.append('guarantee')

    if retry_count > 0:
        headers.append('retry-count:%d' % retry_count)

    send_emqp_message(socket, 'REQUEST',
                      (queue or conf.DEFAULT_QUEUE_NAME,
                       ",".join(headers),
                       serialize(message))
                      )


def job(block=False):  # Move to decorators.py
    """
    run the decorated function on a worker

    Args:
        block (bool): Set to True if you wish to block and wait for the
            response. This may be useful for running quick but cpu intesive
            that would otherwise overwhelm a box that has to do it all alone.
            (decryption?)
    """
    pass
