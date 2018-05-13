## 0.11.0
* Screen insert method
* New Screen.add arguments order
* Screen removes by name instead of id's

* Example
    ```python
    screen.add(Image, "Name", **kwargs)
    screen.insert("Name", OtherImage, "OtherName", **kwargs)
    screen.remove("Name", "OtherName")
    ```

* Minimal plugin:
> Same as 0.10.0

## 0.10.0
* Added a standalone launcher for this project __./lmpm__
* Added an image loader
* PluginBase is now an __abstract class__
* Plugins need a __\_plugin_info__ method and add the information there instead of in the constructor
* __self.data_dir__ is now required to be in \_plugin_info and represents the directory where data like .pbm images are saved for a plugin (_LMPM/GLM/plugindata/your plugin data dir_)
* some bugs fixed on the failsafe plugin and some other places

* minimal plugin:
    ```python
    from ..libs.pluginbase import PluginBase

    class Plugin(PluginBase):
        def __init__(self, start, *args):
            super().__init__(start, *args)

        def _plugin_info(self):
            """Required informations about the plugin
            """
            self.version = "0.10.0"
            self.data_dir = "minimal"

        def _make_layout(self):
            pass

        def _event_loop(self, event):
            pass

        def _start(self):
            pass
    ```

## 0.9.0
* Plugins now inherit from __PluginBase__, it's now pretty simple to make plugins

* minimal plugin:
    ```python
    from ..libs.pluginbase import PluginBase

    class Plugin(PluginBase):
        def __init__(self, start, *args):
            super().__init__(start, *args)
            self.version = "0.9.0"

        def _make_layout(self):
            """Here is where the ingredients to bake a
            great plugin and webview template go
            """
            pass

        def _event_loop(self, event):
            """Event getter
            before every _start cycle
            """
            pass

        def _start(self):
            """Main loop of the plugin
            this includes a refresh of self.screen
            """
            pass
    ```

## 0.0.3
* Plugins and libs have to use relative imports

* example:

    ```python
    from ..libs.screen import Screen
    from ..libs.text import Text

    class Plugin():
        def __init__(self, matrix=True, show=False, guishow=False):
            super(Plugin, self).__init__()
            self.name = "Example Plugin"
            self.version = "0.0.3"

            self.sample_text = Text('sample text')

            self.screen = Screen(matrix=matrix, show=show)
            self.screen.add(self.sample_text, refresh=False)

        def start(self):
            self.screen.refresh()
    ```

## 0.0.2
* The Plugin class is now required to launch the plugin

* example:

    ```python
    from libs.screen import Screen

    class Plugin():
        def __init__(self, matrix=True, show=False, guishow=False):
            super(Plugin, self).__init__()
            self.name = "Example Plugin"
            self.version = "0.0.2"
            self.screen = Screen(matrix=matrix, show=show)

        def start(self):
            self.screen.refresh()
    ```

## 0.0.1
* plugins are now in the *plugins* folder.
* each updated plugin must have a __self.version__ attribute set to the last version value.
* remove the standalone code of the plugin as it has to be launched from glm.py

* example:

    ```python
    from libs.screen import Screen

    class Plugin():
        def __init__(self, matrix=True, show=False, guishow=False):
            super(Plugin, self).__init__()
            self.version = "0.0.1"
            self.screen = Screen(matrix=matrix, show=show)

        def start(self):
            self.screen.refresh()
    ```
