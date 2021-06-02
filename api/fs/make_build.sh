#!/bin/bash

# Imports
. ./fs/constants.sh
. ./fs/util.sh

###############################################################################
# All the build related commands and functions.                               #
###############################################################################

# GLOBAL
BUILD=""

# Create a new build folder with a timestamp and the first 6 digits of the
# desired git hash.
#
# Time stamps are stored in YYYY-mm-DD_HH-MM-SS.
# Full folder name is TIMESTAMP_HASH.
#
# 1: the git hash
make_new_build_dir() {
  date_str=$(date +"%Y-%m-%d_%H-%M-%S")
  BUILD="${BUILD_DIR}/${date_str}_${1:0:6}"
  echo -n Making build directory $BUILD...
  [ -d $BUILD ] && {
    echo error
    exit_error 1 1 "Build dir already exists with this name"
  }
  mkdir $BUILD
  echo done

  echo -n Changing permission...
  chmod 777 -R "$BUILD"
  echo done
}

# Run the cmake configuration for the new build
config_cmake() {
  cd ${BUILD}

  if [ $VERBOSE -eq 0 ]
  then
    cmake "$REPO/llvm"
    cmake "${BUILD_FLAGS}"
  else
    echo -n Configuring cmake...
    out=$(cmake "$REPO/llvm" &>/dev/null)
    out=$(cmake "${BUILD_FLAGS}" &>/dev/null)
    echo done
  fi
}
