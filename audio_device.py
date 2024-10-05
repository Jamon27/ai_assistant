import sounddevice as sd
import threading
import queue

DEBUG = True


def get_wasapi_index():
    hostapis = sd.query_hostapis()

    for idx, hostapi in enumerate(hostapis):
        if hostapi['name'].lower() == 'windows wasapi':
            return idx
            break


def get_wasapi_device_by_name(device_name):
    devices = sd.query_devices()

    if DEBUG:
        print(devices)

    for key, value in enumerate(devices):
        if value['name'].strip() != device_name:
            continue
        if value['hostapi'] < get_wasapi_index():
            continue

        if DEBUG:
            print(f" {key}: {value}")

        return key
        break


class AudioDevice:
    def __init__(self, name, samplerate=48000, channels=2):
        self.name = name
        self.samplerate = samplerate
        self.channels = channels

        self.id = get_wasapi_device_by_name(name)
        self.queue = queue.Queue()
        self.__stop_event = threading.Event()
        self.thread = self.__create_audio_thread()

    def start_recording(self):
        self.thread.start()

    def __record_audio(self):
        if DEBUG:
            print(f"Recording from {self.name} started...")

        with sd.InputStream(samplerate=self.samplerate,
                            device=self.id,
                            channels=self.channels,
                            dtype='float32',
                            blocksize=1024) as stream:
            while not self.__stop_event.is_set():
                data, overflowed = stream.read(1024)

                if overflowed:
                    print(f"Buffer overflow occurred on device {self.id}")

                self.queue.put(data.copy())

    def __create_audio_thread(self):
        return threading.Thread(target=self.__record_audio)

    def stop_recording(self):
        if DEBUG:
            print(f"Recording from {self.name} finished")

        # Signal the threads to stop
        self.__stop_event.set()
        # Wait for threads to finish
        self.thread.join()

    def record_and_play_audio(self):
        if DEBUG:
            print("Recording started...")
        duration_sec = 5  # Record for 5 seconds

        # Record audio
        audio = sd.rec(int(duration_sec * self.samplerate),
                       samplerate=self.samplerate,
                       channels=self.channels,
                       dtype='float64',
                       device=self.id)
        sd.wait()  # Wait until recording is finished
        if DEBUG:
            print("Recording finished")

        # Play back the recorded audio
        if DEBUG:
            print("Playing back the recorded audio...")
        sd.play(audio, samplerate=self.samplerate)
        sd.wait()  # Wait until playback is finished
        if DEBUG:
            print("Playback finished")