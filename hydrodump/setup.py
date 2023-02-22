# =================================================================
#
# Authors: Benjamin Webb <bwebb@lincolninst.edu>
#
# Copyright (c) 2023 Benjamin Webb
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import io
import os
import re
from setuptools import Command, find_packages, setup


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        errno = subprocess.call(['pytest'])
        raise SystemExit(errno)


def read(filename, encoding='utf-8'):
    """read file contents"""
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with io.open(full_path, encoding=encoding) as fh:
        contents = fh.read().strip()
    return contents


def get_package_version():
    """get version from top-level package init"""
    version_file = read('hydrodump/__init__.py')
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


KEYWORDS = [
    'hydroshare',
    'cuashi',
    'internetofwater'
]

DESCRIPTION = ('Hydrodump provides the ability to easily download data from'
               'Hydroshare and upload it to a Postgis database.')


# ensure a fresh MANIFEST file is generated
if (os.path.exists('MANIFEST')):
    os.unlink('MANIFEST')


setup(
    name='hydrodump',
    version=get_package_version(),
    description=DESCRIPTION.strip(),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT Software License',
    platforms='all',
    keywords=' '.join(KEYWORDS),
    author='Ben Webb',
    author_email='bwebb@lincolninst.edu',
    maintainer='Ben Webb',
    maintainer_email='bwebb@lincolninst.edu',
    url='https://github.com/cgs-earth/hydrodump-action',
    install_requires=read('requirements.txt').splitlines(),
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'hydrodump=hydrodump:cli'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    project_urls={
        'Homepage': 'https://github.com/cgs-earth/sensorthings-action',
        'Source Code': 'https://github.com/cgs-earth/sensorthings-action',
        'Issue Tracker': 'https://github.com/cgs-earth/sensorthings-action/issues'
    },
    cmdclass={'test': PyTest},
    test_suite='tests.run_tests'
)
