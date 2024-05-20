# Copyright 2024 Google LLC
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.


import unittest

import argparser


class ArgParserTest(unittest.TestCase):

  def setUp(self):
    super().setUp()
    self.parser = argparser.create_parser()

  def testParseDUTs(self):
    args = self.parser.parse_args(['--duts', '/dev/nvme0n1, /dev/nvme1n1'])
    duts = args.duts.split(',')
    self.assertEqual(len(duts), 2)
    for dev_name in duts:
      self.assertRegex(dev_name, '/dev/nvme[0-9]+n1')

  def testParseScenarioConfig(self):
    args = self.parser.parse_args(['--playbook', 'fio_steps.json'])
    self.assertEqual(args.playbook, 'fio_steps.json')

if __name__ == '__main__':
  unittest.main()
