# Copyright 2024 Google LLC
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

"""A module is a collection of functions used across the tool."""
import subprocess


def cmdexec(cmdline: list[str]) -> str:
  """Executes the command line and returns stdout only.

  Args:
    cmdline: to be executed.
  Returns:
    The output on stdout emitted by the command executed.
  Raises:
    IOError: An error occurred executing this cmdline.
  """
  try:
    result = subprocess.run(cmdline, stdout=subprocess.PIPE,
                            text=True, check=True)
  except subprocess.CalledProcessError as e:
    print('Exception Running command "%s":%s', cmdline, e)
    raise
  return result.stdout
