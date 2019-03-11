import argparse

import storas.commands

def run() -> int:
  """Run the main storas command.

  Returns:
    0 on success, nonzero on failure.
  """
  parser = argparse.ArgumentParser()

  subparsers = parser.add_subparsers(title="command", help="The command to perform.")
  init = subparsers.add_parser("init")
  init.set_defaults(command=storas.commands.init)
  init.add_argument("-u", required=True, help="The URL to pull the manifest file from")
  init.add_argument("-b", default="master", help="The branch to use for the manifest.")

  args = parser.parse_args()

  args.command(args)
  return 0
