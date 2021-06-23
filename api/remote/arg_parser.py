
import sys, getopt

HELP_MSG = '''
usage: python3 main.py [OPTS] where opts are:

  -h)                    : Display this help message.
  -r|--run) RUN_NUM      : The LNT run number to covnert into a git hash.
                           If supplied, options --githash is ignored.
                           If --stdin is used, this option has no effect.
  -g|--githash) GIT_HASH : The git hash to compile and run the testing suite on.
                           If supplied with --run or --stdin, this will option
                           will have no effect.
  -j|--jobs) JOBS        : The number of jobs to pass to make (default: 20).
  -v|--verbose)          : Whether to display verbose output or not (default: OFF).
  -s|--stdin)            : Whether to read from stdin. If this option is used, 
                           data must be redirected via stdin to have any effect.
                           If supplied, --run and --githash options are ignored.
'''

class ArgParser:
    def __init__(self, argv):
        try:
            self._opts, self._args = getopt.getopt(argv, 'hsr:g:vj:c:',
                    ['run=','githash=','jobs=','githashes=','stdin'])
        except getopt.GetoptError:
            print(HELP_MSG)
            sys.exit(2)

        self.stdin = False
        self.is_run_num = False
        self.run_num = ''
        self.is_git_hash = False
        self.git_hashes = []
        self.verbose = 0
        self.jobs = 20

    def parse_args(self):
        for opt, arg in self._opts:
            if opt == '-h':
                print(HELP_MSG)
                sys.exit()
            elif opt in ('-s', '--stdin'):
                self.stdin = True
            elif opt in ('-r', '--run'):
                self.is_run_num = True
                self.run_num = arg
            elif opt in ('-g', '--githash'):
                self.is_git_hash = True
                self.git_hashes = arg.split(',')
            elif opt in ('-v', '--verbose'):
                self.verbose = 1
            elif opt in ('-j', '--jobs'):
                self.jobs = arg
