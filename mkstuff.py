import datetime as dt
import os
import shutil

COMIC_DIR = os.path.join('.', 'comics')
IMAGE_FILES = os.listdir(COMIC_DIR)
POSTS_PATH = os.path.join('.', 'posts')

POST_TEMPLATE = """\
{title}
{title_underline}

:slug: {slug}
:date: {date}

.. image:: /comics/{image_file}
    :alt: {slug}
    :class: comic
"""

if os.path.exists(POSTS_PATH):
    shutil.rmtree(POSTS_PATH)
os.makedirs(POSTS_PATH)

for image_file in IMAGE_FILES:
    post_base, _ = os.path.splitext(os.path.basename(image_file))
    post_date = dt.datetime.strptime(post_base[:10], '%Y-%m-%d').date()
    post_datetime = dt.datetime.combine(
        post_date,
        dt.time(12, 0),
        tzinfo=dt.timezone.utc
    )
    post_slug = f'comic-{post_base}'
    post_filename = f'{post_slug}.rst'
    post_title = post_base
    post_title_underline = '=' * len(post_title)
    folder = os.path.join(POSTS_PATH, f'{post_date.year:04d}')
    os.makedirs(folder, exist_ok=True)
    post_file = os.path.join(folder, post_filename)
    with open(post_file, 'wt') as target:
        target.write(POST_TEMPLATE.format(
            title=post_title,
            title_underline=post_title_underline,
            slug=post_slug,
            date=str(post_datetime),
            image_file=image_file,
        ))
