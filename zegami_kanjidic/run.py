# Copyright 2017 Zegami Ltd

"""Core logic for generating a kanjidic collection."""

from __future__ import absolute_import

import errno
import os

from . import (
    font,
    http,
    kdic,
)


KANJIDIC_URL = "http://ftp.monash.edu.au/pub/nihongo/kanjidic.gz"
KANJD212_URL = "http://ftp.monash.edu.au/pub/nihongo/kanjd212.gz"

TSV_NAME = "dic.tsv"
IMGDIR_NAME = "images/"


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
    image_dir = os.path.join(data_dir, IMGDIR_NAME)
    _ensure_dir(image_dir)
    for kanji in kanji_iter:
        png_path = os.path.join(image_dir, kanji.char + ".png")
        if not os.path.exists(png_path):
            yield kanji, png_path


def _iter_report_images(reporter, image_iter):
    for count, (kanji, path) in enumerate(image_iter):
        if reporter.show_nth(count):
            reporter("Making image {n} for {kanji}", n=count, kanji=kanji)
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
        """``True`` if item in sequence should be reported based on level."""
        if not self.level:
            return False
        factor = step >> (self.level << 1)
        if not factor:
            return True
        return not n % factor


def get_kanjidic(reporter, data_dir, also_212):
    path_208 = get_dic(reporter, data_dir, KANJIDIC_URL)
    dic = kdic.KanjiDic.from_gzip(path_208)
    reporter("Loaded {dic}", dic=dic, level=2)
    if also_212:
        path_212 = get_dic(reporter, data_dir, KANJD212_URL)
        dic_212 = kdic.KanjiDic0212.from_gzip(path_212)
        reporter("Loaded {dic}", dic=dic_212, level=2)
        dic.extend(dic_212)
    return dic


def create_collection(reporter, data_dir, font_path, also_212):
    _ensure_dir(data_dir)
    dic = get_kanjidic(reporter, data_dir, also_212)
    dic.to_tsv(os.path.join(data_dir, TSV_NAME))

    face = font.load_face(font_path)
    new_image_iter = _iter_new_images(data_dir, (k for k in dic.kanji))
    reporting_iter = _iter_report_images(reporter, new_image_iter)
    render_images(face, reporting_iter)
