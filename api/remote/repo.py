
from constants import REPO_DIR
import subprocess

class Repo:
    def checkout_commit(self, commit):
        p = subprocess.call("../fs/main.sh {}".format(commit), shell=True)

