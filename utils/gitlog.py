import subprocess
import os
import json
import datetime
from dateutil import parser


def get_latest_commit_time(path):
    os.chdir(path)
    # Run the git log command to get the latest commit information
    log_output = subprocess.check_output(['git', 'log', '-n', '1',
                                          '--pretty=format:{%n  "commit": "%H",%n  "author": {%n    "name": "%aN",%n    "email": "%aE",%n    "date": "%aI"%n  },%n  "committer": {%n    "name": "%cN",%n    "email": "%cE",%n    "date": "%cI"%n  },%n  "message": "%f"%n}'])

    # Parse the output as a JSON object
    commit_info = json.loads(log_output)

    time = commit_info["author"]["date"]
    commit_date = parser.parse(time).date()
    return commit_date
