import os
import os.path

from argparse import ArgumentParser

from PIL import Image
from mako.template import Template


__here__ = os.path.dirname(__file__)


extensions = set(['jpg', 'jpeg', 'tif', 'tiff', 'bmp', 'png', 'gif'])


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

    def __init__(self, original_path, thumb_path):
        self.original_path = original_path
        self.thumb_path = thumb_path


def main():
    p = ArgumentParser(
        description='Make thumbs and an index.html from a folder of images.')

    args = p.parse_args()

    print "Making thumbnails for local directory."

    path = os.getcwd()
    name = os.path.basename(path)
    dimensions = (300, 300)
    thumb_dir = 'thumbs'
    thumb_abs = os.path.join(path, thumb_dir)

    if not os.path.exists(thumb_abs):
        os.makedirs(thumb_abs)

    thumbs = []
    for fn in find_images(path):
        thumb_path = make_thumbnail_path(fn, thumb_dir)
        write_thumbnail(fn, thumb_path, dimensions)
        thumbs.append(ThumbInfo(fn, thumb_path))

    write_index_page(os.path.join(path, 'index.html'), thumbs, name)
