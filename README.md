# EEG Signal Explorer

An educational Streamlit app for exploring simulated EEG-like signals and CSV data.

## Features

- Adjust the frequency of a simulated signal.
- Upload a CSV file with `time_seconds` and `simulated_voltage_uv` columns.
- View a waveform and estimated dominant frequency.
- See the signal power in the 8–13 Hz alpha range.
- Download the simulated data as a CSV file.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install streamlit numpy pandas
streamlit run app.py