import argparse
import os
import shutil
import logging
from logger_setup import setup_logger
from download_utils import download_users_csv
from processing_functions import process_csv
from data_organizer import organize_and_save
from archive_utils import log_folder_structure, archive_folder
from constants import CSV_FORMAT


log = logging.getLogger("lab_3_logger")


def parse_args():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments with the following fields:
            dest (str): Destination directory for the output.
            filename (str): Name of the output CSV file.
            gender (str, optional): Filter users by gender ('male' or 'female').
            rows (int, optional): Limit the number of rows to download. 
            log_level (str): Logging level (default: INFO).
    """
    
    parser = argparse.ArgumentParser(
        description="Prepare user data for analysis")
    parser.add_argument("--dest", required=True,
                        help="Destination path for the output file")
    parser.add_argument("--filename", default="output",
                        help="Output CSV filename (default: output)")
    parser.add_argument(
        "--gender", choices=["male", "female"], help="Filter by gender")
    parser.add_argument("--rows", type=int, help="Number of rows to process")
    parser.add_argument("log_level", nargs="?", default="INFO",
                        help="Log level (default: INFO)")
    return parser.parse_args()


def prepare_destination_folder(dest: str):
    """
    Create the destination folder if it doesn't exist.
    
    Args:
        dest (str): Path to the destination folder.
    
    Returns:
        str: The same path, guaranteeing the folder exists.
        
    Side effects:
        May create a new directory on disk.
        Logs creation using the 'lab_3_logger'.
    """
    if not os.path.exists(dest):
        os.makedirs(dest)
        log.info(f"Destination folder '{dest}' created.")
    return dest


def main():
    args = parse_args()

    setup_logger(log_level=args.log_level)
    log.info("Script started")

    log.info(f"Destination: {args.dest}")
    log.info(f"Filename: {args.filename}")
    if args.gender:
        log.info(f"Filtering by gender: {args.gender}")
    if args.rows:
        log.info(f"Filtering by row count: {args.rows}")

    dest_folder = prepare_destination_folder(args.dest)

    csv_file = download_users_csv(
        filename=args.filename,
        dest_folder=dest_folder,
        gender=args.gender,
        rows=args.rows,
    )

    dest_file_path = os.path.join(dest_folder, f"{args.filename}.{CSV_FORMAT}")
    shutil.move(csv_file, dest_file_path)
    log.info(f"Moved CSV to: {dest_file_path}")

    data = process_csv(dest_file_path)
    organize_and_save(data, dest_folder)

    log.info("Final folder structure:")
    log_folder_structure(dest_folder)

    archive_path = archive_folder(dest_folder)
    log.info(f"Final archive saved as: {archive_path}")


if __name__ == "__main__":
    main()