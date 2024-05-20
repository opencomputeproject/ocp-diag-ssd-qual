# Copyright 2024 Google LLC
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

"""Base class for all diags."""
import abc


class TestError(Exception):
  """Base exception class to notify that some of the test steps failed.

    Different steps have different context about what happened. So it's
    expected that every steps will put as much context to the error message
    as it's aware of.
  """
  pass


class Diag(abc.ABC):
  """Base class for all diags, provides methods covering all scenarios."""

  @abc.abstractmethod
  def setUp(self):  # pylint: disable=invalid-name
    """Sets up the device in the required mode.

    Raises:
      TestException: An error occurred while running one of the steps.
    """
    pass

  @abc.abstractmethod
  def PreDiag(self):
    """Implements extra steps required before test such as disk formating.

    Raises:
      TestException: An error occurred while running one of the steps.
    """
    pass

  @abc.abstractmethod
  def Run(self):
    """Runs the fio tests and other diagnostics.

    Raises:
      TestException: An error occurred while running one of the steps.
    """
    pass

  @abc.abstractmethod
  def PostDiag(self):
    """Checks if the diags meet the success criteria.

    Raises:
      TestException: An error occurred while running one of the steps.
    """
    pass

  @abc.abstractmethod
  def Report(self):
    """Collects the logs and generates the output in required format.

    Raises:
      TestException: An error occurred while running one of the steps.
    """
    pass

  @abc.abstractmethod
  def tearDown(self):  # pylint: disable=invalid-name
    """Rolls back the changes made in setUp method to the original state.

    Raises:
      TestException: An error occurred while running one of the steps.
    """
    pass
