"""Render latest post as index.html."""

import os
import pprint

from nikola.plugins.task import pages
from nikola.plugin_categories import Task
from nikola import utils


class LatestAsIndex(pages.RenderPages):
    """Horrible hack to render latest post as index.html."""

    name = 'latest_as_index'

    def gen_tasks(self):
        yield self.group_task()

        tasks = list(super().gen_tasks())
        rev_posts = sorted(self.site.timeline, key=lambda p: p.date, reverse=True)
        latest_post = rev_posts[0]
        [latest_task] = [
            t for t in tasks
            if latest_post.base_path in t.get('file_dep', ())]
        render_action = latest_task['actions'][0]
        target = os.path.join(self.site.config['OUTPUT_FOLDER'], 'index.html')
        render_action[1][1] = target
        latest_task['actions'] = [render_action]
        latest_task['name'] = target
        latest_task['targets'] = [target]
        yield utils.apply_filters(latest_task, self.site.config['FILTERS'])
