#!/usr/bin/env python3

# Silly pdf combine script
# Written by Luke Erbsen

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
    required_arguments.add_argument(
        "--tabloid", "-t", action="store", help="Path to tabloid pdf", required=True,
    )

    centerfold_arguments = parser.add_argument_group("Centerfold paths")

    centerfold_arguments.add_argument(
        "--centerfold1", "-c1", action="store", help="First centerfold pdf (absolute path)", required=False,
    )
    centerfold_arguments.add_argument(
        "--centerfold2", "-c2", action="store", help="Path to second centerfold pdf (absolute path)", required=False,
    )

    args = parser.parse_args()

    # PDF readers
    tabloid_reader = PdfReader(args.tabloid)
    if args.centerfold1:
        centerfold1_reader = PdfReader(args.centerfold1)
    if args.centerfold2:
        centerfold2_reader = PdfReader(args.centerfold2)

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

    # Last two pages of the tabloid
    writer.add_page(tabloid_reader.pages[2])
    writer.add_page(tabloid_reader.pages[3])

    filepath = args.destination + "VOLUME" + args.volume + "ISSUE" + args.issue + "FULL.pdf"
    with open(filepath, "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    main()

