#
# This demo is part of "The Principles of Modern Game AI"
# Copyright (c) 2015, AiGameDev.com KG.
#

import os
import random

import nuclai.bootstrap         # Demonstration specific setup.
import vispy.scene              # Canvas & visuals for rendering.


CONSOLE_PREFIX = '> '
CONSOLE_LINEHEIGHT = 40.0
CONSOLE_LINEOFFSET = 16.0
CONSOLE_MARGIN = 16.0


class Application(object):
    
    def __init__(self):
        self.canvas = vispy.scene.SceneCanvas(
                                title='nucl.ai Course',
                                size=(1280, 720),
                                bgcolor='#F0F0F0',
                                show=False,
                                keys='interactive')

        self.widget = self.canvas.central_widget
        self.widget.set_transform('matrix')
        self.widget.transform.translate((0.0, -CONSOLE_LINEOFFSET))

        vispy.scene.visuals.GridLines(parent=self.widget, scale=(0.0, 15.984/CONSOLE_LINEHEIGHT))

        self.text_buffer = ''
        self.entry_offset = CONSOLE_LINEOFFSET - CONSOLE_LINEHEIGHT / 2 + self.canvas.size[1] 
        self.entry_blink = 0
        self.entries = []
        self.old_size = self.canvas.size

        self.log(CONSOLE_PREFIX, color='#00805A')
        self.log('Operator started the chat.', side='left', color='#808080')
        self.log('HAL9000 joined.', side='right', color='#808080')
        
        self.canvas.events['resize'].connect(self.on_resize)
        self.canvas.events['key_press'].connect(self.on_key_press)
        self.canvas.events['key_release'].connect(self.on_key_release)
        self.canvas.show(visible=True)
        
        # HACK: Bug in VisPy 0.5.0 requires a click for layout to occur.
        self.canvas.events.mouse_press()

    def on_resize(self, evt):
        self._scroll(self.old_size[1] - evt.size[1])
        self.old_size = evt.size

    def on_type(self, text):
        self.entries[0].text = CONSOLE_PREFIX + text
        self.entries[0].update()

    def on_command(self, cmd):
        if cmd == 'quit':
            vispy.app.quit()

    def on_key_release(self, evt):
        pass

    def on_key_press(self, evt):
        if evt.text:
            self.on_key_char(evt.text)

        c = evt.key
        if c.name == 'Enter' and self.text_buffer != '':
            if self.text_buffer.startswith('/'):
                self.on_command(self.text_buffer[1:])
            else:
                self.log(self.text_buffer, side='left')
            self.text_buffer = ''
        if c.name == 'Backspace':
            self.text_buffer = self.text_buffer[:-1]
        self.on_type(self.text_buffer)       

    def on_key_char(self, text):
        self.text_buffer += text
        self.on_type(self.text_buffer)

    def process(self, _):
        if random.random() < 0.02:
            self.log('This is a reply from a bot.', side='right', color='#1463A3')

        if (self.entry_blink%2) == 0:
            self.on_type(self.text_buffer+'_')
        if (self.entry_blink%2) == 1:
            self.on_type(self.text_buffer)
        self.entry_blink += 1
        
    def _scroll(self, height):
        self.widget.transform.translate((0.0, -height))

    def log(self, text, side='left', color='#00805A'):
        assert side in ('left', 'right')
        position = CONSOLE_MARGIN if side=='left' else self.canvas.size[0] - CONSOLE_MARGIN
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
        self._scroll(CONSOLE_LINEHEIGHT)
        self.entry_offset += CONSOLE_LINEHEIGHT
        
        self.entries[0].pos[0][1] = self.entry_offset

    def run(self):
        timer = vispy.app.Timer(interval=1.0 / 3.0)
        timer.connect(self.process)
        timer.start()
    
        vispy.app.run()


if __name__ == "__main__":
    vispy.set_log_level('WARNING')
    vispy.use(app='glfw')
    
    app = Application()
    app.run()
