FROM ghcr.io/actions/actions-runner:latest AS base

ARG TARGETARCH
ARG COMPOSE_VERSION=5.0.1

WORKDIR /actions-runner
USER root

RUN apt-get update && apt-get install -y \
        python3-pip \
        golang-go \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && true

RUN export RUNNER_ARCH=${TARGETARCH} \
    && if [ "$RUNNER_ARCH" = "amd64" ]; then export DOCKER_ARCH=x86_64 ; fi \
    && if [ "$RUNNER_ARCH" = "arm64" ]; then export DOCKER_ARCH=aarch64 ; fi \
    && curl -fLo /usr/local/lib/docker/cli-plugins/docker-compose \
        "https://github.com/docker/compose/releases/download/v${COMPOSE_VERSION}/docker-compose-linux-${DOCKER_ARCH}" \
    && chmod +x /usr/local/lib/docker/cli-plugins/docker-compose \
    && true

ENV PIP_BREAK_SYSTEM_PACKAGES=1
WORKDIR /home/runner
USER runner
