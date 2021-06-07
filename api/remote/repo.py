
from remote.constants import REPO_DIR
import subprocess

class Repo:
    def checkout_commit(self, commit, verb, jobs):
        p = subprocess.call("./fs/main.sh {} {} {}".format(commit, verb, jobs), shell=True)

