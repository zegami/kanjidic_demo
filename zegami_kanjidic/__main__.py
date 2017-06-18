#!/usr/bin/env python3
#
# Copyright 2017 Zegami Ltd

"""Command line script for making a Zegami collection from KANJIDIC."""

from __future__ import absolute_import

import argparse
import errno
import os
import sys

from . import (
    font,
    http,
    kdic,
    )


KANJIDIC_URL = "http://ftp.monash.edu.au/pub/nihongo/kanjidic.gz"
KANJIDIC_NAME = "kanjidic.gz"
DEFAULT_FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def _ensure_dir(dirname):
    try:
        os.mkdir(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def get_dic(to_dir):
    dic_path = os.path.join(to_dir, KANJIDIC_NAME)
    if not os.path.exists(dic_path):
        http.download(KANJIDIC_URL, dic_path)
    return dic_path


def render_all(to_dir, face, dic):
    image_dir = os.path.join(to_dir, "images")
    _ensure_dir(image_dir)
    for c in dic.kanji:
        glyph_filename = os.path.join(image_dir, c.kanji + ".png")
        if not os.path.exists(glyph_filename):
            font.render_glyph(face, c.kanji, glyph_filename)


def parse_args(argv):
    parser = argparse.ArgumentParser(argv[0], description=__doc__)
    parser.add_argument("--dir", default="data", help="dir for output")
    parser.add_argument("--font", default=DEFAULT_FONT, help="path of font")
    return parser.parse_args(argv[1:])


def main(argv):
    args = parse_args(argv)
    try:
        _ensure_dir(args.dir)
        dic = kdic.KanjiDic.from_gzip(get_dic(args.dir))
        face = font.load_face(args.font)
        dic.to_tsv(os.path.join(args.dir, "dic.tsv"))
        render_all(args.dir, face, dic)
    except (EnvironmentError, ValueError) as e:
        sys.stderr.write("error: {}\n".format(e))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
