Simplified image storage
=============

Sometimes, we need to download images from url in our applications. But each project has own crop sizes for images.
But the problem with adding new crop size for images. Often we need to regenerate all images.
The idea of this project is a lazy crop sizes for images

Example of the code worth million words:

.. code-block:: python

    from imagestorage import storage
    from celery import app

    # storage.s3_store_image should be celery task, so let's patch it
    # in production environments you may decide to use CELERY_ROUTES
    # see this documentation: http://celery.readthedocs.org/en/latest/userguide/routing.html#automatic-routing
    storage.s3_store_image = app.task(storage.s3_store_image)

    # please pass image_id you stored image in your database. and image extension you are going to manipulate
    # unfortunately, for now package doesn't support storing image info to database.
    # later, we will use this image_id to build proper links to images
    storage = storage.S3ImageStorage(image_id, 'jpg')

    # please pass s3 tokens to storage
    # testimagestorageforpippackage - bucket_name
    # s3 base path - https://s3.eu-central-1.amazonaws.com/testimagestorageforpippackage/
    # '/' - base path upload image to
    # uploaded url would be: s3_base_path + base_path + image_id + '/' + (size_tuple or 'origin') + image_ext
    storage.configure(
        {'access_key': 'access_key', 'secret_key': 'secret_key'},
        'testimagestorageforpippackage',
        'https://s3.eu-central-1.amazonaws.com/testimagestorageforpippackage/',
        '/'
    )
    # pass webengine you would like to use to get image responses, permanent redirects, etc
    storage.configure_webengine('wheezy')

    # configure memcache by passing hosts for memcache
    storage.configure_memcache(['127.0.0.1:11211'])

    # when you call this method, we download image from specified url
    # make a thumbnail with specific dimensions (using Pillow thumbnail method)
    # return url to uploaded origin image
    storage.store_origin(
        'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQUIfplgoueTfSX1A3UnJtMEy0xMqJJ5ECirkASkw3xT7R81WrJ',
        '4000x4000'
    )

    # please pass here url actually requested, there's should be a param in query string "size" which should contain
    # size tuple joined with x. Or you can pass there tuple with parameters (200, 100)
    # this method could return two types of results:
    #     1. webengine permanent_redirect
    #     2. webengine image response
    # you can use result of this method in your webengine ( I hope :) )
    # to prevent race conditions, we lock celery task execution for 1 minute
    # that's why we need memcache
    storage.get_requested_image(
        'https://microsoft.com/?size=200x100',
    )
