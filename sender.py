import sys
import pygame
import numpy as np
import scipy.io.wavfile as wav

from qpsk_modulate import qpsk_modulate


SAMPLE_RATE = 48000
SIGNAL_FREQ = 20000
AMPLITUDE = 1 / np.sqrt(2)
BIT_DURATION = 0.025
PREAMBLE = '010101010101101000100111010010101011010001000101011001'


def string_to_utf8_binary(input_string):
    utf8_bytes = input_string.encode('utf-8')
    binary_string = ''.join(format(byte, '08b') for byte in utf8_bytes)
    return binary_string


string_origin = sys.argv[1]
string_utf8 = string_to_utf8_binary(string_origin)
string_utf8 = PREAMBLE + string_utf8 + PREAMBLE
qpsk_signal = qpsk_modulate(string_utf8, SAMPLE_RATE, SIGNAL_FREQ, AMPLITUDE, BIT_DURATION)
modulated_signal_filename = './qpsk_signal.wav'
wav.write(modulated_signal_filename, SAMPLE_RATE, qpsk_signal.astype(np.float32))


def play_wav_file(file_path):
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))
    pygame.mixer.quit()
    pygame.quit()


# 播放 WAV 文件
play_wav_file(modulated_signal_filename)

