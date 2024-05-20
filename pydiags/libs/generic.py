# Copyright 2024 Google LLC
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

"""Implementation of generic operations supported by any vendor."""
import os
import subprocess

from . import commonlib
from . import operations

_NVME_SMART_LOG = "nvme smart-log -o json %s"
_NVME_ERROR_LOG = "nvme error-log -o json %s"
_NVME_PERSISTENT_LOG = "nvme persistent-event-log -o json %s -l 512"
_NVME_TELEMETRY_LOG = "nvme telemetry-log %s  --output-file=%s"

_NVME_CMDS = {
    "smart-log": _NVME_SMART_LOG,
    "error-log": _NVME_ERROR_LOG,
    "persistent-event-log": _NVME_PERSISTENT_LOG,
}


class GenericDUTOperations(operations.DUTOperations):
  """Implementation for generic operations that are supported by all vendors."""
  _vendor_disk_cfg = {}
  _generic_disk_cfg = {}
  _vendor_error_log = []
  _generic_error_log = []

  def __init__(self, dev_name, logs_dir, ocp_dut):
    self._name = dev_name
    self._logs_dir = logs_dir
    self._ocp_dut = ocp_dut

  @property
  def name(self):
    return self._name

  @property
  def ocp_dut(self):
    return self._ocp_dut

  @property
  def logs_dir(self):
    return self._logs_dir

  def IdentifyDUT(self) -> bool:
    """Implement generic identification of DUT.

    Returns:
      True in case of success, False otherwise.
    """
    return True

  def VUIdentifyDUT(self) -> bool:
    """Implement vendor specific identification of DUT.

    Returns:
      True in case of success, False otherwise.
    """
    raise NotImplementedError()

  def ChangeMode(self) -> bool:
    """Implement the generic mode changes.

    Returns:
      True in case of success, False otherwise.
    """
    return True

  def VUChangeMode(self) -> bool:
    """Implement any vendor specific change mode.

    Returns:
      True in case of success, False otherwise.
    """
    raise NotImplementedError()

  def LogCollect(self) -> list[str]:
    """Implement all generic logs collection when error occurs.

    Returns:
      A list of collected items.
    """
    collected_logs = []
    for name, nvme_cmd in _NVME_CMDS.items():
      cmd = nvme_cmd % self._name
      print("Collecting output for %s ..." % cmd)
      out = ""
      try:
        out = commonlib.cmdexec(cmd.split())
      except (IOError, subprocess.CalledProcessError) as _:
        print("Non-critical error occured while running: %s" % cmd)
        continue
      output_file = os.path.join(self._logs_dir, name)
      with open(output_file, "w") as f:
        f.write(out)
      collected_logs.append(output_file)
    # separately handle telemetry-log as it's already stored in the file
    output_file = os.path.join(self._logs_dir, "telemetry-log")
    cmd = _NVME_TELEMETRY_LOG % (self._name, output_file)
    commonlib.cmdexec(cmd.split())
    collected_logs.append(output_file)
    return collected_logs

  def VULogCollect(self) -> int:
    """Implement vendor unique log collection, overriden by vendor.

    Returns:
      Number of collected items.
    """
    raise NotImplementedError()

  def GetErrorLog(self) -> str:
    """Returns a path to generic error log."""
    return self._logs_dir

  def GetVUErrorLog(self) -> str:
    """Returns a path to vendor specific error log."""
    return ""
