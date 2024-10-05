import audio_utils as au

# ToDo: visualisation of recording

mic_name = "Headset Microphone (Realtek(R) Audio)"
headphones_name = "Line 1 Mic (Virtual Audio Cable)"

mixed_audio = au.get_mixed_audio_from_2_devices(mic_name, headphones_name)
au.save_audio_to_file(mixed_audio)
