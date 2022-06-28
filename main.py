from flask import Flask, request, jsonify
import argparse
import logging
import json
import os
import uuid
from constants import *


"""
    - how to merge 2 different branches from 2 different repos
        https://stackoverflow.com/questions/1425892/how-do-you-merge-two-git-repositories
    - to change a commited user you should change local config
        git config --local user.name <yourname>
        git config --local user.email <youremail>

    Webhook headers:
        X-GitHub-Event
"""


parser = argparse.ArgumentParser()
parser.add_argument("--branch")
parser.add_argument("--reps", nargs='*')
parser.add_argument("--host")
parser.add_argument("--port", type=int)
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
general_branch = args.branch
reps = args.reps
logging.info("Tracing branch %s" % general_branch)

from git_api import *


"""
    Forking an repositories
"""
def get_repName(repository):
    return os.path.splitext(os.path.split(repository)[-1])[0]

repsNames = []
for rep in reps:
    repsNames.append(get_repName(rep))
    clone(rep)
print(repsNames)


BLOCK = 0
    

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_push_event():
    global BLOCK
    committername, committeremail = None, None
    payload = json.loads(request.form.to_dict()['payload'])

    logging.info("Got request..")
    if request.headers['X-GitHub-Event'] == 'push' and BLOCK == 0:
        logging.info("Event-type: push")
            
        if not payload['ref'].endswith(general_branch):
            logging.info("Another branch")
        logging.info("Got push on branch %s" % general_branch)

        committername = payload['commits'][0]['committer']['name']
        committeremail = payload['commits'][0]['committer']['email']
        
        logging.info("Commiter:\n\tname: %s\n\temail: %s" % (committername, committeremail))
        rep_name = payload['repository']['name']
        full_rep_name = payload['repository']['url']

        for rep in repsNames:
            print([rep, rep_name])
            if rep != rep_name:
                logging.info("Updating %s", rep)
                if not os.path.exists(os.path.join('.', rep)):
                    logging.warn("dir not exists!")
                    clone(full_rep_name)
                os.chdir(rep)
                try:
                    rem = add_remote(rep_name, full_rep_name)
                    set_config(committername, committeremail)
                    add_all()
                    commit('commit')
                    pull()
                    fetch(rem)
                    merge(rem, general_branch, payload['commits'][0]['message'])
                    BLOCK += 1
                    push('origin', general_branch)
                    remove_remote(rem)
                except:
                    pass
                os.chdir('..')
    BLOCK -= 1

    return "success"


app.run(port=args.port, host=args.host)

