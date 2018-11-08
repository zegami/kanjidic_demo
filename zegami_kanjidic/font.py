# Copyright 2017 Zegami Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for loading font and rendering characters."""

import freetype
import PIL.Image
import PIL.ImageOps


def load_face(path):
    return freetype.Face(path)


def render_glyph(face, char, filename):
    """Render a glyph to an image on disk."""
    face.set_char_size(256 * 256)
    face.load_char(
        char, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_NORMAL)
    _do_render(face.glyph.bitmap, filename)


def _do_render(bitmap, filename):
    """Hackish rendering into png on disk using PIL."""
    bb = bytes(bytearray(bitmap.buffer))
    # Using pitch below is bogus, should adjust for width after
    img = PIL.Image.frombytes("L", (bitmap.pitch, bitmap.rows), bb)
    img = img.resize((img.width // 2, img.height // 2), PIL.Image.BILINEAR)
    img = PIL.ImageOps.expand(img, 10)
    img = PIL.ImageOps.invert(img)
    img.save(filename)
