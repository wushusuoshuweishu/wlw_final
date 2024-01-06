import numpy as np


sample_rate = 48000
pulse_freq = 20000
amplitude = 1
initial_phase = 0
pulse_duration = 0.01
bit_0_interval = 0.2
bit_1_interval = 0.5


# 生成指定长度的脉冲信号
def generate_pulse(frequency, duration, phase, amplitude=1):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)


# 调制函数
def modulate_pulse(binary_string):
    signal = []

    # 在最开始添加一个脉冲
    initial_pulse = generate_pulse(pulse_freq, pulse_duration, initial_phase, amplitude)
    signal.extend(initial_pulse)
    last_end_time = pulse_duration
    for bit in binary_string:
        if bit == '0':
            interval = bit_0_interval
        else:
            interval = bit_1_interval
        start_time = last_end_time + interval - pulse_duration
        pulse = generate_pulse(pulse_freq, pulse_duration, initial_phase, amplitude)

        # 在脉冲后添加对应长度的间隔
        silence_duration = start_time - last_end_time
        silence = np.zeros(int(silence_duration * sample_rate))
        signal.extend(silence)
        signal.extend(pulse)
        last_end_time = start_time + pulse_duration
    return np.array(signal)


# modulated_signal = modulate_pulse(binary_input)
# modulated_signal_normalized = np.int16(modulated_signal / np.max(np.abs(modulated_signal)) * 32767)
# wav_file_name = './modulated_signal.wav'
# write(wav_file_name, sample_rate, modulated_signal_normalized)
#
#
# # 下面代码将生成含噪音的信号
# snr_db = [20, 10, 5, 0]
#
#
# def calculate_noise_variance(signal_power, snr_db):
#     snr_linear = 10 ** (snr_db / 10)
#     noise_variance = signal_power / snr_linear
#     return noise_variance
#
#
# modulated_signal = modulate_pulse(binary_input)
#
# # 计算信号的强度
# signal_power = np.mean(modulated_signal ** 2)
#
# # 将不同强度的AWGN加到信号上，并存储为wav
# for snr in snr_db:
#     # 根据信噪比和信号强度计算噪音强度并生成噪音
#     noise_variance = calculate_noise_variance(signal_power, snr)
#     noise = np.random.normal(0, np.sqrt(noise_variance), modulated_signal.shape)
#
#     # 将噪音加到信号上
#     noisy_signal = modulated_signal + noise
#
#     # 正则化信号并输出到wav中
#     noisy_signal_normalized = np.int16(noisy_signal / np.max(np.abs(noisy_signal)) * 32767)
#     wav_file_name = f'modulated_signal_snr_{snr}dB.wav'
#     write(wav_file_name, sample_rate, noisy_signal_normalized)
