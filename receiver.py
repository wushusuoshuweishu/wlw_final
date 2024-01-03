import pyaudio
import wave
import sys

from qpsk_demodulate import qpsk_demodulate


# 配置录音参数
FORMAT = pyaudio.paInt16
CHANNELS = 1  # 单声道
RATE = 48000  # 采样率 (samples per second)
CHUNK = 1024  # 缓冲区大小
RECORD_SECONDS = float(sys.argv[1])  # 录制的时长
OUTPUT_FILENAME = "output.wav"

SIGNAL_FREQ = 20000
BIT_DURATION = 0.025

audio = pyaudio.PyAudio()

demodulated_binary_data = qpsk_demodulate('./qpsk_signal.wav', SIGNAL_FREQ, BIT_DURATION)
print(demodulated_binary_data)
exit(0)

try:
    # 打开音频输入流
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("录音中...")

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束.")

    # 关闭音频输入流
    stream.stop_stream()
    stream.close()

    # 停止音频设备
    audio.terminate()

    # 保存录音数据为.wav文件
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        print(f"录音已保存为{OUTPUT_FILENAME}")

except KeyboardInterrupt:
    print("录音已被中断")

finally:
    audio.terminate()

demodulated_binary_data = qpsk_demodulate('./qpsk_signal.wav', SIGNAL_FREQ, BIT_DURATION)

print(demodulated_binary_data)
