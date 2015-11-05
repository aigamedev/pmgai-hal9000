#
# This file is part of The Principles of Modern Game AI.
# Copyright (c) 2015, AiGameDev.com KG.
#

import vispy                    # Main application support.

import window                   # Terminal input and display.


class Application(object):
    
    def __init__(self):
        # Create and open the window for user interaction.
        self.window = window.TerminalWindow()

        # Print some default lines in the terminal as hints.
        self.window.log('Operator started the chat.', side='left', color='#808080')
        self.window.log('HAL9000 joined.', side='right', color='#808080')

        # Connect the terminal's existing events.
        self.window.events.user_input.connect(self.on_input)
        self.window.events.user_command.connect(self.on_command)

    def on_input(self, evt):
        print(evt.text)
        self.window.log('This is a reply from a bot.', side='right', color='#00805A')

    def on_command(self, evt):
        if evt.text == 'quit':
            vispy.app.quit()
        else:
            self.window.log('Command `{}` unknown.'.format(evt.text), side='left', color='#ff3000')    

    def run(self):
        vispy.app.run()


if __name__ == "__main__":
    vispy.set_log_level('WARNING')
    vispy.use(app='glfw')
    
    app = Application()
    app.run()
