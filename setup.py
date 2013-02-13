from distutils.core import setup

setup(
    name="pyfatcache",
    version="1.0.0",
    author="Panu P",
    author_email="panuph@gmail.com",
    maintainer="Panu P",
    maintainer_email="panuph@gmail.com",
    url="https://github.com/panuph/pyfatcache",
    description="a simple python client for twitter fatcache",
    long_description="""Example usage::

        import pyfatcache
        conn = get_conn()
        print "expect None / get %s" % (conn.get("a"),)
        conn.set("a", "a")
        print "expect a / get %s" % (conn.get("a"),)
        conn.set("a", dict(name="pyfatcache"))
        print "expect {'name': 'pyfatcache'} / get %s" % (conn.get("a"),)
        conn.set("a", None)
        print "expect None / get %s" % (conn.get("a"),)
        conn.close()
    """,
    download_url="https://github.com/panuph/pyfatcache",
    classifiers=["Programming Language :: Python"],
    platforms=["python"],
    license="Freeware",
    py_modules=["pyfatcache"]
)
