"""Logic for all subcommands."""
import argparse
import logging
import os
import typing
import subprocess

LOGGER = logging.getLogger(__name__)

def _run_git(args: typing.List[typing.Text], cwd: typing.Text) -> None:
	args = ["git", "-C", cwd] + args
	LOGGER.debug("Running '%s'", " ".join(args))
	process = subprocess.run(args, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	LOGGER.info("Result: %s", process.stdout)

def init(args: argparse.Namespace) -> None:
	"""Initialize a build area."""
	branch = args.branch
	url = args.url

	repo_path = os.path.join(os.path.abspath("."), ".repo")
	LOGGER.info("Creating repo directory at %s", repo_path)
	os.makedirs(repo_path, exist_ok=True)
	_run_git(["clone", "-b", branch, url, "manifests.git"], repo_path)
