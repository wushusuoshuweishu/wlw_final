import numpy as np
import scipy.io.wavfile as wav


SIGNAL_FREQ = 20000
AMPLITUDE = 1 / np.sqrt(2)
BIT_DURATION = 0.025


def qpsk_demodulate(wav_filename, signal_freq, bit_duration):
    sample_rate, signal = wav.read(wav_filename)
    samples_per_bit = int(sample_rate * bit_duration)

    binary_sequence = ''

    t = np.arange(0, bit_duration, 1 / sample_rate)

    # 生成信号
    reference_carrier_i_0 = AMPLITUDE * np.sin(2 * np.pi * signal_freq * t)
    reference_carrier_i_1 = AMPLITUDE * np.sin(2 * np.pi * signal_freq * t + np.pi)
    reference_carrier_q_0 = AMPLITUDE * np.cos(2 * np.pi * signal_freq * t)
    reference_carrier_q_1 = AMPLITUDE * np.cos(2 * np.pi * signal_freq * t + np.pi)

    reference_carrier_00 = reference_carrier_i_0 + reference_carrier_q_0
    reference_carrier_01 = reference_carrier_i_0 + reference_carrier_q_1
    reference_carrier_10 = reference_carrier_i_1 + reference_carrier_q_0
    reference_carrier_11 = reference_carrier_i_1 + reference_carrier_q_1

    for i in range(0, len(signal), samples_per_bit):
        # 取对应于一个bit长度的数据
        bit_signal = signal[i:i + samples_per_bit]

        # 分别将bit为0和1的信号与当前信号计算相关性
        correlation_00 = np.mean(np.correlate(bit_signal, reference_carrier_00, mode='valid'))
        correlation_01 = np.mean(np.correlate(bit_signal, reference_carrier_01, mode='valid'))
        correlation_10 = np.mean(np.correlate(bit_signal, reference_carrier_10, mode='valid'))
        correlation_11 = np.mean(np.correlate(bit_signal, reference_carrier_11, mode='valid'))

        correlations = [correlation_00, correlation_01, correlation_10, correlation_11]

        # 根据相关性判断当前bit
        if correlation_00 >= max(correlations):
            bits = '00'
        elif correlation_01 >= max(correlations):
            bits = '01'
        elif correlation_10 >= max(correlations):
            bits = '10'
        else:
            bits = '11'
        binary_sequence += bits

    return binary_sequence
