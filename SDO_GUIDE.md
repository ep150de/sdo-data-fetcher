# SDO (Solar Dynamic Observatory) Data Fetcher

Complete Python solution for fetching the latest live solar images from NASA's Solar Dynamic Observatory.

## 📦 Files Included

- **`sdo_fetcher_v2.py`** - **RECOMMENDED** - Uses NASA's direct image URLs (most reliable)
- **`sdo_data_fetcher.py`** - Original version using Helioviewer API
- **`requirements.txt`** - Python dependencies
- **`README.md`** - This guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Script

```bash
# Get the latest AIA 171Å image (default)
python sdo_fetcher_v2.py

# Get a specific wavelength
python sdo_fetcher_v2.py --source AIA_304

# Download multiple wavelengths at once
python sdo_fetcher_v2.py --multiple

# List all available sources
python sdo_fetcher_v2.py --list
```

## 🌟 Features

✨ **Live Data** - Fetches the absolute latest SDO observations (updated every ~12 seconds)  
🌈 **Multiple Wavelengths** - Support for all AIA wavelengths (94Å-1700Å)  
🧲 **HMI Data** - Magnetogram and continuum images  
📊 **Automatic Metadata** - JSON files with observation details  
⚡ **Fast & Reliable** - Direct from NASA's servers  
🎯 **CLI Interface** - Simple command-line usage  
📦 **Batch Downloads** - Get multiple wavelengths at once  

## 📡 Available Data Sources

| Source | Wavelength | Temperature | Description |
|--------|------------|-------------|-------------|
| **AIA_94** | 94 Å | ~6 MK | Hot flare plasma |
| **AIA_131** | 131 Å | ~10 MK | Flaring regions |
| **AIA_171** | 171 Å | ~0.6 MK | Quiet corona, coronal loops (most common) |
| **AIA_193** | 193 Å | ~1.5 MK | Hot plasma in active regions |
| **AIA_211** | 211 Å | ~2 MK | Active regions |
| **AIA_304** | 304 Å | ~0.05 MK | Chromosphere, prominences |
| **AIA_335** | 335 Å | ~2.5 MK | Active regions |
| **AIA_1600** | 1600 Å | - | Upper photosphere, transition region |
| **AIA_1700** | 1700 Å | - | Temperature minimum, photosphere |
| **HMI_Continuum** | Visible | - | Solar surface (white light) |
| **HMI_Magnetogram** | - | - | Magnetic field strength |

*MK = Million Kelvin*

## 💻 Usage Examples

### Command Line

```bash
# Simple download
python sdo_fetcher_v2.py

# Specific wavelength for prominences
python sdo_fetcher_v2.py --source AIA_304

# Download common wavelengths for analysis
python sdo_fetcher_v2.py --multiple

# Custom output directory
python sdo_fetcher_v2.py --output my_solar_data --source AIA_193

# View all available options
python sdo_fetcher_v2.py --help
```

### Python Code

```python
from sdo_fetcher_v2 import SDOFetcher

# Initialize fetcher
fetcher = SDOFetcher(output_dir="solar_images")

# Download latest AIA 171Å image
metadata = fetcher.get_latest_image_direct(source="AIA_171")

if metadata:
    print(f"Image saved to: {metadata['filepath']}")
    print(f"Observation time: {metadata['last_modified']}")

# Download multiple wavelengths
sources = ["AIA_171", "AIA_193", "AIA_304", "HMI_Magnetogram"]
results = fetcher.download_multiple(sources)

print(f"Downloaded {len(results)} images successfully!")
```

## 📂 Output Structure

```
sdo_data/
├── SDO_AIA_171_20260206_234009.jpg    # Solar image
├── SDO_AIA_171_20260206_234009.json   # Metadata
├── SDO_AIA_193_20260206_234025.jpg
├── SDO_AIA_193_20260206_234025.json
└── ...
```

### Metadata Example (JSON)

```json
{
  "source": "AIA_171",
  "wavelength": "171Å",
  "filepath": "sdo_data\\SDO_AIA_171_20260206_234009.jpg",
  "download_time": "2026-02-06T23:40:09.123456+00:00",
  "image_url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171.jpg",
  "last_modified": "Fri, 06 Feb 2026 23:32:06 GMT",
  "note": "This is the latest available image from NASA SDO"
}
```

## 🔬 Understanding SDO Images

### AIA (Atmospheric Imaging Assembly)
- **10 wavelengths** observing different temperatures in the corona
- **4096×4096 pixels** at full resolution (scripts fetches 1024×1024 for speed)
- **12-second cadence** - new images every 12 seconds
- **Different colors** show different temperatures of solar plasma

### HMI (Helioseismic and Magnetic Imager)
- **Continuum**: White-light images of the solar surface (photosphere)
- **Magnetogram**: Magnetic field strength and polarity
- **45-second cadence** for full-disk images

### Common Use Cases
- **AIA 171** - General corona structure, best for everyday monitoring
- **AIA 304** - Filaments and prominences on the solar limb
- **AIA 193** - Active regions and hot plasma
- **HMI Magnetogram** - Sunspot magnetic fields, space weather forecasting

## 🛠️ Troubleshooting

### Import Errors
```bash
pip install --upgrade requests
```

### No Images Downloaded
- Check your internet connection
- NASA servers may occasionally be down for maintenance
- Try again in a few minutes

### Wrong Date/Time
The script fetches the absolute latest image available from NASA servers. The timestamp in metadata shows when SDO captured the image.

## 📚 Data Sources

This script uses:
- **NASA SDO Direct URLs**: `https://sdo.gsfc.nasa.gov/assets/img/latest/`
- Updates approximately every 12 seconds for AIA, 45 seconds for HMI
- Images are ~1024×1024 JPEGs (smaller than raw FITS for convenience)

## 🔗 Additional Resources

- [SDO Mission Website](https://sdo.gsfc.nasa.gov/)
- [Helioviewer.org](https://helioviewer.org/) - Interactive solar image browser
- [SDO Data](https://sdo.gsfc.nasa.gov/data/) - Full resolution data access
- [Space Weather Prediction Center](https://www.swpc.noaa.gov/) - Solar activity forecasts

## 🎓 About SDO

NASA's **Solar Dynamics Observatory** launched in February 2010 to study the Sun's atmosphere. It provides:

- 🛰️ **24/7 observations** from geosynchronous orbit
- 📸 **4K images** every 12 seconds in 10 wavelengths
- 🧲 **Magnetic field maps** of the Sun's surface
- ☀️ **Solar activity monitoring** for space weather forecasting
- 📊 **Over 20 million images** captured to date

## ⚡ Performance Tips

- Use `--multiple` flag to batch download several wavelengths efficiently
- Images are typically 150-250 KB each
- Download time: ~1-2 seconds per image on typical connections
- Metadata JSON files are < 1 KB each

## 📄 License

This script is provided as-is for educational and research purposes. SDO data is publicly available courtesy of NASA/SDO and the AIA, EVE, and HMI science teams.

## 🤝 Contributing

Feel free to modify and extend this script for your needs. Consider adding:
- FITS file support for full scientific data
- Time-series downloads
- Automatic video generation from image sequences
- Integration with other solar missions (STEREO, SOHO, etc.)

---

**Made for solar physics research, education, and space weather monitoring** ☀️🔭
