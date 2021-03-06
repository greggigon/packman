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

__author__ = 'nir0s'

from packman.packman import do
from packman.packman import CommonHandler
from packman.packman import PythonHandler
from packman.packman import WgetHandler
from packman.packman import TemplateHandler
from packman.packman import PackagerError
from packman.packman import init_logger
from packman.packman import get_component_config
from packman.packman import check_distro, get_distro
from packman.packman import set_global_verbosity_level


import unittest
import os
from functools import wraps
from fabric.api import hide
from testfixtures import log_capture
import logging
from platform import dist


TEST_DIR = '{0}/test_dir'.format(os.path.expanduser("~"))
TEST_FILE_NAME = 'test_file'
TEST_FILE = TEST_DIR + '/' + TEST_FILE_NAME
TEST_TAR_NAME = 'test_tar.tar.gz'
TEST_TAR = TEST_DIR + '/' + TEST_TAR_NAME
TEST_VENV = '{0}/test_venv'.format(os.path.expanduser("~"))
TEST_MODULE = 'xmltodict'
TEST_MOCK_MODULE = 'mockmodule'
TEST_TEMPLATES_DIR = 'packman/tests/templates'
TEST_TEMPLATE_FILE = 'mock_template.template'
MOCK_TEMPLATE_CONTENTS = 'TEST={{ test_template_parameter }}'
MOCK_PACKAGES_FILE = 'mock_packages.py'
MOCK_PACKAGES_CONTENTS = '''PACKAGES = {'test_component':'x'}'''
MOCK_PACKAGES_DICT = {'test_component': 'x'}

HIDE_LEVEL = 'everything'


def file(func):
    @wraps(func)
    def execution_handler(*args, **kwargs):
        client = CommonHandler()
        client.rmdir(TEST_DIR, sudo=False)
        do('mkdir -p ' + TEST_DIR, sudo=False)
        do('touch ' + TEST_FILE, sudo=False)
        func(*args, **kwargs)
        client.rmdir(TEST_DIR, sudo=False)

    return execution_handler


def dir(func):
    @wraps(func)
    def execution_handler(*args, **kwargs):
        client = CommonHandler()
        client.rmdir(TEST_DIR, sudo=False)
        do('mkdir -p ' + TEST_DIR, sudo=False)
        func(*args, **kwargs)
        client.rmdir(TEST_DIR, sudo=False)

    return execution_handler


def venv(func):
    @wraps(func)
    def execution_handler(*args, **kwargs):
        client = PythonHandler()
        with hide(HIDE_LEVEL):
            client.pip('virtualenv==1.11.4', sudo=False)
            client.venv(TEST_VENV, sudo=False)
        func(*args, **kwargs)
        client.rmdir(TEST_VENV, sudo=False)

    return execution_handler


def mock_template(func):
    @wraps(func)
    def execution_handler(*args, **kwargs):
        client = CommonHandler()
        template_file = TEST_TEMPLATES_DIR + '/' + TEST_TEMPLATE_FILE
        do('mkdir -p ' + TEST_TEMPLATES_DIR, sudo=False)
        with open(template_file, 'w+') as f:
            f.write(MOCK_TEMPLATE_CONTENTS)
        func(*args, **kwargs)
        client.rm(template_file, sudo=False)
    return execution_handler


def mock_packages(func):
    @wraps(func)
    def execution_handler(*args, **kwargs):
        client = CommonHandler()
        packages_file = TEST_TEMPLATES_DIR + '/' + MOCK_PACKAGES_FILE
        do('mkdir -p ' + TEST_TEMPLATES_DIR, sudo=False)
        with open(packages_file, 'w+') as f:
            f.write(MOCK_PACKAGES_CONTENTS)
        func(*args, **kwargs)
        client.rm(packages_file, sudo=False)
        client.rm(packages_file + 'c', sudo=False)
    return execution_handler


