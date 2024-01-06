from scipy.io.wavfile import read
import numpy as np


pulse_duration = 0.01
bit_0_interval = 0.2
bit_1_interval = 0.5


def demodulate_pulse(file_path, threshold=150):
    sample_rate, data = read(file_path)
    normalized_data = data / 32767.0  # ??????????????
    binary_string = ""
    normalized_data = detect_first_pulse(normalized_data, sample_rate)
    last_pulse_end = 0

    while (last_pulse_end + bit_1_interval) * sample_rate < len(normalized_data):
        bit_0_pulse_possibility = np.sum(np.abs(normalized_data[
                                                int((last_pulse_end + bit_0_interval) * sample_rate):int(
                                                    (last_pulse_end + bit_0_interval) * sample_rate) + int(
                                                    sample_rate * pulse_duration)]))
        bit_1_pulse_possibility = np.sum(np.abs(normalized_data[
                                                int((last_pulse_end + bit_1_interval) * sample_rate):int(
                                                    (last_pulse_end + bit_1_interval) * sample_rate) + int(
                                                    sample_rate * pulse_duration)]))
        if bit_1_pulse_possibility > bit_0_pulse_possibility:
            binary_string += '1'
            last_pulse_end += (bit_1_interval + pulse_duration)
        else:
            binary_string += '0'
            last_pulse_end += (bit_0_interval + pulse_duration)
    return binary_string

    for i in range(0, len(normalized_data), int(sample_rate * pulse_duration)):
        # print(np.sum(np.abs(normalized_data[i:i + int(sample_rate * pulse_duration)])))
        # print(i)
        # continue

        # 每次检测当前0.1秒是不是脉冲，如果是脉冲且不是第一个脉冲，则检测当前脉冲与上一个脉冲之间的距离，根据距离离哪种bit更近判定当前是哪个bit
        if np.sum(np.abs(normalized_data[i:i + int(sample_rate * pulse_duration)])) > threshold:
            current_pulse_end = i / sample_rate + pulse_duration
            if last_pulse_end:
                if current_pulse_end - last_pulse_end > (bit_0_interval + bit_1_interval) / 2:
                    binary_string += '1'
                else:
                    binary_string += '0'
            last_pulse_end = current_pulse_end
    return binary_string


def detect_first_pulse(data, sample_rate):
    threshold = 0.01
    with open('output_0.2_0.5.txt', 'w') as file:
        for i in range(0, len(data) - int(pulse_duration * sample_rate)):
            amplitude = np.sum(np.abs(data[i:i + int(sample_rate * pulse_duration)]))
            print(data[i], file=file)
            if amplitude > threshold:
                print('FIRST PULSE FOUND AT ' + str(i))
                return data[i:]
    print('FIRST PULSE NOT FOUND')
    return data

#
# def detect_every_possible_pulse(data, sample_rate):
#     last_position =
#     for i in range(int(pulse_duration * sample_rate), len(data) - int(pulse_duration * sample_rate)):
#         next_position = np.sum(np.abs(data[i:i + int(sample_rate * pulse_duration)]))
