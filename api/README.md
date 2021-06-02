# API 

## Overview
These scripts locate a git hash from the LNT site by a run number (or if a
git hash is supplied, this is skipped) and reverts the llvm repo to this
desired commit.

Then, a build folder is generated with a cmake configuration to be compiled.
Once compiled, this does nothing. Soon, it will run the testing suite.

## Usage
First navigate to the api directory
```shell
$ cd api
```

Source the virtualenv
```shell
$ source env/bin/activate
```

Run the main script with the following usage (only supply either -r or -g)
```shell
$ python3 main.py -r RUN_NUM -g GIT_HASH [-v|--verbose]
```
where `-v` or `--verbose` provides verbose output and `-h` displays the above help message.

A build directory will be created in /localdata/ROP\_CSC499/builds with the
following name: `YYYY-mm-dd\_HH-MM-SS\_{first 6 digits of the git hash}`

# Warning
This script modifies the localdata/llvm repo, that is, if you supply a run num
or a git hash to the main python script, it will checkout said commit in the
llvm project, so be sure not to run this whilst others are compiling or using 
the repo.

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
