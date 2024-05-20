# Copyright 2024 Google LLC
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from dataclasses import dataclass

_BANDWIDTH = "bwMbytesPerSec"
_FIO_BANDWIDTH = "bw"
_SUPPORTED_IO_TYPES = ("read", "write", "trim")
KB_IN_MB = 1024
NS_IN_US = 1000
_JSON_TO_FIO_MAPPING = {
  "lat50thUsec": "50.000000",
  "lat95thUsec": "95.000000",
  "lat99thUsec": "99.000000",
  "lat999thUsec": "99.900000",
  "lat9999thUsec": "99.990000",
  "latMaxUsec": "max",
  "latMeanUsec": "mean",
  _BANDWIDTH: _FIO_BANDWIDTH,
}
_FIO_TO_JSON_MAPPING = {v: k for k,v in _JSON_TO_FIO_MAPPING.items()}

@dataclass
class FailedWorkload:
  io_type: str
  workload_id: int
  failed_metrics: list

@dataclass
class FailedBenchmark:
  name: str
  failed_workloads: list[FailedWorkload]

def _to_kilobytes(num_megabytes):
  return num_megabytes * KB_IN_MB

def _to_nanosec(usecs):
  return usecs * NS_IN_US

class Benchmark:
  def __init__(self, descriptor):
    self._basename = descriptor["basename"]
    self._workloads = [
        Workload(workload) for workload in descriptor["workloads"]
    ]

  def evaluate(self, fio_output):
    failed_targets = []
    for workload in self._workloads:
      result = workload.evaluate(fio_output)
      if result != None:
        failed_targets.append(result)
    return FailedBenchmark(self._basename, failed_targets)


class Workload:
  def __init__(self, workload):
    self._io_type = ''
    for io_type in _SUPPORTED_IO_TYPES:
      if workload["ioType"].endswith(io_type):
        self._io_type = io_type
        break

    self._targets = {
        _JSON_TO_FIO_MAPPING[k]: int(v)
        for k,v in workload["targets"].items()}
    for metric, usec in self._targets.items():
      if metric == _FIO_BANDWIDTH:
        # it's a bandwidth, skipping
        continue
      self._targets[metric] = _to_nanosec(usec) # convert us to ns

    self._targets[_FIO_BANDWIDTH] = _to_kilobytes(self._targets.get(_FIO_BANDWIDTH, 0))
    self._workload_num = workload["workloadNum"]

  def evaluate(self, fio_output):
    actual_numbers = fio_output["jobs"][0][self._io_type]["clat_ns"]["percentile"]
    failed_metrics = []
    for metric, expected_value in self._targets.items():
      if metric == _FIO_BANDWIDTH:
        # let's handle bandwidth separately
        continue
      if expected_value < actual_numbers[metric]:
        failed_metrics.append(_FIO_TO_JSON_MAPPING[metric])
    actual_bandwidth = fio_output["jobs"][0][self._io_type][_FIO_BANDWIDTH]
    if (_FIO_BANDWIDTH in self._targets and
        self._targets[_FIO_BANDWIDTH] > actual_bandwidth):
      failed_metrics.append(_FIO_TO_JSON_MAPPING[_FIO_BANDWIDTH])

    if failed_metrics:
      return FailedWorkload(
          self._io_type,
          self._workload_num,
          failed_metrics
      )
    return None
