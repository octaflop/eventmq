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
:mod:`messages` -- Message Utilities
==========================================
"""
import logging

from .. import constants, exceptions
from . import random_characters

logger = logging.getLogger(__name__)


def parse_router_message(message):
    """
    Parses the generic format of an eMQP/1.0 message and returns the
    parts.

    Args:
        message: the message you wish to have parsed

    Returns (tuple) (sender_id, command, message_id, (message_body, and_data))
    """
    try:
        sender = message[0]
        # noop = message[1]
        # protocol_version = message[2]
        command = message[3]
        msgid = message[4]
    except IndexError:
        raise exceptions.InvalidMessageError('Invalid Message Encountered: %s'
                                             % str(message))
    if len(message) > 5:
        msg = message[5:]
    else:
        msg = ()
    return (sender, command, msgid, msg)


def parse_message(message):
    """
    Parses the generic format of an eMQP/1.0 message and returns the
    parts.

    Args:
        message: the message you wish to have parsed

    Returns (tuple) (command, message_id, (message_body, and_data))
    """
    try:
        # noop = message[0]
        # protocol_version = message[1]
        command = message[2]
        msgid = message[3]
    except IndexError:
        raise exceptions.InvalidMessageError('Invalid Message Encountered: %s'
                                             % str(message))

    if len(message) > 4:
        msg = message[4:]
    else:
        msg = ()
    return (command, msgid, msg)


def generate_msgid(prefix=None):
    """
    Returns a random string to be used for message ids. Optionally the ID can
    be prefixed with `prefix`.

    Args:
        prefix (str): Value to prefix on to the random part of the id. Useful
            for prefixing some meta data to use for things
    """
    id = random_characters()
    return id if not prefix else str(prefix) + id


def send_emqp_message(socket, command, message=None):
    """
    Formats and sends an eMQP message

    Args:
        socket
        command
        message
    Raises:
    """
    msg = (str(command).upper(), generate_msgid())
    if message and isinstance(message, (tuple, list)):
        msg += tuple(message)
    elif message:
        msg += (message,)

    socket.send_multipart(msg, constants.PROTOCOL_VERSION)


def send_emqp_router_message(socket, recipient_id, command, message=None):
    """
    Formats and sends an eMQP message taking into account the recipient frame
    used by a :attr:`zmq.ROUTER` device.

    Args:
        socket: socket to send the message with
        recipient_id (str): the id of the connected device to reply to
        command (str): the eMQP command to send
        message: a msg tuple to send

    Raises:

    Returns
    """
    msg = (str(command).upper(), generate_msgid())
    if message and isinstance(message, (tuple, list)):
        msg += message
    elif message:
        msg += (message,)

    socket.send_multipart(msg, constants.PROTOCOL_VERSION,
                          _recipient_id=recipient_id)


def fwd_emqp_router_message(socket, recipient_id, payload):
    """
    Forwards `payload` to socket untouched.

    .. note:
       Because it's untouched, and because this function targets
       :prop:`zmq.ROUTER`, it may be a good idea to first strip off the
       leading sender id before forwarding it. If you dont you will need to
       account for that on the recipient side.
    """
    socket.zsocket.send_multipart([recipient_id, ] + payload)
