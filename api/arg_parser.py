
import sys, getopt

class ArgParser:
    def __init__(self, argv):
        try:
            self._opts, self._args = getopt.getopt(argv, 'hr:g:', ['run=','githash='])
        except getopt.GetoptError:
            print('main.py -r <run_num> -g <git_hash>')
            sys.exit(2)

        self.run_num = ''
        self.git_hash = ''

    def parse_args(self):
        for opt, arg in self._opts:
            if opt == '-h':
                print('main.py -r <run_num> -g <git_hash>')
                sys.exit()
            elif opt in ('-r', '--run'):
                self.run_num = arg
            elif opt in ('-g', '--githash'):
                self.git_hash = arg
