"""
rover

A plugin manager for ranger.
Sits on top of ranger + git.
"""

import os
import subprocess
import shutil
import json

from ranger.api.commands import *
from ranger.core.loader import CommandLoader

class rover_update(Command):
    """:rover_update

    Updates all plugins, defined in plugins.json.
    """

    def execute(self):
        plugins_location = os.path.join(os.path.expanduser('~'), '.config', 'ranger', 'plugins')
        plugins_json = os.path.join(plugins_location, 'plugins.json')

        if not os.path.isfile(plugins_json):
            raise Exception("Plugins JSON manifest not found.")

        with open(plugins_json) as f:
            plugins = json.load(f)

        dirs = set([f for f in os.listdir(plugins_location) if os.path.isdir(os.path.join(plugins_location, f))])

        for plugin in plugins:
            stripped_repo_name = plugin.split('/')[-1]

            for name in dirs:
                try:
                    plugin_folder = os.path.join(plugins_location, stripped_repo_name)

                    if os.path.isdir(plugin_folder):
                        child = subprocess.call(
                            ['git', 'rev-parse', '--is-inside-work-tree'],
                            stderr=subprocess.STDOUT,
                            stdout=open(os.devnull, 'w'),
                            cwd=plugin_folder
                        )

                        if child == 0:
                            fetcher = subprocess.call(
                                ['git', 'pull'],
                                stderr=subprocess.STDOUT,
                                stdout=open(os.devnull, 'w'),
                                cwd=plugin_folder
                            )

                    else:
                        fetcher = subprocess.call(
                            ['git', 'clone', plugin],
                            stderr=subprocess.STDOUT,
                            stdout=open(os.devnull, 'w'),
                            cwd=plugins_location
                        )

                    scripts_in_repo = set([
                        f for f in os.listdir(plugin_folder) if os.path.isfile(os.path.join(plugin_folder, f)) and '.py' in f[-3:]
                    ])

                    scripts_in_plugins = set([
                        f for f in os.listdir(plugins_location) if os.path.isfile(os.path.join(plugins_location, f)) and '.py' in f[-3]
                    ])

                    for to_copy in list(scripts_in_repo - scripts_in_plugins):
                        if os.path.isfile(os.path.join(plugins_location, to_copy)):
                            os.remove(os.path.join(plugins_location, to_copy))
                        shutil.copy2(os.path.join(plugin_folder, to_copy), os.path.join(plugins_location, to_copy))

                except Exception as ex:
                    self.fm.notify(ex.__str__())

class rover_plugins(Command):
    """:rover_plugins

    Opens your plugins.json, if you have one.
    """

    def execute(self):
        plugins_location = os.path.join(os.path.expanduser('~'), '.config', 'ranger', 'plugins')
        plugins_json = os.path.join(plugins_location, 'plugins.json')
        self.fm.edit_file(plugins_json)
