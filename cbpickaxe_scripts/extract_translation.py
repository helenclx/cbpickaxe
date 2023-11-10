# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
from typing import Dict, List

import argparse
import csv
import pathlib
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
        with open(filepath, "r", encoding="utf-8") as input_stream:
            for line in input_stream:
                line = line.strip()
                if line == "":
                    continue

                strings_to_translate.append(line)

    tables: Dict[str, cbp.TranslationTable] = {}
    for translation_filepath in args.translation_files:
        with open(translation_filepath, "rb") as input_stream:
            translation_table = cbp.TranslationTable.from_translation(input_stream)

        tables[translation_filepath], _ = translation_table

    locales = {
        translation_filepath: pathlib.Path(translation_filepath).name.split(".")[-2]
        for translation_filepath in args.translation_files
    }

    with open(args.output_file, "w", encoding="utf-8") as ouput_stream:
        writer = csv.DictWriter(
            ouput_stream, fieldnames=["id", *sorted(set(locales.values()))]
        )
        writer.writeheader()
        
        def find_string(id):
            for name, table in tables.items():
                locale = locales[name]
                message = table.get(id, "")
                assert isinstance(message, str)

                if message != "":
                    row[locale] = message

        for i in strings_to_translate:
            row = {
                "id": i,
            }
            
            find_string(i)

            if len(row.keys()) == 1:
                pronouns = [".f", ".m", ".n"]
                ids_with_pronouns = []
                for pronoun in pronouns:
                    ids_with_pronouns.append(i + pronoun)
                for id_with_pronoun in ids_with_pronouns:
                    row["id"] = id_with_pronoun
                    find_string(id_with_pronoun)
                    writer.writerow(row)
            else:
                writer.writerow(row)
                        
            """
            NOTES REGARDING THE ORIGINAL CODE:
            - IDs with no string found did not have the locale key
                Possible solutions:
                - Check if the string ID does not have the locale key
                    - if locale not in row.keys():
                - Check if the string ID only has one key (id)
                    - if len(row.keys()) == 1:
            """

    return SUCCESS

def main_without_args() -> int:
    return main(sys.argv[1:])
