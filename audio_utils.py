import numpy as np
import queue
from scipy.io.wavfile import write
from audio_device import AudioDevice


def get_mixed_frames(mic_queue, headphones_queue, duration_sec):
    # List to hold mixed audio data
    mixed_frames = []
    # Calculate the number of chunks to read
    num_chunks = int(48000 / 1024 * duration_sec)

    for _ in range(num_chunks):
        # Get audio data from queues
        try:
            mic_data = mic_queue.get(timeout=1)
            headphones_data = headphones_queue.get(timeout=1)
        except queue.Empty:
            print("Queue is empty. Recording might have stopped unexpectedly.")
            break

        # Mix the audio data
        mixed_data = (mic_data + headphones_data) / 2.0  # Simple average

        mixed_frames.append(mixed_data)

    return mixed_frames


def get_mixed_audio_from_2_devices(mic_name, headphones_name):
    microphone = AudioDevice(mic_name)
    headphone = AudioDevice(headphones_name)

    microphone.start_recording()
    headphone.start_recording()

    mixed_frames = get_mixed_frames(microphone.queue, headphone.queue, 5)
    microphone.stop_recording()
    headphone.stop_recording()
    mixed_audio = np.concatenate(mixed_frames)

    return mixed_audio


def save_audio_to_file(audio, output_filename="combined_output.wav"):
    # Save the mixed audio to a WAV file
    write(output_filename, 48000, audio)

    print(f"Audio saved to {output_filename}")
