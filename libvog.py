from datetime import datetime
import os
import sys
import re
import argparse
import collections
import configparser
import grp
import pwd
from fnmatch import fnmatch
import hashlib
from math import ceil
import zlib


argparser = argparse.ArgumentParser(description="VCS VOYAGER")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

# handle the argument commands and direct them to the specific methods


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        # case "add": cmd_add(args)
        # case "cat-file": cmd_cat_file(args)
        # case "check-ignore": cmd_check_ignore(args)
        # case "checkout": cmd_checkout(args)
        # case "commit": cmd_commit(args)
        # case "hash-object": cmd_hash_object(args)
        case "init": cmd_init(args)
        # case "log": cmd_log(args)
        # case "ls-files": cmd_ls_files(args)
        # case "ls-tree": cmd_ls_tree(args)
        # case "merge": cmd_merge(args)
        # case "rebase": cmd_rebase(args)
        # case "rev-parse": cmd_rev_parse(args)
        # case "rm": cmd_rm(args)
        # case "show-ref": cmd_show_ref(args)
        # case "status": cmd_status(args)
        # case "tag": cmd_tag(args)
        # case _: print("Bad command.")


# an object to represent a git repository
class GitRepo(object):
    """A git repository"""

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception("Not a Git repository %s" % path)

        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(
                    "Unsupported repositoryformatversion %s" % vers)


def repo_path(repo, *path):
    return os.path.join(repo.gitdir, *path)


# ensure directory for the file exists and return path for file
def repo_file(repo, *path, mkdir=False):
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)


# give path and mkdir if not already there
def repo_dir(repo, *path, mkdir=False):
    path = repo_path(repo, *path)

    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception("Not a directory %s" % path)

    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None


def repo_create(path):
    repo = GitRepo(path, True)  # only create an object doesn't create a dir

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception("%s is not a directory!" % path)
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception("%s is not empty!" % path)

    else:
        os.makedirs(repo.worktree)  # create the dir

# create the necessary child directories
    assert repo_dir(repo, "branches", mkdir=True)
    assert repo_dir(repo, "objects", mkdir=True)
    assert repo_dir(repo, "refs", "tags", mkdir=True)
    assert repo_dir(repo, "refs", "heads", mkdir=True)


# create the files in folder
    with open(repo_file(repo, "description"), "w") as f:
        f.write(
            "Unnamed repository; edit this file 'description' to name the repository.\n")

    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(repo_file(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)

    return repo


def repo_default_config():
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core", "bare", "false")

    return ret


argsp = argsubparsers.add_parser(
    "init", help="Initialize a new, empty repository.")
argsp.add_argument("path",
                   metavar="directory",
                   nargs="?",
                   default=".",
                   help="Where to create the repository.")


def cmd_init(args):
    repo_create(args.path)


def repo_find(path=".", required=True):
    path = os.path.realpath(path)

    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepo(path)

    # If we haven't returned, recurse in parent, if w
    parent = os.path.realpath(os.path.join(path, ".."))

    if parent == path:
        # Bottom case
        # os.path.join("/", "..") == "/":
        # If parent==path, then path is root.
        if required:
            raise Exception("No git directory.")
        else:
            return None

    # Recursive case
    return repo_find(parent, required)
