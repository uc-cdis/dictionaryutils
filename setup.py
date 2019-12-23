from setuptools import setup, find_packages
from subprocess import check_output


def get_version():
    # https://github.com/uc-cdis/dictionaryutils/pull/37#discussion_r257898408
    try:
        tag = check_output(
            ["git", "describe", "--tags", "--abbrev=0", "--match=[0-9]*"]
        )
        return tag.decode("utf-8").strip("\n")
    except Exception:
        raise RuntimeError(
            "The version number cannot be extracted from git tag in this source "
            "distribution; please either download the source from PyPI, or check out "
            "from GitHub and make sure that the git CLI is available."
        )


setup(
    name="dictionaryutils",
    version=get_version(),
    packages=find_packages(),
    install_requires=["PyYAML~=5.1", "jsonschema~=3.2", "requests~=2.18", "cdislogging~=1.0"],
    package_data={"dictionaryutils": ["schemas/*.yaml"]},
)
