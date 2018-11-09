=============================
KANJIDIC to Zegami collection
=============================

Scripts for the conversion of the KANJIDIC_ Japanese kanji dictionary into a
Zegami_ collection. This includes parsing the database file, rendering images
using an OpenType font, generating a metadata subset, and uploading to the api.


License
-------

This code is copyright Zegami Ltd released under the `Apache License 2.0`_ see
`<LICENSE>`_ for a copy of the terms and conditions.

The `EDRDG Licence Statement`_ allows for reuse of the dictionaries, and
therefore the derived collection, under the `CC BY-SA 3.0`_ license.

Images may be generated with any font, but the default `Noto Sans CJK`_ face is
published under the `SIL Open Font Licence, Version 1.1`_ which allows reuse.

Usage
-----

Installation::

    cd kanjidic_demo
    pip install .

To run::

    ktoz --project $PROJECT --token $TOKEN

Or run as a module to use a different Python version::

    python3 -m zegami_kanjidic --help

Note that the location of the font is going to be OS-specific and may have to
be separately installed. The free `Noto Sans CJK`_ face can be downloaded from
Google or different local font can be specified with the ``--font`` argument.

TODO
----

- Reuse generic Zegami client when available
- Include pretty description with links and licences


.. _KANJIDIC: http://www.edrdg.org/kanjidic/kanjidic.html
.. _Zegami: https://zegami.com/
.. _Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0
.. _EDRDG Licence Statement: http://www.edrdg.org/edrdg/licence.html
.. _CC BY-SA 3.0: http://creativecommons.org/licenses/by-sa/3.0/
.. _Noto Sans CJK: http://www.google.com/get/noto/help/cjk/
.. _SIL Open Font Licence, Version 1.1: http://scripts.sil.org/OFL
