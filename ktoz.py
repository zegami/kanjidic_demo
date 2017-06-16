#!/usr/bin/env python
"""Turn kanjidic into a Zegami collection."""

from __future__ import absolute_import
from __future__ import print_function

import argparse
import codecs
import errno
import os
import sys

import font
import kanjidic


DEFAULT_FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def _ensure_dir(dirname):
    try:
        os.mkdir(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def create_tsv(to_dir, dic):
    filename = os.path.join(to_dir, "dic.tsv")
    with codecs.open(filename, "wb", encoding='utf-8') as f:
        f.write(kanjidic.Kanji.header_row())
        f.writelines(k.to_row() for k in dic.kanji)


def render_all(to_dir, face, dic):
    image_dir = os.path.join(to_dir, "images")
    _ensure_dir(image_dir)
    for c in dic.kanji:
        glyph_filename = os.path.join(image_dir, c.kanji + ".png")
        if not os.path.exists(glyph_filename):
            font.render_glyph(face, c.kanji, glyph_filename)


def parse_args(argv):
    parser = argparse.ArgumentParser(argv[0], description=__doc__)
    parser.add_argument("kanjidic", help="path of kanjidic.gz file")
    parser.add_argument("--to", default="", help="dir for  data and images")
    parser.add_argument("--font", default=DEFAULT_FONT, help="path of font")
    return parser.parse_args(argv[1:])


def main(argv):
    args = parse_args(argv)
    try:
        kdic = kanjidic.KanjiDic.from_gzip(args.kanjidic)
        face = font.load_face(args.font)
        create_tsv(args.to, kdic)
        render_all(args.to, face, kdic)
        for k in kdic.kanji[:3]:
            print(repr(k))
    except (EnvironmentError, ValueError) as e:
        sys.stderr.write("error: {}\n".format(e))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
