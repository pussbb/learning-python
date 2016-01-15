# -*- coding: utf-8 -*-
"""

"""
import unittest

import sys

from shell_command import is_quoted, ShellCommand, ShellIORedirection, \
    ShellCommandNotFound, ShellCommandRuntimeException, using_command_full_path


class ShellCommandTest(unittest.TestCase):

    def test_is_quoted(self):
        self.assertTrue(is_quoted('"WARN\|ERROR\|at.*\.java\:.*"'))
        self.assertTrue(is_quoted('\'WARN\|ERROR\|at.*\.java\:.*\''))
        self.assertFalse(is_quoted('\'WARN\|ERROR\|at.*\.java\:.*\'ee'))
        self.assertFalse(is_quoted('\'WARN\|ERROR\|at.*\.java\:.*'))
        self.assertFalse(is_quoted('"'))
        self.assertFalse(is_quoted('\''))

    def test_command_simple(self):
        self.assertEqual(
                ShellCommand('java', '-version'),
                'java -version'
        )

        self.assertEqual(
                ShellCommand('java', '-version', file_='asasa'),
                'java -version file_=asasa'
        )

        self.assertEqual(
                ShellCommand('java', '-version', '2>&1'),
                'java -version \'2>&1\''
        )

    def test_command_io_redir_to_file(self):
        self.assertEqual(
                ShellCommand('java', '-version') > 'some_file',
                'java -version > some_file'
        )

        self.assertEqual(
                ShellCommand('java', '-version') >> 'some_file',
                'java -version >> some_file'
        )

    def test_command_logical_op(self):
        self.assertEqual(
                ShellCommand('java', '-version') | ShellCommand('something'),
                'java -version || something'
        )

        self.assertEqual(
                ShellCommand('java', '-version') & ShellCommand('something'),
                'java -version && something'
        )

    def test_add_append_another_cmd(self):

        self.assertEqual(
                ShellCommand('java', '-version', ShellIORedirection.error_to_out()) + ShellCommand('grep', 'version'),
                'java -version 2>&1 | grep version'
        )

        self.assertEqual(
                ShellCommand('java', '-version') + ShellIORedirection.error_to_out(),
                'java -version 2>&1'
        )

    def test_command_exceptions(self):
        with self.assertRaises(ShellCommandNotFound) as exp:
            ShellCommand('some_non_existing_command').execute()

        self.assertEqual(
                exp.exception.command,
                'some_non_existing_command'
        )
        self.assertEqual(exp.exception.result.exit_code, 127)
        self.assertIsNotNone(exp.exception.result.response)

        with self.assertRaises(ShellCommandRuntimeException) as exp:
            ShellCommand('cat', '/wew/wewe/wew').execute()

        self.assertGreater(exp.exception.result.exit_code, 0)
        self.assertIsNotNone(exp.exception.result.response)

    def test_command_execution(self):
        result = ShellCommand(sys.executable, '-h').execute()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, ShellCommand.Response)
        self.assertEqual(result.exit_code, 0)
        self.assertIsNotNone(result.response)
        self.assertIsInstance(list(result), list)

    def test_wrapping_command_name(self):
        self.assertEqual(
                using_command_full_path('java'),
                '$(type -P java)'
        )

        self.assertEqual(
                using_command_full_path('java', use_which=True),
                '$(which java)'
        )
