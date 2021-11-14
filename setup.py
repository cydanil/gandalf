import os.path as osp
import re
from setuptools import setup, find_packages
import sys


def get_script_path():
    return osp.dirname(osp.realpath(sys.argv[0]))


def read(*parts):
    return open(osp.join(get_script_path(), *parts)).read()


def find_version(*parts):
    vers_file = read(*parts)
    match = re.search(r'^__version__ = "(\d+\.\d+\.\d+)"', vers_file, re.M)
    if match is not None:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name="Gandalf",
      version=find_version("gandalf", "__init__.py"),
      author="Cyril Danilevski",
      author_email="cydanil@gmail.com",
      description="Bot to interact through Zulip",
      packages=find_packages(),
      entry_points={
          "console_scripts": [
              "gandalf = gandalf.main:main"
          ],
          "gandalf_reply_scripts": [
              "sensors = gandalf.sensors:main",
              "raise = gandalf.raise:main",
          ],
          "gandalf_event_scripts": [  # subprocesses?
          ],
      },
      install_requires=[
          'zulip',
      ],
      extras_require={
          'test': [
              'pytest',
          ]
      },
      python_requires='>=3.6',
)
