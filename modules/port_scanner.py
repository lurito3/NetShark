import socket
import time
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.colors import Colors

class PortScanner:
    
    COMMON_SERVICES = {
        20: 'FTP Data',
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        8080: 'HTTP-Proxy',
        8443: 'HTTPS-Alt'
    }
    
    def __init__(self, target: str, timeout: float = 1.0, grab_banner: bool = False):
        self.target = target
        self.timeout = timeout
        self.grab_banner = grab_banner
        self.results: Dict = {
            'open_ports': [],
            'closed_count': 0,
            'filtered_count': 0,
            'total_scanned': 0,
            'start_time': None,
            'end_time': None,
            'duration': 0
        }
    
    def scan(self, ports: List[int], scan_type: str = 'tcp') -> Dict:
        self.results['start_time'] = time.time()
        
        try:
            ip = socket.gethostbyname(self.target)
            print(f"{Colors.INFO}Target IP: {ip}{Colors.RESET}\n")
        except socket.gaierror:
            raise ValueError(f"Cannot resolve: {self.target}")
        
        scan_types = []
        if scan_type in ['tcp', 'both']:
            scan_types.append('tcp')
        if scan_type in ['udp', 'both']:
            scan_types.append('udp')
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(self._scan_port, p, st, ip) 
                      for p in ports for st in scan_types]
            
            completed = 0
            total = len(futures)
            
            for future in as_completed(futures):
                completed += 1
                self._process_result(future.result())
                
                if completed % 10 == 0 or completed == total:
                    progress = (completed / total) * 100
                    print(f"\r{Colors.INFO}Progress: {progress:.1f}% ({completed}/{total}){Colors.RESET}", 
                          end='', flush=True)
        
        print()
        
        self.results['end_time'] = time.time()
        self.results['duration'] = self.results['end_time'] - self.results['start_time']
        self.results['total_scanned'] = len(ports) * len(scan_types)
        
        return self.results
    
    def _scan_port(self, port: int, scan_type: str, ip: str) -> Dict:
        result = {
            'port': port,
            'type': scan_type,
            'state': 'closed',
            'service': self.COMMON_SERVICES.get(port, 'unknown'),
            'banner': ''
        }
        
        try:
            if scan_type == 'tcp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                
                if sock.connect_ex((ip, port)) == 0:
                    result['state'] = 'open'
                    if self.grab_banner:
                        try:
                            banner = self._grab_banner(sock, port)
                            if banner:
                                result['banner'] = banner
                        except:
                            pass
                sock.close()
            
            elif scan_type == 'udp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(self.timeout)
                try:
                    sock.sendto(b'', (ip, port))
                    sock.recvfrom(1024)
                    result['state'] = 'open'
                except socket.timeout:
                    result['state'] = 'open|filtered'
                except:
                    result['state'] = 'closed'
                finally:
                    sock.close()
        
        except socket.error:
            result['state'] = 'filtered'
        except Exception as e:
            result['state'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def _grab_banner(self, sock: socket.socket, port: int) -> str:
        probes = {
            21: b'QUIT\r\n',
            22: b'SSH-2.0-NetShark\r\n',
            25: b'QUIT\r\n',
            80: b'HEAD / HTTP/1.0\r\n\r\n',
            8080: b'HEAD / HTTP/1.0\r\n\r\n'
        }
        
        try:
            if port in [443, 8443]:
                return ''
            
            if port not in probes:
                return ''
            
            sock.settimeout(2)
            sock.send(probes[port])
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            return banner[:100]
        except:
            return ''
    
    def _process_result(self, result: Dict):
        state = result['state']
        if state == 'open':
            self.results['open_ports'].append(result)
        elif state == 'closed':
            self.results['closed_count'] += 1
        elif 'filtered' in state:
            self.results['filtered_count'] += 1

