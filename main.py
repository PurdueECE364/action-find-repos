import json
import os
import re
from datetime import datetime

from actions_toolkit import core
from github import Github


def search_repos(args):
    g = Github(args['token'])
    repos = g.get_organization(args['org']).get_repos()
    matched = []
    remaining = repos.totalCount
    page_num = 0
    while remaining > 0:
        # get next page
        page_results = repos.get_page(page_num)
        # check each repo in page
        for repo in page_results:
            if re.match(args['pattern'], repo.name) != None:
                if repo.created_at >= args['created_after'] and \
                        repo.created_at <= args['created_before']:
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
    args['created_after'] = datetime.strptime(
        args['created_after'], '%d/%m/%Y %H:%M:%S')
    args['created_before'] = datetime.strptime(
        args['created_before'], '%d/%m/%Y %H:%M:%S')
    if args['created_after'] >= args['created_before']:
        raise Exception('created_after must come before created_before.')
    return args


def set_default_env():
    os.environ.setdefault('INPUT_CREATED_AFTER', '01/01/1970 00:00:00')
    if os.environ.get('INPUT_CREATED_BEFORE', '') == '':
        os.environ['INPUT_CREATED_BEFORE'] = datetime.now().strftime(
            '%d/%m/%Y %H:%M:%S')


def main():
    try:
        set_default_env()
        args = parse_env()
        matched = search_repos(args)
        core.set_output('repos', json.dumps(matched))
        core.info(f'{json.dumps(matched)}')
    except Exception as e:
        core.set_failed(str(e))


if __name__ == "__main__":
    main()
