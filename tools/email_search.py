import subprocess
import json
import os
from typing import Dict, List, Any, Optional, Set, Union
import asyncio
from holehe.core import *
from holehe.core import import_submodules, get_functions
from holehe.modules import *
import requests
from bs4 import BeautifulSoup
import re

class EmailSearch:
    def __init__(self):
        self.results_dir = "results"
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    async def check_email_services(self, email: str) -> Dict[str, Union[List[Dict[str, Any]], Optional[str]]]:
        """
        Check email registration status across various services using Holehe
        """
        try:
            modules = import_submodules("holehe.modules")
            websites = get_functions(modules)
            out = []
            
            for website in websites:
                try:
                    result = await website(email)
                    if result:
                        out.append(result)
                except Exception as e:
                    continue
                    
            return {
                "registered": [x for x in out if x.get("exists") is True],
                "not_registered": [x for x in out if x.get("exists") is False],
                "error": None
            }
            
        except Exception as e:
            return {
                "registered": [],
                "not_registered": [],
                "error": str(e)
            }

    def check_email_breaches(self, email: str) -> Dict[str, Union[List[str], Optional[str]]]:
        """
        Check if email appears in any data breaches using H8mail
        """
        try:
            process = subprocess.Popen(
                ["h8mail", "-t", email, "-o", f"{self.results_dir}/h8mail_{email}.txt"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            output, error = process.communicate()
            
            results = {
                "breaches": [],
                "error": None
            }
            
            if os.path.exists(f"{self.results_dir}/h8mail_{email}.txt"):
                with open(f"{self.results_dir}/h8mail_{email}.txt", 'r') as f:
                    for line in f:
                        if "FOUND:" in line:
                            results["breaches"].append(line.strip())
                            
            if error:
                results["error"] = error
                
            return results
            
        except Exception as e:
            return {
                "breaches": [],
                "error": str(e)
            }

    def search_domain_emails(self, domain: str) -> Dict[str, Union[List[str], List[str], Optional[str]]]:
        """
        Search for email addresses associated with a domain using various methods
        """
        try:
            results = {
                "emails": set(),
                "sources": [],
                "error": None
            }

            # Search Google
            google_results = self._search_google(domain)
            results["emails"].update(google_results)
            if google_results:
                results["sources"].append("Google Search")

            # Search GitHub
            github_results = self._search_github(domain)
            results["emails"].update(github_results)
            if github_results:
                results["sources"].append("GitHub")

            # Search LinkedIn
            linkedin_results = self._search_linkedin(domain)
            results["emails"].update(linkedin_results)
            if linkedin_results:
                results["sources"].append("LinkedIn")

            # Convert set to list for JSON serialization
            results["emails"] = list(results["emails"])
            return results

        except Exception as e:
            return {
                "emails": [],
                "sources": [],
                "error": str(e)
            }

    def _search_google(self, domain: str) -> Set[str]:
        """
        Search Google for email addresses
        """
        emails = set()
        try:
            # Use dorks to find emails
            dorks = [
                f"site:{domain} email",
                f"site:{domain} contact",
                f"site:{domain} mailto:",
                f"@{domain} email"
            ]

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            for dork in dorks:
                response = requests.get(
                    f"https://www.google.com/search?q={dork}",
                    headers=headers
                )
                if response.status_code == 200:
                    # Extract emails using regex
                    found = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', response.text)
                    # Filter only emails from the target domain
                    emails.update([e for e in found if domain in e])

        except Exception:
            pass
        return emails

    def _search_github(self, domain: str) -> Set[str]:
        """
        Search GitHub for email addresses
        """
        emails = set()
        try:
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Mozilla/5.0'
            }
            
            response = requests.get(
                f"https://api.github.com/search/code?q={domain}",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    # Extract emails using regex from file content and commit messages
                    content_url = item.get('url')
                    if content_url:
                        content_response = requests.get(content_url, headers=headers)
                        if content_response.status_code == 200:
                            found = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', content_response.text)
                            emails.update([e for e in found if domain in e])

        except Exception:
            pass
        return emails

    def _search_linkedin(self, domain: str) -> Set[str]:
        """
        Search LinkedIn for email addresses
        """
        emails = set()
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(
                f"https://www.linkedin.com/company/{domain}",
                headers=headers
            )
            
            if response.status_code == 200:
                # Extract emails using regex
                found = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', response.text)
                emails.update([e for e in found if domain in e])
                
        except Exception:
            pass
        return emails

    def format_results(self, services: Dict[str, Union[List[Dict[str, Any]], Optional[str]]], 
                      breaches: Dict[str, Union[List[str], Optional[str]]], 
                      domain_info: Dict[str, Union[List[str], List[str], Optional[str]]]) -> str:
        """
        Format all results for display in Streamlit
        """
        output = []
        
        # Format service registration results
        output.append("### 📧 Service Registrations")
        if services.get("error"):
            output.append(f"⚠️ Error checking services: {services['error']}")
        else:
            registered = services.get("registered", [])
            not_registered = services.get("not_registered", [])
            
            if registered:
                output.append("\n✅ Registered on:")
                for service in registered:
                    if isinstance(service, dict) and "name" in service:
                        output.append(f"  • {service['name']}")
                        
            if not_registered:
                output.append("\n❌ Not registered on:")
                for service in not_registered:
                    if isinstance(service, dict) and "name" in service:
                        output.append(f"  • {service['name']}")
                    
        # Format breach results
        output.append("\n### 🚨 Data Breaches")
        if breaches.get("error"):
            output.append(f"⚠️ Error checking breaches: {breaches['error']}")
        else:
            breach_list = breaches.get("breaches", [])
            if breach_list:
                for breach in breach_list:
                    output.append(f"  • {breach}")
            else:
                output.append("✅ No breaches found")
            
        # Format domain email search results
        output.append("\n### 🌐 Domain Email Search")
        if domain_info.get("error"):
            output.append(f"⚠️ Error gathering domain info: {domain_info['error']}")
        else:
            sources = domain_info.get("sources", [])
            emails = domain_info.get("emails", [])
            
            if sources:
                output.append("\n🔍 Search Sources:")
                for source in sources:
                    output.append(f"  • {source}")
            
            if emails:
                output.append("\n📧 Found Email Addresses:")
                for email in emails:
                    output.append(f"  • {email}")
            else:
                output.append("\n❌ No email addresses found")
                    
        return "\n".join(output)

    def save_results(self, email: str, services: Dict[str, Union[List[Dict[str, Any]], Optional[str]]], 
                    breaches: Dict[str, Union[List[str], Optional[str]]], 
                    domain_info: Dict[str, Union[List[str], List[str], Optional[str]]]) -> str:
        """
        Save all results to JSON file
        """
        results = {
            "email": email,
            "services": services,
            "breaches": breaches,
            "domain_info": domain_info
        }
        
        filename = f"{self.results_dir}/email_search_{email}_results.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        return filename 