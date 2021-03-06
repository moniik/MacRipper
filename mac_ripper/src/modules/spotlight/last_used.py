# -*- coding: utf-8 -*-
import argparse
import os
from modules.spotlight.base_spotlight import BaseSpotlight, BaseBinarySpotlight
import logging


class BaseLastUsed:

    def is_target(self, data):
        return data["kMDItemLastUsedDate"] != self.NULL_VALUE

    def find_cmd(self):
        return "mdfind -onlyin {} -name 'kMDItemLastUsedDate == *'".format(self.evidence_root())


class LastUsed(BaseLastUsed, BaseSpotlight):

    def output_file_name(self):
        return "spotlight_last_used_command.csv"

    def attrs(self):
        return [
            "FilePath",
            "kMDItemDisplayName",
            "kMDItemKind",
            "kMDItemLastUsedDate",
            "kMDItemTitle"
        ]


class LastUsedBinary(BaseLastUsed, BaseBinarySpotlight):

    def output_file_name(self):
        return "spotlight_last_used_binary.csv"

    def attrs(self):
        # "Inode_Num" is required.
        return [
            "FilePath",
            "kMDItemDisplayName",
            "kMDItemKind",
            "kMDItemLastUsedDate",
            "kMDItemTitle",
            "Inode_Num",
            "Parent_Inode_Num"
        ]


if __name__ == "__main__":
    LOG = logging.getLogger(__name__)
    LOG.setLevel(logging.INFO)

    print("[+]LastUsed for Mac OSX 13.x Ver.20190926")
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-r", "--evidence_root_path",
                             help="please input evidence root path:e.g. /Volumes/disk3s1/",
                             type=str, default="/")
    args_parser.add_argument("-o", "--output", help="please input the output path.", type=str, default=os.getcwd())
    args_parser.add_argument("-t", "--timezone_difference", help="please input the timezone difference hour.", type=int,
                             default=0)
    args_parser.add_argument("-b", "--parse_spotlight_database", help="parse the raw spotlight database",
                             action="store_true")
    args = args_parser.parse_args()

    print("[+]start processing...")
    if args.parse_spotlight_database:
        LastUsedBinary(
            args.evidence_root_path,
            args.output,
            args.timezone_difference).parse()
    else:
        LastUsed(
            args.evidence_root_path,
            args.output,
            args.timezone_difference).parse()