class CommonHandlerTest(unittest.TestCase, CommonHandler):

    @file
    def test_find_in_dir_found(self):
        with hide(HIDE_LEVEL):
            outcome = self.find_in_dir(TEST_DIR, TEST_FILE_NAME, sudo=False)
        self.assertEquals(outcome, TEST_FILE)

    def test_find_in_dir_not_found(self):
        with hide(HIDE_LEVEL):
            outcome = self.find_in_dir(TEST_DIR, TEST_FILE, sudo=False)
        self.assertEquals(outcome, None)

    @dir
    def test_is_dir(self):
        outcome = self.is_dir(TEST_DIR)
        self.assertTrue(outcome)

    def test_is_not_dir(self):
        outcome = self.is_dir(TEST_DIR)
        self.assertFalse(outcome)

    @file
    def test_is_file(self):
        outcome = self.is_file(TEST_FILE)
        self.assertTrue(outcome)

    def test_is_not_file(self):
        outcome = self.is_file(TEST_FILE)
        self.assertFalse(outcome)

    @dir
    def test_touch(self):
        outcome = self.touch(TEST_FILE, sudo=False)
        self.assertTrue(outcome.succeeded)
        self.assertTrue(self.is_file(TEST_FILE))

    def test_make_dir(self):
        outcome = self.mkdir(TEST_DIR, sudo=False)
        self.assertTrue(outcome.succeeded)
        self.assertTrue(self.is_dir(TEST_DIR))

    @dir
    def test_make_dir_already_exists(self):
        outcome = self.mkdir(TEST_DIR, sudo=False)
        self.assertFalse(outcome)
        self.assertTrue(self.is_dir(TEST_DIR))

    @dir
    def test_remove_dir(self):
        outcome = self.rmdir(TEST_DIR, sudo=False)
        self.assertTrue(outcome.succeeded)
        self.assertFalse(self.is_dir(TEST_DIR))

    def test_remove_nonexistent_dir(self):
        outcome = self.rmdir(TEST_DIR, sudo=False)
        self.assertFalse(outcome)
        self.assertFalse(self.is_dir(TEST_DIR))

    @file
    def test_remove(self):
        outcome = self.rm(TEST_FILE, sudo=False)
        self.assertTrue(outcome.succeeded)
        self.assertFalse(self.is_file(TEST_FILE))

    def test_remove_nonexistent_file(self):
        outcome = self.rm(TEST_FILE, sudo=False)
        self.assertFalse(outcome)
        self.assertFalse(self.is_file(TEST_FILE))

    @file
    def test_copy(self):
        outcome = self.cp(TEST_FILE, '.', sudo=False)
        self.assertTrue(outcome.succeeded)
        self.assertTrue(self.is_file('./' + TEST_FILE_NAME))
        self.assertTrue(self.rm('./' + TEST_FILE_NAME, sudo=False).succeeded)

    def test_copy_noexistent_file(self):
        with hide(HIDE_LEVEL):
            outcome = self.cp(TEST_FILE, '.', sudo=False)
        self.assertTrue(outcome.failed)
        self.assertFalse(self.is_file('./' + TEST_FILE_NAME))

    @file
    def test_tar(self):
        with hide(HIDE_LEVEL):
            outcome = self.tar('.', './' + TEST_FILE_NAME, TEST_DIR,
                               sudo=False)
        self.assertTrue(outcome.succeeded)
        self.assertTrue(self.is_file('./' + TEST_FILE_NAME))
        self.assertTrue(self.rm('./' + TEST_FILE_NAME, sudo=False).succeeded)

    def test_tar_bad_options(self):
        with hide(HIDE_LEVEL):
            outcome = self.tar('.', './' + TEST_FILE_NAME, TEST_DIR,
                               'ttt', sudo=False)
        self.assertTrue(outcome.failed)
        self.assertFalse(self.is_file('./' + TEST_FILE_NAME))


