import json
import os
import re
from datetime import datetime, timezone

from actions_toolkit import core
from github import Github
from github.PaginatedList import PaginatedList
from github.Repository import Repository


def search_repos(args):
    g = Github(args['token'])
    repos = g.get_organization(args['org']).get_repos()
    matched = []
    remaining = repos.totalCount
    page_num = 0
    while remaining > 0:
        # get next page
        page_results: PaginatedList[Repository] = repos.get_page(page_num)
        # check each repo in page
        for repo in page_results:
            repo: Repository = repo
            # filtering
            filters = []
            # name filtering
            filters.append(re.match(args['pattern'], repo.name))
            # date filtering
            filters.append(args['created_after'] <=
                           repo.created_at.replace(tzinfo=timezone.utc) <= args['created_before'])
            if (all(filters)):
                matched.append(repo.full_name)
        # update indeces
        remaining -= len(page_results)
        page_num += 1
    if len(matched) < 1:
        raise Exception(f'No repositories found.\nargs = {args}')
    return matched


def parse_env():
    inputs = ['org', 'token', 'pattern', 'created_after', 'created_before']
    args = {}
    for input in inputs:
        args[input] = core.get_input(input, trim_whitespace=False)
    args['created_after'] = datetime.fromisoformat(
        args['created_after'])
    args['created_before'] = datetime.fromisoformat(
        args['created_before'])
    if args['created_after'] >= args['created_before']:
        raise Exception('created_after must come before created_before.')
    return args


def set_default_env():
    os.environ.setdefault('INPUT_CREATED_AFTER', datetime.min.replace(
        tzinfo=timezone.utc).isoformat())
    os.environ.setdefault('INPUT_CREATED_BEFORE', datetime.max.replace(
        tzinfo=timezone.utc).isoformat())


def main():
    try:
        set_default_env()
        args = parse_env()
        matched = search_repos(args)
        core.set_output('repos', json.dumps(matched))
        core.info(f'{json.dumps(matched)}')
        core.export_variable('OUTPUT_REPOS', json.dumps(matched))
    except Exception as e:
        core.set_failed(str(e))


if __name__ == "__main__":
    main()
