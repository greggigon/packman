
########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

from setuptools import setup
# from setuptools import find_packages
from setuptools.command.test import test as TestCommand
import sys
import re
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        print('VERSION: ', version_match.group(1))
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

setup(
    name='packman',
    version=find_version('packman', '__init__.py'),
    url='https://github.com/cloudify-cosmo/packman',
    download_url='https://github.com/cloudify-cosmo/packman/tarball/0.1',
    author='nir0s',
    author_email='nir36g@gmail.com',
    license='LICENSE',
    platforms='Ubuntu',
    description='Package Generator',
    long_description='My description is shorter than yours',
    packages=['packman'],
    entry_points={
        'console_scripts': [
            'pkm = packman.pkm:main',
        ]
    },
    install_requires=[
        "fabric==1.8.3",
        "jinja2==2.7.2",
        "docopt==.0.6.1",
        # "pika==0.9.13",
        # "infi.docopt_completion==0.2.1",
        # "sphinx-rtd-theme",
    ],
    tests_require=['nose', 'tox'],
    test_suite='packman.test.test_packman',
    cmdclass={'test': Tox},
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving :: Packaging',
    ],
)
