# Find Repos Action

This action will search an organization for repos that match a provided RegEx pattern. It is meant to populate the build matrix of another job.

# Usage
## Basic
```yaml
jobs:
  find_repos:
    runs-on: ubuntu-latest
    steps:
      - uses: PurdueECE/action-find-repos@v1.4
        id: get_repos
        with:
          # Org to search in
          org: PurdueECE
          # Personal access token
          token: ${{ github.token }}
          # Pattern to match against
          pattern: ^prelabs-.*$
          # Earliest creation date (DD/MM/YY HH:MM:SS). Defaults to '01/01/1970 00:00:00'.
          created_after: '01/01/2022 00:00:00'
          # Latest creation date (DD/MM/YY HH:MM:SS). Defaults to current time.
          created_before: '01/06/2022 00:00:00'
      # Prints results - output parameters is 'repos'
      - run: "echo results: ${{ steps.get_repos.outputs.repos }}"
```
## Run job on each repository
```yaml
jobs:
  # First job retrieves repos and sets the result as the job's output
  get_repos:
    runs-on: ubuntu-latest
    outputs:
      # Assign result of action-find-repos to output of job
      repos: ${{ steps.find_repos.outputs.repos }}
    steps:
      - id: find_repos
        uses: PurdueECE/action-find-repos@main
        with:
          pattern: ^homework1.*$
  # Second job has build matrix that is populated by first job
  grade:
    runs-on: ubuntu-latest
    # Make this job depend on first job
    needs: get_repos
    strategy:
      fail-fast: false
      matrix:
        # Populate build matrix with repo list using fromJson()
        repo: ${{ fromJson(needs.get_repos.outputs.repos) }}
    steps:
      - uses: actions/checkout@v3
        with:
          repository: ${{ matrix.repo }}
      - uses: PurdueECE/action-dircheck@main
        with:
          paths: src/main.py
      - uses: PurdueECE/action-pylint@main
        with:
          args: src
```

# Testing
Unit tests are in the `test-unit/` directory. They can be run with `pytest`.