import subprocess
import json
import os
from typing import Dict, List, Any
import asyncio
import requests
from bs4 import BeautifulSoup
import re
import sherlock

class NameSearch:
    def __init__(self):
        self.results_dir = "results"
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        
    async def search_social_media(self, name: str) -> Dict[str, Any]:
        """
        Search for social media profiles using Sherlock
        """
        try:
            results = {
                "profiles": [],
                "possible_emails": set(),
                "social_media": [],
                "error": None
            }
            
            # Search using Sherlock
            sherlock_results = await self._search_sherlock(name)
            results["profiles"].extend(sherlock_results)
            
            # Generate possible email patterns
            email_patterns = [
                f"{name.lower().replace(' ', '.')}@{domain}"
                for domain in ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
            ]
            results["possible_emails"].update(email_patterns)
            
            # Basic social media search
            social_results = await self._basic_social_search(name)
            results["social_media"].extend(social_results)
            
            # Convert set to list for JSON serialization
            results["possible_emails"] = list(results["possible_emails"])
            return results
            
        except Exception as e:
            return {
                "profiles": [],
                "possible_emails": [],
                "social_media": [],
                "error": str(e)
            }
            
    async def _search_sherlock(self, username: str) -> List[Dict[str, Any]]:
        """
        Search for username across social media platforms using Sherlock
        """
        try:
            results = []
            sites = sherlock.Sherlock(username).results
            for site in sites:
                if site.is_found():
                    results.append({
                        "platform": site.name,
                        "url": site.url,
                        "status": "found"
                    })
            return results
        except Exception as e:
            print(f"Error in Sherlock search: {str(e)}")
            return []
            
    async def _basic_social_search(self, name: str) -> List[Dict[str, Any]]:
        """
        Basic social media search using common patterns
        """
        try:
            results = []
            platforms = {
                "Facebook": f"https://www.facebook.com/search/top/?q={name.replace(' ', '%20')}",
                "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={name.replace(' ', '%20')}",
                "Twitter": f"https://twitter.com/search?q={name.replace(' ', '%20')}",
                "Instagram": f"https://www.instagram.com/{name.replace(' ', '')}"
            }
            
            for platform, url in platforms.items():
                results.append({
                    "platform": platform,
                    "url": url,
                    "username": name.replace(" ", ""),
                    "name": name
                })
            return results
        except Exception as e:
            print(f"Error in basic social search: {str(e)}")
            return []
            
    def search_web(self, name: str) -> Dict[str, Any]:
        """
        Search web for information about the name using basic web search
        """
        try:
            results = {
                "websites": [],
                "emails": set(),
                "social_links": [],
                "error": None
            }
            
            # Basic web search simulation
            search_urls = [
                f"https://www.google.com/search?q={name.replace(' ', '+')}",
                f"https://www.bing.com/search?q={name.replace(' ', '+')}",
                f"https://duckduckgo.com/?q={name.replace(' ', '+')}"
            ]
            
            results["websites"].extend(search_urls)
            
            # Add some common social media profile URLs
            social_links = [
                f"https://www.facebook.com/{name.replace(' ', '')}",
                f"https://twitter.com/{name.replace(' ', '')}",
                f"https://www.linkedin.com/in/{name.replace(' ', '-')}"
            ]
            results["social_links"].extend(social_links)
            
            # Convert set to list for JSON serialization
            results["emails"] = list(results["emails"])
            return results
            
        except Exception as e:
            return {
                "websites": [],
                "emails": [],
                "social_links": [],
                "error": str(e)
            }
            
    def format_results(self, social_results: Dict[str, Any], 
                      web_results: Dict[str, Any]) -> str:
        """
        Format all search results into a readable string
        """
        output = []
        
        output.append("🔍 Name Search Results\n")
        output.append("=" * 50 + "\n")
        
        # Social Media Profiles
        output.append("\n📱 Social Media Profiles:")
        if social_results["profiles"]:
            for profile in social_results["profiles"]:
                output.append(f"\n- {profile['platform']}: {profile['url']}")
        else:
            output.append("\nNo social media profiles found.")
            
        # Social Media Analysis
        output.append("\n\n🌐 Social Media Analysis:")
        if social_results["social_media"]:
            for profile in social_results["social_media"]:
                output.append(f"\n- Platform: {profile['platform']}")
                output.append(f"  URL: {profile['url']}")
                output.append(f"  Username: {profile['username']}")
                output.append(f"  Name: {profile['name']}")
        else:
            output.append("\nNo additional social media information found.")
            
        # Possible Email Addresses
        output.append("\n\n📧 Possible Email Addresses:")
        if social_results["possible_emails"]:
            for email in social_results["possible_emails"]:
                output.append(f"\n- {email}")
        else:
            output.append("\nNo possible email addresses generated.")
            
        # Web Search Results
        output.append("\n\n🌍 Web Presence:")
        if web_results["websites"]:
            output.append("\nWebsites:")
            for website in web_results["websites"][:10]:  # Limit to top 10
                output.append(f"\n- {website}")
        else:
            output.append("\nNo relevant websites found.")
            
        if web_results["social_links"]:
            output.append("\n\nSocial Links:")
            for link in web_results["social_links"]:
                output.append(f"\n- {link}")
                
        # Errors
        if social_results["error"] or web_results["error"]:
            output.append("\n\n⚠️ Errors:")
            if social_results["error"]:
                output.append(f"\n- Social Media Search: {social_results['error']}")
            if web_results["error"]:
                output.append(f"\n- Web Search: {web_results['error']}")
                
        return "\n".join(output)
        
    def save_results(self, name: str, social_results: Dict[str, Any], 
                    web_results: Dict[str, Any]) -> str:
        """
        Save search results to a file
        """
        try:
            filename = os.path.join(self.results_dir, f"name_search_{name.replace(' ', '_')}.txt")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.format_results(social_results, web_results))
            return filename
        except Exception as e:
            print(f"Error saving results: {str(e)}")
            return "" 