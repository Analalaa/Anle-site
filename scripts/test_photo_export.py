"""Regression checks for photo URLs on a domain and GitHub project subpath."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import export_site


class PhotoExportTests(unittest.TestCase):
    def check_export(self, base_url, prefix):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'source'
            source.mkdir()
            (source / 'photography.html').write_text('''<button data-original="/photography/photos/%E5%B0%81%E9%9D%A234.jpg"><img src="/photography/optimized/a-480.webp" srcset="/photography/optimized/a-480.webp 480w, /photography/optimized/a-800.webp 800w, https://example.org/photo.webp 1200w" sizes="310px"></button><p>Unrelated text, /keep-this.</p>''')
            (source / 'rss.xml').write_text('<rss><channel><link>https://www.milo.me</link></channel></rss>')
            output = root / 'output'
            with patch.object(export_site, 'SITE', source):
                export_site.export(output, base_url)
            html = (output / 'photography.html').read_text()
            self.assertIn(f'data-original="{prefix}/photography/photos/%E5%B0%81%E9%9D%A234.jpg"', html)
            self.assertIn(f'src="{prefix}/photography/optimized/a-480.webp"', html)
            self.assertIn(f'srcset="{prefix}/photography/optimized/a-480.webp 480w, {prefix}/photography/optimized/a-800.webp 800w, https://example.org/photo.webp 1200w"', html)
            self.assertIn('sizes="310px"', html)
            self.assertIn('Unrelated text, /keep-this.', html)

    def test_custom_domain(self):
        self.check_export('https://anlening.me', '')

    def test_project_subpath(self):
        self.check_export('https://analalaa.github.io/Anle-site', '/Anle-site')


if __name__ == '__main__':
    unittest.main()
