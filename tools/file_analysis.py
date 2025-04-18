import subprocess
import json
import os
import tempfile
import mimetypes
import filetype
from PIL import Image
import exifread
from typing import Dict, Any, List, Optional
from pathlib import Path

class FileAnalysis:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.results: Dict[str, Any] = {}

    def _get_basic_info(self) -> Dict[str, Any]:
        """Get basic file information including size, mime type, and file type."""
        file_stats = os.stat(self.file_path)
        
        # Get MIME type using mimetypes
        mime_type, _ = mimetypes.guess_type(str(self.file_path))
        
        # Use filetype for more accurate file type detection
        kind = filetype.guess(str(self.file_path))
        file_type = kind.mime if kind else mime_type if mime_type else 'unknown'
        
        return {
            'file_size': file_stats.st_size,
            'mime_type': mime_type if mime_type else 'unknown',
            'file_type': file_type,
            'created': os.path.getctime(self.file_path),
            'modified': os.path.getmtime(self.file_path)
        }

    def analyze(self) -> Dict[str, Any]:
        """Analyze the file and return results."""
        try:
            self.results['basic_info'] = self._get_basic_info()
            
            # Additional analysis based on file type
            mime_type = self.results['basic_info']['mime_type']
            
            if mime_type.startswith('image/'):
                self._analyze_image()
            elif mime_type == 'application/pdf':
                self._analyze_pdf()
            
            return self.results
        except Exception as e:
            return {'error': str(e)}

    def _analyze_image(self) -> None:
        """Analyze image files for metadata."""
        try:
            with open(self.file_path, 'rb') as f:
                tags = exifread.process_file(f)
                
            image_info = {}
            for tag, value in tags.items():
                image_info[tag] = str(value)
            
            self.results['image_metadata'] = image_info
            
            # Get image dimensions using PIL
            with Image.open(self.file_path) as img:
                self.results['image_info'] = {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format
                }
        except Exception as e:
            self.results['image_analysis_error'] = str(e)

    def _analyze_pdf(self) -> None:
        """Analyze PDF files."""
        try:
            # PDF analysis implementation
            pass
        except Exception as e:
            self.results['pdf_analysis_error'] = str(e)

    def format_results(self) -> List[str]:
        """Format analysis results for display."""
        output = []
        
        # Format basic info
        basic = self.results.get('basic_info', {})
        if basic:
            output.append("📌 Basic Information:")
            output.append(f"📎 MIME Type: {basic.get('mime_type', 'Unknown')}")
            output.append(f"📁 File Type: {basic.get('file_type', 'Unknown')}")
            output.append(f"📊 Size: {basic.get('file_size', 0)} bytes")
            output.append(f"📅 Created: {basic.get('created', 'Unknown')}")
            output.append(f"🔄 Modified: {basic.get('modified', 'Unknown')}")
        
        # Format image info
        image_info = self.results.get('image_info', {})
        if image_info:
            output.append("\n📷 Image Information:")
            output.append(f"📐 Dimensions: {image_info.get('width', 0)}x{image_info.get('height', 0)}")
            output.append(f"🖼️ Format: {image_info.get('format', 'Unknown')}")
        
        # Format image metadata
        image_metadata = self.results.get('image_metadata', {})
        if image_metadata:
            output.append("\n📸 Image Metadata:")
            for key, value in image_metadata.items():
                output.append(f"  {key}: {value}")
        
        return output 