# SDO Data Fetcher

A Python script to fetch the latest solar images from NASA's Solar Dynamic Observatory (SDO) using the Helioviewer API.

## Features

- ✨ Fetch latest SDO images in real-time
- 🌈 Support for multiple wavelengths (AIA 94Å - 1700Å)
- 🧲 HMI magnetogram and continuum data
- 📊 Automatic metadata saving
- 🎯 Command-line interface
- 📦 Batch download multiple wavelengths

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

Fetch the latest AIA 171Å image (default):
```bash
python sdo_data_fetcher.py
```

### Specific Wavelength

```bash
python sdo_data_fetcher.py --source AIA_304
```

### Download Multiple Wavelengths

```bash
python sdo_data_fetcher.py --multiple
```

### List Available Sources

```bash
python sdo_data_fetcher.py --list
```

### Custom Output Directory

```bash
python sdo_data_fetcher.py --output my_solar_data
```

### Check Latest Data Timestamp

```bash
python sdo_data_fetcher.py --timestamp
```

## Available Data Sources

| Source | Description |
|--------|-------------|
| AIA_94 | Hot flare plasma (~6 million K) |
| AIA_131 | Flaring regions (~10 million K) |
| AIA_171 | Quiet corona and coronal loops (~600,000 K) |
| AIA_193 | Hot plasma in active regions (~1.5 million K) |
| AIA_211 | Active regions (~2 million K) |
| AIA_304 | Chromosphere and prominence (~50,000 K) |
| AIA_335 | Active regions (~2.5 million K) |
| AIA_1600 | Upper photosphere and lower transition region |
| AIA_1700 | Temperature minimum and photosphere |
| HMI_Continuum | Visible light from solar surface |
| HMI_Magnetogram | Magnetic field measurements |

## Using in Your Code

```python
from sdo_data_fetcher import SDODataFetcher

# Initialize fetcher
fetcher = SDODataFetcher(output_dir="my_data")

# Get latest AIA 171Å image
metadata = fetcher.get_latest_image(source="AIA_171")

if metadata:
    print(f"Image saved to: {metadata['filepath']}")
    print(f"Description: {metadata['description']}")

# Download multiple wavelengths
fetcher.download_multiple_wavelengths(['AIA_171', 'AIA_304', 'HMI_Magnetogram'])
```

## Output

The script creates:
- **PNG images** - Latest solar observations
- **JSON metadata** - Timestamp, source info, and URLs

Example output structure:
```
sdo_data/
├── SDO_AIA_171_20260206_143025.png
├── SDO_AIA_171_20260206_143025.json
├── SDO_AIA_304_20260206_143030.png
└── SDO_AIA_304_20260206_143030.json
```

## API Source

This script uses the [Helioviewer API](https://api.helioviewer.org/docs/v2/), which provides access to solar imagery from multiple missions including SDO.

## About SDO

NASA's Solar Dynamics Observatory (SDO) is a mission launched in 2010 to study the Sun. It provides:
- Images every 12 seconds in 10 different wavelengths
- 4096x4096 pixel resolution
- Magnetic field measurements
- Continuous 24/7 observations

## License

This script is provided as-is for educational and research purposes.
