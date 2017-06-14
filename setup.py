#!/usr/bin/env python

from io import open
from setuptools import setup, find_packages


setup(
    name='django_phone_confirmation',
    version='0.2.5',
    packages=find_packages(),
    license='MIT',
    author='Ricardo S. A. Silva',
    description='A Django app to validate cell phone numbers through SMS messages and REST.',
    keywords='django cell phone confirmation',
    author_email='ricardo@salamandra.cc',
    long_description=open('README.md').read(),
    install_requires=['django_rest', 'django-sendsms==0.2.3'],
    include_package_data=True,
    url='https://github.com/ricardosasilva/django_phone_confirmation',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
