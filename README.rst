=============================
KANJIDIC to Zegami collection
=============================

Scripts for the conversion of the KANJIDIC_ Japanese kanji dictionary into a
Zegami_ collection. This includes parsing the database file, rendering images
using an OpenType font, and generating a metadata subset.


Licence
-------

This code is copyright Zegami Ltd and not currently released under any licence.

The `EDRDG Licence Statement`_ allows for reuse of the dictionaries, and
therefore the derived collection, under the `CC BY-SA 3.0`_ license.

Images may be generated with any font, but the default `Noto Sans CJK`_ face is
published under the `SIL Open Font Licence, Version 1.1`_ which allows reuse.


Usage
-----

Installation::

    cd kanjidic_demo
    pip install -e .

To run::

    python -m zegami_kanjidic --api-url https://app.zegami.net/api/ \
    --project djFPOGtB --token XXXXXX \
    --font /Library/Fonts/NotoSansCJK-Regular.ttc

Note that the location of the font is going to be OS-specific and the kanji
font may not be installed on your machine by default. If not, the
NotoSansCJK-Regular font (amongst others) can be downloaded from
https://www.google.com/get/noto/help/cjk/

TODO
----

- Some amount of additional polish
- Reuse generic Zegami client when available
- Include pretty description with links and licences


.. _KANJIDIC: http://www.edrdg.org/kanjidic/kanjidic.html
.. _Zegami: https://zegami.com/
.. _EDRDG Licence Statement: http://www.edrdg.org/edrdg/licence.html
.. _CC BY-SA 3.0: http://creativecommons.org/licenses/by-sa/3.0/
.. _Noto Sans CJK: http://www.google.com/get/noto/help/cjk/
.. _SIL Open Font Licence, Version 1.1: http://scripts.sil.org/OFL
