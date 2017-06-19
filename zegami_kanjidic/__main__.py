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
KANJD212_URL = "http://ftp.monash.edu.au/pub/nihongo/kanjd212.gz"
DEFAULT_FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def _ensure_dir(dirname):
    try:
        os.mkdir(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def get_dic(reporter, to_dir, dic_url):
    dic_name = dic_url.rsplit("/", 1)[-1]
    dic_path = os.path.join(to_dir, dic_name)
    if not os.path.exists(dic_path):
        reporter("Dowloading dictionary {url}", url=dic_url)
        http.download(dic_url, dic_path)
    return dic_path


def _iter_new_images(data_dir, kanji_iter):
    image_dir = os.path.join(data_dir, "images")
    _ensure_dir(image_dir)
    for kanji in kanji_iter:
        png_path = os.path.join(image_dir, kanji.char + ".png")
        if not os.path.exists(png_path):
            yield kanji, png_path


def _iter_report_images(reporter, image_iter):
    for count, (kanji, path) in enumerate(image_iter):
        if reporter.show_nth(count):
            reporter("Rendering image {n} for {kanji}", n=count, kanji=kanji)
        yield kanji, path


def render_images(face, image_iter):
    for kanji, path in image_iter:
        font.render_glyph(face, kanji.char, path)


class Reporter(object):
    """Simplistic output to a stream with verbosity support."""

    def __init__(self, stream, verbosity):
        self._stream = stream
        self.level = verbosity

    def __call__(self, format_string, level=1, **kwargs):
        if self.level >= level:
            self._stream.write(format_string.format(**kwargs) + "\n")
            self._stream.flush()

    def show_nth(self, n, step=(1 << 10)):
        """True if item in sequence should be reported based on level."""
        if not self.level:
            return False
        factor = step >> (self.level << 1)
        if not factor:
            return True
        return not n % factor


def create_collection(reporter, data_dir, font_path, also_212=False):
    path_208 = get_dic(reporter, data_dir, KANJIDIC_URL)
    dic = kdic.KanjiDic.from_gzip(path_208)
    if also_212:
        path_212 = get_dic(reporter, data_dir, KANJD212_URL)
        dic.extend(kdic.KanjiDic0212.from_gzip(path_212))
    face = font.load_face(font_path)
    dic.to_tsv(os.path.join(data_dir, "dic.tsv"))
    new_image_iter = _iter_new_images(data_dir, (k for k in dic.kanji))
    reporting_iter = _iter_report_images(reporter, new_image_iter)
    render_images(face, reporting_iter)


def parse_args(argv):
    parser = argparse.ArgumentParser(argv[0], description=__doc__)
    parser.add_argument("--dir", default="data", help="dir for output")
    parser.add_argument("--font", default=DEFAULT_FONT, help="path of font")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="show progress")
    parser.add_argument(
        "--also-212", action="store_true",
        help="include supplementary kanji from JIS X 0212-1990")
    return parser.parse_args(argv[1:])


def main(argv):
    args = parse_args(argv)
    reporter = Reporter(sys.stderr, args.verbose)
    try:
        _ensure_dir(args.dir)
        create_collection(reporter, args.dir, args.font, args.also_212)
    except (EnvironmentError, ValueError) as e:
        sys.stderr.write("error: {}\n".format(e))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