class PythonHandlerTest(unittest.TestCase, PythonHandler, CommonHandler):

    def test_pip_existent_module(self):
        with hide(HIDE_LEVEL):
            outcome = self.pip(TEST_MODULE, sudo=False)
        self.assertTrue(outcome.succeeded)

    def test_pip_nonexistent_module(self):
        with hide(HIDE_LEVEL):
            outcome = self.pip(TEST_MOCK_MODULE,
                               attempts=1, sudo=False, timeout=2)
        self.assertTrue(outcome.failed)

    @venv
    def test_venv(self):
        with hide(HIDE_LEVEL):
            self.pip('virtualenv==1.11.4', sudo=False)
        outcome = self.is_file('{0}/bin/python'.format(TEST_VENV))
        self.assertTrue(outcome)

    @venv
    def test_pip_existent_module_in_venv(self):
        with hide(HIDE_LEVEL):
            outcome = self.pip(TEST_MODULE, TEST_VENV, sudo=False)
        self.assertTrue(outcome.succeeded)

    @venv
    def test_pip_nonexistent_module_in_venv(self):
        with hide(HIDE_LEVEL):
            outcome = self.pip(TEST_MOCK_MODULE, TEST_VENV,
                               attempts=1, sudo=False)
        self.assertTrue(outcome.failed)

    def test_check_module_not_installed(self):
        with hide(HIDE_LEVEL):
            outcome = self.check_module_installed(TEST_MOCK_MODULE)
        self.assertFalse(outcome)

    def test_check_module_installed(self):
        with hide(HIDE_LEVEL):
            self.pip(TEST_MODULE, sudo=False)
        outcome = self.check_module_installed(TEST_MODULE)
        self.assertTrue(outcome)


class WgetHandlerTest(unittest.TestCase, WgetHandler,
                      CommonHandler):

    @dir
    def test_wgets_file_to_dir(self):
        with hide(HIDE_LEVEL):
            self.downloads(['www.google.com'], dir=TEST_DIR, sudo=False)
        outcome = self.is_file('{0}/index.html'.format(TEST_DIR))
        self.assertTrue(outcome)

    @dir
    def test_wget_file_to_dir(self):
        with hide(HIDE_LEVEL):
            self.download('www.google.com', dir=TEST_DIR, sudo=False)
        outcome = self.is_file('{0}/index.html'.format(TEST_DIR))
        self.assertTrue(outcome)

    @dir
    def test_wget_file_to_file(self):
        with hide(HIDE_LEVEL):
            self.download('www.google.com', file=TEST_FILE, sudo=False)
        outcome = self.is_file(TEST_FILE)
        self.assertTrue(outcome)

    def test_wget_nonexistent_url(self):
        with hide(HIDE_LEVEL):
            outcome = self.download('www.google.comd', dir=TEST_DIR,
                                    sudo=False)
        self.assertTrue(outcome.failed)

    # TODO: (TEST) add wget archives dir test


