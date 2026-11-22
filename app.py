import numpy as np
import streamlit as st
import csv
import io
import pandas as pd
st.title("EEG Signal Explorer")
st.write("Explore a simulated signal by changing its frequency.")
uploaded_file = st.file_uploader("Upload EEG CSV", type="csv")
frequency = st.slider("Signal frequency (Hz)", 1, 30, 10)
sample_rate = 256
duration_seconds = 5

time_axis = np.arange(sample_rate * duration_seconds) / sample_rate
random_generator = np.random.default_rng(42)
noise = random_generator.normal(0, 3, len(time_axis))
signal = 20 * np.sin(2 * np.pi * frequency * time_axis) + noise
if uploaded_file is not None:
    uploaded_data = pd.read_csv(uploaded_file)
    required_columns = {"time_seconds", "simulated_voltage_uv"}

    if not required_columns.issubset(uploaded_data.columns):
        st.error("CSV needs time_seconds and simulated_voltage_uv columns.")
        st.stop()

    time_axis = uploaded_data["time_seconds"].to_numpy()
    signal = uploaded_data["simulated_voltage_uv"].to_numpy()
    sample_rate = int(round(1 / np.mean(np.diff(time_axis))))
frequency_bins = np.fft.rfftfreq(len(signal), d=1 / sample_rate)
magnitudes = np.abs(np.fft.rfft(signal))
peak_index = np.argmax(magnitudes[1:]) + 1

st.metric("Detected frequency", f"{frequency_bins[peak_index]:.2f} Hz")
total_power = np.sum(magnitudes[frequency_bins > 0] ** 2)
alpha_mask = (frequency_bins >= 8) & (frequency_bins <= 13)
alpha_power = np.sum(magnitudes[alpha_mask] ** 2)
alpha_percent = alpha_power / total_power * 100

st.metric("Simulated alpha-range power", f"{alpha_percent:.1f}%")
csv_buffer = io.StringIO()
csv_writer = csv.writer(csv_buffer)
csv_writer.writerow(["time_seconds", "simulated_voltage_uv"])
csv_writer.writerows(zip(time_axis, signal))

st.download_button(
    label="Download simulated data as CSV",
    data=csv_buffer.getvalue(),
    file_name="simulated-eeg-data.csv",
    mime="text/csv",
)
st.line_chart({"Simulated voltage (µV)": signal[: 2 * sample_rate]})
st.caption("This dashboard uses simulated data, not headset measurements.")