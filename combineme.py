#!/usr/bin/env python3

# Silly pdf combine script
# Written by Luke Erbsen

import os
import sys
import argparse
from pypdf import PdfWriter, PdfReader

def main():
    parser = argparse.ArgumentParser(description="pdf combining software for ReadMe")
    required_arguments = parser.add_argument_group("Required arguments")

    required_arguments.add_argument(
        "--volume", "-v", action="store", help="Volume Number", required=True,
    )
    required_arguments.add_argument(
        "--issue", "-i", action="store", help="Issue Number", required=True,
    )
    required_arguments.add_argument(
        "--destination", "-d", action="store", help="Folder destination for new pdf include leading slash such as foo/", required=True,
    )

    content_arguments = parser.add_argument_group("Paths to pdfs")

    content_arguments.add_argument(
            "--tabloid", "-t", action="store", help="Path to tabloid pdf", required=False,
    )
    content_arguments.add_argument(
        "--centerfold1", "-c1", action="store", help="First centerfold pdf (absolute path)", required=False,
    )
    content_arguments.add_argument(
        "--centerfold2", "-c2", action="store", help="Path to second centerfold pdf (absolute path)", required=False,
    )
    content_arguments.add_argument(
        "--centerfold3", "-c3", action="store", help="Path to third centerfold pdf (absolute path)", required=False,
    )

    parser.add_argument(
        "--automatic", "-a", action="store_true",
        help="Automatically locate the tabloid and centerfold pdfs in the destination folder "
             "using the naming pattern VOL<volume>ISSUE<issue>.pdf, "
             "VOL<volume>ISSUE<issue>_CENTER.pdf, VOL<volume>ISSUE<issue>_CENTER_2.pdf, "
             "and VOL<volume>ISSUE<issue>_CENTER_3.pdf",
    )

    args = parser.parse_args()

    if args.automatic:
        base = f"VOL{args.volume}ISSUE{args.issue}"

        tabloid_path = os.path.join(args.destination, f"{base}.pdf")
        if not os.path.isfile(tabloid_path):
            sys.exit(f"Automatic mode: could not find tabloid pdf at {tabloid_path}")
        args.tabloid = tabloid_path

        centerfold1_path = os.path.join(args.destination, f"{base}_CENTER.pdf")
        args.centerfold1 = centerfold1_path if os.path.isfile(centerfold1_path) else None

        centerfold2_path = os.path.join(args.destination, f"{base}_CENTER_2.pdf")
        args.centerfold2 = centerfold2_path if os.path.isfile(centerfold2_path) else None

        centerfold3_path = os.path.join(args.destination, f"{base}_CENTER_3.pdf")
        args.centerfold3 = centerfold3_path if os.path.isfile(centerfold3_path) else None
    else:
        if not args.tabloid:
            parser.error("--tabloid/-t is required unless --automatic/-a is used")

    # PDF readers
    tabloid_reader = PdfReader(args.tabloid)
    if args.centerfold1:
        centerfold1_reader = PdfReader(args.centerfold1)
    if args.centerfold2:
        centerfold2_reader = PdfReader(args.centerfold2)
    if args.centerfold3:
        centerfold3_reader = PdfReader(args.centerfold3)

    writer = PdfWriter()

    # First two pages of the tabloid
    writer.add_page(tabloid_reader.pages[0])
    writer.add_page(tabloid_reader.pages[1])

    # Centerfold 1
    if args.centerfold1:
        writer.add_page(centerfold1_reader.pages[0])
        writer.add_page(centerfold1_reader.pages[1])

    # Centerfold 2
    if args.centerfold2:
        writer.add_page(centerfold2_reader.pages[0])
        writer.add_page(centerfold2_reader.pages[1])

    # Centerfold 3
    if args.centerfold3:
        writer.add_page(centerfold3_reader.pages[0])
        writer.add_page(centerfold3_reader.pages[1])

    # Last two pages of the tabloid
    writer.add_page(tabloid_reader.pages[2])
    writer.add_page(tabloid_reader.pages[3])

    filepath = args.destination + "VOLUME" + args.volume + "ISSUE" + args.issue + "FULL.pdf"
    with open(filepath, "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    main()