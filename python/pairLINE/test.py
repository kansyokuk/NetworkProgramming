from pyhooked import Hook, KeyboardEvent, MouseEvent
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

def handle_events(args):
    if isinstance(args, KeyboardEvent):
        print(args.key_code, args.current_key, args.event_type)

hk = Hook()  # make a new instance of PyHooked
hk.handler = handle_events  # add a new shortcut ctrl+a, or triggered on mouseover of (300,400)
hk.hook()  # hook into the events, and listen to the press