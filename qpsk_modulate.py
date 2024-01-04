import numpy as np


SAMPLE_RATE = 48000
SIGNAL_FREQ = 20000
AMPLITUDE = 1000 / np.sqrt(2)
BIT_DURATION = 0.025


def qpsk_modulate(bit_sequence, sample_rate, signal_freq, amplitude, bit_duration):
    t = np.arange(0, bit_duration, 1 / sample_rate)
    signal = np.array([])

    for bit1, bit2 in zip(bit_sequence[0::2], bit_sequence[1::2]):
        if bit1 == '1':
            modulated_bit_i = amplitude * np.sin(2 * np.pi * signal_freq * t + np.pi)  # 相位为pi
        else:
            modulated_bit_i = amplitude * np.sin(2 * np.pi * signal_freq * t)  # 相位为0
        if bit2 == '1':
            modulated_bit_q = amplitude * np.cos(2 * np.pi * signal_freq * t + np.pi)  # 相位为pi
        else:
            modulated_bit_q = amplitude * np.cos(2 * np.pi * signal_freq * t)  # 相位为0
        modulated_bit = modulated_bit_i + modulated_bit_q
        signal = np.concatenate([signal, modulated_bit])

    return signal
