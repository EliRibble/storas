"""Main entrypoint module. Used by bin/storas."""
import argparse
import logging
import subprocess

import storas.commands

def run() -> int:
	"""Run the main storas command.

	Returns:
		0 on success, nonzero on failure.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument("--verbose", action="store_true", help="Show more verbose logging")

	subparsers = parser.add_subparsers(title="command", help="The command to perform.")
	init = subparsers.add_parser("init")
	init.set_defaults(command=storas.commands.init)
	init.add_argument("-b", "--branch", default="master", help="The branch to use for the manifest.")
	init.add_argument("-u", "--url", required=True, help="The URL to pull the manifest file from")

	args = parser.parse_args()

	logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
	try:
		args.command(args)
	except subprocess.CalledProcessError as err:
		logging.error("Subprocess call '%s' failed (%d)", err.args, err.returncode)
		logging.error("stdout: %s", err.stdout)
		logging.error("stderr: %s", err.stderr)
		return 1
	return 0
