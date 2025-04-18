import subprocess
import json
import os
from typing import Dict, List, Union, Optional

class UsernameSearch:
    def __init__(self):
        self.results_dir = "results"
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def search_username(self, username: str) -> Dict[str, Union[List[str], Optional[str]]]:
        """
        Search for username across social media platforms using Sherlock
        """
        try:
            # Run Sherlock command
            process = subprocess.Popen(
                ["sherlock", username, "--output", f"{self.results_dir}/sherlock_{username}.txt"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            output, error = process.communicate()
            
            # Parse results
            results = {
                "found": [],
                "not_found": [],
                "error": None
            }
            
            if os.path.exists(f"{self.results_dir}/sherlock_{username}.txt"):
                with open(f"{self.results_dir}/sherlock_{username}.txt", 'r') as f:
                    for line in f:
                        if line.strip():
                            results["found"].append(line.strip())
            
            if error:
                results["error"] = error
                
            return results
            
        except Exception as e:
            return {
                "found": [],
                "not_found": [],
                "error": str(e)
            }

    def format_results(self, results: Dict[str, Union[List[str], Optional[str]]]) -> str:
        """
        Format results for display in Streamlit
        """
        output = []
        
        if results["error"]:
            output.append(f"⚠️ Error: {results['error']}")
            
        if results["found"]:
            output.append("✅ Found profiles:")
            for profile in results["found"]:
                output.append(f"  • {profile}")
                
        if results["not_found"]:
            output.append("\n❌ Not found on:")
            for platform in results["not_found"]:
                output.append(f"  • {platform}")
                
        return "\n".join(output)

    def save_results(self, results: Dict[str, Union[List[str], Optional[str]]], username: str) -> str:
        """
        Save results to JSON file
        """
        filename = f"{self.results_dir}/sherlock_{username}_results.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        return filename 