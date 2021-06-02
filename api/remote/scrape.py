
import requests
from bs4 import BeautifulSoup

from remote.constants import LNT_URL

def get_hash_from_run(run):
    page = requests.get(LNT_URL.format(run))
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find(id='run-table-Current')

    if not table:
        return 0

    git_hash = table.find_all('a')[1].contents[0]
    return git_hash
