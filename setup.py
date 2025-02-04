#!/usr/bin/env python

''' To make a new release:
    1. Bump version number in setup.py
    2. Update CHANGELOG
    3. $ git commit ...
    4. $ git tag -a x.x.x  # see `git tag` for latest
    5. $ git push origin main
    6. $ git push --tags
    7. $ python setup.py register sdist
    8. $ twine upload dist/*
'''

from setuptools import setup, find_packages  # noqa: E402


VERSION = '.'.join(('0', '3', '0'))

DESCRIPTION = '''Drag-and-drop multiple uploading of related images/files for
              Django admin, using Dropzone.js'''

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Framework :: Django',
    'Framework :: Django :: 3.2',
    'Framework :: Django :: 4.0',
]

setup(
    name='django-dragndrop-related',
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords=['django'],
    platforms=['OS Independent'],
    url='http://github.com/NeuralDynamicsWeb/django-dragndrop-related',
    packages=find_packages(),
    include_package_data=True,

    author='Neural Dynamics',
    author_email='neuraldynamics.web@gmail.com',

    zip_safe=False,
    python_requires='>=3.6,<4',
    install_requires=['Django>=3.2'],
    classifiers=CLASSIFIERS
)
