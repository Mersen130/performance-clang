#!/bin/bash

# Imports
. ./fs/constants.sh
. ./fs/util.sh
. ./fs/git.sh
. ./fs/make_build.sh

# We don't use getopts because this should never be called directly!

# Globals
HASH=$1
VERBOSE=$2

checkout_commit "$HASH"
make_new_build_dir "$HASH"
config_cmake

