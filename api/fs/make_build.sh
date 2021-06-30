#!/bin/bash

# Imports
. ./fs/constants.sh
. ./fs/util.sh

###############################################################################
# All the build related commands and functions.                               #
###############################################################################

# Create a new build folder with a timestamp and the first 6 digits of the
# desired git hash.
#
# Time stamps are stored in YYYY-mm-DD_HH-MM-SS.
# Full folder name is TIMESTAMP_HASH.
#
# 1: the git hash
make_new_build_dir() {
  date_str=$(date +"%Y-%m-%d_%H-%M-%S")
  BUILD_DIR="${BUILD_DIR}/${date_str}_${1:0:6}"
  echo -n Making build directory $BUILD_DIR...
  [ -d $BUILD_DIR ] && {
    echo error
    exit_error 1 1 "Build dir already exists with this name"
  }
  mkdir $BUILD_DIR
  echo done

  echo -n Changing permission...
  chmod 777 -R "$BUILD_DIR"
  echo done
}

# Run the cmake configuration for the new build
config_cmake() {
  cd ${BUILD_DIR}

  if [ $VERBOSE -eq 1 ]
  then
    cmake "$REPO/llvm"
    cmake "$BUILD_TARGET" "$BUILD_PROJECTS" "$BUILD_TYPE" .
  else
    echo -n Configuring cmake...
    out=$(cmake "$REPO/llvm" &>/dev/null)
    out=$(cmake "$BUILD_TARGET" "$BUILD_PROJECTS" "$BUILD_TYPE" . &>/dev/null)
    echo done
  fi
}

# Run make with desired jobs
run_make() {
  cd ${BUILD_DIR}
  if [ $VERBOSE -eq 1 ]
  then
    make -j ${MAKE_JOB_COUNT}
  else
    echo -n Running make...
    echo done
  fi
}
