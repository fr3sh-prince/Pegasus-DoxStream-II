import subprocess
import json
import os
from typing import Dict, Any, List, Union
import whois
import dns.resolver
import requests
from bs4 import BeautifulSoup

class DomainSearch:
    def __init__(self):
        self.results_dir = "results"
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def analyze_domain(self, domain: str) -> Dict[str, Any]:
        """
        Perform comprehensive domain analysis
        """
        results = {
            "whois": self._get_whois_info(domain),
            "dns": self._get_dns_info(domain),
            "subdomains": self._get_subdomains(domain),
            "technologies": self._get_technologies(domain),
            "error": None
        }
        
        return results
        
    def _get_whois_info(self, domain: str) -> Dict[str, Any]:
        """
        Get WHOIS information for the domain
        """
        try:
            w = whois.whois(domain)
            return {
                "registrar": w.registrar,
                "creation_date": w.creation_date,
                "expiration_date": w.expiration_date,
                "name_servers": w.name_servers,
                "status": w.status,
                "emails": w.emails,
                "error": None
            }
        except Exception as e:
            return {"error": str(e)}
            
    def _get_dns_info(self, domain: str) -> Dict[str, Any]:
        """
        Get DNS records for the domain
        """
        try:
            records = {}
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    records[record_type] = [str(rdata) for rdata in answers]
                except dns.resolver.NoAnswer:
                    continue
                except dns.resolver.NXDOMAIN:
                    return {"error": "Domain does not exist"}
                    
            return {
                "records": records,
                "error": None
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _get_subdomains(self, domain: str) -> Dict[str, Union[List[str], str]]:
        """
        Find subdomains using Sublist3r
        """
        try:
            process = subprocess.Popen(
                ["sublist3r", "-d", domain, "-o", f"{self.results_dir}/subdomains_{domain}.txt"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            output, error = process.communicate()
            
            results = {
                "subdomains": [],
                "error": None
            }
            
            if os.path.exists(f"{self.results_dir}/subdomains_{domain}.txt"):
                with open(f"{self.results_dir}/subdomains_{domain}.txt", 'r') as f:
                    results["subdomains"] = [line.strip() for line in f if line.strip()]
                    
            if error:
                results["error"] = error
                
            return results
            
        except Exception as e:
            return {
                "subdomains": [],
                "error": str(e)
            }
            
    def _get_technologies(self, domain: str) -> Dict[str, Any]:
        """
        Identify technologies using WhatWeb
        """
        try:
            process = subprocess.Popen(
                ["whatweb", "--log-json", f"{self.results_dir}/whatweb_{domain}.json", domain],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            output, error = process.communicate()
            
            results = {
                "technologies": [],
                "server_info": {},
                "error": None
            }
            
            if os.path.exists(f"{self.results_dir}/whatweb_{domain}.json"):
                with open(f"{self.results_dir}/whatweb_{domain}.json", 'r') as f:
                    data = json.load(f)
                    if data:
                        entry = data[0]  # WhatWeb returns a list with one item
                        results["technologies"] = list(entry.get("plugins", {}).keys())
                        results["server_info"] = {
                            "ip": entry.get("ip"),
                            "country": entry.get("country"),
                            "server": entry.get("http_headers", {}).get("server"),
                            "powered_by": entry.get("http_headers", {}).get("x-powered-by")
                        }
                        
            if error:
                results["error"] = error
                
            return results
            
        except Exception as e:
            return {
                "technologies": [],
                "server_info": {},
                "error": str(e)
            }
            
    def format_results(self, results: Dict[str, Any]) -> str:
        """
        Format results for display in Streamlit
        """
        output = []
        
        # Format WHOIS information
        output.append("### 🔍 WHOIS Information")
        if results["whois"].get("error"):
            output.append(f"⚠️ Error: {results['whois']['error']}")
        else:
            whois = results["whois"]
            output.append(f"📋 Registrar: {whois.get('registrar', 'Unknown')}")
            output.append(f"📅 Created: {whois.get('creation_date', 'Unknown')}")
            output.append(f"⏰ Expires: {whois.get('expiration_date', 'Unknown')}")
            if whois.get('name_servers'):
                output.append("\n🌐 Name Servers:")
                for ns in whois['name_servers']:
                    output.append(f"  • {ns}")
            if whois.get('emails'):
                output.append("\n📧 Contact Emails:")
                for email in whois['emails']:
                    output.append(f"  • {email}")
                    
        # Format DNS information
        output.append("\n### 📡 DNS Records")
        if results["dns"].get("error"):
            output.append(f"⚠️ Error: {results['dns']['error']}")
        elif results["dns"].get("records"):
            for record_type, records in results["dns"]["records"].items():
                output.append(f"\n{record_type} Records:")
                for record in records:
                    output.append(f"  • {record}")
                    
        # Format subdomain information
        output.append("\n### 🌍 Subdomains")
        if results["subdomains"].get("error"):
            output.append(f"⚠️ Error: {results['subdomains']['error']}")
        elif results["subdomains"].get("subdomains"):
            for subdomain in results["subdomains"]["subdomains"]:
                output.append(f"  • {subdomain}")
        else:
            output.append("No subdomains found")
            
        # Format technology information
        output.append("\n### 💻 Technologies & Server Info")
        if results["technologies"].get("error"):
            output.append(f"⚠️ Error: {results['technologies']['error']}")
        else:
            if results["technologies"].get("technologies"):
                output.append("\n🔧 Detected Technologies:")
                for tech in results["technologies"]["technologies"]:
                    output.append(f"  • {tech}")
                    
            if results["technologies"].get("server_info"):
                server = results["technologies"]["server_info"]
                output.append("\n🖥️ Server Information:")
                output.append(f"  • IP: {server.get('ip', 'Unknown')}")
                output.append(f"  • Country: {server.get('country', 'Unknown')}")
                output.append(f"  • Server: {server.get('server', 'Unknown')}")
                output.append(f"  • Powered By: {server.get('powered_by', 'Unknown')}")
                
        return "\n".join(output)
        
    def save_results(self, domain: str, results: Dict[str, Any]) -> str:
        """
        Save results to JSON file
        """
        filename = f"{self.results_dir}/domain_search_{domain}_results.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        return filename 