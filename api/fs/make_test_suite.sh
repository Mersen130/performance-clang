#!/bin/bash

# Imports
. ./fs/constants.sh
. ./fs/util.sh

###############################################################################
# All the test suite related commands and functions.                          #
###############################################################################

# Start the virtual enviornment
start_venv() {
  source $VENV
}

# Deactive the virtual enviornment
end_venv() {
  deactivate
}

# Create the LNT server instance with the following name:
# {BUILD_DIR_NAME}_db
create_lnt_server_instance() {
  TEST_DIR="${BUILD_DIR}/test_db"
  if [ $VERBOSE -eq 1 ]
  then
    lnt create ${TEST_DIR}
  else 
    echo -n Creating db...
    lnt create ${TEST_DIR}
    echo done
  fi
}

run_test_suite() {
  if [ $VERBOSE -eq 1 ]
  then
    lnt runtest test-suite \
      --sandbox /tmp/automated \
      --use-cmake=/usr/bin/cmake \
      --use-lit=/localdata/ROP_CSC499Y/llvm-project-automated/llvm/utils/lit/lit.py \
      --test-suite /localdata/ROP_CSC499Y/llvm-test-suite \
      --cmake-cache Release \
      --cc ${BUILD_DIR}/bin/clang \
      --cxx ${BUILD_DIR}/bin/clang++ \
      --submit $TEST_DIR
  else
    echo -n Running tests...
    out=$(lnt runtest test-suite \
      --sandbox /tmp/automated \
      --use-cmake=/usr/bin/cmake \
      --use-lit=/localdata/ROP_CSC499Y/llvm-project-automated/llvm/utils/lit/lit.py \
      --test-suite /localdata/ROP_CSC499Y/llvm-test-suite \
      --cmake-cache Release \
      --cc ${BUILD_DIR}/bin/clang \
      --cxx ${BUILD_DIR}/bin/clang++ \
      --submit $TEST_DIR &>/dev/null) 
    echo done
  fi
}
