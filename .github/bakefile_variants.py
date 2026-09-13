#!/usr/bin/env python3
"""Create bakefile"""
from typing import Dict, Any, List, Sequence, Tuple
import asyncio
import datetime
import os
import sys

PLATFORMS = ("linux/amd64", "linux/arm64")
ISODATE = datetime.datetime.now(datetime.UTC).date().isoformat()
ORIG_REPO = "ghcr.io"
ALT_REPOS = ("docker.io", os.environ.get("ACR_REPO", None))
DOCKER_TAG_EXTRA = os.environ.get("DOCKER_TAG_EXTRA", "")
RUNNER_IMAGE = f"{ORIG_REPO}/pvarki/actions-runner:latest{DOCKER_TAG_EXTRA}"


def image_tags(image: str) -> List[str]:
    """Resolve all the tags (in all the repos) for given image"""
    imgtags_orig = [f"{image}", f"{image}-{ISODATE}"]
    imgtags_more = []
    for alt_repo in ALT_REPOS:
        if not alt_repo:
            continue
        imgtags_more += [tag.replace(ORIG_REPO, alt_repo) for tag in imgtags_orig]
    return imgtags_orig + imgtags_more


def service_hcl(
    servicename: str, servicedef: Dict[str, Any]
) -> Tuple[Sequence[str], str]:
    """Make the HCL"""
    hcl_targets = ""
    tgtname = servicename
    imgtags = image_tags(servicedef["image"])
    hcl_targets += f"""
target "{tgtname}" {{
    tags = [{", ".join(f'"{imgtag}"' for imgtag in imgtags)}]
    dockerfile = "{servicedef['build']['dockerfile']}"
    context = "{servicedef['build']['context']}"
    platforms = [{", ".join(f'"{platform}"' for platform in PLATFORMS)}]
"""
    if "target" in servicedef["build"]:
        hcl_targets += f"""    target = "{servicedef['build']['target']}"\n"""

    if "args" in servicedef["build"]:
        hcl_targets += "    args = {\n"
        for argname, argval in servicedef["build"]["args"].items():
            hcl_targets += f"""        {argname}: "{argval}"\n"""
        hcl_targets += "    }\n"

    hcl_targets += "}"
    return [tgtname], hcl_targets


async def main() -> None:
    """Main entry point."""
    if "--tags" in sys.argv[1:]:
        # Used by the CI to create the manifest list from per-arch builds
        print("\n".join(image_tags(RUNNER_IMAGE)))
        return
    ret_tgts, ret_hcl = service_hcl(
        "actions-runner",
        {
            "image": RUNNER_IMAGE,
            "build": {
                "context": "./",
                "dockerfile": "Dockerfile",
            },
        },
    )
    print(
        f"""
group "default" {{
    targets = [{", ".join(f'"{tgt}"' for tgt in ret_tgts)}]
}}
"""
    )
    print(ret_hcl)


if __name__ == "__main__":
    asyncio.run(main())
