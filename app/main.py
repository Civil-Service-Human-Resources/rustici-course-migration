import argparse
from models.ResetOpts import ResetOpts
from database import setup
from service import migrate_all, migrate_selected, reset_selected, check_all, check_selected
from log import logger

def run():
    args = format_args()
    run_commands(args)

def format_args():
    parser = argparse.ArgumentParser()
    
    sub_parsers = parser.add_subparsers(dest="command")

    upload_parser = sub_parsers.add_parser("upload", help="Run the upload for all courses in the database")
    upload_parser.add_argument("--modules", dest="modules", help="Run the upload command for specific modules", nargs="+")

    reset_parser = sub_parsers.add_parser("reset", help="reset uploaded course/modules from the database and blob storage")
    reset_parser.add_argument("modules", help="Run the reset command for specific modules. Resets the rustici course upload by default", nargs="+")
    reset_parser.add_argument("--zip-upload", dest="zip_upload", action=argparse.BooleanOptionalAction, help="Additionally resets the zip upload")
    
    check_parser = sub_parsers.add_parser("check", help="Check the status of migrations")
    check_parser.add_argument("--modules", dest="modules", help="Run the check command for specific modules", nargs="+")
    check_parser.add_argument("--check-zip", dest="check_zip", help="Validate that the zip file exists", action=argparse.BooleanOptionalAction, default=False)

    sub_parsers.add_parser("setup", help="Setup the database")

    return parser.parse_args()

def run_commands(args):

    if args.command == "upload":
        if args.modules:
            migrate_selected(args.modules)
        else:
            migrate_all()
    elif args.command == "reset":
        options = ResetOpts(args.zip_upload)
        reset_selected(args.modules, options)
    elif args.command == "check":
        if args.modules:
            check_selected(args.modules, args.check_zip)
        else:
            check_all(args.check_zip)
    elif args.command == "setup":
        setup()
    else:
        logger.error(f"{args.command} is not a valid command")

if __name__ == '__main__':
    run()