#!/bin/bash

cd /usr/sasl/diags/
python3 -m pydiags.diags.basic_io.basic_io_diag "$@"
