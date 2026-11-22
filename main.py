import math
import random

sample_rate = 256  # Samples per second
duration_seconds = 5
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--frequency", type=int, choices=[6, 10, 18], default=10)
frequency = parser.parse_args().frequency

random.seed(42)  # Use the same random noise each time we run the script

samples = []
for index in range(sample_rate * duration_seconds):
    time_seconds = index / sample_rate
    wave = 20 * math.sin(2 * math.pi * frequency * time_seconds)
    noise = random.gauss(0, 3)
    samples.append(wave + noise)

print(f"Generated {len(samples)} simulated EEG samples.")
print("First 10 samples (µV):", [round(sample, 2) for sample in samples[:10]])
import matplotlib.pyplot as plt

sample_count = 2 * sample_rate
time_axis = [index / sample_rate for index in range(sample_count)]

plt.plot(time_axis, samples[:sample_count])
plt.title("Simulated EEG signal")
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (µV)")
plt.tight_layout()
plt.savefig("eeg-signal.png", dpi=150)
peak_to_peak = max(samples) - min(samples)
print(f"Peak-to-peak range: {peak_to_peak:.2f} µV")
import numpy as np

frequencies = np.fft.rfftfreq(len(samples), d=1 / sample_rate)
magnitudes = np.abs(np.fft.rfft(samples))
peak_index = np.argmax(magnitudes[1:]) + 1

print(f"Dominant frequency: {frequencies[peak_index]:.2f} Hz")
plt.figure()
plt.plot(frequencies[1:], magnitudes[1:])
plt.axvline(frequencies[peak_index], color="red", linestyle="--")
plt.xlim(0, 40)
plt.title("Frequency spectrum of the simulated EEG signal")
plt.xlabel("Frequency (Hz)")
plt.ylabel("FFT magnitude")
plt.tight_layout()
plt.savefig("eeg-spectrum.png", dpi=150)
import csv

with open("eeg-samples.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["time_seconds", "simulated_voltage_uv"])

    for index, voltage in enumerate(samples):
        writer.writerow([index / sample_rate, voltage])

print("Saved eeg-samples.csv")
total_power = np.sum(magnitudes[frequencies > 0] ** 2)
alpha_mask = (frequencies >= 8) & (frequencies <= 13)
alpha_power = np.sum(magnitudes[alpha_mask] ** 2)
alpha_percent = alpha_power / total_power * 100

print(f"Simulated alpha-range power: {alpha_percent:.1f}%")