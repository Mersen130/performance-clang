# API 

## Overview
These scripts locate a git hash from the LNT site by a run number (or if a
git hash is supplied, this is skipped) and reverts the llvm repo to this
desired commit.

Our changes are then rebased on top of the commit and our testing suite is then
run with the output logged.

The purpose of this is to streamline local testing of one or more commits once
we have hand picked (or computer picked) specific commits.

## TODO
[ ] Execute compile scripts once commit is rebased
[ ] Execute testing suite once new bin is ready
[ ] Parse and format testing suite output

## Future
[ ] Find a way to nicely catergorize testing suite output

[ ] Add ability to build multiple commits at once 
    [ ] Isolate non-llvm p/tids
    [ ] Taskset script should do this trivially

[ ] ccache for recompiling
