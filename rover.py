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

ROVER_EXCEPTIONS = {'rover', 'rover.py', '__init__.py'}

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

        updated = []
        installed = []

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
                            updated.append(str(plugin))

                    else:
                        fetcher = subprocess.call(
                            ['git', 'clone', plugin],
                            stderr=subprocess.STDOUT,
                            stdout=open(os.devnull, 'w'),
                            cwd=plugins_location
                        )
                        installed.append(str(plugin))

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

                self.fm.notify('Updated: {updated} plugins, Installed: {installed} plugins.'.format(
                    updated=len(updated),
                    installed=len(installed)
                ))

class rover_clean(Command):
    """:rover_clean

    Removes all plugins not inside plugins.json
    """
    def execute(self):
        plugins_location = os.path.join(os.path.expanduser('~'), '.config', 'ranger', 'plugins')
        plugins_json = os.path.join(plugins_location, 'plugins.json')

        if not os.path.isfile(plugins_json):
            raise Exception("Plugins JSON manifest not found.")

        with open(plugins_json) as f:
            plugins = json.load(f)
            plugins = set([p.split('/')[-1] for p in plugins])

        dirs = [f for f in os.listdir(plugins_location) if os.path.isdir(os.path.join(plugins_location, f))]
        purged = []

        for name in dirs:
            try:
                if name not in plugins and name not in ROVER_EXCEPTIONS:
                    plugin_folder = os.path.join(plugins_location, name)

                    scripts_in_repo = set([
                        f for f in os.listdir(plugin_folder) if os.path.isfile(os.path.join(plugin_folder, f)) and '.py' in f[-3:]
                    ])

                    scripts_in_plugins = set([
                        f for f in os.listdir(plugins_location) if os.path.isfile(os.path.join(plugins_location, f)) and ('.py' in f[-3:] or '.pyo' in f[-4:])
                    ])

                    for to_delete in list(scripts_in_repo.intersection(scripts_in_plugins)):
                        if os.path.isfile(os.path.join(plugins_location, to_delete)):
                            os.remove(os.path.join(plugins_location, to_delete))

                    shutil.rmtree(plugin_folder)

                    purged.append(str(name))

            except Exception as ex:
                self.fm.notify(ex.__str__())

        self.fm.notify("Removed {length} plugins: {names}".format(length=len(purged), names=purged))

class rover_plugins(Command):
    """:rover_plugins

    Opens your plugins.json, if you have one.
    """

    def execute(self):
        plugins_location = os.path.join(os.path.expanduser('~'), '.config', 'ranger', 'plugins')
        plugins_json = os.path.join(plugins_location, 'plugins.json')
        self.fm.edit_file(plugins_json)
