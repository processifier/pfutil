import sys
from argparse import ArgumentParser


class Parser:
    COMMAND_PUT = "put"
    def __init__(self):
        self._parser = ArgumentParser(description="Command line tool for managing process data.")
        self._parser.add_argument('-c', '--config', help='load config from CONFIG_FILE', metavar='CONFIG_FILE')

        self._subparsers = self._parser.add_subparsers(help=f'available commands. '
                f'Run {sys.argv[0]} <COMMAND> -h to see command help, eg. {sys.argv[0]} put -h',
            required=True,
            dest="command")
        self._init_cmd_put()

    def args(self):
        return self._parser.parse_args()
    
    def print_usage(self):
        return self._parser.print_usage()

    def _init_cmd_put(self):
        parser = self._subparsers.add_parser(self.COMMAND_PUT,
            help='insert data into database or to csv files.')
        parser.add_argument('-e', '--eventlog', metavar="CSV_FILE", help='load eventlog from CSV_FILE', required=True)
        parser.add_argument('-f', '--force-overwrite', action='store_true',
            help='force overwrite output data (overwriting directory)')
        parser.add_argument('--csv-out', metavar='DIR', help='save output data into DIR directory')
