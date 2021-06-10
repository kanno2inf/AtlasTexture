import sys
from argparse import ArgumentParser
from math import ceil, sqrt, floor

from PIL import Image


def main(argv):
    parser = ArgumentParser()
    parser.add_argument('path', nargs='+')
    parser.add_argument('-m', '--max', type=int)
    parser.add_argument('-x', '--x', type=int)
    parser.add_argument('-y', '--y', type=int)
    parser.add_argument('-s', '--sort', action='store_true')
    opt = parser.parse_args(argv)

    if not opt.path:
        exit(0)

    image_files = opt.path
    if opt.sort:
        image_files = sorted(opt.path)
    image_count = len(image_files)

    tex_size = Image.open(image_files[0]).size

    # タイルXY
    tile_size_c = ceil(sqrt(image_count))
    tile_size = (opt.x if opt.x else tile_size_c, opt.y if opt.y else tile_size_c)

    # アトラス語のテクスチャサイズ
    atlas_tex_size = (tile_size[0] * tex_size[0], tile_size[1] * tex_size[1])
    atlas_tex_size = (opt.max, opt.max) if opt.max else atlas_tex_size

    # 1タイルのサイズ
    per_tile_size = (floor(atlas_tex_size[0] / tile_size[0]), floor(atlas_tex_size[1] / tile_size[1]))

    atlas_image = Image.new('RGBA', atlas_tex_size)

    for n, image_file in enumerate(image_files):
        im = Image.open(image_file)
        # アトラスに収める
        if per_tile_size != im.size:
            im = im.resize(per_tile_size, Image.BICUBIC)
        x = n % tile_size[0]
        y = floor(n / tile_size[0])
        # 座標
        offset = (x * per_tile_size[0], y * per_tile_size[1])
        atlas_image.paste(im, offset)

    atlas_image.save('atlas.png', quality=100)


if __name__ == '__main__':
    main(sys.argv[1:])
