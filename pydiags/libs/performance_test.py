# Copyright 2024 Google LLC
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import unittest

import performance


_TARGET_NUMBERS =  {
    "layers": [
        {
            "microbenchmarks": [
                {
                    "basename": "A1_2_1",
                    "workloads": [
                        {
                            "ioType": "randread",
                            "namespaceNum": 1,
                            "targets": {
                                "bwMbytesPerSec": "950",
                                "lat999thUsec": "7000"
                            },
                            "workloadNum": 1
                        },
                        {
                            "ioType": "randwrite",
                            "namespaceNum": 1,
                            "targets": {
                                "bwMbytesPerSec": "470",
                                "lat999thUsec": "15000",
                                "lat99thUsec": "5000"
                            },
                            "workloadNum": 2
                        },
                        {
                            "ioType": "randtrim",
                            "namespaceNum": 1,
                            "targets": {
                                "bwMbytesPerSec": "50"
                            },
                            "workloadNum": 3
                        }
                    ]
                }
            ]
        }
    ]
}

_UNREACHABLE_TARGET_NUMBERS =  {
    "layers": [
        {
            "microbenchmarks": [
                {
                    "basename": "A1_2_1",
                    "workloads": [
                        {
                            "ioType": "randwrite",
                            "namespaceNum": 1,
                            "targets": {
                                "bwMbytesPerSec": "4700",
                                "lat999thUsec": "150",
                                "lat99thUsec": "50"
                            },
                            "workloadNum": 1
                        },
                        {
                            "ioType": "randread",
                            "namespaceNum": 1,
                            "targets": {
                                "bwMbytesPerSec": "4700",
                                "lat999thUsec": "150",
                                "lat99thUsec": "50"
                            },
                            "workloadNum": 1
                        },
                        {
                            "ioType": "randtrim",
                            "namespaceNum": 1,
                            "targets": {
                                "bwMbytesPerSec": "4700",
                                "lat999thUsec": "150",
                                "lat99thUsec": "50"
                            },
                            "workloadNum": 1
                        },
                    ]
                }
            ]
        }
    ]
}

# some fields are intentionally stripped
_FIO_JSON_OUTPUT = {
    'jobs': [{
           'job options': {'bs': '8k',
                           'bwavgtime': '5000',
                           'continue_on_error': 'io',
                           'direct': '1',
                           'do_verify': '0',
                           'end_fsync': '0',
                           'experimental_verify': '1',
                           'fsync': '0',
                           'group_reporting': '0',
                           'iodepth': '1024',
                           'ioengine': 'libaio',
                           'numjobs': '1',
                           'randrepeat': '0',
                           'rw': 'write',
                           'sync': '0',
                           'thread': '1',
                           'verify': 'meta',
                           'verify_pattern': '0x5a5a5a5a'},
           'jobname': 'basic_io_logical_writes-seq_wr',
           'write': {'bw': 3184604,
                     'bw_agg': 100.0,
                     'bw_bytes': 3261035227,
                     'bw_dev': 9930.933533,
                     'bw_max': 3201289,
                     'bw_mean': 3185035.66383,
                     'bw_min': 3103697,
                     'bw_samples': 235,
                     'clat_ns': {'N': 468842283,
                                 'max': 7906934,
                                 'mean': 2570223.881463,
                                 'min': 1501121,
                                 'percentile': {'1.000000': 2375680,
                                                '10.000000': 2408448,
                                                '20.000000': 2441216,
                                                '30.000000': 2473984,
                                                '40.000000': 2506752,
                                                '5.000000': 2408448,
                                                '50.000000': 2506752,
                                                '60.000000': 2539520,
                                                '70.000000': 2572288,
                                                '80.000000': 2637824,
                                                '90.000000': 2736128,
                                                '95.000000': 2801664,
                                                '99.000000': 3653632,
                                                '99.500000': 4227072,
                                                '99.900000': 6520832,
                                                '99.950000': 6782976,
                                                '99.990000': 7110656},
                                 'stddev': 262241.67668},
                     },
           'read': {'bw': 3184604,
                     'bw_agg': 100.0,
                     'bw_bytes': 3261035227,
                     'bw_dev': 9930.933533,
                     'bw_max': 3201289,
                     'bw_mean': 3185035.66383,
                     'bw_min': 3103697,
                     'bw_samples': 235,
                     'clat_ns': {'N': 468842283,
                                 'max': 7906934,
                                 'mean': 2570223.881463,
                                 'min': 1501121,
                                 'percentile': {'1.000000': 2375680,
                                                '10.000000': 2408448,
                                                '20.000000': 2441216,
                                                '30.000000': 2473984,
                                                '40.000000': 2506752,
                                                '5.000000': 2408448,
                                                '50.000000': 2506752,
                                                '60.000000': 2539520,
                                                '70.000000': 2572288,
                                                '80.000000': 2637824,
                                                '90.000000': 2736128,
                                                '95.000000': 2801664,
                                                '99.000000': 3653632,
                                                '99.500000': 4227072,
                                                '99.900000': 6520832,
                                                '99.950000': 6782976,
                                                '99.990000': 7110656},
                                 'stddev': 262241.67668},
                     },
           'trim': {'bw': 3184604,
                     'bw_agg': 100.0,
                     'bw_bytes': 3261035227,
                     'bw_dev': 9930.933533,
                     'bw_max': 3201289,
                     'bw_mean': 3185035.66383,
                     'bw_min': 3103697,
                     'bw_samples': 235,
                     'clat_ns': {'N': 468842283,
                                 'max': 7906934,
                                 'mean': 2570223.881463,
                                 'min': 1501121,
                                 'percentile': {'1.000000': 2375680,
                                                '10.000000': 2408448,
                                                '20.000000': 2441216,
                                                '30.000000': 2473984,
                                                '40.000000': 2506752,
                                                '5.000000': 2408448,
                                                '50.000000': 2506752,
                                                '60.000000': 2539520,
                                                '70.000000': 2572288,
                                                '80.000000': 2637824,
                                                '90.000000': 2736128,
                                                '95.000000': 2801664,
                                                '99.000000': 3653632,
                                                '99.500000': 4227072,
                                                '99.900000': 6520832,
                                                '99.950000': 6782976,
                                                '99.990000': 7110656},
                                 'stddev': 262241.67668},
                     },
}]}



