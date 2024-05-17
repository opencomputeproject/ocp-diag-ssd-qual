# ocp-diag-ssd-qualStorage diagnostic

fio is a Linux utility that evaluates storage performance. This repo contains
Python scripts that turn fio into an OCP-compliant diagnostic.

Usage:
To run the diag do the following:
1. Install fio on your hardware.
2. Install all the dependencies specified in requirements.txt.
3. Run the diag with fio config files describing your test scenario.

For Debian-based operating systems the procedure above may look as follows:
1. apt install fio nvme-cli
2. git clone https://github.com/opencomputeproject/ocp-diag-ssd-qual.git
3. cd ocp-diag-ssd-qual/
4. python3 -m venv .
5. source bin/activate
6. pip install -r requirements.txt

Running the tests:
Basic IO test:
This test consists of four steps:
1. Sequential write entire device with 8KiB blocksize, 1024 queue depth, with known data pattern
2. Sequential read verify entire device with 8KiB blocksize, 1024 queue depth
3. Sequential read verify entire device with 4KiB blocksize, 1024 queue depth
4. Random read verify with 4KiB blocksize for 4 minutes, 1024 queue depth
python3 -m pydiags.diags.basic_io.basic_io_diag  --dut=/path/to/your/device --playbook=pydiags/configs/basic_io.json

IOPS test:
This test consists of two sequential (run one after another) steps:
1. Random read with 4KiB blocksize for 2 minutes, 256 queue depth
python3 -m pydiags.diags.basic_io.basic_io_diag  --dut=/path/to/your/device --playbook=pydiags/configs/iops_rd.json
2. Random write with 4KiB blocksize for 2 minutes, 256 queue depth
python3 -m pydiags.diags.basic_io.basic_io_diag  --dut=/path/to/your/device --playbook=pydiags/configs/iops_wr.json

Bandwidth test:
This test consists of two sequince steps:
1. Sequential read with 128KiB blocksize, 256 queue depth
python3 -m pydiags.diags.basic_io.basic_io_diag  --dut=/path/to/your/device --playbook=pydiags/configs/bandwidth_rd.json
2. Sequential write with 128KiB blocksize, 256 queue depth
python3 -m pydiags.diags.basic_io.basic_io_diag  --dut=/path/to/your/device --playbook=pydiags/configs/bandwidth_wr.json

Mixed workload test:
Prerequisites: user preconditions a device before running the test. Typical
scenario is to use the prepopulated device with 25%/50/75% fullness. Depending
on this the device's performance characteristics may vary. A user has to specify
the expected performance targets for p95, p99, p999 and bandwidth numbers.
1. Random write and read with 8Kib blocksize, 1024 queue depth
python3 -m pydiags.diags.basic_io.basic_io_diag  --dut=/path/to/your/device --playbook=pydiags/configs/mixed_workload_rdwr.json


Config files.
Config file contains scenarios described in JSON format. It has required field
"test_steps" that sets the sequince of test steps. Every step is a separate fio
config file. So that you can create your own test scenarios with arbitrary
complexity. There's an optional field "benchmark_targets" that specifies which
file to use to evaluate performance characteristics of the device under test.
For test targets you can specify the test name and the workloads. Each workload
can have different targets for different workload types - read, write, trim.
To evaluate bandwidth we should use "bwMbytesPerSec" field. For latencies we
have several options that can be used simultaneously - lat50thUsec,
lat95thUsec, lat99thUsec, lat999thUsec, lat9999thUsec, latMaxUsec, latMeanUsec.
See examples in configs folder.
