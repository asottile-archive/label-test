import argparse


def luminance(r8, g8, b8):
    rs, gs, bs = r8 / 255., g8 / 255., b8 / 255.
    if rs <= 0.03928:
        r = rs / 12.92
    else:
        r = ((rs + 0.055) / 1.055) ** 2.4
    if gs <= 0.03928:
        g = gs / 12.92
    else:
        g = ((gs + 0.055) / 1.055) ** 2.4
    if bs <= 0.03928:
        b = bs / 12.92
    else:
        b = ((bs + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def to_rgb(s):
    x = int(s, 16)
    r = (x & (0xff << 16)) >> 16
    g = (x & (0xff << 8)) >> 8
    b = x & 0xff
    return r, g, b


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('fg')
    parser.add_argument('bg')
    args = parser.parse_args(argv)

    fg, bg = to_rgb(args.fg), to_rgb(args.bg)
    lum_fg, lum_bg = luminance(*fg), luminance(*bg)
    print((max(lum_fg, lum_bg) + 0.05) / (min(lum_fg, lum_bg) + 0.05))


if __name__ == '__main__':
    exit(main())
