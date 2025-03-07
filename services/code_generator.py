import json
from typing import Dict, Any

class CodeGenerator:
    @staticmethod
    def generate_curl(base_url: str, payload: Dict[str, Any]) -> str:
        """
        Generates a cURL command to send a POST request to the workflow execution server.
        """
        payload_json = json.dumps(payload, indent=2)
        return f"""curl -X POST \\
    "{base_url}/execute" \\
    -H 'Content-Type: application/json' \\
    -d '{payload_json}'"""

    @staticmethod
    def generate_python(base_url: str, payload: Dict[str, Any]) -> str:
        """
        Generates Python code to send a POST request to the workflow execution server.
        """
        payload_str = json.dumps(payload, indent=4)
        return f"""import requests
import json

def send_workflow_request():
    url = "{base_url}/execute"
    payload = {payload_str}
    
    headers = {{"Content-Type": "application/json"}}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# Call the function
if __name__ == "__main__":
    send_workflow_request()"""

    @staticmethod
    def generate_js(base_url: str, payload: Dict[str, Any]) -> str:
        """
        Generates JavaScript code to send a POST request to the workflow execution server.
        """
        payload_str = json.dumps(payload, indent=4)
        return f"""// JavaScript API Example
async function sendWorkflowRequest() {{
    const url = "{base_url}/execute";
    const payload = {payload_str};
    
    try {{
        const response = await fetch(url, {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify(payload)
        }});
        
        if (!response.ok) {{
            throw new Error(`HTTP error! Status: ${{response.status}}`);
        }}
        
        const data = await response.json();
        console.log("Response:", data);
    }} catch (error) {{
        console.error("Error:", error);
    }}
}}

// Call the function
sendWorkflowRequest();"""

    @staticmethod
    def generate_ts(base_url: str, payload: Dict[str, Any]) -> str:
        """
        Generates TypeScript code to send a POST request to the workflow execution server.
        """
        payload_str = json.dumps(payload, indent=4)
        return f"""// TypeScript API Example
interface Payload {{
    [key: string]: string | number; // Dynamic payload structure
}}

async function sendWorkflowRequest(): Promise<void> {{
    const url = "{base_url}/execute";
    const payload: Payload = {payload_str};
    
    try {{
        const response = await fetch(url, {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify(payload)
        }});
        
        if (!response.ok) {{
            throw new Error(`HTTP error! Status: ${{response.status}}`);
        }}
        
        const data = await response.json();
        console.log("Response:", data);
    }} catch (error) {{
        console.error("Error:", error);
    }}
}}

// Call the function
sendWorkflowRequest();"""

    @staticmethod
    def generate_code(language: str, base_url: str, payload: Dict[str, Any]) -> str:
        """
        Generates code in the specified language (cURL, Python, JS, TS).
        """
        if language == "curl":
            return CodeGenerator.generate_curl(base_url, payload)
        elif language == "python":
            return CodeGenerator.generate_python(base_url, payload)
        elif language == "js":
            return CodeGenerator.generate_js(base_url, payload)
        elif language == "ts":
            return CodeGenerator.generate_ts(base_url, payload)
        else:
            raise ValueError(f"Unsupported language: {language}")