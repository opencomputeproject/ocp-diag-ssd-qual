# Copyright 2024 Google LLC
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

"""This module provides a method to creats a parser for CLI args."""
import argparse


def create_parser():
  """This method creates parser based on standard argparse functionality.

  This method provides a single entry for registering the CLI args.

  Returns:
    A parser that can be used in the main program.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--duts',
      help='Devices under tests, comma separated.'
  )
  parser.add_argument(
      '--playbook',
      help='The playbook file that contains list of fio pre-canned scenario'
      + ' files that should be performed sequentially.',
      default='basic_io.json'
  )
  return parser
