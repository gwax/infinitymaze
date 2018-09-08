#!/usr/bin/env python3
"""Generate an app.yaml file given various snippets."""

import collections
import copy

import yaml


def dict_representer(dumper, data):
    """Representer to dump OrderedDict in the correct order."""
    return dumper.represent_dict(data.items())
yaml.add_representer(collections.OrderedDict, dict_representer)

OUTPUT_DIRECTORY = 'output'
HEADER_VALUES = [
    # ('X-Narwhal', 'A small arctic whale. The male has a long tusk.'),
]

EXTENSION_MIME = [
    # html
    ('html', 'text/html'),
    ('css', 'text/css'),
    ('js', 'application/javascript'),
    # source code
    ('c', 'text/x-c'),
    ('h', 'text/x-c'),
    ('py', 'text/x-python'),
    # text / markup
    ('txt', 'text/plain'),
    ('md', 'text/x-markdown'),
    ('rst', 'text/x-rst'),
    ('xml', 'application/xml'),
    ('xsl', 'application/xml'),
    # documents
    ('pdf', 'application/pdf'),
    # fonts
    ('eot', 'application/vnd.ms-fontobject'),
    ('otf', 'application/font-otf'),
    ('ttf', 'application/font-ttf'),
    ('woff', 'application/font-woff'),
    ('woff2', 'application/font-woff2'),
    # images
    ('ico', 'image/x-icon'),
    ('jpg', 'image/jpeg'),
    ('svg', 'image/svg+xml'),
    # videos
    ('mp4', 'video/mp4'),
]

BASE = [
    ('runtime', 'python27'),
    ('api_version', 1),
    ('threadsafe', True),
    ('default_expiration', '30d'),
]


def asset_handler(extension, mime):
    url = r'/(.+\.{ext}$)'.format(ext=extension)
    handler = collections.OrderedDict([
        ('url', url),
        ('static_files', rf'{OUTPUT_DIRECTORY}/\1'),
        ('upload', f'{OUTPUT_DIRECTORY}' + url),
        ('mime_type', mime),
        ('secure', 'always'),
    ])
    if extension == 'html':
        handler['expiration'] = '1h'
    if HEADER_VALUES:
        handler['http_headers'] = collections.OrderedDict(HEADER_VALUES)
    return handler


def file_catch_all_handler():
    url = r'/(.+\.[A-Za-z0-9]+$)'
    handler = collections.OrderedDict([
        ('url', url),
        ('static_files', rf'{OUTPUT_DIRECTORY}/\1'),
        ('upload', f'{OUTPUT_DIRECTORY}' + url),
        ('secure', 'always'),
        ('http_headers', collections.OrderedDict(HEADER_VALUES)),
    ])
    return handler


def index_handlers():
    handlers = []
    for url in [r'/(.+)/', r'/(.+)']:
        upload_url = (f'{OUTPUT_DIRECTORY}' + url + '/index.html').replace('//', '/')
        handler = collections.OrderedDict([
            ('url', url),
            ('static_files', rf'{OUTPUT_DIRECTORY}/\1/index.html'),
            ('upload', upload_url),
        ])
        handlers.append(handler)
    handlers.append(collections.OrderedDict([
        ('url', '/'),
        ('static_files', f'{OUTPUT_DIRECTORY}/index.html'),
        ('upload', f'{OUTPUT_DIRECTORY}/index.html')
    ]))

    for handler in handlers:
        handler['mime_type'] = 'text/html'
        handler['secure'] = 'always'
        handler['expiration'] = '10m'
        handler['http_headers'] = collections.OrderedDict(HEADER_VALUES)

    return handlers


def main():
    app_dict = collections.OrderedDict([
        *BASE,
        ('handlers', [
            *(asset_handler(ext, mime) for ext, mime in EXTENSION_MIME),
            file_catch_all_handler(),
            *index_handlers()
        ]),
    ])
    print(yaml.dump(app_dict, default_flow_style=False))

if __name__ == '__main__':
    main()
