"""Logic for all subcommands."""
import argparse
import logging
import os
from typing import List
import subprocess
import urllib.parse

import storas.manifest

MANIFEST_DIRECTORY = "manifests.git"
LOGGER = logging.getLogger(__name__)

class RepoNotFoundError(Exception):
	"""The .repo directory could not be found."""

def init(args: argparse.Namespace) -> None:
	"""Initialize a build area."""
	branch = args.branch
	url = args.url

	repo_path = os.path.join(os.path.abspath("."), ".repo")
	LOGGER.info("Creating repo directory at %s", repo_path)
	os.makedirs(repo_path, exist_ok=True)
	_run_git(["clone", "-b", branch, url, MANIFEST_DIRECTORY], repo_path)
	LOGGER.info("Initialized repository at %s", repo_path)

def show(args: argparse.Namespace) -> None:
	"""Show status."""
	manifest = storas.manifest.load(args.manifest)
	for project in manifest.projects:
		print(project)

def sync(args: argparse.Namespace) -> None:
	"""Sync to the latest code."""
	del args
	repo_path = _find_repo()
	manifest_file = os.path.join(repo_path, MANIFEST_DIRECTORY, storas.manifest.DEFAULT_MANIFEST_FILE)
	manifest = storas.manifest.load(manifest_file)
	for project in manifest.projects:
		full_path = os.path.join(repo_path, "..", project.path)
		remote = project.remote
		full_fetch_url = urllib.parse.urljoin(remote.fetch_host, project.name)
		if not os.path.exists(full_path):
			os.makedirs(full_path, exist_ok=True)
			LOGGER.debug("Created '%s'", full_path)
			_run_git(["clone", "-b", project.revision, full_fetch_url], cwd=full_path)

def _find_repo() -> str:
	"""Find the directory in the parent chain where .repo lives."""
	start = os.path.abspath(os.getcwd())
	current = start
	while current != "/":
		repo = os.path.join(current, ".repo")
		if os.path.exists(repo):
			LOGGER.debug("Found .repo at %s", repo)
			return repo
		current = os.path.dirname(current)
	raise RepoNotFoundError("Not .repo found in any directory along {}".format(start))

def _run_git(args: List[str], cwd: str) -> None:
	args = ["git", "-C", cwd] + args
	LOGGER.info("Running '%s' in %s", " ".join(args), cwd)
	process = subprocess.run(args, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	LOGGER.info("Result: %s", process.stdout)
