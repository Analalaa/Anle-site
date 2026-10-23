#!/usr/bin/env python3
"""Create checked-in WebP gallery images; keep original photographs untouched.

Requires Pillow with WebP support. Run after adding or replacing photographs,
then run build_site.py. Normal site builds need only the Python standard library.
"""
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import unquote

from PIL import Image, ImageCms, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site/www.milo.me'
OUTPUT = SITE / 'photography/optimized'
RECIPE = b'webp-v1:480,800:q82:srgb:method6'


def main():
    photos = json.loads((ROOT / 'content/photos.json').read_text())
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for group in photos.values():
        for photo in group:
            src = photo['src']
            if src in manifest:
                continue
            source = (SITE / unquote(src).lstrip('/')).read_bytes()
            key = hashlib.sha256(source + RECIPE).hexdigest()[:16]
            with Image.open(io.BytesIO(source)) as original:
                image = ImageOps.exif_transpose(original)
                profile = image.info.get('icc_profile')
                if profile:
                    image = ImageCms.profileToProfile(
                        image, ImageCms.ImageCmsProfile(io.BytesIO(profile)),
                        ImageCms.createProfile('sRGB'), outputMode='RGB')
                else:
                    image = image.convert('RGB')
                width, height = image.size

                def save(size, label, quality):
                    dest = OUTPUT / f'{key}-{label}.webp'
                    if not dest.exists():
                        resized = image.resize(size, Image.Resampling.LANCZOS)
                        # The pixels are sRGB; omit camera/location metadata.
                        resized.save(dest, 'WEBP', quality=quality, method=6,
                                     exif=b'', icc_profile=b'')
                    return {'src': '/' + dest.relative_to(SITE).as_posix(),
                            'width': size[0], 'height': size[1],
                            'bytes': dest.stat().st_size}

                variants = [save((w, max(1, round(height * w / width))), str(w), 82)
                            for w in sorted({min(width, 480), min(width, 800)})]
                manifest[src] = {'width': width, 'height': height, 'sourceBytes': len(source),
                                 'variants': variants}
    (ROOT / 'content/photo-assets.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    for name, group in photos.items():
        originals = sum(manifest[p['src']]['sourceBytes'] for p in group)
        small = sum(manifest[p['src']]['variants'][0]['bytes'] for p in group)
        large = sum(manifest[p['src']]['variants'][-1]['bytes'] for p in group)
        print(f'{name}: {len(group)} photos; originals {originals / 1024**2:.2f} MiB; '
              f'480px {small / 1024**2:.2f} MiB; 800px {large / 1024**2:.2f} MiB')


if __name__ == '__main__':
    main()
