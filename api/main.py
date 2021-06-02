
import sys
from arg_parser import ArgParser
from repo import Repo
import scrape

if __name__ == '__main__':
    ap = ArgParser(sys.argv[1:])
    ap.parse_args()

    r = Repo()
    if ap.run_num:
        sys.stdout.write('Finding git hash for run {}...'.format(ap.run_num))
        sys.stdout.flush()
        git_hash = scrape.get_hash_from_run(ap.run_num)

        if git_hash == 0:
            print('not found\nPerhaps you specified a nonexistent run number?')
            print('Aborting..')
            sys.exit(1)

        print('found ({})'.format(git_hash))
        r.checkout_commit(git_hash)
    elif ap.git_hash:
        print('Checking out {}'.format(ap.git_hash))
        r.checkout_commit(ap.git_hash)

    sys.exit(0)
