import sys
import pygame
import numpy as np
# import scipy.io.wavfile as wav

# from qpsk_modulate import qpsk_modulate
from modulate_pulse import modulate_pulse
from scipy.io.wavfile import write


SAMPLE_RATE = 48000
SIGNAL_FREQ = 20000
AMPLITUDE = 1000 / np.sqrt(2)
BIT_DURATION = 0.025
# PREAMBLE = '01010101010111011011010000101011010000101'


def string_to_binary(input_string):
    binary_string = ''.join(format(ord(char), '08b') for char in input_string)
    return binary_string


string_origin = sys.argv[1]
string_utf8 = string_to_binary(string_origin)
# string_utf8 = PREAMBLE + string_utf8 + PREAMBLE
# qpsk_signal = qpsk_modulate(string_utf8, SAMPLE_RATE, SIGNAL_FREQ, AMPLITUDE, BIT_DURATION)
# modulated_signal_filename = './qpsk_signal.wav'
# wav.write(modulated_signal_filename, SAMPLE_RATE, qpsk_signal.astype(np.float32))
print(string_utf8)
modulated_signal = modulate_pulse(string_utf8)
modulated_signal_normalized = np.int16(modulated_signal / np.max(np.abs(modulated_signal)) * 3276700)
wav_file_name = './modulated_signal.wav'
write(wav_file_name, SAMPLE_RATE, modulated_signal_normalized)


def play_wav_file(file_path):
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))
    pygame.mixer.quit()
    pygame.quit()


# 播放 WAV 文件
# play_wav_file(modulated_signal_filename)
play_wav_file(wav_file_name)

