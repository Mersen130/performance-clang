
import sys

from remote.arg_parser import ArgParser
from remote.repo import Repo
from remote.scrape import get_hash_from_run

if __name__ == '__main__':
    ap = ArgParser(sys.argv[1:])
    ap.parse_args()

    r = Repo()
    if ap.stdin:
        for line in sys.stdin:
            if len(line) == 0:
                pass
            for hash in line.split(','):
                r.checkout_commit(hash.strip(), ap.verbose, ap.jobs)
    elif ap.is_run_num:
        sys.stdout.write('Finding git hash for run {}...'.format(ap.run_num))
        sys.stdout.flush()
        git_hash = get_hash_from_run(ap.run_num)

        if git_hash == 0:
            print('not found\nPerhaps you specified a nonexistent run number?')
            print('Aborting..')
            sys.exit(1)

        print('found ({})'.format(git_hash))
        r.checkout_commit(git_hash, ap.verbose, ap.jobs)
    elif ap.is_git_hash:
        for hash in ap.git_hashes:
            sys.stdout.write('Verifying {} builds...'.format(hash))
            sys.stdout.flush()

            print('done (TODO actually scrape and check this...)')
            r.checkout_commit(hash, ap.verbose, ap.jobs)

    sys.exit(0)
