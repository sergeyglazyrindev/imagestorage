Simplified redis usage in complex applications
=============

This package aimed to organize redis structures into something similar to *models*.
It doesn't make sense to use redis to store *real models*. It should be used as a key-value storage
But mostly we still need to organize code into anything similar to *models*.

Installation
-----------

Simply run in your bash:

.. code-block:: bash
                
    python setup.py install

Usage
-----------

.. code-block:: python

    from redisext import (
        ConnectionHandler,
        List,
    )

    class TestConnectionHandler(ConnectionHandler):
        connection = {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        }


    class TestList(List, ConnectionHandler):
        KEY = 'testlist'

    # call specific redis list methods
    TestList.llen()
    # package provides access to most useful redis commands
    # in data types: Hash, Key, List, Set, SortedSet
