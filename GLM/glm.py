#!/usr/bin/env python3

import glob
import semver
import importlib
if __name__ == "__main__" and __package__ == None:
    from source.libs.rainbow import color, msg
else:
    from .source.libs.rainbow import color, msg

VERSION = "0.0.3"
PLUGIN_PREFIX = "plugins"
PLUGIN_PACKAGE = "source.plugins"
PLUGIN_DIRECTORY = "./source/" + PLUGIN_PREFIX + "/"


def plugin_scan(_dir=PLUGIN_DIRECTORY):
    """Scans the plugin directory"""
    return [x.replace(_dir, '')
            for x in glob.glob(_dir + "*.py")
            if x.replace(_dir, '') != "__init__.py"]


def import_plugin(plugin):
    """Does this even need a docstring ?
    """
    try:
        main_plugin = importlib.import_module(plugin)
        msg("plugin imported", 0, "import_plugin", plugin, level=2)

        return main_plugin

    except ImportError as ie:
        msg("Import error", 2, "import_plugin", ie, level=0)


def plugin_checker(main_plugin, start, *args):
    """Check wether a plugin is suitable for launch or not
    """
    if not hasattr(main_plugin, "Plugin"):
        msg("Plugin outdated", 2, "plugin_checker", level=0)
        return False
    else:
        loaded_plugin = main_plugin.Plugin(start, *args)
    if not hasattr(loaded_plugin, "_start"):
        msg("Plugin outdated", 2, "plugin_checker", level=0)
        return False
    if not hasattr(loaded_plugin, "version"):
        msg("Plugin outdated", 2, "plugin_checker", level=0)
        return False
    else:
        if loaded_plugin.version != VERSION:
            msg("Plugin outdated", 2, "plugin_checker", loaded_plugin.version, level=0)
            return False
        else:
            msg("Plugin version ok", 0, "plugin_checker", loaded_plugin.version, level=2)
    return loaded_plugin


def plugin_loader(plugin, start, *args):
    main_plugin = import_plugin(PLUGIN_PACKAGE + "." + plugin.replace(".py", ''))
    loaded_plugin = plugin_checker(main_plugin, False, *args)
    if loaded_plugin:
        print_plugin_info(loaded_plugin)
        loaded_plugin = main_plugin.Plugin(True, *args)

def print_plugin_info(plugin):
    if hasattr(plugin, "name"):
        msg(plugin.name, 0, "Plugin", level=2)
    else:
        msg("No name", 1, "print_plugin_info", level=2)
    if hasattr(plugin, "author"):
        msg(plugin.author, 0, 'Plugin', level=2)
    else:
        msg("No author", 1, "print_plugin_info", level=2)
    if hasattr(plugin, "version"):
        msg(plugin.version, 0, 'Plugin', level=2)
    else:
        msg("No version", 1, "print_plugin_info", level=2)


def plugin_selector(plugins):
    for num, plugin in enumerate(plugins):
        print(num, plugin, sep=") ")

    select = input("Select plugin: ")
    return plugins[int(select)]


def main():
    plugin_loader(plugin_selector(plugin_scan()))

if __name__ == '__main__':
    main()
