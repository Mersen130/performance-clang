#!/bin/bash

# Imports
. ./fs/constants.sh
. ./fs/util.sh
. ./fs/git.sh
. ./fs/make_build.sh
. ./fs/make_test_suite.sh

# We don't use getopts because this should never be called directly!

# Globals
HASH=$1
VERBOSE=$2
JOBS=$3

checkout_commit "$HASH"
make_new_build_dir "$HASH"
config_cmake
run_make
start_venv
create_lnt_server_instance
run_test_suite
end_venv
