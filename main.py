from model import windows
from model import Cow

if __name__ == '__main__':
    win = windows.Window()

    win.init()

    cow = Cow()

    win.add_object(cow)

    win.run()
