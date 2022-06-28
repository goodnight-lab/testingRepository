import logging
import uuid
import os

def pull():
    logging.info("pulling..")
    pid = os.fork()
    if pid == 0:
        os.execlp('git', 'git pull', 'pull')
    code = os.wait()
    logging.info("Return code of pulling: %d" % code[0])
    return 0


def add_remote(name, remote_rep):
    logging.info("adding remote..")
    pid = os.fork()
    if pid == 0:
        os.execlp('git', 'git adding remote', 'remote', 'add', name, remote_rep)
    code = os.wait()
    logging.info("Return code of adding remote: %d" % code[0])
    return name


def remove_remote(remote_rep):
    logging.info("removing remote..")
    pid = os.fork()
    if pid == 0:
        os.execlp('git', 'git adding remote', 'remote', 'remove', remote_rep)
    code = os.wait()
    logging.info("Return code of removing remote: %d" % code[0])
    return 0


def set_config(name, email):
    logging.info("setting config..")
    pid = os.fork()
    if pid == 0:
        os.execlp('git', 'git configuring', 'config', '--local', 'user.name', name)
    code = os.wait()
    logging.info("Return code of configuring: %d" % code[0])
    pid = os.fork()
    if pid == 0:
        os.execlp('git', 'git configuring', 'config', '--local', 'user.email', email)
    code = os.wait()
    logging.info("Return code of configuring: %d" % code[0])
    return


def merge(remote_rep, branch, msg):
    logging.info("merging..")
    pid = os.fork()
    if pid == 0:
        os.execlp('git', 'git merge', 'merge',
         '--allow-unrelated-histories', remote_rep + '/' + branch,
         '--no-commit', '--overwrite-ignore')
    code = os.wait()
    logging.info("Return code of merging: %d" % code[0])
    return 0


def commit(msg):
    logging.info("commiting..")
    pid = os.fork()
    if pid == 0:
        os.execlp('git', 'git merge', 'commit', '-am', msg)
    code = os.wait()
    logging.info("Return code of commiting: %d" % code[0])
    return 0


def fetch(remote_rep):
    logging.info("fetching..")
    pid = os.fork()
    if pid == 0:
        os.execlp('git', 'git fetching', 'fetch', remote_rep, '--tags')
    code = os.wait()
    logging.info("Return code of fetching: %d" % code[0])
    return 0


def clone(remote_rep):
    logging.info("cloning..")
    pid = os.fork()
    if pid == 0:
        os.execlp('git', 'git cloning', 'clone', remote_rep)
    code = os.wait()
    logging.info("\tReturn code of cloning %d" % code[0])
    return 0


def push(remote_rep, branch):
    logging.info("pushing..")
    pid = os.fork()
    if pid == 0:
        os.execlp('git', 'git cloning', 'push', '-u', remote_rep, branch)
    code = os.wait()
    logging.info("\tReturn code of pushing %d" % code[0])
    return 0


def add_all():
    pid = os.fork()
    if pid == 0:
        os.execlp('git', 'git cloning', 'add', '.')
    code = os.wait()
    return 0