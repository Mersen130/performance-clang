
import sys, getopt

class ArgParser:
    def __init__(self, argv):
        try:
            self._opts, self._args = getopt.getopt(argv, 'hr:g:vj:', ['run=','githash=','jobs='])
        except getopt.GetoptError:
            print('main.py -r RUN_NUM -g GIT_HASH -j JOBS [-v|--verbose]')
            sys.exit(2)

        self.run_num = ''
        self.git_hash = ''
        self.verbose = 0
        self.jobs = 20

    def parse_args(self):
        for opt, arg in self._opts:
            if opt == '-h':
                print('main.py -r RUN_NUM -g GIT_HASH -j JOBS [-v|--verbose]')
                sys.exit()
            elif opt in ('-r', '--run'):
                self.run_num = arg
            elif opt in ('-g', '--githash'):
                self.git_hash = arg
            elif opt in ('-v', '--verbose'):
                self.verbose = 1
            elif opt in ('-j', '--jobs'):
                self.jobs = arg
