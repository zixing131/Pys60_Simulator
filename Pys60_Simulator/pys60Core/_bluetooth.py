"""In-process virtual Bluetooth services carried over loopback TCP.

This does not advertise to physical Bluetooth devices. OBEX transfers only to
an explicitly waiting simulator receiver, using its chosen destination path.
"""

import os
import weakref
import select
import socket as _socket
import e32

AF_BT, BTPROTO_RFCOMM = 0x101, 3
RFCOMM, OBEX, AUTH, ENCRYPT, AUTHOR = 101, 102, 1, 2, 4
_address = "02:00:00:00:00:01"
_native = _socket.socket
_channels = weakref.WeakValueDictionary()
_services = weakref.WeakKeyDictionary()
_receivers = {}


class Socket(_native):
    def __init__(
        self, family=_socket.AF_INET, type=_socket.SOCK_STREAM, proto=0, fileno=None
    ):
        self._bluetooth = family == AF_BT
        self._channel = None
        self._operations = []
        if self._bluetooth:
            if type != _socket.SOCK_STREAM or proto not in (0, BTPROTO_RFCOMM):
                raise _socket.error("unsupported Bluetooth socket type")
            family, proto = _socket.AF_INET, 0
        super().__init__(family, type, proto, fileno=fileno)

    def bind(self, address):
        if not self._bluetooth:
            return super().bind(address)
        host, channel = address
        if not isinstance(channel, int) or not 1 <= channel <= 30:
            raise _socket.error("invalid channel")
        if channel in _channels:
            raise _socket.error("channel already bound")
        super().bind(("127.0.0.1", 0))
        self._channel = channel
        _channels[channel] = self

    def connect(self, address, callback=None):
        if not self._bluetooth:
            return super().connect(address)
        if callback is not None and not callable(callback):
            raise TypeError("callback must be callable")
        host, channel = address
        if host.lower() != _address or channel not in _channels:
            raise _socket.error("virtual Bluetooth service not found")
        super().connect(_native.getsockname(_channels[channel]))
        if callback is not None:
            e32._schedule(0, lambda: callback(None))

    def _wait_read(self, operation, callback):
        if callback is not None and not callable(callback):
            raise TypeError("callback must be callable")
        if callback is None:
            timeout = self.gettimeout()
            deadline = None if timeout is None else e32._clock() + timeout
            while not select.select([self], [], [], 0)[0]:
                if deadline is not None and e32._clock() >= deadline:
                    raise _socket.timeout("timed out")
                e32.ao_sleep(0.001)
            return operation()

        def poll():
            if self.fileno() < 0:
                return
            if select.select([self], [], [], 0)[0]:
                callback(operation())
            else:
                self._operations.append(e32._schedule(0.001, poll))

        self._operations.append(e32._schedule(0, poll))

    def accept(self, callback=None):
        if not self._bluetooth:
            return super().accept()

        def accept():
            fd, address = self._accept()
            child = Socket(fileno=fd)
            child._bluetooth = True
            return child, _address

        return self._wait_read(accept, callback)

    def recv(self, bufsize, flags=0, callback=None):
        if not self._bluetooth:
            return super().recv(bufsize, flags)
        return self._wait_read(lambda: _native.recv(self, bufsize, flags), callback)

    def close(self):
        for operation in self._operations:
            e32._cancel(operation)
        self._operations[:] = []
        _services.pop(self, None)
        if self._channel is not None and _channels.get(self._channel) is self:
            _channels.pop(self._channel, None)
        super().close()


def _check(sock, bound=False):
    if not isinstance(sock, Socket) or not sock._bluetooth:
        raise _socket.error("Given Socket is not of AF_BT family")
    if sock.fileno() < 0:
        raise _socket.error("socket closed")
    if bound and sock._channel is None:
        raise _socket.error("Socket has not a valid port. Bind it first")


def bt_rfcomm_get_available_server_channel(sock):
    _check(sock)
    for channel in range(1, 31):
        if channel not in _channels:
            return channel
    raise _socket.error("no available channels")


def bt_advertise_service(name, sock, flag, service_type=RFCOMM):
    _check(sock, True)
    if not isinstance(name, str):
        raise TypeError("Unicode service name expected")
    if not name or flag not in (0, 1) or service_type not in (RFCOMM, OBEX):
        raise _socket.error("invalid service name, flag or type")
    if flag:
        _services[sock] = (name, service_type)
    else:
        _services.pop(sock, None)


def _discover(address, service_type):
    if address is not None and address.lower() != _address:
        raise _socket.error("virtual Bluetooth device not found")
    return _address, {
        name: sock._channel
        for sock, (name, kind) in list(_services.items())
        if kind == service_type
    }


def bt_discover(address=None):
    return _discover(address, RFCOMM)


def bt_obex_discover(address=None):
    return _discover(address, OBEX)


def set_security(sock, mode):
    _check(sock, True)
    if not isinstance(mode, int):
        raise TypeError("integer security mode expected")
    # Flags are retained for inspection; physical pairing/encryption is not emulated.
    sock._security = mode


def bt_obex_receive(sock, filename):
    _check(sock, True)
    if sock._channel in _receivers:
        raise _socket.error("receiver already active")
    transfer = {"path": os.fspath(filename), "done": False, "error": None}
    _receivers[sock._channel] = transfer
    try:
        e32._wait_until(lambda: transfer["done"] or sock.fileno() < 0)
        if transfer["error"]:
            raise transfer["error"]
        if not transfer["done"]:
            raise _socket.error("socket closed")
    finally:
        _receivers.pop(sock._channel, None)


def bt_obex_send_file(address, channel, filename):
    if address.lower() != _address or channel not in _receivers:
        raise _socket.error("no waiting virtual OBEX receiver")
    transfer = _receivers[channel]
    try:
        import shutil

        shutil.copyfile(filename, transfer["path"])
    except OSError as exc:
        transfer["error"] = exc
        raise
    finally:
        transfer["done"] = True


def install():
    _socket.socket = Socket
    for name in (
        "AF_BT",
        "BTPROTO_RFCOMM",
        "RFCOMM",
        "OBEX",
        "AUTH",
        "ENCRYPT",
        "AUTHOR",
        "bt_rfcomm_get_available_server_channel",
        "bt_advertise_service",
        "bt_discover",
        "bt_obex_discover",
        "set_security",
        "bt_obex_receive",
        "bt_obex_send_file",
    ):
        setattr(_socket, name, globals()[name])
