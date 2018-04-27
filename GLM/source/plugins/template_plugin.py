import json
from ..libs.slide import *
from ..libs.text import Text
from ..libs.rainbow import msg
from ..libs.screen import Screen
from ..libs.templater import Templater
from ..libs.webclient import WebClient

class Plugin():
    def __init__(self, process_events, start, matrix, show, guishow):
        super(Plugin, self).__init__()
        self.name = "Template Plugin"
        self.version = "0.0.3"
        self.author = "Infected"

        if start: # If start is True
            # Required
            self.process_events = process_events # Event queue
            self.screen = Screen( # Create matrix screen
                matrix=matrix,
                show=show,
                guishow=guishow,
                fps=30
                )
            self.client = WebClient(process_events) # Initialize web client

            self.make_layout() # Create screen layout and process web template
            self._start() # Start plugin loop

    def refresh_template(self):
        """ Render the template again and send it to the client
        """
        self.data = self.templater.render()
        self.client.set_data(self.data)

    def make_layout(self):
        self.template = """\
        {{ title;label;My Input Label }}{{ matrix_text;input;example }}{# Comment #}
        {% <h1>Raw html</h1> %}{# ID cannot start with html_ #}
        {{submit;button;My Button}}
        """
        self.templater = Templater(self.template)
        self.templater.parse()
        self.refresh_template()

        self.sample_text = Text('example')
        self.screen.add(self.sample_text, refresh=False, x=6, y=7, name='entry')


    def _start(self):
        # Plugin loop
        msg("STARTING PLUGIN", level=1)
        loop = True
        self.client.handle_data() # Start self.client
        while loop:
            if self.client.get_exit():
                msg("ENDING PLUGIN", 3, level=1)
                loop = False
            else:
                # Plugin loop
                event_json = self.client.get_event() # Get events (non blocking)
                if event_json:
                    event = json.loads(event_json)
                    if 'matrix_text' in event.keys():
                        self.sample_text.edit(event['matrix_text'].lower())
                        self.templater.edit_value(
                            'matrix_text',
                            event['matrix_text'].lower()
                            )
                        self.refresh_template()
                    if 'submit' in event.keys():
                        self.sample_text.edit('reset')
                        self.templater.edit_value('matrix_text', 'reset')
                        self.refresh_template()

                self.screen.refresh()
