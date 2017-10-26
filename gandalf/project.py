# coding=utf-8
import os
import subprocess

from pygit2 import Repository, GIT_CHECKOUT_FORCE, clone_repository, UserPass, RemoteCallbacks
from gandalf.config import GITHUB_URL, WORK_DIR, FLAKE8_EXECUTABLE, USERNAME, PASSWORD


def update_remote(work_tree, repo, repo_name, remote_name, callbacks):
    remote = next((r for r in repo.remotes if r.name == remote_name), None)
    if remote is None:
        url = '{0}{1}.git'.format(GITHUB_URL, repo_name)
        remote = repo.create_remote(remote_name, url)
    remote.fetch(callbacks=callbacks)


def sync_handler(fork_from: str, from_sha: str, repo_name: str,
                 ticket_id: int, pr_url: str):
    output_path = '{}.txt'.format(pr_url.split('/', 3)[3].rsplit('/', 2)[0])
    output_path = os.path.join(WORK_DIR, output_path.replace('/', '_'))
    work_tree = os.path.join(WORK_DIR, fork_from)
    parent_path = os.path.dirname(work_tree)
    credentials = UserPass(USERNAME, PASSWORD)
    callbacks = pygit2.RemoteCallbacks(credentials=credentials)
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    if not os.path.exists(work_tree):
        repo = clone_repository(
            '{0}{1}.git'.format(GITHUB_URL, fork_from), work_tree, callbacks=callables)
    else:
        repo = Repository(work_tree)

    remote_name = repo_name.split('/')[0]
    update_remote(work_tree, repo, repo_name, remote_name, callbacks=callbacks)

    if remote_name == 'origin':
        commit = repo.revparse_single(from_sha)
        repo.checkout_tree(commit, strategy=GIT_CHECKOUT_FORCE)
    else:
        ref_name = 'refs/pull/{0}/head'.format(ticket_id)
        try:
            repo.create_reference(ref_name, from_sha)
        except ValueError:
            pass
        ref = repo.lookup_reference(ref_name)
        repo.checkout(ref, strategy=GIT_CHECKOUT_FORCE)
    cwd = os.getcwd()
    os.chdir(work_tree)
    subprocess.call(
        '{} . --output-file={}'.format(FLAKE8_EXECUTABLE, output_path),
        shell=True)
    os.chdir(cwd)
    return output_path
