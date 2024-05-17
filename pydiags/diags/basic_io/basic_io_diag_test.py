# Copyright 2024 Google LLC
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import subprocess
import unittest
from unittest.mock import patch, mock_open

from ...libs import argparser
from . import basic_io_diag


class BasicIODiagTest(unittest.TestCase):
  @patch('os.getcwd')
  @patch('subprocess.run',
         side_effect=subprocess.CalledProcessError(cmd='fio', returncode=-1)
         )

  def test_run_fail(self, _, mock_getcwd):
    mock_getcwd.return_value = '/mydir/'
    parser = argparser.create_parser()
    diag = basic_io_diag.BasicIODiag(
        parser.parse_args(
            ['--duts', '/dev/nvme1n1', '--playbook', 'playbook.fio'])
    )
    file_contents = [
        '["basic_io_seq_wr_8kb_bs_1024_qd_known_pattern.fio"]',
        '[basic_io_logical_reads-seq_wr]'
    ]
    mock_files = [
        mock_open(read_data=content).return_value for content in file_contents
    ]
    mock_opener = mock_open()
    mock_opener.side_effect = mock_files
    with self.assertRaises(subprocess.CalledProcessError) as cm:
      with patch('builtins.open', mock_opener):
        diag.Run()
    self.assertEqual(cm.exception.returncode, -1)
    mock_opener.assert_called_once_with('playbook.fio')


if __name__ == '__main__':
  unittest.main()
