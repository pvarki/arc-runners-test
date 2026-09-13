# arc-runners-test

Test ARC runners and build the runner image

## Runner image

The runner image (`Dockerfile`) is built by `.github/workflows/runnerimg.yaml`. The build is
distributed across native GitHub hosted runners, `ubuntu-latest` for `linux/amd64` and
`ubuntu-24.04-arm` for `linux/arm64`. Each arch is pushed to  ghcr.io by digest and a
separate `merge` job creates the multiarch manifest lists for all the  configured repos
(ghcr.io, docker.io and the optional `ACR_REPO`) from those digests.

**This workflow must keep using the GitHub hosted "community" runners**, we need to be able to
build a new runner image also when our own ARC installation is broken.

The tags are resolved by `.github/bakefile_variants.py --tags` so that they stay in sync with the
bakefile the script generates for local/manual `docker buildx bake` builds.

## Development

### Pre-Commit

Pre-commit is configured under `.pre-commit-config.yaml`. The recommended tool to run it locally is [Prek](https://github.com/j178/prek), which is also used in the GitHub Action. There are no additional required dependencies apart from prek. Installing the pre-commit is done via `prek install`.

And checks can be manually run with `prek run --all-files`
