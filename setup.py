import sys

# dirty hack, always use wheel
sys.argv.append('bdist_wheel')

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='imagestoragesimplified',
    version='0.1',
    description='Extension to simplify uploading images to s3 and decrease network usage',
    long_description=readme(),
    classifiers=[
        'Development Status :: 0.1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Topic :: Amazon :: S3',
    ],
    url='https://github.com/sergeyglazyrindev/s3images',
    author='Sergey Glazyrin',
    author_email='sergey.glazyrin.dev@gmail.com',
    license='MIT',
    package_dir={'': 'src'},
    packages=['imagestorage', ],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': ['nose', 'mock'],
    },
    test_suite='tests',
    install_requires=['boto==2.38.0', 'Pillow==2.9.0', 'celery==3.1.18', 'requests==2.7.0',
                      'python3-memcached==1.51']
)
