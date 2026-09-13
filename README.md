# arc-runners-test
Test ARC runners

## Development

### Pre-Commit

Pre-commit is configured under `.pre-commit-config.yaml`. The recommended tool to run it locally is [Prek](https://github.com/j178/prek), which is also used in the GitHub Action. There are no additional required dependencies apart from prek. Installing the pre-commit is done via `prek install`.

And checks can be manually run with `prek run --all-files`
