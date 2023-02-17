import json
import os
import re
from datetime import datetime, timezone

from actions_toolkit import core
from dateutil import parser
from github import Github
from github.PaginatedList import PaginatedList
from github.Repository import Repository


def search_repos(args):
    g = Github(args['INPUT_TOKEN'])
    repos = g.get_organization(args['INPUT_ORG']).get_repos()
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
            filters.append(re.match(args['INPUT_PATTERN'], repo.name))
            filters.append(args['INPUT_AFTER'] <= repo.created_at.replace(
                tzinfo=timezone.utc) <= args['INPUT_BEFORE'])
            # update matched
            if all(filters):
                matched.append(repo.full_name)
        # update indeces
        remaining -= len(page_results)
        page_num += 1
    if len(matched) < 1:
        raise Exception(f'No repositories found.\nargs = {args}')
    return matched


def setup():
    if not os.environ.get('INPUT_AFTER'):
        os.environ['INPUT_AFTER'] = datetime(
            1970, 1, 1).replace(tzinfo=timezone.utc).isoformat()
        core.notice(
            f"INPUT_AFTER is empty, defaulting to {os.environ['INPUT_AFTER']}")
    if not os.environ.get('INPUT_BEFORE'):
        os.environ['INPUT_BEFORE'] = datetime.utcnow().replace(
            tzinfo=timezone.utc).isoformat()
        core.notice(
            f"INPUT_BEFORE is empty, defaulting to {os.environ['INPUT_BEFORE']}")
    if os.environ['INPUT_AFTER'] > os.environ['INPUT_BEFORE']:
        raise Exception(
            f'INPUT_AFTER ({os.environ["INPUT_AFTER"]}) must come before INPUT_BEFORE ({os.environ["INPUT_BEFORE"]})')
    return {
        'INPUT_ORG': os.environ['INPUT_ORG'],
        'INPUT_TOKEN': os.environ.get('INPUT_TOKEN'),
        'INPUT_PATTERN': os.environ['INPUT_PATTERN'],
        'INPUT_AFTER': parser.parse(os.environ.get('INPUT_AFTER')),
        'INPUT_BEFORE': parser.parse(os.environ.get('INPUT_BEFORE')),
    }


def main():
    try:
        args = setup()
        matched = search_repos(args)
        core.set_output('repos', json.dumps(matched))
        core.info(f'{json.dumps(matched)}')
        core.export_variable('OUTPUT_REPOS', json.dumps(matched))
    except Exception as e:
        core.set_failed(e)


if __name__ == "__main__":
    main()
