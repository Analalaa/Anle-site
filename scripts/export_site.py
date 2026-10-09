#!/usr/bin/env python3
"""Export the static site for either a GitHub project URL or a custom domain."""
import argparse
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site/www.milo.me'


def export(output, base_url):
    parsed = urlsplit(base_url)
    if parsed.scheme not in ('https', 'http') or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError('base-url must be a full HTTP(S) site URL without a query or fragment')
    base_url = base_url.rstrip('/')
    prefix = parsed.path.rstrip('/')
    output = Path(output).resolve()
    # Never erase an existing folder, or write an export into the source site.
    if output.exists() or SITE == output or SITE in output.parents:
        raise ValueError('output must be a new directory outside the source site')
    shutil.copytree(SITE, output, ignore=shutil.ignore_patterns('.*', '__pycache__'))
    for path in output.rglob('*.html'):
        source = path.read_text(encoding='utf-8')
        # Generated pages use quoted root-relative href/src attributes. Relative,
        # external, protocol-relative, mailto, and in-page links stay unchanged.
        source = re.sub(r'''(\b(?:href|src|poster|action)\s*=\s*["'])/(?!/)''',
                        lambda m: m[1] + prefix + '/', source, flags=re.I)
        source = re.sub(r'''(content=["']0;url=)/(?!/)''',
                        lambda m: m[1] + prefix + '/', source, flags=re.I)
        path.write_text(source, encoding='utf-8')
    # Preserve the existing feed, replacing its historic site origin with the
    # actual configured URL. The directory name is not a domain-ownership claim.
    feed = output / 'rss.xml'
    xml = ET.fromstring(feed.read_text(encoding='utf-8'))
    for item in xml.iter():
        if item.text:
            item.text = item.text.replace('https://www.milo.me', base_url)
        for key, value in item.attrib.items():
            item.set(key, value.replace('https://www.milo.me', base_url))
    ET.ElementTree(xml).write(feed, encoding='utf-8', xml_declaration=True)
    (output / '.nojekyll').write_text('')
    print(f'Exported site to {output} for {base_url}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--base-url', required=True)
    args = parser.parse_args()
    export(args.output, args.base_url)
