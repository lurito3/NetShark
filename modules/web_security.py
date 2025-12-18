import socket
import ssl
import requests
from typing import Dict, Optional
from urllib.parse import urlparse
from datetime import datetime
from utils.colors import Colors

try:
    import urllib3
    urllib3.disable_warnings()
except ImportError:
    pass

class WebSecurity:
    
    def __init__(self, url: str):
        self.url = url if url.startswith(('http://', 'https://')) else f'https://{url}'
        self.parsed_url = urlparse(self.url)
        self.domain = self.parsed_url.netloc or self.parsed_url.path
    
    def full_analysis(self) -> Dict:
        results = {
            'url': self.url,
            'ip': None,
            'headers': {},
            'ssl': {},
            'security_score': 0
        }
        
        try:
            results['ip'] = socket.gethostbyname(self.domain)
        except:
            results['ip'] = 'Unknown'
        
        try:
            response = requests.get(self.url, timeout=10, allow_redirects=True, verify=False)
            results['headers'] = dict(response.headers)
        except Exception as e:
            print(f"{Colors.WARNING}Warning: {e}{Colors.RESET}")
        
        if self.url.startswith('https://'):
            results['ssl'] = self._analyze_ssl()
        
        results['security_score'] = self._calculate_security_score(results)
        return results
    
    def check_ssl_only(self) -> Dict:
        results = {'url': self.url, 'ssl': {}}
        
        if not self.url.startswith('https://'):
            results['ssl'] = {'error': 'Not HTTPS'}
            return results
        
        results['ssl'] = self._analyze_ssl()
        return results
    
    def _analyze_ssl(self) -> Dict:
        ssl_info = {}
        
        try:
            context = ssl.create_default_context()
            
            with socket.create_connection((self.domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                    ssl_info['valid'] = True
                    ssl_info['subject'] = dict(x[0] for x in cert['subject'])
                    ssl_info['issuer'] = dict(x[0] for x in cert['issuer'])
                    ssl_info['version'] = cert.get('version', 'N/A')
                    
                    not_after = cert.get('notAfter', '')
                    if not_after:
                        try:
                            expires = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                            ssl_info['expires'] = expires.strftime('%Y-%m-%d')
                            if expires < datetime.now():
                                ssl_info['valid'] = False
                                ssl_info['error'] = 'Expired'
                        except:
                            ssl_info['expires'] = not_after
                    
                    if cipher:
                        ssl_info['protocol'] = cipher[1]
                        ssl_info['cipher'] = cipher[0]
                        ssl_info['key_size'] = cipher[2]
                    
                    protocol = ssl_info.get('protocol', '')
                    if protocol.startswith(('TLSv1.0', 'TLSv1.1')):
                        ssl_info['warning'] = 'Weak TLS'
        
        except ssl.SSLError as e:
            ssl_info['valid'] = False
            ssl_info['error'] = f'SSL: {e}'
        except socket.timeout:
            ssl_info['valid'] = False
            ssl_info['error'] = 'Timeout'
        except Exception as e:
            ssl_info['valid'] = False
            ssl_info['error'] = str(e)
        
        return ssl_info
    
    def _calculate_security_score(self, results: Dict) -> int:
        score = 0
        
        if 'ssl' in results and results['ssl'].get('valid'):
            score += 40
            protocol = results['ssl'].get('protocol', '')
            if 'TLSv1.3' in protocol:
                score += 10
            elif 'TLSv1.2' in protocol:
                score += 5
            if results['ssl'].get('key_size', 0) >= 256:
                score += 5
        else:
            score -= 20
        
        headers = results.get('headers', {})
        header_points = {
            'Strict-Transport-Security': 10,
            'X-Frame-Options': 10,
            'X-Content-Type-Options': 10,
            'X-XSS-Protection': 5,
            'Content-Security-Policy': 15,
            'Referrer-Policy': 5
        }
        
        for header, points in header_points.items():
            if header in headers:
                score += points
        
        if 'Permissions-Policy' in headers or 'Feature-Policy' in headers:
            score += 5
        
        return max(0, min(100, score))