class WorkloadTest(unittest.TestCase):

  def test_Workload_object_successfully_built(self):
    benchmark_descriptor = _TARGET_NUMBERS["layers"][0]["microbenchmarks"][0]
    workload_descriptor = benchmark_descriptor["workloads"][0]
    workload = performance.Workload(workload_descriptor)

  def test_Workload_evaluate_reachable_perf_targets(self):
    workload_descriptor = _TARGET_NUMBERS["layers"][0]["microbenchmarks"][0]
    workload = performance.Workload(workload_descriptor["workloads"][1])
    self.assertIsNone(workload.evaluate(_FIO_JSON_OUTPUT))

  def test_Workload_evaluate_unreachable_perf_targets(self):
    workload_descriptor = _UNREACHABLE_TARGET_NUMBERS["layers"][0]["microbenchmarks"][0]
    workload = performance.Workload(workload_descriptor["workloads"][0])
    failed_metrics = ['bwMbytesPerSec', 'lat999thUsec', 'lat99thUsec']
    result = workload.evaluate(_FIO_JSON_OUTPUT)
    self.assertIsNotNone(result)
    self.assertEqual(sorted(failed_metrics), sorted(result.failed_metrics))

class BenchmarkTest(unittest.TestCase):

  def test_benchmark_evaluate_multiple_reachable_perf_targets(self):
    benchmark_descriptor = _TARGET_NUMBERS["layers"][0]["microbenchmarks"][0]
    benchmark = performance.Benchmark(benchmark_descriptor)
    result = benchmark.evaluate(_FIO_JSON_OUTPUT)
    self.assertEqual(len(result.failed_workloads), 0)

  def test_benchmark_evaluate_multiple_unreachable_perf_targets(self):
    benchmark_descriptor = _UNREACHABLE_TARGET_NUMBERS["layers"][0]["microbenchmarks"][0]
    benchmark = performance.Benchmark(benchmark_descriptor)
    result = benchmark.evaluate(_FIO_JSON_OUTPUT)
    failed_metrics = ['bwMbytesPerSec', 'lat999thUsec', 'lat99thUsec']
    self.assertEqual(len(result.failed_workloads), 3)
    for failed_workload in result.failed_workloads:
      self.assertEqual(sorted(failed_metrics), sorted(failed_workload.failed_metrics))

if __name__ == '__main__':
  unittest.main()
