# 🌞 SDO Data Fetcher

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NASA SDO](https://img.shields.io/badge/NASA-SDO-red.svg)](https://sdo.gsfc.nasa.gov/)

A powerful Python application to fetch real-time solar images from NASA's **Solar Dynamics Observatory (SDO)**. Get the latest solar data in seconds with support for all AIA wavelengths and HMI instruments!

<p align="center">
  <img src="https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171.jpg" width="300" alt="SDO AIA 171">
  <img src="https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0304.jpg" width="300" alt="SDO AIA 304">
</p>

## ✨ Features

- 🔴 **Live Data** - Fetches the latest SDO observations (updated every 12 seconds!)
- 🌈 **11 Wavelengths** - All AIA channels (94Å - 1700Å) plus HMI magnetogram
- 📊 **Auto Metadata** - Each image includes JSON metadata with observation details
- ⚡ **Fast & Reliable** - Direct from NASA servers, downloads in 1-2 seconds
- 🎯 **CLI & Python API** - Use from command line or integrate into your code
- 📦 **Batch Downloads** - Get multiple wavelengths simultaneously
- 🔬 **Space Weather Ready** - Perfect for monitoring solar activity

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/sdo-data-fetcher.git
cd sdo-data-fetcher

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Get the latest AIA 171Å image (default)
python sdo_fetcher_v2.py

# Get a specific wavelength
python sdo_fetcher_v2.py --source AIA_304

# Download multiple wavelengths
python sdo_fetcher_v2.py --multiple

# List all available sources
python sdo_fetcher_v2.py --list
```

## 📡 Available Data Sources

| Source | Wavelength | Temperature | Best For |
|--------|------------|-------------|----------|
| **AIA_94** | 94 Å | ~6 MK | Hot flare plasma |
| **AIA_131** | 131 Å | ~10 MK | Flaring regions |
| **AIA_171** | 171 Å | ~0.6 MK | Quiet corona, coronal loops ⭐ |
| **AIA_193** | 193 Å | ~1.5 MK | Active regions |
| **AIA_211** | 211 Å | ~2 MK | Active regions |
| **AIA_304** | 304 Å | ~0.05 MK | Prominences, filaments |
| **AIA_335** | 335 Å | ~2.5 MK | Active regions |
| **AIA_1600** | 1600 Å | - | Upper photosphere |
| **AIA_1700** | 1700 Å | - | Temperature minimum |
| **HMI_Continuum** | Visible | - | Solar surface |
| **HMI_Magnetogram** | - | - | Magnetic fields |

## 💡 Usage Examples

### Command Line

```bash
# Monitor solar activity
python sdo_fetcher_v2.py --source AIA_193

# Space weather check
python sdo_advanced_examples.py  # Choose option 3

# Download full comparison set
python sdo_advanced_examples.py  # Choose option 1
```

### Python Code

```python
from sdo_fetcher_v2 import SDOFetcher

# Initialize fetcher
fetcher = SDOFetcher(output_dir="solar_images")

# Download latest image
metadata = fetcher.get_latest_image_direct(source="AIA_171")

if metadata:
    print(f"Image saved: {metadata['filepath']}")
    print(f"Observation time: {metadata['last_modified']}")

# Download multiple wavelengths
sources = ["AIA_171", "AIA_193", "AIA_304", "HMI_Magnetogram"]
results = fetcher.download_multiple(sources)
```

## 🎓 Advanced Features

The `sdo_advanced_examples.py` script includes:

1. **Multi-wavelength comparison sets** - Download complementary wavelengths for analysis
2. **Active region monitoring** - Track solar flares and active regions
3. **Space weather quick check** - Rapid assessment tool
4. **Prominence monitoring** - Track eruptions and filaments
5. **Continuous monitoring** - Automated periodic downloads
6. **Monitoring daemon generator** - Create long-running monitoring scripts

```bash
python sdo_advanced_examples.py
```

## 📂 Output Structure

```
sdo_data/
├── SDO_AIA_171_20260206_123456.jpg    # Solar image
├── SDO_AIA_171_20260206_123456.json   # Metadata
├── SDO_AIA_304_20260206_123457.jpg
└── SDO_AIA_304_20260206_123457.json
```

Each JSON file contains:
- Source and wavelength information
- Exact observation timestamp
- Download metadata
- Direct image URL

## 🔬 About NASA's SDO

The **Solar Dynamics Observatory** is a NASA mission launched in February 2010 to study the Sun's atmosphere and magnetic activity. It provides:

- 🛰️ **24/7 observations** from geosynchronous orbit
- 📸 **4K images every 12 seconds** in 10 wavelengths
- 🧲 **Magnetic field measurements** of the Sun's surface
- ☀️ **Real-time space weather monitoring**
- 📊 **Over 20 million images captured** since launch

Learn more at [sdo.gsfc.nasa.gov](https://sdo.gsfc.nasa.gov/)

## 📖 Documentation

- **[SDO_GUIDE.md](SDO_GUIDE.md)** - Comprehensive guide with detailed examples
- **[QUICK_REFERENCE.txt](QUICK_REFERENCE.txt)** - Quick command reference card
- **[NASA SDO Website](https://sdo.gsfc.nasa.gov/)** - Official mission website
- **[Helioviewer.org](https://helioviewer.org/)** - Interactive solar image viewer

## 🛠️ Requirements

- Python 3.7+
- `requests` library (installed via requirements.txt)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- **NASA/SDO** and the AIA, EVE, and HMI science teams for providing open access to solar data
- **Helioviewer Project** for API access and tools
- All solar physics researchers and space weather forecasters

## 🔗 Useful Links

- [SDO Mission Overview](https://sdo.gsfc.nasa.gov/mission/)
- [Space Weather Prediction Center](https://www.swpc.noaa.gov/)
- [Solar Data Analysis Center](https://umbra.nascom.nasa.gov/)
- [Helioviewer API Docs](https://api.helioviewer.org/docs/)

---

**Made with ☀️ for solar physics research, education, and space weather monitoring**

*If you find this tool useful, please ⭐ star this repository!*