class TemplateHandlerTest(unittest.TestCase, TemplateHandler,
                          CommonHandler):

    @file
    @mock_template
    def test_template_creation(self):
        component = {'test_template_parameter': 'test_template_output'}
        template_file = TEST_TEMPLATE_FILE
        self.generate_from_template(component, TEST_FILE, template_file,
                                    templates=TEST_TEMPLATES_DIR)
        with open(TEST_FILE, 'r') as f:
            self.assertIn('test_template_output', f.read())

    @mock_template
    def test_template_creation_template_file_missing(self):
        component = {'test_template_parameter': 'test_template_output'}
        template_file = 'mock_template'
        try:
            self.generate_from_template(component, TEST_FILE, template_file,
                                        templates=TEST_TEMPLATES_DIR)
        except PackagerError as ex:
            self.assertEqual(str(ex), 'template file missing')

    @mock_template
    def test_template_creation_template_dir_missing(self):
        component = {'test_template_parameter': 'test_template_output'}
        template_file = TEST_TEMPLATE_FILE
        try:
            self.generate_from_template(component, TEST_FILE, template_file,
                                        templates='')
        except PackagerError as ex:
            self.assertEqual(str(ex), 'template dir missing')

    @file
    @mock_template
    def test_template_creation_invalid_component_dict(self):
        component = ''
        template_file = TEST_TEMPLATE_FILE
        try:
            self.generate_from_template(component, TEST_FILE, template_file,
                                        templates=TEST_TEMPLATES_DIR)
        except PackagerError as ex:
            self.assertEqual(str(ex), 'component must be of type dict')

    @file
    @mock_template
    def test_template_creation_template_file_not_string(self):
        component = {'test_template_parameter': 'test_template_output'}
        template_file = False
        try:
            self.generate_from_template(component, TEST_FILE, template_file,
                                        templates=TEST_TEMPLATES_DIR)
        except PackagerError as ex:
            self.assertEqual(str(ex), 'template_file must be of type string')

    @file
    @mock_template
    def test_template_creation_template_dir_not_string(self):
        component = {'test_template_parameter': 'test_template_output'}
        template_file = TEST_TEMPLATE_FILE
        try:
            self.generate_from_template(component, TEST_FILE, template_file,
                                        templates=False)
        except PackagerError as ex:
            self.assertEqual(str(ex), 'template_dir must be of type string')

    @dir
    @mock_template
    def test_config_generation_from_config_dir(self):
        config_file = TEST_TEMPLATE_FILE
        component = {
            "sources_path": TEST_DIR,
            "test_template_parameter": "test_template_parameter",
            "config_templates": {
                "__config_dir": {
                    "files": TEST_TEMPLATES_DIR,
                    "config_dir": "config",
                }
            }
        }
        self.generate_configs(component, sudo=False)
        with open('{}/{}/{}'.format(component['sources_path'],
                  component['config_templates']['__config_dir']['config_dir'],
                  config_file), 'r') as f:
            self.assertIn(component['test_template_parameter'], f.read())

    @dir
    @mock_template
    def test_config_generation_from_template_dir(self):
        config_file = TEST_TEMPLATE_FILE
        component = {
            "sources_path": TEST_DIR,
            "test_template_parameter": "test_template_output",
            "config_templates": {
                "__template_dir": {
                    "templates": TEST_TEMPLATES_DIR,
                    "config_dir": "config",
                }
            }
        }
        self.generate_configs(component, sudo=False)
        with open('{}/{}/{}'.format(component['sources_path'],
                  component['config_templates']['__template_dir']['config_dir'],  # NOQA
                  config_file.split('.')[0:-1][0]), 'r') as f:
            self.assertIn(component['test_template_parameter'], f.read())

    @dir
    @mock_template
    def test_config_generation_from_template_file(self):
        config_file = TEST_TEMPLATE_FILE
        component = {
            "sources_path": TEST_DIR,
            "test_template_parameter": "test_template_output",
            "config_templates": {
                "__template_file": {
                    "template": TEST_TEMPLATES_DIR + '/' + config_file,
                    "output_file": config_file.split('.')[0:-1][0],
                    "config_dir": "config",
                }
            }
        }
        self.generate_configs(component, sudo=False)
        with open('{}/{}/{}'.format(component['sources_path'],
                  component['config_templates']['__template_file']['config_dir'],  # NOQA
                  config_file.split('.')[0:-1][0]), 'r') as f:
            self.assertIn(component['test_template_parameter'], f.read())


