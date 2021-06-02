
from remote.constants import REPO_DIR
import subprocess

class Repo:
    def checkout_commit(self, commit, verb):
        p = subprocess.call("./fs/main.sh {} {}".format(commit, verb), shell=True)

