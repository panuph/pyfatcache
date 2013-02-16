from distutils.core import setup

setup(
    name="pyfatcache",
    version="1.0.0",
    author="Panu P",
    author_email="panuph@gmail.com",
    maintainer="Panu P",
    maintainer_email="panuph@gmail.com",
    url="https://github.com/panuph/pyfatcache",
    description="a simple python client for twitter's fatcache",
    long_description="""Example usage::

        import pyfatcache

        conn = pyfatcache.get_conn()
        conn.delete("a")
        print "expect (None, None) / get %s" % (str(conn.get("a")),)
        conn.set("a", "a", flags=1)
        print "expect ('a', 1) / get %s" % (str(conn.get("a")),)
        conn.set("a", dict(name="pyfatcache"))
        print "expect ({'name': 'pyfatcache'}, 0) / get %s" % (str(conn.get("a")),)
        conn.set("a", None)
        print "expect (None, 0) / get %s" % (str(conn.get("a")),)
        conn.close()
    """,
    download_url="https://github.com/panuph/pyfatcache",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    platforms=["python"],
    license="Freeware",
    py_modules=["pyfatcache"]
)
