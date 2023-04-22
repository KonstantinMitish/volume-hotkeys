from time import sleep

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from pynput.keyboard import Listener, Key


def on_press(key):
    if type(key) == Key:
        return
    if key.vk == 169:
        queue.append(-1)
    elif key.vk == 12:
        queue.append(1)


def change_volume(session, coef):
    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
    new_vol = volume.GetMasterVolume() + val * coef
    new_vol = max(min(new_vol, 1), 0)
    volume.SetMasterVolume(new_vol, None)
    print(f"Set {session.Process.name()} to {new_vol}")


if __name__ == "__main__":
    queue = []
    listener = Listener(on_press=on_press)
    listener.start()
    while True:
        while len(queue):
            val = queue.pop()
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                if session.Process and session.Process.name() == "Y.Music.exe":
                    change_volume(session, 0.1)
                if session.Process and session.Process.name() == "wmplayer.exe":
                    change_volume(session, 0.01)
        sleep(0.1)
