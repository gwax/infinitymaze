#!/usr/bin/env python3
"""Generate an app.yaml file given various snippets."""

import yaml

HEADERS = {
    # "X-Narwhal": "A small arctic whale. The male has a long tusk.",
}

EXTENSION_MIME = [
    # html
    ("html", "text/html"),
    ("css", "text/css"),
    ("js", "application/javascript"),
    # source code
    ("c", "text/x-c"),
    ("h", "text/x-c"),
    ("py", "text/x-python"),
    # text / markup
    ("txt", "text/plain"),
    ("md", "text/x-markdown"),
    ("rst", "text/x-rst"),
    ("xml", "application/xml"),
    ("xsl", "application/xml"),
    # documents
    ("pdf", "application/pdf"),
    # fonts
    ("eot", "application/vnd.ms-fontobject"),
    ("otf", "application/font-otf"),
    ("ttf", "application/font-ttf"),
    ("woff", "application/font-woff"),
    ("woff2", "application/font-woff2"),
    # images
    ("ico", "image/x-icon"),
    ("jpg", "image/jpeg"),
    ("svg", "image/svg+xml"),
    # videos
    ("mp4", "video/mp4"),
]

BASE = {"runtime": "python37", "default_expiration": "10m"}


def asset_handler(extension, mime):
    url = r"/(.+\.{ext}$)".format(ext=extension)
    handler = {
        "url": url,
        "static_files": r"static/\1",
        "upload": "static" + url,
        "mime_type": mime,
        "secure": "always",
    }
    if HEADERS:
        handler['http_headers'] = {**HEADERS}
    return handler


def file_catch_all_handler():
    url = r"/(.+\.[A-Za-z0-9]+$)"
    handler = {
        "url": url,
        "static_files": r"static/\1",
        "upload": "static" + url,
        "secure": "always",
    }
    if HEADERS:
        handler['http_headers'] = {**HEADERS}
    return handler


def index_handlers():
    handlers = []
    for url in [r"/(.+)/", r"/(.+)"]:
        upload_url = ("static" + url + "/index.html").replace("//", "/")
        handler = {
            "url": url,
            "static_files": r"static/\1/index.html",
            "upload": upload_url,
        }
        handlers.append(handler)
    handlers.append(
        {"url": "/", "static_files": "static/index.html", "upload": "static/index.html"}
    )

    for handler in handlers:
        handler["mime_type"] = "text/html"
        handler["secure"] = "always"
        if HEADERS:
            handler['http_headers'] = {**HEADERS}

    return handlers


def main():
    app_dict = {
        **BASE,
        "handlers": [
            *(asset_handler(ext, mime) for ext, mime in EXTENSION_MIME),
            file_catch_all_handler(),
            *index_handlers(),
        ],
    }
    print(yaml.dump(app_dict, default_flow_style=False))


if __name__ == "__main__":
    main()
