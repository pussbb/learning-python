# -*- coding: utf-8 -*-
"""

"""
import unittest

from shell_command import is_quoted, ShellCommand, ShellIORedirection, \
    ShellCommandNotFound, ShellCommandRuntimeException


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
                '$(type -P java) -version'
        )

        self.assertEqual(
                ShellCommand('java', '-version', full_path=False),
                'java -version'
        )

        self.assertEqual(
                ShellCommand('java', '-version', file_='asasa'),
                '$(type -P java) -version file_=asasa'
        )

        self.assertEqual(
                ShellCommand('java', '-version', '2>&1', full_path=False),
                'java -version \'2>&1\''
        )

    def test_command_io_redir_to_file(self):
        self.assertEqual(
                ShellCommand('java', '-version') > 'some_file',
                '$(type -P java) -version > some_file'
        )

        self.assertEqual(
                ShellCommand('java', '-version') >> 'some_file',
                '$(type -P java) -version >> some_file'
        )

    def test_command_logical_op(self):
        self.assertEqual(
                ShellCommand('java', '-version') | ShellCommand('something'),
                '$(type -P java) -version || $(type -P something)'
        )

        self.assertEqual(
                ShellCommand('java', '-version') & ShellCommand('something'),
                '$(type -P java) -version && $(type -P something)'
        )

    def test_add_append_another_cmd(self):

        self.assertEqual(
                ShellCommand('java', '-version', ShellIORedirection.error_to_out()) + ShellCommand('grep', 'version'),
                '$(type -P java) -version 2>&1 | $(type -P grep) version'
        )

        self.assertEqual(
                ShellCommand('java', '-version') + ShellIORedirection.error_to_out(),
                '$(type -P java) -version 2>&1'
        )

    def test_command_exceptions(self):
        with self.assertRaises(ShellCommandNotFound) as exp:
            ShellCommand('some_non_existing_command', full_path=False).execute()

        self.assertEqual(
                exp.exception.command,
                'some_non_existing_command'
        )
        self.assertEqual(exp.exception.exit_code, 127)
        self.assertIsNotNone(exp.exception.output)

        with self.assertRaises(ShellCommandRuntimeException) as exp:
            ShellCommand('cat', '/wew/wewe/wew').execute()

        self.assertGreater(exp.exception.exit_code, 0)
        self.assertIsNotNone(exp.exception.output)
