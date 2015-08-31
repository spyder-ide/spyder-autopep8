#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for spyderplugin.ui.autopep8
"""

from setuptools import setup, find_packages
import os
import os.path as osp
import sys


# Check for Python 3
PY3 = sys.version_info[0] == 3


def get_version():
    """ """
    with open("spyplugins/ui/example/__init__.py") as f:
        lines = f.read().splitlines()
        for l in lines:
            if "__version__" in l:
                version = l.split("=")[1].strip()
                version = version.replace("'", '').replace('"', '')
                return version


def get_readme():
    """ """
    with open('README.rst') as f:
        readme = str(f.read())
    return readme


# TODO:
def get_data_files():
    """Return data_files in a platform dependent manner"""
    if sys.platform.startswith('linux'):
        if PY3:
            data_files = [('share/applications',
                           ['scripts/conda-manager3.desktop']),
                          ('share/pixmaps',
                           ['img_src/conda-manager3.png'])]
        else:
            data_files = [('share/applications',
                           ['scripts/conda-manager.desktop']),
                          ('share/pixmaps',
                           ['img_src/conda-manager.png'])]
    elif os.name == 'nt':
        data_files = [('scripts', ['img_src/conda-manager.ico'])]
    else:
        data_files = []
    return data_files


def get_package_data(name, extlist):
    """Return data files for package *name* with extensions in *extlist*"""
    flist = []
    # Workaround to replace os.path.relpath (not available until Python 2.6):
    offset = len(name) + len(os.pathsep)
    for dirpath, _dirnames, filenames in os.walk(name):
        for fname in filenames:
            if not fname.startswith('.') and osp.splitext(fname)[1] in extlist:
                flist.append(osp.join(dirpath, fname)[offset:])
    return flist


# Requirements
REQUIREMENTS = ['autopep8']
EXTLIST = ['.jpg', '.png', '.json', '.mo', '.ini']
LIBNAME = 'spyplugin.ui.autopep8'


setup(
    name=LIBNAME,
    version=get_version(),
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    package_data={LIBNAME: get_package_data(LIBNAME, EXTLIST)},
    namespace_packages=['spyplugins', 'spyplugins.ui'],
    keywords=["Qt PyQt4 PyQt5 PySide spyder plugins autopep8 pep8"],
    install_requires=REQUIREMENTS,
    url='https://github.com/spyder-ide/spyplugins.ui.autopep8',
    license='MIT',
    author='Joseph Martinot-Lagarde',
    author_email='contrebasse@gmail.com',
    maintainer='Gonzalo Peña-Castellanos',
    maintainer_email='goanpeca@gmail.com',
    description='A simple plugin example package for spyder.',
    long_description=get_readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Widget Sets'])
