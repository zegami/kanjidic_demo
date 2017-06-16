# coding: utf-8
"""In memory representation of kanjidic."""

import gzip
import re
import sys


text = str if sys.version_info > (3,) else unicode

# Overly complex regexp for parsing kanjidic
_pat = re.compile(
    u"^(?P<kanji>[^ ]+)"
    u" (?P<jis>[0-9a-fA-F]+)"
    u" U(?P<unicode>[0-9a-f]+)"
    u" B(?P<classification>\\d+)"
    u"(?: C\\d+)?"
    u"(?: G(?P<grade>\\d+)\\b)?"
    u" S(?P<stroke_count>\\d+)\\b"
    u".*?"
    u"\\bQ(?P<four_corner>[.\\d]+)\\b"
    u".*?"
    u"(?P<on_readings>(?: [ア-ン]+)+)?"
    u"(?P<kun_readings>(?: [-.あ-ん]+)+)?"
    u"(?: T\\d+(?: [-.あ-ん]+)+)?"
    u"(?P<translations>(?: {[^}]+})+)"
    u" $", re.UNICODE)


def optional(conversion):
    def _wrapped_conversion(content):
        if content is None:
            return None
        return conversion(content)
    return _wrapped_conversion


def trans(string):
    return string.strip("{} ").split("} {")


optint = optional(int)
optsplit = optional(text.split)


class Kanji(object):

    __slots__ = (
        "kanji", "jis", "unicode", "classification", "stroke_count", "grade",
        "four_corner", "on_readings", "kun_readings", "translations")

    _conversions = dict(zip(__slots__, (
        text, text, text, int, int, optint, text, optsplit, optsplit,  trans)))

    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

    @classmethod
    def from_line(cls, line):
        match = _pat.match(line)
        if match is None:
            raise ValueError("unparsable line {!r}".format(line))
        d = match.groupdict()
        return cls(**dict((k, cls._conversions[k](d[k])) for k in d))

    @classmethod
    def header_row(cls):
        return "id\t{}\n".format(
            "\t".join(n.replace("_", " ") for n in cls.__slots__[1:]))

    def to_row(self):
        return "\t".join(self._as_data(k) for k in self.__slots__) + "\n"

    def _as_data(self, key):
        value = getattr(self, key, None)
        if value is None:
            return ""
        if isinstance(value, list):
            return ",".join(v.replace(",", "\\,") for v in value)
        return text(value)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, ", ".join(
            "{}={!r}".format(k, getattr(self, k)) for k in self.__slots__
            if getattr(self, k, None) is not None))


class KanjiDic(object):

    ENCODING = "EUC_JP"

    def __init__(self, line_iter):
        self.kanji = tuple(Kanji.from_line(line) for line in line_iter)

    @classmethod
    def from_file(cls, fileobj):
        first = fileobj.readline()
        if not first.startswith(b"# KANJIDIC"):
            raise ValueError("Not a kanjidic file")
        return cls(line.decode(cls.ENCODING) for line in fileobj)

    @classmethod
    def from_gzip(cls, gzip_filename):
        with gzip.GzipFile(gzip_filename) as f:
            return cls.from_file(f)
