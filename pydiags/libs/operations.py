# Copyright 2024 Google LLC
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

"""Base class providing interface for supported operations."""
import abc


class DUTOperations(abc.ABC):
  """Interface for operations supported by vendors."""

  @abc.abstractmethod
  def IdentifyDUT(self) -> bool:
    """Interface for identification of DUT.

    Returns:
      True in case of success, False otherwise.
    """
    pass

  @abc.abstractmethod
  def VUIdentifyDUT(self) -> bool:
    """Interface for vendor specific identification of DUT.

    Returns:
      True in case of success, False otherwise.
    """
    pass

  @abc.abstractmethod
  def ChangeMode(self) -> bool:
    """Interface for mode changes like from Normal mode to Stream directive.

    Returns:
      True in case of success, False otherwise.
    """
    pass

  @abc.abstractmethod
  def VUChangeMode(self) -> bool:
    """Interface for any vendor specific change mode.

    Returns:
      True in case of success, False otherwise.
    """
    pass

  @abc.abstractmethod
  def LogCollect(self) -> int:
    """Implement all generic logs collection when error occurs.

    Returns:
      Number of collected items.
    """
    pass

  @abc.abstractmethod
  def VULogCollect(self) -> int:
    """Interface for vendor unique log collection implementation.

    Returns:
      Number of collected items.
    """
    pass

  @abc.abstractmethod
  def GetErrorLog(self) -> str:
    """Interface for getting error log.

    Returns:
      a path to generic error log.
    """
    pass

  @abc.abstractmethod
  def GetVUErrorLog(self) -> str:
    """Interface for getting vendor specific error log.

    Returns:
      a path to vendor specific error log.
    """
    pass
