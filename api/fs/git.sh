#!/bin/bash

# Imports
. ./fs/constants.sh
. ./fs/util.sh

###############################################################################
# All the git related commands and functions.                                 #
###############################################################################

# Top commit of the repo
LCOMMIT=""

# Find the latest commit current checkouted in the repo.
get_top_commit() {
  echo -n Finding current commit...

  LCOMMIT=$(git "$GIT_FLAG" rev-parse HEAD)
  exit_error $? "0" "Could not find top commit"

  echo "done ($LCOMMIT)"
}

# Verify that the given commit actually exists in the repo.
#
# 1: the commit to verify
verify_commit_exists() {
  echo -n Verifying commit $1 exists...

  git "$GIT_FLAG" cat-file -e $1^{commit} &> /dev/null
  exit_error $? "0" "Commit hash is not valid!\nPerhaps it is a run number?"

  echo done
}

# Checkout the desired commit in the repo
# 
# 1: the commit to checkout
checkout_commit() {
  cd $REPO
  get_top_commit
  verify_commit_exists "$1"

  echo -n "Verifying repository isn't already based at desired commit..."
  echo done

  echo -n "Unstaging any changes..."
  git fetch origin
  git reset --hard origin/main
  echo done

  cd $PWD
  git "$GIT_FLAG" checkout "$1" 
}
