#!/bin/bash

export REPO="/localdata/ROP_499Y_Andi/llvm-project-automated"
export BUILD_DIR="/localdata/ROP_499Y_Andi/builds/"
export GIT_FLAG="--git-dir=$REPO/.git"
export BUILD_TARGET="-DLLVM_TARGETS_TO_BUILD=X86"
export BUILD_PROJECTS="-DLLVM_ENABLE_PROJECTS=clang"
export BUILD_TYPE="-DCMAKE_BUILD_TYPE=Release"
export MAKE_JOB_COUNT="20"
export VENV="/localdata/ROP_499Y_Andi/automated-env/bin/activate"
export TEST_DIR="/localdata/ROP_499Y_Andi/tests"