class TestBaseMethods(unittest.TestCase):

    def test_do(self):
        with hide(HIDE_LEVEL):
            outcome = do('uname -n', sudo=False)
        self.assertTrue(outcome.succeeded)

    def test_do_failure(self):
        with hide(HIDE_LEVEL):
            outcome = do('illegal operation', attempts=1, sudo=False)
        self.assertTrue(outcome.failed)

    def test_do_zero_attempts(self):
        try:
            with hide(HIDE_LEVEL):
                do('uname -n', attempts=0, sudo=False)
        except RuntimeError as ex:
            self.assertEqual(str(ex), 'attempts must be at least 1')

    def test_do_zero_sleeper(self):
        try:
            with hide(HIDE_LEVEL):
                do('uname -n', sleep_time=0, sudo=False)
        except RuntimeError as ex:
            self.assertEqual(str(ex), 'sleep_time must be larger than 0')

    @log_capture()
    def test_logger(self, capture):
        lgr = init_logger(base_level=logging.DEBUG)
        lgr.debug('TEST_LOGGER_OUTPUT')
        capture.check(('user', 'DEBUG', 'TEST_LOGGER_OUTPUT'))

    def test_logger_bad_config(self):
        try:
            init_logger(logging_config={'x': 'y'})
        except SystemExit as ex:
            self.assertIn('could not init', str(ex))

    @log_capture()
    def test_set_global_verbosity_level(self, capture):
        lgr = init_logger(base_level=logging.INFO)

        set_global_verbosity_level(is_verbose_output=False)
        lgr.debug('TEST_LOGGER_OUTPUT')
        capture.check()
        lgr.info('TEST_LOGGER_OUTPUT')
        capture.check(('user', 'INFO', 'TEST_LOGGER_OUTPUT'))

        set_global_verbosity_level(is_verbose_output=True)
        lgr.debug('TEST_LOGGER_OUTPUT')
        capture.check(
            ('user', 'INFO', 'TEST_LOGGER_OUTPUT'),
            ('user', 'DEBUG', 'TEST_LOGGER_OUTPUT'))

    def test_get_component_config_dict(self):
        c = get_component_config('test_component', MOCK_PACKAGES_DICT)
        self.assertEqual(c, 'x')

    def test_get_component_config_dict_missing_component(self):
        try:
            get_component_config('WRONG', MOCK_PACKAGES_DICT)
        except PackagerError as ex:
            self.assertEqual(str(ex), 'no config found for package')

    @mock_packages
    def test_get_component_config_file(self):
        packages_file = TEST_TEMPLATES_DIR + '/' + MOCK_PACKAGES_FILE
        c = get_component_config('test_component',
                                 components_file=packages_file)
        self.assertEqual(c, 'x')

    @mock_packages
    def test_get_component_config_file_missing_component(self):
        packages_file = TEST_TEMPLATES_DIR + '/' + MOCK_PACKAGES_FILE
        try:
            get_component_config('WRONG',
                                 components_file=packages_file)
        except PackagerError as ex:
            self.assertEqual(str(ex), 'no config found for package')

    def test_get_component_config_missing_file(self):
        try:
            get_component_config('test_component',
                                 components_file='x')
        except PackagerError as ex:
            self.assertEqual(str(ex), 'missing components file')

    def test_get_distro(self):
        test_distro = dist()[0]
        distro = get_distro()
        self.assertEqual(distro, test_distro)

    def test_check_distro_success(self):
        check_distro()

    def test_check_distro_fail(self):
        try:
            check_distro(supported='nodistro')
        except RuntimeError as ex:
            self.assertEqual(str(ex), 'distro not supported')

    # @dir
    # def test_pack(self):
    #     template_file = TEST_TEMPLATE_FILE
    #     config_file = TEST_TEMPLATE_FILE
    #     component = {
    #         "name": "test_package",
    #         "version": "3.0.0",
    #         "depends": [
    #             'test_dependency',
    #         ],
    #         "package_path": TEST_DIR,
    #         "sources_path": TEST_DIR + '/test_sources_dir',
    #         "src_package_type": "dir",
    #         "dst_package_type": "deb",
    #         # "bootstrap_script": 'bootstrap_script.sh',
    #         # "bootstrap_template": template_file,
    #         "config_templates": {
    #             "__template_file": {
    #                 "template": TEST_TEMPLATES_DIR + '/' + config_file,
    #                 "output_file": config_file.split('.')[0:-1][0],
    #                 "config_dir": "config",
    #             },
    #             # "__template_dir": {
    #             #     "templates": TEST_TEMPLATES_DIR,
    #             #     "config_dir": "config",
    #             # },
    #             # "__config_dir": {
    #             #     "files": TEST_TEMPLATES_DIR,
    #             #     "config_dir": "config",
    #             # }
    #         }
    #     }
    #     pack(component)

# TODO: (TEST) add apt handler tests
# TODO: (TEST) add yum handler tests (hrm.. how to?)
