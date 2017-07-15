"""
Like a firewall but smaller.

Protect your views from intruders!
"""
import os

from setuptools import find_packages, setup


DEPENDENCIES = [
    'ipcalc >= 1.99.0',
    'six >= 1.10.0',
]

ROOT = os.path.abspath(os.path.dirname(__file__))

version = __import__('firefence').__version__


setup(
    name='django-firefence',
    version=version,
    url='https://github.com/rehandalal/django-firefence',
    license='Mozilla Public License Version 2.0',
    author='Rehan Dalal',
    author_email='rehan@meet-rehan.com',
    description='A firewall for your Django views.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests', 'docs']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=DEPENDENCIES,
    py_modules=['firefence'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
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
    ]
)
