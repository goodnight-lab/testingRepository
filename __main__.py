from flask import Flask
from flask import request
from constants import *
import uuid
import json
import argparse
import os
import logging
from git_api import *


parser = argparse.ArgumentParser()
parser.add_argument('--host', default='localhost')
parser.add_argument('--port', type=int, default=8080)
parser.add_argument('--repositories')
parser.add_argument('--dest', default='./repositories')
parser.add_argument('--password')
parser.add_argument('--username')
args = parser.parse_args()


def check_exists(path, arg):
    if not os.path.exists(path):
        logging.warn("Wrong parameter '%s'" % arg)
        exit(1)
    return 0


def get_repository_name(url):
    return os.path.splitext(os.path.split(url)[-1])[0]


def init():
    logging.basicConfig(level=logging.INFO)
    check_exists(args.dest, 'dest')
    check_exists(args.repositories, 'repositories')
    
    repositories = []

    with open(args.repositories, "r") as src:
        for line in src:
            url, *branches = line.split()
            repositories.append({
                    'url': url,
                    'branches': branches,
                    'path': os.path.join(args.dest, get_repository_name(url)),
                    'name': get_repository_name(url)
                })
    
    cur_path = os.path.abspath(os.path.curdir)
    os.chdir(args.dest)
    for element in repositories:
        try:
            clone(url)
        except:
            pass
    os.chdir(cur_path)


def clean():
    cur_dir = os.path.abspath(os.path.curdir)
    os.chdir(args.dest)
    for root, dirs, files in os.walk('.', topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.chdir(cur_dir)


if __name__ == '__main__':
    init()
    clean()
