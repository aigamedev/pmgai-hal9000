#
# This file is part of The Principles of Modern Game AI.
# Copyright (c) 2015, AiGameDev.com KG.
#

import nuclai.bootstrap         # Demonstration specific setup.
import vispy.scene              # Canvas & visuals for rendering.
import vispy.util.event         # Events and observer support.

CONSOLE_PREFIX = '> '
CONSOLE_LINEHEIGHT = 40.0
CONSOLE_LINEOFFSET = 16.0
CONSOLE_MARGIN = 16.0


class TextEvent(vispy.util.event.Event):
    """Simple data-structure to store a text string, as processed by the terminal window.
    """

    def __init__(self, text):
        super(TextEvent, self).__init__('text_event')
        self.text = text


class TerminalWindow(object):
    """Creates and manages a window used for terminal input. You can setup notifications via
    `self.events` that emits notifications for user inputs and user commands. 
    """

    def __init__(self):
        """Constructor sets up events, creates a canvas and data for processing input.
        """ 
        self.events = vispy.util.event.EmitterGroup(
                                user_input=TextEvent,
                                user_command=TextEvent)
 
        self._create_canvas()
        self._create_terminal()

    def _create_canvas(self):
        """Initialize the Vispy scene and a canvas, connect up the events to this object.
        """
        self.canvas = vispy.scene.SceneCanvas(
                                title='HAL9000 Terminal - nucl.ai Courses',
                                size=(1280, 720),
                                bgcolor='#F0F0F0',
                                show=False,
                                keys='interactive')
        
        self.widget = self.canvas.central_widget
        self.widget.set_transform('matrix')
        self.widget.transform.translate((0.0, -CONSOLE_LINEOFFSET))

        vispy.scene.visuals.GridLines(parent=self.widget, scale=(0.0, 15.984/CONSOLE_LINEHEIGHT))

        self.canvas.show(visible=True)
        self.canvas.events.mouse_press()            # HACK: Layout workaround for bug in Vispy 0.5.0.

        self.old_size = self.canvas.size
        self.canvas.events.resize.connect(self.on_resize)
        self.canvas.events.key_press.connect(self.on_key_press)

    def _create_terminal(self):
        """Setup everything that's necessary for processing key events and the text.
        """
        self.text_buffer = ''
        self.entry_offset = CONSOLE_LINEOFFSET - CONSOLE_LINEHEIGHT / 2 + self.canvas.size[1] 
        self.entry_blink = 0
        self.entries = []

        self.log(CONSOLE_PREFIX, color='#1463A3')

        timer = vispy.app.Timer(interval=1.0 / 3.0)
        timer.connect(self.on_blink)
        timer.start()

    def scroll(self, height):
        self.widget.transform.translate((0.0, -height))

    def on_resize(self, evt):
        self.scroll(self.old_size[1] - evt.size[1])
        self.old_size = evt.size

    def log(self, text, side='left', color='#1463A3'):
        assert side in ('left', 'right', 'center')

        if side == 'center':
            position = self.canvas.size[0] / 2
        elif side == 'left':
            position = CONSOLE_MARGIN
        else:
            position = self.canvas.size[0] - CONSOLE_MARGIN

        entry = vispy.scene.visuals.Text(parent=self.widget,
                                         text=text,
                                         face='Questrial',
                                         color=color,
                                         bold=False,
                                         font_size=10 * self.canvas.pixel_scale,
                                         anchor_x=side,
                                         anchor_y='bottom',
                                         pos=[position, self.entry_offset, 0.0])
        self.entries.append(entry)
        self.scroll(CONSOLE_LINEHEIGHT)
        self.entry_offset += CONSOLE_LINEHEIGHT
        
        self.entries[0].pos[0][1] = self.entry_offset

    def show_input(self, text):
        self.entries[0].text = CONSOLE_PREFIX + text
        self.entries[0].update()

    def on_key_press(self, evt):
        if evt.text:
            self.on_key_char(evt.text)

        c = evt.key
        if c.name == 'Enter' and self.text_buffer != '':
            if self.text_buffer.startswith('/'):
                self.events.user_command(TextEvent(self.text_buffer[1:]))
            else:
                self.log(self.text_buffer, side='left')
            self.text_buffer = ''

        if c.name == 'Backspace':
            self.text_buffer = self.text_buffer[:-1]

        self.show_input(self.text_buffer)       

    def on_key_char(self, text):
        self.text_buffer += text
        self.show_input(self.text_buffer)

    def on_blink(self, _):
        if (self.entry_blink%2) == 0:
            self.show_input(self.text_buffer+'_')
        if (self.entry_blink%2) == 1:
            self.show_input(self.text_buffer)
        self.entry_blink += 1
