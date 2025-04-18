import geoip2.database
import requests
import json
import os
from typing import Dict, Any, Optional
import folium
import tempfile

class IPSearch:
    def __init__(self):
        self.results_dir = "results"
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
            
        # Initialize GeoIP2 database
        self.geoip_db = "GeoLite2-City.mmdb"  # User needs to download this
        
    def get_ip_info(self, ip_address: str) -> Dict[str, Any]:
        """
        Get comprehensive IP information using multiple sources
        """
        results = {
            "geolocation": self._get_geolocation(ip_address),
            "whois": self._get_whois_info(ip_address),
            "threat_intel": self._get_threat_intel(ip_address),
            "error": None
        }
        
        return results
        
    def _get_geolocation(self, ip_address: str) -> Dict[str, Any]:
        """
        Get geolocation information using GeoIP2
        """
        try:
            if not os.path.exists(self.geoip_db):
                return {
                    "error": "GeoIP2 database not found. Please download GeoLite2-City.mmdb"
                }
                
            reader = geoip2.database.Reader(self.geoip_db)
            response = reader.city(ip_address)
            
            return {
                "country": response.country.name,
                "city": response.city.name,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
                "timezone": response.location.time_zone,
                "error": None
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _get_whois_info(self, ip_address: str) -> Dict[str, Any]:
        """
        Get WHOIS information for the IP
        """
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            data = response.json()
            
            if data.get("status") == "success":
                return {
                    "isp": data.get("isp"),
                    "org": data.get("org"),
                    "as": data.get("as"),
                    "asname": data.get("asname"),
                    "error": None
                }
            else:
                return {"error": data.get("message", "Unknown error")}
                
        except Exception as e:
            return {"error": str(e)}
            
    def _get_threat_intel(self, ip_address: str) -> Dict[str, Any]:
        """
        Get threat intelligence information about the IP
        """
        try:
            response = requests.get(f"https://api.abuseipdb.com/api/v2/check",
                                  params={"ipAddress": ip_address},
                                  headers={"Key": os.getenv("ABUSEIPDB_KEY", "")})
            
            data = response.json()
            
            if "data" in data:
                return {
                    "abuse_confidence_score": data["data"].get("abuseConfidenceScore"),
                    "total_reports": data["data"].get("totalReports"),
                    "last_reported_at": data["data"].get("lastReportedAt"),
                    "error": None
                }
            else:
                return {"error": "No threat data available"}
                
        except Exception as e:
            return {"error": str(e)}
            
    def generate_map(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Generate an HTML map using folium
        Returns the path to the generated HTML file or None if generation fails
        """
        try:
            # Create map centered on IP location
            m = folium.Map(location=[latitude, longitude], zoom_start=10)
            
            # Add marker
            folium.Marker(
                [latitude, longitude],
                popup="Target IP Location",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)
            
            # Save to temporary file
            _, temp_path = tempfile.mkstemp(suffix=".html")
            m.save(temp_path)
            
            return temp_path
            
        except Exception as e:
            return None
            
    def format_results(self, results: Dict[str, Any]) -> str:
        """
        Format results for display in Streamlit
        """
        output = []
        
        # Format geolocation results
        output.append("### 🌍 Geolocation Information")
        if results["geolocation"].get("error"):
            output.append(f"⚠️ Error: {results['geolocation']['error']}")
        else:
            geo = results["geolocation"]
            output.append(f"🏳️ Country: {geo.get('country', 'Unknown')}")
            output.append(f"🏙️ City: {geo.get('city', 'Unknown')}")
            output.append(f"📍 Coordinates: {geo.get('latitude', 0)}, {geo.get('longitude', 0)}")
            output.append(f"⏰ Timezone: {geo.get('timezone', 'Unknown')}")
            
        # Format WHOIS results
        output.append("\n### 🔍 Network Information")
        if results["whois"].get("error"):
            output.append(f"⚠️ Error: {results['whois']['error']}")
        else:
            whois = results["whois"]
            output.append(f"🏢 ISP: {whois.get('isp', 'Unknown')}")
            output.append(f"🏛️ Organization: {whois.get('org', 'Unknown')}")
            output.append(f"🌐 AS: {whois.get('as', 'Unknown')}")
            output.append(f"📡 AS Name: {whois.get('asname', 'Unknown')}")
            
        # Format threat intelligence results
        output.append("\n### 🛡️ Threat Intelligence")
        if results["threat_intel"].get("error"):
            output.append(f"⚠️ Error: {results['threat_intel']['error']}")
        else:
            threat = results["threat_intel"]
            output.append(f"⚠️ Abuse Confidence: {threat.get('abuse_confidence_score', 'Unknown')}%")
            output.append(f"📊 Total Reports: {threat.get('total_reports', 'Unknown')}")
            output.append(f"📅 Last Reported: {threat.get('last_reported_at', 'Never')}")
            
        return "\n".join(output)
        
    def save_results(self, ip_address: str, results: Dict[str, Any]) -> str:
        """
        Save results to JSON file
        """
        filename = f"{self.results_dir}/ip_search_{ip_address}_results.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        return filename 