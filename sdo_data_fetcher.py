"""
SDO (Solar Dynamic Observatory) Data Fetcher

This script fetches the latest solar images from NASA's Solar Dynamic Observatory
using the Helioviewer API. It supports multiple instruments and wavelengths.
"""

import requests
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Optional, Dict
import argparse


class SDODataFetcher:
    """Fetches latest SDO data from Helioviewer API"""
    
    BASE_URL = "https://api.helioviewer.org/v2/"
    
    # Available SDO/AIA wavelengths and their descriptions
    SDO_SOURCES = {
        "AIA_94": {"sourceId": 13, "description": "AIA 94 Å - Hot flare plasma"},
        "AIA_131": {"sourceId": 14, "description": "AIA 131 Å - Flaring regions"},
        "AIA_171": {"sourceId": 15, "description": "AIA 171 Å - Quiet corona and coronal loops"},
        "AIA_193": {"sourceId": 16, "description": "AIA 193 Å - Hot plasma in active regions"},
        "AIA_211": {"sourceId": 17, "description": "AIA 211 Å - Active regions"},
        "AIA_304": {"sourceId": 18, "description": "AIA 304 Å - Chromosphere and prominence"},
        "AIA_335": {"sourceId": 19, "description": "AIA 335 Å - Active regions"},
        "AIA_1600": {"sourceId": 20, "description": "AIA 1600 Å - Upper photosphere"},
        "AIA_1700": {"sourceId": 21, "description": "AIA 1700 Å - Temperature minimum"},
        "HMI_Continuum": {"sourceId": 22, "description": "HMI Continuum - Solar surface"},
        "HMI_Magnetogram": {"sourceId": 23, "description": "HMI Magnetogram - Magnetic field"},
    }
    
    def __init__(self, output_dir: str = "sdo_data"):
        """Initialize the fetcher with an output directory"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def get_latest_available_date(self) -> Optional[str]:
        """Query the API for the latest available SDO observation time"""
        try:
            url = f"{self.BASE_URL}getDataSources/"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Find SDO/AIA data source and get the end date (latest available)
            for source in data:
                if source.get("name") == "SDO":
                    for child in source.get("children", []):
                        if child.get("name") == "AIA":
                            end_date = child.get("end")
                            if end_date:
                                print(f"Latest SDO data available: {end_date}")
                                return end_date
            
            # Fallback to a date 30 minutes ago if API doesn't provide info
            fallback = (datetime.now(timezone.utc) - timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
            print(f"Using fallback date: {fallback}")
            return fallback
            
        except Exception as e:
            print(f"Warning: Could not determine latest date from API: {e}")
            # Fallback to Dec 2024 (a known date with data)
            fallback = "2024-12-01T12:00:00.000Z"
            print(f"Using safe fallback date: {fallback}")
            return fallback
    
    def get_latest_image(self, source: str = "AIA_171", image_scale: float = 2.4) -> Optional[Dict]:
        """
        Fetch the latest SDO image
        
        Args:
            source: SDO source identifier (e.g., 'AIA_171', 'HMI_Magnetogram')
            image_scale: Resolution in arcseconds per pixel (lower = higher resolution)
            
        Returns:
            Dictionary with image metadata and file path
        """
        if source not in self.SDO_SOURCES:
            raise ValueError(f"Invalid source. Choose from: {list(self.SDO_SOURCES.keys())}")
        
        source_id = self.SDO_SOURCES[source]["sourceId"]
        
        print(f"Fetching latest {source} data...")
        print(f"Description: {self.SDO_SOURCES[source]['description']}")
        
        try:
            # Get the latest available date from the API
            date = self.get_latest_available_date()
            if not date:
                print("Could not determine latest data date")
                return None
            
            print(f"Requesting data from: {date}")
            
            # Request the latest image
            params = {
                "date": date,
                "imageScale": image_scale,
                "layers": f"[SDO,{source_id},1,100]",
                "eventLabels": "false",
                "scale": "true",
                "scaleType": "earth",
                "scaleX": 0,
                "scaleY": 0,
                "width": 1024,
                "height": 1024,
                "display": "true",
                "watermark": "false"
            }
            
            screenshot_url = f"{self.BASE_URL}takeScreenshot/"
            response = requests.get(screenshot_url, params=params, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Download the image
            image_url = "https://api.helioviewer.org" + result["url"]
            print(f"Downloading image from: {image_url}")
            image_response = requests.get(image_url, stream=True, timeout=30)
            image_response.raise_for_status()
            
            # Create filename with timestamp
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            filename = f"SDO_{source}_{timestamp}.png"
            filepath = self.output_dir / filename
            
            # Save the image
            with open(filepath, 'wb') as f:
                for chunk in image_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ Image saved to: {filepath}")
            
            # Get metadata about the observation
            metadata = {
                "source": source,
                "description": self.SDO_SOURCES[source]["description"],
                "filepath": str(filepath),
                "download_time": datetime.now(timezone.utc).isoformat(),
                "image_url": image_url,
                "requested_date": date
            }
            
            # Save metadata
            metadata_file = filepath.with_suffix('.json')
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✓ Metadata saved to: {metadata_file}")
            
            return metadata
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def get_latest_data_timestamp(self) -> Optional[str]:
        """Get the timestamp of the latest available SDO data"""
        try:
            url = f"{self.BASE_URL}getDataSources/"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Find SDO/AIA data source
            for source in data:
                if source.get("name") == "SDO":
                    for child in source.get("children", []):
                        if child.get("name") == "AIA":
                            # Return the end date (latest available)
                            return child.get("end")
            
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error getting latest timestamp: {e}")
            return None
    
    def download_multiple_wavelengths(self, sources: list = None):
        """
        Download images from multiple SDO sources
        
        Args:
            sources: List of source identifiers (defaults to common wavelengths)
        """
        if sources is None:
            sources = ["AIA_171", "AIA_193", "AIA_304", "HMI_Magnetogram"]
        
        results = []
        for source in sources:
            print(f"\n{'='*60}")
            result = self.get_latest_image(source)
            if result:
                results.append(result)
        
        print(f"\n{'='*60}")
        print(f"Downloaded {len(results)} images successfully!")
        return results
    
    @staticmethod
    def list_available_sources():
        """Print all available SDO sources"""
        print("\nAvailable SDO Data Sources:")
        print("="*60)
        for key, value in SDODataFetcher.SDO_SOURCES.items():
            print(f"{key:20} - {value['description']}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Fetch latest SDO (Solar Dynamic Observatory) data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download latest AIA 171 Å image
  python sdo_data_fetcher.py
  
  # Download specific wavelength
  python sdo_data_fetcher.py --source AIA_304
  
  # Download multiple wavelengths
  python sdo_data_fetcher.py --multiple
  
  # List all available sources
  python sdo_data_fetcher.py --list
  
  # Download to specific directory
  python sdo_data_fetcher.py --output my_sdo_images
        """
    )
    
    parser.add_argument(
        '--source', '-s',
        type=str,
        default='AIA_171',
        help='SDO source to fetch (default: AIA_171)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='sdo_data',
        help='Output directory for downloaded data (default: sdo_data)'
    )
    
    parser.add_argument(
        '--scale',
        type=float,
        default=2.4,
        help='Image scale in arcseconds per pixel (default: 2.4)'
    )
    
    parser.add_argument(
        '--multiple', '-m',
        action='store_true',
        help='Download multiple common wavelengths'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available SDO sources'
    )
    
    parser.add_argument(
        '--timestamp', '-t',
        action='store_true',
        help='Get the timestamp of latest available data'
    )
    
    args = parser.parse_args()
    
    # List available sources and exit
    if args.list:
        SDODataFetcher.list_available_sources()
        return
    
    # Initialize fetcher
    fetcher = SDODataFetcher(output_dir=args.output)
    
    # Get latest timestamp
    if args.timestamp:
        timestamp = fetcher.get_latest_data_timestamp()
        if timestamp:
            print(f"Latest SDO data available at: {timestamp}")
        return
    
    # Download data
    if args.multiple:
        fetcher.download_multiple_wavelengths()
    else:
        fetcher.get_latest_image(source=args.source, image_scale=args.scale)


if __name__ == "__main__":
    main()
