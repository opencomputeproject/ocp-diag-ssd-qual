# Copyright 2024 Google LLC
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

"""Basic IO Diag, fio based test to check basic storage functionality."""
import argparse
import collections
import json
import os
import tempfile

import ocptv.output as tv

from ...libs import argparser
from ...libs import commonlib
from ...libs import diag
from ...libs import generic
from ...libs import operations
from ...libs import performance
from ...libs.diag import TestError

_FIO_PATH = '/usr/bin/fio'
_OUTPUT_FORMAT = '--output-format=json+'
_ARGS = [_FIO_PATH, _OUTPUT_FORMAT]


class BasicIODiag(diag.Diag):
  """Implementation of basic IO test for storage using fio tool."""

  def __init__(self,
               config: argparse.Namespace,
               driver: operations.DUTOperations = generic.GenericDUTOperations
               ):
    """Constructs the object and runs the tests passed.

    Args:
      config: a config file used to properly configure the test env and specify
      the steps needed to perform.
      driver: a driver that will be used to issue nvme commands to the drive
      before and after test.
    Raises:
      TestError: An error occurred while running one of the steps.
    """
    self._config = config
    self._logs = collections.defaultdict(list)
    self._driver = driver
    self._drives = []
    self._log_dir = tempfile.mkdtemp()
    self._run = tv.TestRun(name='BasicIODiag', version='1.0')
    instructions = {}
    with open(self._config.playbook) as playbook:
      instructions = json.load(playbook)
    self._scenarios = instructions['test_steps']
    benchmark_targets = instructions.get('benchmark_targets', '')
    self._configs_path = os.path.join(os.getcwd(), 'pydiags', 'configs')
    self._benchmark_evaluator = None
    if benchmark_targets:
      with open(os.path.join(self._configs_path, benchmark_targets)) as f:
        self._benchmark_evaluator = performance.Benchmark(json.load(f))
    hostid = commonlib.cmdexec(['hostid']).strip()
    hostname = commonlib.cmdexec(['hostname']).strip()
    self._ocp_duts = dict()
    for dut in self._config.duts.split():
      path = os.path.join(self._log_dir, dut.split('/')[-1])
      os.makedirs(path, exist_ok=True)
      ocp_dut = tv.Dut(id=hostid, name=':'.join((hostname, dut)))
      self._drives.append(self._driver(dut, path, ocp_dut))
      self._ocp_duts[dut] = ocp_dut

  def _report_errors(self, operation='test running'):
    """Reports the errors occured while performing different steps.

    Args:
      operation: specifes during what operation the execution failed.
    """
    print('Errors occured while %s.' % operation)
    if self._driver.GetErrorLog():
      print('See generic errors at:\n\t%s' % (self._driver.GetErrorLog()))
    if self._driver.GetVUErrorLog():
      print('See vendor errors at:\n\t%s' % (self._driver.GetVUErrorLog()))

  def setUp(self):
    """Sets up the device in the required mode.

    Raises:
      TestError: An error occurred while running one of the steps.
    """
    for drive in self._drives:
      if not drive.IdentifyDUT():
        self._report_errors('identifying DUT')
        raise TestError("error occured in 'setUp' step.")

      if not drive.ChangeMode():
        self._report_errors('changing mode')
        raise TestError("error occured in 'setUp' step.")

  def PreDiag(self):
    """Implements extra steps required before test such as disk formating.

    Raises:
      TestError: An error occurred while running one of the steps.
    """
    pass

  def Run(self):
    """Runs the fio tests and emits log messages in OCP format.

    Raises:
      TestError: An error occurred while running one of the steps.
    """
    for dut in self._drives:
      logs = self._logs[dut.name]
      with self._run.scope(dut=dut.ocp_dut):
        device_name = '--filename=%s' % dut.name
        for scenario in self._scenarios:
          step = self._run.add_step(scenario)
          scenario_path = os.path.join(self._configs_path, scenario)
          args = _ARGS + [device_name, scenario_path]
          with step.scope():
            try:
              logs.append(json.loads(commonlib.cmdexec(args)))
              if logs[-1].get('jobs', [{'error': 1}])[0]['error']:
                raise IOError('fio run completed with error.')
            except IOError as exc:
              step.add_diagnosis(
                  tv.DiagnosisType.FAIL, verdict='%s failed' % scenario)
              nvme_logs = dut.LogCollect()
              nvme_logs.append(
                  self._save_fio_log(logs[-1], scenario, dut.logs_dir))
              self._add_logs_on_error(nvme_logs, step)
              raise diag.TestError("error occured in 'Run' step.") from exc

            step.add_diagnosis(
                tv.DiagnosisType.PASS,
                verdict=('%s passed' % scenario))

  def _save_fio_log(self, log_entry, scenario, log_dir):
    filename = os.path.join(log_dir, scenario + '_fio_error_log')
    with open(filename, 'w') as f:
      f.write(log_entry)
    return filename

  def _add_logs_on_error(self, logs, ocp_step):
    for log in logs:
      ocp_step.add_file(name=log, uri=('file://' + log))

  def PostDiag(self):
    """Checks if the diags meet the success criteria.

    Raises:
      TestError: An error occurred while running one of the steps.
    """
    if not self._benchmark_evaluator:
      return
    for dut, logs in self._logs.items():
      with self._run.scope(dut=self._ocp_duts[dut]):
        if not logs:
          continue
        # we only evaluate the first fio workload for perf targets on each dut
        results = self._benchmark_evaluator.evaluate(logs[0])
        step = self._run.add_step('Performance targets for %s' % dut)
        with step.scope():
          if results.failed_workloads:
            error_messages = []
            for failed_workload in results.failed_workloads:
              error_message = '%d: %s %s' % (
                  failed_workload.workload_id,
                  failed_workload.io_type,
                  ', '.join(failed_workload.failed_metrics))
              error_messages.append(error_message)
            step.add_diagnosis(
                tv.DiagnosisType.FAIL,
                verdict='Failed performance targets: %s' % '\n'.join(
                    error_messages))
          else:
            step.add_diagnosis(
                tv.DiagnosisType.PASS,
                verdict=('Performance test passed for %s' % dut))

  def Report(self):
    """Prints previously collected fio logs in JSON format.
    """
    for logs in self._logs.values():
      for log in logs:
        print(log)

  def tearDown(self):
    """Rolls back the changes made in setUp method to the original state.

    Raises:
      TestError: An error occurred while running one of the steps.
    """
    pass

if __name__ == '__main__':
  parser = argparser.create_parser()
  io_diag = BasicIODiag(parser.parse_args())
  try:
    io_diag.setUp()
    io_diag.PreDiag()
    io_diag.Run()
    io_diag.PostDiag()
    io_diag.Report()
    io_diag.tearDown()
  except diag.TestError as error_exc:
    print(error_exc)
