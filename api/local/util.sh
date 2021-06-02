#!/bin/bash

# Verify that two variables hold the same value, and exit with the desired error
# message if not.
# 
# [1]: the first variable to check
# [2]: the variable to compare too
# [3]: the error message
#
# This function exits!
exit_error() {
  [ "$1" == "$2" ] || {
    echo Error
    echo -e "$3"
    echo Aborting...
    exit 1
  }
}

# Verify that two variables hold the same value, and exit with the desired error
# message if they do.
# 
# [1]: the first variable to check
# [2]: the variable to compare too
# [3]: the error message
#
# This function exits!
exit_error_not() {
  [ ! "$1" == "$2" ] || {
    echo Error
    echo -e "$3"
    exit 1
  }
}

