from setuptools import setup

import firefence


DEPENDENCIES = [
    'ipcalc >= 1.99.0',
    'six >= 1.10.0',
]


setup(
    name='django-firefence',
    version=firefence.__version__,
    packages=[
        'firefence',
    ],
    author='Rehan Dalal',
    author_email='rehan@meet-rehan.com',
    license='Mozilla Public License Version 2.0',
    description='A firewall for your Django views',
    long_description='',
    url='https://github.com/rehandalal/django-firefence',
    install_requires=DEPENDENCIES,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=DEPENDENCIES,
    test_suite='tests',
    zip_safe=False
)
