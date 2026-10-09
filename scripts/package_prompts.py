#!/usr/bin/env python3
"""Package a portable Prompts marketplace from an explicit source directory."""
import argparse
import json
import stat
import zipfile
from pathlib import Path

FILES = [
    '.codex-plugin/plugin.json', '.mcp.json', 'README.md',
    'scripts/launch', 'scripts/prompt_atlas.py', 'scripts/history_index.py',
    'skills/search-codex-history/SKILL.md',
    'web/index.html', 'web/app.js', 'web/style.css', 'web/native-bridge.js',
]
INSTALL = '''Prompts for Codex — macOS / Codex desktop + CLI / Python 3.9+

1. Extract this archive to a permanent folder.
2. In a terminal, from the directory containing the extracted prompts folder:
   codex plugin marketplace add ./prompts
3. Open the Codex Plugins directory, select Anle · Prompts, and install Prompts.
4. Start a new chat and ask: Open the conversation search panel.

This package contains application code only. The index is built from conversations
stored on the installing user's own computer. No conversation history or runtime
cache is included.

Official packaging guide: https://developers.openai.com/plugins/build/plugins
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    # A strict allowlist avoids accidentally publishing .env, .runtime, or history files.
    payload = {}
    for name in FILES:
        path = source / name
        if not path.is_file() or path.is_symlink():
            parser.error(f'Missing or symlinked source file: {name}')
        payload[name] = path.read_bytes()
    manifest = json.loads(payload['.codex-plugin/plugin.json'])
    if manifest['name'] != 'prompt-atlas':
        parser.error('Expected the prompt-atlas plugin')
    marketplace = {
        'name': 'anle-prompts', 'interface': {'displayName': 'Anle · Prompts'},
        'plugins': [{
            'name': manifest['name'],
            'source': {'source': 'local', 'path': './plugins/prompt-atlas'},
            'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
            'category': 'Productivity',
        }],
    }
    payload = {'plugins/prompt-atlas/' + k: v for k,v in payload.items()}
    payload['.agents/plugins/marketplace.json'] = (json.dumps(marketplace,ensure_ascii=False,indent=2)+'\n').encode()
    payload['INSTALL.txt'] = INSTALL.encode()
    output = Path(__file__).resolve().parents[1] / 'site/www.milo.me/downloads/prompts.zip'
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,data in payload.items():
            info=zipfile.ZipInfo('prompts/'+name)
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(stat.S_IFREG | (0o755 if name.endswith('/scripts/launch') else 0o644))<<16
            archive.writestr(info,data)
    print(f'Packaged {manifest["name"]} {manifest["version"]}: {len(payload)} source files, {output.stat().st_size} bytes.')


if __name__ == '__main__':
    main()
