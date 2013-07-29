import os
import os.path

from argparse import ArgumentParser

from PIL import Image
from mako.template import Template


__here__ = os.path.dirname(__file__)


extensions = set(['jpg', 'jpeg', 'tif', 'tiff', 'bmp', 'png', 'gif'])


def readable_bytes(n):
    n = float(n)
    for exponent, prefix in ((5, 'P'),
                             (4, 'T'),
                             (3, 'G'),
                             (2, 'M'),
                             (1, 'K')):
        cutoff = (1024 ** exponent)
        if n >= cutoff:
            return "%0.2f %sB" % (n / cutoff, prefix)
    return "%d B" % n


def find_images(path):
    for fn in os.listdir(path):
        ext = fn.rsplit('.', 1)[-1].lower()
        if ext in extensions:
            yield fn


def make_thumbnail_path(fn, thumb_dir):
    prefix, base = os.path.split(fn)
    out_base = os.path.join(prefix, 'thumb-%s' % base)
    return os.path.join(thumb_dir, out_base)


def write_thumbnail(in_path, out_path, dimensions):
    im = Image.open(in_path)
    im.thumbnail(dimensions)
    im.save(out_path)


def write_index_page(path, thumbs, name):
    templ = Template(filename=os.path.join(__here__, 'index-templ.html'))
    out = templ.render(thumbs=thumbs, name=name)
    with open(path, 'w') as f:
        f.write(out)


class ThumbInfo(object):

    def __init__(self, original_path, thumb_dir):
        self.original_path = original_path
        self.thumb_path = make_thumbnail_path(original_path, thumb_dir)

    def write_thumbnail(self, dimensions):
        self.bytes = os.path.getsize(self.original_path)
        self.readable_bytes = readable_bytes(self.bytes)
        im = Image.open(self.original_path)
        self.dimensions = im.size
        self.format = im.format
        im.thumbnail(dimensions)
        im.save(self.thumb_path)


def main():
    p = ArgumentParser(
        description='Make thumbs and an index.html from a folder of images.')

    args = p.parse_args()

    print "Making thumbnails for local directory."

    path = os.getcwd()
    name = os.path.basename(path)
    dimensions = (300, 800)
    thumb_dir = 'thumbs'
    thumb_abs = os.path.join(path, thumb_dir)

    if not os.path.exists(thumb_abs):
        os.makedirs(thumb_abs)

    thumbs = []
    for fn in find_images(path):
        thumb = ThumbInfo(fn, thumb_dir)
        thumb.write_thumbnail(dimensions)
        thumbs.append(thumb)

    write_index_page(os.path.join(path, 'index.html'), thumbs, name)
