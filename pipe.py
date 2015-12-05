import os
import cmd



import cmd, sys


class TerminalShell(cmd.Cmd):
    intro = 'Terminal emulator.   Type help or ? to list commands.\n'
    prompt = '> '
    file = None

    def __init__(self):
        super().__init__(self)
        fd = os.open('\\\\.\\pipe\\debian', os.O_RDWR)

        self.f = os.fdopen(fd, "wb")
        self.last_card = None
        self.led0 = 0
        self.led1 = 0


    def do_test(self, arg):
        "Test command"
        self.f.write(arg.encode("latin-1"))
        self.f.flush()
        



if __name__ == '__main__':
    TerminalShell().cmdloop()

