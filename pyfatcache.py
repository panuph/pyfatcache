import re
import socket
try:
    import simplejson as json
except:
    import json

class Client(object):
    """A client for fatcache server. This client covers only simple usage
    scenarios."""

    GET_RES_1 = re.compile(r"^END\r\n$")
    GET_RES_2 = re.compile(r"^VALUE\s(.+)\s0\s\d+\r\n(.*)\r\nEND\r\n$")
    GET_RES_3 = re.compile(r"^STORED\r\nVALUE\s(.+)\s0\s\d+\r\n(.*)\r\nEND\r\n$")

    def __init__(self, host, port):
        """Constructor
        host: str
            fatcache host
        port: int
            fatcache port
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def set(self, key, value, timeout=60):
        """Sets the key and value on the server. Theh value must be str.
        key: str
            the key of the value to set
        val: str
            the value to be set
        """
        self.socket.settimeout(timeout)
        packet = "set %s 0 0 %d\r\n%s\r\n" % (key, len(value), value)
        self.socket.sendall(packet)

    def get(self, key, timeout=60):
        """Returns the value (str) of the key or None if not found.
        key: str
            the key of the value to get
        """
        self.socket.settimeout(timeout)
        packet = "get %s\r\n" % (key,)
        self.socket.sendall(packet)
        so_far = ""
        while True:
            data = self.socket.recv(512)
            if data:
                so_far += data
                length = len(so_far)
                if length >= 5:
                    if so_far[-5:] == "END\r\n":
                        m = Client.GET_RES_1.match(so_far)
                        if m:
                            return None
                        m = Client.GET_RES_2.match(so_far)
                        if m and m.group(1) == key:
                            return m.group(2)
                        m = Client.GET_RES_3.match(so_far)
                        if m and m.group(1) == key:
                            return m.group(2)
                        raise Exception("get %s => %s" % (key, repr(so_far)))
            else:
                self.socket.close()
                raise Exception("connection error")

    def close(self):
        self.socket.close()

class JsonClient(Client):
    """Similar to Client, but treating the value in JSON format."""

    def set(self, key, value, timeout=60):
        """See method set() in class Client."""
        return super(JsonClient, self).set(key, json.dumps(value), 
            timeout=timeout)

    def get(self, key, timeout=60):
        """See method get() in class Client."""
        value = super(JsonClient, self).get(key, timeout=timeout)
        return value if value is None else json.loads(value) 

def get_conn(host="localhost", port=11211, json=True):
    """Factory method."""
    return JsonClient(host, port) if json else Client(host, port)

if __name__ == "__main__":
    """Example usage -- python -m pyfatcache"""
    conn = get_conn()
    print "expect None / get %s" % (conn.get("a"),)
    conn.set("a", "a")
    print "expect a / get %s" % (conn.get("a"),)
    conn.set("a", dict(name="pyfatcache"))
    print "expect {'name': 'pyfatcache'} / get %s" % (conn.get("a"),)
    conn.set("a", None)
    print "expect None / get %s" % (conn.get("a"),)
    conn.close()
