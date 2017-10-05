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

DEFAULT_FONTS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
]


def _ensure_dir(dirname):
    try:
        os.mkdir(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def get_default_font():
    for font_path in DEFAULT_FONTS:
        if os.path.exists(font_path):
            return font_path


def get_dic(reporter, session, to_dir, dic_url):
    dic_name = dic_url.rsplit("/", 1)[-1]
    dic_path = os.path.join(to_dir, dic_name)
    if not os.path.exists(dic_path):
        reporter("Dowloading dictionary {url}", url=dic_url)
        http.download(session, dic_url, dic_path)
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


def get_kanjidic(reporter, session, data_dir, also_212):
    path_208 = get_dic(reporter, session, data_dir, KANJIDIC_URL)
    dic = kdic.KanjiDic.from_gzip(path_208)
    reporter("Loaded {dic}", dic=dic, level=2)
    if also_212:
        path_212 = get_dic(reporter, session, data_dir, KANJD212_URL)
        dic_212 = kdic.KanjiDic0212.from_gzip(path_212)
        reporter("Loaded {dic}", dic=dic_212, level=2)
        dic.extend(dic_212)
    return dic


def create_collection(reporter, client, data_dir, font_path, also_212):
    _ensure_dir(data_dir)
    if client is not None:
        session = client.session
    else:
        session = http.make_session()

    dic = get_kanjidic(reporter, session, data_dir, also_212)
    dic.to_tsv(os.path.join(data_dir, TSV_NAME))

    face = font.load_face(font_path)
    new_image_iter = _iter_new_images(data_dir, dic.kanji)
    reporting_iter = _iter_report_images(reporter, new_image_iter)
    render_images(face, reporting_iter)

    if client is not None:
        api_upload(reporter, client, data_dir, dic, also_212)


def api_upload(reporter, client, data_dir, dic, also_212):
    """Upload images and data to new Zegami collection.

    For now this is dumb and syncronous, can intermingle with image creation
    and parallelise later.
    """
    name = "Kanjidic"
    description = "Zegami view of Jim Breen's KANJIDIC"
    if also_212:
        name += "2"
        description += "with JIS 0212 characters"
    collection = client.create_collection(name, description)
    reporter("Created collection {id} {name}", level=0, **collection)

    imageset_id = collection["imageset_id"]
    image_dir = os.path.join(data_dir, IMGDIR_NAME)
    for n, kanji in enumerate(dic.kanji):
        if reporter.show_nth(n):
            reporter("Uploading image {n} for {kanji}", n=n, kanji=kanji)
        png_path = os.path.join(image_dir, kanji.char + ".png")
        client.upload_png(imageset_id, png_path)

    reporter("Uploading to dataset {dataset_id}", level=0, **collection)
    dataset_id = collection["dataset_id"]
    client.upload_data(dataset_id, os.path.join(data_dir, TSV_NAME))

    join_ds = client.create_join("Join for " + name, imageset_id, dataset_id)
    reporter("Created join dataset {id} {name}", level=0, **join_ds)

    collection['join_dataset_id'] = join_ds['id']
    client.update_collection(collection['id'], collection)
