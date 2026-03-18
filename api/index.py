from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# State law source mapping
STATE_LAW_SOURCES = {
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
        'small_estates': 'https://law.justia.com/codes/california/2014/code-pro/division-7/part-1/chapter-6/section-13100/',
        'probate': 'https://www.policygenius.com/estate-planning/small-estate-affidavit-california/',
        'poa': 'https://eforms.com/power-of-attorney/california/'
    },
    'texas': {
        'small_estates': 'https://law.justia.com/codes/texas/2014/estates-code/title-2/subtitle-e/chapter-205/',
        'probate': 'https://www.policygenius.com/estate-planning/small-estate-affidavit-texas/',
        'poa': 'https://eforms.com/power-of-attorney/texas/'
    },
    'florida': {
        'small_estates': 'https://law.justia.com/codes/florida/2014/title-xlii/chapter-735/section-735-301/',
        'probate': 'https://www.policygenius.com/estate-planning/small-estate-affidavit-florida/',
        'poa': 'https://eforms.com/power-of-attorney/florida/'
    }
}

def extract_states_from_query(query):
    """Extract state names from user query"""
    query_lower = query.lower()
    found_states = []
    
    for state in STATE_LAW_SOURCES.keys():
        if state in query_lower or state.replace('_', ' ') in query_lower:
            found_states.append(state)
    
    return found_states

def classify_legal_area(query):
    """Classify the legal area based on query content"""
    query_lower = query.lower()
    
    if any(term in query_lower for term in ['probate', 'estate', 'inheritance', 'will', 'testament']):
        return 'probate'
    elif any(term in query_lower for term in ['power of attorney', 'poa', 'healthcare directive']):
        return 'poa'
    elif any(term in query_lower for term in ['small estate', 'affidavit', 'summary administration']):
        return 'small_estates'
    else:
        return 'probate'  # Default

def get_state_law_links(states, legal_area):
    """Get relevant state law links"""
    links = []
    
    for state in states:
        if state in STATE_LAW_SOURCES and legal_area in STATE_LAW_SOURCES[state]:
            links.append({
                'url': STATE_LAW_SOURCES[state][legal_area],
                'state': state.replace('_', ' ').title(),
                'area': legal_area.replace('_', ' ').title(),
                'source': 'State Legal Code'
            })
    
    return links

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if path == '/api/health':
            response = {
                'status': 'connected',
                'message': 'Netherworld Navigator API is running',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            }
        elif path == '/api/initialize':
            response = {
                'status': 'initialized',
                'message': 'Welcome to the Netherworld Navigator',
                'realms': [
                    'Mortal Realm', 'Transition Realm', 'Authority Realm',
                    'Inheritance Realm', 'Judgment Realm', 'Wisdom Realm'
                ],
                'timestamp': datetime.now().isoformat()
            }
        else:
            response = {'error': 'Endpoint not found', 'path': path}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if path == '/api/search':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                query = data.get('query', '')
                
                # Extract states and classify legal area
                states = extract_states_from_query(query)
                legal_area = classify_legal_area(query)
                
                # Generate response based on states found
                if len(states) >= 2:
                    navigation_message = f"I found references to multiple jurisdictions: {', '.join([s.replace('_', ' ').title() for s in states])}. For multi-state estate matters, you'll need to comply with the laws of each relevant jurisdiction. Here are the specific legal resources for each state:"
                elif len(states) == 1:
                    state_name = states[0].replace('_', ' ').title()
                    navigation_message = f"I can help you navigate {state_name} estate law requirements. Here are the relevant legal resources:"
                else:
                    navigation_message = "I can guide you through general estate law principles. For specific legal requirements, please specify which state(s) you're dealing with."
                
                # Get state law links
                state_law_links = get_state_law_links(states, legal_area)
                
                response = {
                    'navigation_message': navigation_message,
                    'query': query,
                    'states_detected': [s.replace('_', ' ').title() for s in states],
                    'legal_area': legal_area.replace('_', ' ').title(),
                    'state_law_links': state_law_links,
                    'timestamp': datetime.now().isoformat()
                }
                
            except Exception as e:
                response = {
                    'error': f'Search processing error: {str(e)}',
                    'navigation_message': 'I encountered an issue processing your request. Please try rephrasing your question.'
                }
        else:
            response = {'error': 'Endpoint not found', 'path': path}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        # Handle preflight CORS requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

