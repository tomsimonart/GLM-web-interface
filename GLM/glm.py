#!/usr/bin/env python3

import glob
import semver
import traceback
import importlib
if __name__ == "__main__" and __package__ == None:
    from source.libs.rainbow import color, msg
    from source.libs.pluginbase import PluginBase, VERSION
    from source.specialplugins import failsafe
else:
    from .source.libs.rainbow import color, msg
    from .source.libs.pluginbase import PluginBase, VERSION
    from .source.specialplugins import failsafe

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
    """Check whether a plugin is suitable for execution or not
    Here are some free msg templates:
    msg('OK', 0, 'plugin_checker', '', level=2, slevel='check')
    msg('WARN', 1, 'plugin_checker', '', level=1, slevel='check')
    msg('ERROR', 2, 'plugin_checker', '', level=0, slevel='check')
    msg('FATAL', 3, 'plugin_checker', '', level=0, slevel='check')
    """
    if hasattr(main_plugin, "Plugin"): # Check if plugin is launchable
        msg('OK', 0, 'plugin_checker', 'Plugin', level=3, slevel='check')
    else:
        msg('FATAL', 3, 'plugin_checker', 'Plugin', level=0, slevel='check')
        return None

    # Launch plugin (without start)
    try:
        loaded_plugin = main_plugin.Plugin(start, *args)
    except TypeError:
        start_failsafe(*args)

    if isinstance(loaded_plugin, PluginBase):
        msg('OK', 0, 'plugin_checker', 'PluginBase', level=2, slevel='check')
    else:
        msg('ERROR', 2, 'plugin_checker', 'PluginBase', level=0, slevel='check')

    if hasattr(loaded_plugin, "version"): # Check versions
        current = semver.parse_version_info(VERSION)
        plugin = semver.parse_version_info(loaded_plugin.version)

        if current.major > plugin.major: # Check X.y.z
            e_reason = 'Major version change, please update plugin'
            error = (e_reason, VERSION, loaded_plugin.version)
            msg('FATAL', 3, 'plugin_checker', *error, level=0, slevel='check')
            return None
        if current.minor > plugin.minor: # Check x.Y.z
            e_reason = 'New functionalities are availible, please update plugin'
            error = (e_reason, VERSION, loaded_plugin.version)
            msg('WARN', 1, 'plugin_checker', *error, level=1, slevel='check')
        elif current.patch > plugin.patch: # Check x.y.Z
            e_reason = 'Some bugs were fixed, just sayin\''
            error = (e_reason, VERSION, loaded_plugin.version)
            msg('WARN', 1, 'plugin_checker', *error, level=1, slevel='check')
        else: # Version is ok
            e_reason = 'Version ok'
            error = (e_reason, loaded_plugin.version)
            msg('OK', 0, 'plugin_checker', *error, level=2, slevel='check')

    else:
        msg('FATAL', 3, 'plugin_checker', 'No version', level=0, slevel='check')
        return None

    if hasattr(loaded_plugin, '_plugin_info'): # Check if data_dir exists
        msg('OK', 0, 'plugin_checker', '_plugin_info', level=2, slevel='check')
    else:
        e_reason = 'No _plugin_info'
        msg('ERROR', 2, 'plugin_checker', e_reason, level=0, slevel='check')
        return None

    if hasattr(loaded_plugin, "_make_layout"): # Check if make layout exists
        msg('OK', 0, 'plugin_checker', '_make_layout', level=2, slevel='check')
    else:
        e_reason = "No _make_layout"
        msg('ERROR', 2, 'plugin_checker', e_reason, level=0, slevel='check')
        return None

    if hasattr(loaded_plugin, "_start"): # Check if start loop exists
        msg('OK', 0, 'plugin_checker', '_start', level=2, slevel='check')
    else:
        msg('ERROR', 2, 'plugin_checker', 'No _start', level=0, slevel='check')
        return None

    if hasattr(loaded_plugin, "_event_loop"): # Check if event loop exists
        msg('OK', 0, 'plugin_checker', '_event_loop', level=2, slevel='check')
    else:
        e_reason = 'No _event_loop'
        msg('ERROR', 2, 'plugin_checker', e_reason, level=0, slevel='check')
        return None

    return loaded_plugin


def start_failsafe(*args):
    msg('ERROR', 2, 'plugin_loader', 'failsafe plugin activation')
    print_plugin_info(failsafe.Plugin(False, *args))
    loaded_plugin = failsafe.Plugin(True, *args)


def plugin_loader(plugin, start, *args):
    main_plugin = import_plugin(PLUGIN_PACKAGE + "." + plugin.replace(".py", ''))
    loaded_plugin = plugin_checker(main_plugin, False, *args)
    if loaded_plugin:
        print_plugin_info(loaded_plugin)
        try:
            loaded_plugin = main_plugin.Plugin(True, *args)
        except Exception as e:
            # traceback.print_exc() # Keep in case there is a plugin error
            msg(e, 2)
            start_failsafe(*args)
    else:
        start_failsafe(*args)


def print_plugin_info(plugin):
    if hasattr(plugin, "name"):
        msg(plugin.name, 0, "Plugin", level=2, slevel='info')
    else:
        msg("No name", 1, "Plugin", level=1)
    if hasattr(plugin, "author"):
        msg(plugin.author, 0, 'Plugin', level=2, slevel='info')
    else:
        msg("No author", 1, "Plugin", level=1)
    if hasattr(plugin, "version"):
        msg(plugin.version, 0, 'Plugin', level=2, slevel='info')
    else:
        msg("No version", 1, "Plugin", level=1)


def plugin_selector(plugins):
    for num, plugin in enumerate(plugins):
        print(num, plugin, sep=") ")

    select = input("Select plugin: ")
    return plugins[int(select)]


def main():
    plugin_loader(plugin_selector(plugin_scan()))

if __name__ == '__main__':
    main()
