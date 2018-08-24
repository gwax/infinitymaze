#!/usr/bin/env python3
import argparse
import collections
import mimetypes
import os

import magic

def main(target):
    ext_to_mimes = collections.defaultdict(set)
    for root, _, filenames in os.walk(args.target):
        for filename in filenames:
            mimetypes_guess, _ = mimetypes.guess_type(filename, strict=False)
            magic_guess = magic.from_file(os.path.join(root, filename), mime=True)
            _, ext = os.path.splitext(filename)
            ext = ext.lstrip('.')

            ext_to_mimes[ext] |= {t for t in (mimetypes_guess, magic_guess) if t is not None}

    for ext, mimes in sorted(ext_to_mimes.items()):
        mimestr = ', '.join(sorted(mimes))
        print(f'{ext}: {mimestr}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Guess mime types')
    parser.add_argument('target', help='Target folder for file consideration')
    args = parser.parse_args()
    main(args.target)
