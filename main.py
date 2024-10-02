import pyaudio
import sounddevice as sd
import numpy as np

DEBUG = True

print(sd.query_devices())

devices = sd.query_devices()

def get_wasapi_index():
    hostapis = sd.query_hostapis()

    for idx, hostapi in enumerate(hostapis):
        if hostapi['name'].lower() == 'windows wasapi':
            return idx
            break

def get_wasapi_device_by_name(device_name):
    for key, value in enumerate(devices):
        if value['name'].strip() != device_name:
            continue
        if value['hostapi'] < get_wasapi_index():
            continue

        if DEBUG:
            print(f" {key}: {value}")

        return key
        break


microphone_id = get_wasapi_device_by_name("Headset Microphone (Realtek(R) Audio)")
headphone_id = get_wasapi_device_by_name("Line 1 Mic (Virtual Audio Cable)")


# Set the duration of the recording in seconds
duration_sec = 5  # Record for 5 seconds
sampling_rate = 48000

print("Recording started...")
# Record audio
audio = sd.rec(int(duration_sec * sampling_rate),
               samplerate=sampling_rate,
               channels=2,
               dtype='float64',
               device=headphone_id)
sd.wait()  # Wait until recording is finished
print("Recording finished.")

# Play back the recorded audio
print("Playing back the recorded audio...")
sd.play(audio, samplerate=sampling_rate)
sd.wait()  # Wait until playback is finished
print("Playback finished.")

