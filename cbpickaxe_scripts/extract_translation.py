from typing import List

import argparse
import csv
import json
import pathlib
import re
import sys

import cbpickaxe as cbp

SUCCESS = 0
FAILURE = 1


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument("--translation_files", nargs="+", required=True)
    parser.add_argument("--strings_text_files", nargs="+", required=True)
    parser.add_argument("--output_file", required=True)

    args = parser.parse_args(argv)

    strings_to_translate = []
    for filepath in args.strings_text_files:
        with open(filepath, "r") as input_stream:
            for line in input_stream:
                line = line.strip()
                if line == "":
                    continue

                strings_to_translate.append(line)

    tables = {}
    for translation_filepath in args.translation_files:
        with open(translation_filepath, "rb") as input_stream:
            translation_table = cbp.TranslationTable.from_translation(
                input_stream, strings_to_translate
            )

        tables[translation_filepath] = translation_table

    locales = {
        translation_filepath: pathlib.Path(translation_filepath).name.split(".")[-2]
        for translation_filepath in args.translation_files
    }

    with open(args.output_file, "w") as ouput_stream:
        writer = csv.DictWriter(
            ouput_stream, fieldnames=["id", *sorted(set(locales.values()))]
        )
        writer.writeheader()

        for i in strings_to_translate:
            row = {
                "id": i,
            }
            for name, table in tables.items():
                locale = locales[name]
                message = table.messages.get(i, "")
                assert isinstance(message, str)

                if message != "":
                    row[locale] = message

            writer.writerow(row)

    return SUCCESS


def main_without_args() -> int:
    return main(sys.argv[1:])
