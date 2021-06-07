#!/bin/bash

export REPO="/localdata/ROP_CSC499Y/llvm-project"
export BUILD_DIR="/localdata/ROP_CSC499Y/builds"
export GIT_FLAG="--git-dir=$REPO/.git"
export BUILD_FLAGS="-DLLVM_TARGETS_TO_BUILD=\"X86\""
export MAKE_JOB_COUNT="20"
