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
