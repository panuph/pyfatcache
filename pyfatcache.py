import re
import socket
try:
    import simplejson as json
except:
    import json


class Client(object):
    """A client for fatcache server. This client covers only simple usage
    scenarios."""

    SET_RES_1 = re.compile(r"^(STORED)\r\n$")
    SET_RES_2 = re.compile(r"^(NOT_STORED)\r\n$")

    GET_RES_1 = re.compile(r"^(END)\r\n$")
    GET_RES_2 = re.compile(r"^(VALUE)\s(.+)\s(\d+)\s\d+\r\n(.*)\r\nEND\r\n$")
    GET_RES_3 = re.compile(r"^(NOT_FOUND)\r\n$")

    DELETE_RES_1 = re.compile(r"^NOT_FOUND\r\n$")
    DELETE_RES_2 = re.compile(r"^DELETED\r\n$")

    def __init__(self, host, port):
        """Constructor
        host: str
            fatcache host
        port: int
            fatcache port
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def _recv_until_match(self, *patterns):
        """Keeps receiving the data from the server until they match one of the
        patterns (defined as class variables); returns the response from the
        server and the corresponding match object, i.e. re.MatchObject. Raises
        an exception if an error occurs."""
        so_far = ""
        while True:
            data = self.socket.recv(512)
            if data:
                so_far += data
                for pattern in patterns:
                    m = pattern.match(so_far)
                    if m:
                        return (so_far, m)
            else:
                self.socket.close()
                raise Exception

    def set(self, key, value, flags=0, expiry=0, timeout=None):
        """Sets the key and value on the server. The value must be str. Raises
        an exception if the value cannot be set.
        key: str
            the key of the value to set
        value: str
            the value to be set
        flags: int (unsigned)
            data specific client flags
        expiry: int (unsigned)
            expiration time (in seconds)
        timeout: int
            the socket timeout in seconds (None = no timeout)
        """
        self.socket.settimeout(timeout)
        packet = "set %s %d %d %d\r\n%s\r\n" % (key, flags, expiry,
            len(value), value)
        self.socket.sendall(packet)
        res, m = self._recv_until_match(Client.SET_RES_1, Client.SET_RES_2)
        if m.group(1) == "NOT_STORED":
            raise Exception("set", key, value, flags, expiry, res)

    def get(self, key, timeout=None):
        """Returns a tuple of value and data specific client flags, i.e.
        (str, int) of the key or (None, None) if not found.
        key: str
            the key of the value to get
        timeout: int
            the socket timeout in seconds (None = no timeout)
        """
        self.socket.settimeout(timeout)
        packet = "get %s\r\n" % (key,)
        self.socket.sendall(packet)
        res, m = self._recv_until_match(Client.GET_RES_1, Client.GET_RES_2, Client.GET_RES_3)
        if m.group(1) == "END" or m.group(1) == "NOT_FOUND":
            return (None, None)
        else:
            if m.group(2) == key:   # double check the key again
                return (m.group(4), int(m.group(3)))
            else:
                raise Exception("get", key, res)

    def delete(self, key, timeout=None):
        """Deletes the value associated with the key. Calling get() after this
        delete on the key will return (None, None).
        key: str
            the key of the value to delete
        timeout: int
            the socket timeout in seconds (None = no timeout)
        """
        self.socket.settimeout(timeout)
        packet = "delete %s\r\n" % (key,)
        self.socket.sendall(packet)
        self._recv_until_match(Client.DELETE_RES_1, Client.DELETE_RES_2)

    def close(self):
        """Closes the client socket."""
        self.socket.close()


class JsonClient(Client):
    """Similar to Client, but treating the value in JSON format."""

    def set(self, key, value, flags=0, expiry=0, timeout=None):
        """See method set() in class Client."""
        return super(JsonClient, self).set(key, json.dumps(value),
            flags=flags, expiry=expiry, timeout=timeout)

    def get(self, key, timeout=None):
        """See method get() in class Client."""
        value, flags = super(JsonClient, self).get(key, timeout=timeout)
        return (None if value is None else json.loads(value), flags)


def get_conn(host="localhost", port=11211, json=True):
    """Factory method (function) returning a new connection to fatcache server.
    host: str
        the fatcache host
    port: int
        the faatcache port
    json: boolean
        whether to use JsonClient (True by default and recommended)
    """
    return JsonClient(host, port) if json else Client(host, port)


if __name__ == "__main__":
    """Example usage -- python -m pyfatcache"""
    conn = get_conn()
    conn.delete("a")
    print "expect (None, None) / get %s" % (str(conn.get("a")),)
    conn.set("a", "a", flags=1)
    print "expect ('a', 1) / get %s" % (str(conn.get("a")),)
    conn.set("a", dict(name="pyfatcache"))
    print "expect ({'name': 'pyfatcache'}, 0) / get %s" % (str(conn.get("a")),)
    conn.set("a", None)
    print "expect (None, 0) / get %s" % (str(conn.get("a")),)
    conn.close()
