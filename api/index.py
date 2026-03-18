from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    
    def __init__(self):
        # State law source mapping
        self.state_law_sources = {
            'oklahoma': {
                'small_estates': 'https://law.justia.com/codes/oklahoma/2014/title-58/section-58-393/',
                'probate': 'https://www.policygenius.com/estate-planning/small-estate-affidavit-oklahoma/',
                'poa': 'https://eforms.com/power-of-attorney/oklahoma/'
            },
            'new_york': {
                'small_estates': 'https://law.justia.com/codes/new-york/2014/sur/article-13/1301/',
                'probate': 'https://www.policygenius.com/estate-planning/small-estate-affidavit-new-york/',
                'poa': 'https://eforms.com/power-of-attorney/new-york/'
            },
            'california': {
                'small_estates': 'https://law.justia.com/codes/california/2014/code-pro/division-8/part-1/chapter-3/',
                'probate': 'https://www.policygenius.com/estate-planning/small-estate-affidavit-california/',
                'poa': 'https://eforms.com/power-of-attorney/california/'
            },
            'texas': {
                'small_estates': 'https://law.justia.com/codes/texas/2014/estates-code/title-2/subtitle-e/chapter-205/',
                'probate': 'https://www.policygenius.com/estate-planning/small-estate-affidavit-texas/',
                'poa': 'https://eforms.com/power-of-attorney/texas/'
            },
            'florida': {
                'small_estates': 'https://law.justia.com/codes/florida/2014/title-xlii/chapter-735/',
                'probate': 'https://www.policygenius.com/estate-planning/small-estate-affidavit-florida/',
                'poa': 'https://eforms.com/power-of-attorney/florida/'
            }
        }
        
        self.general_sources = {
            'justia_survey': 'https://www.justia.com/estate-planning/small-estates/',
            'nolo_guidance': 'https://www.nolo.com/legal-encyclopedia/powers-of-attorney',
            'practical_law': 'https://content.next.westlaw.com/practical-law/document/I0bdc6e5eef0511e28578f7ccc38dcbee/Power-of-Attorney-Toolkit',
            '50_state_survey': 'https://drive.google.com/file/d/1234567890/view'
        }
    
    def do_GET(self):
        self.__init__()  # Initialize state mappings
        
        # Add CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Parse the URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/api/health':
            response = {
                "status": "connected",
                "message": "Netherworld Navigator API is running",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/api/search':
            query_params = parse_qs(parsed_url.query)
            query = query_params.get('q', [''])[0].lower()
            
            # Detect states in query
            detected_states = []
            for state in self.state_law_sources.keys():
                if state.replace('_', ' ') in query:
                    detected_states.append(state)
            
            # Determine legal area
            legal_area = 'probate'  # default
            if 'power of attorney' in query or 'poa' in query:
                legal_area = 'poa'
            elif 'small estate' in query:
                legal_area = 'small_estates'
            
            # Build response
            state_law_links = []
            for state in detected_states:
                if state in self.state_law_sources and legal_area in self.state_law_sources[state]:
                    state_law_links.append({
                        "url": self.state_law_sources[state][legal_area],
                        "state": state.replace('_', ' ').title(),
                        "area": legal_area.replace('_', ' ').title(),
                        "source": "State Legal Code"
                    })
            
            # Multi-state guidance
            if len(detected_states) > 1:
                navigation_message = f"Multi-jurisdiction query detected for {', '.join([s.replace('_', ' ').title() for s in detected_states])}. Each state has different {legal_area.replace('_', ' ')} requirements. Review the specific statutes for each jurisdiction and consult with local counsel for comprehensive guidance."
            else:
                navigation_message = f"Legal guidance for {legal_area.replace('_', ' ')} matters. Review applicable state laws and consult with qualified legal counsel for specific situations."
            
            response = {
                "query": query,
                "navigation_message": navigation_message,
                "detected_states": detected_states,
                "legal_area": legal_area,
                "state_law_links": state_law_links,
                "general_resources": list(self.general_sources.values()),
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/api/initialize':
            response = {
                "status": "initialized",
                "message": "Netherworld Navigator system ready",
                "realms": ["Mortal", "Transition", "Authority", "Inheritance", "Judgment", "Wisdom"],
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        # Handle POST requests (same as GET for now)
        self.do_GET()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

