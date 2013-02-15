pyfatcache: a simple python client for twitter's fatcache
========================================================= 

See an example usage below.

```python
import pyfatcache

conn = get_conn()   # for a specific host use get_conn(host=XXXX, port=YYYY)
conn.delete("a")
print "expect (None, None) / get %s" % (str(conn.get("a")),)
conn.set("a", "a", flags=1)
print "expect ('a', 1) / get %s" % (str(conn.get("a")),)
conn.set("a", dict(name="pyfatcache"))
print "expect ({'name': 'pyfatcache'}, 0) / get %s" % (str(conn.get("a")),)
conn.set("a", None)
print "expect (None, 0) / get %s" % (str(conn.get("a")),)
conn.close()
```

In fact, you can run the example above via command line:

<pre>
python -m pyfatcache
</pre>

For detailed information, see pyfatcache.py directly.

All information about twitter's fatcache is available [here](https://github.com/twitter/fatcache)

The library does not do much, as this is all that I need currently. If you need
other features, please feel free to raise issues or, even better, implement
them yourselves and submit pull requests, which are always welcome :-)
