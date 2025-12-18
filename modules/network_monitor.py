import platform
from typing import Dict, Optional
from utils.colors import Colors

class NetworkMonitor:
    
    def __init__(self, interface: Optional[str] = None, count: int = 100, filter: Optional[str] = None):
        self.interface = interface
        self.count = count
        self.filter = filter
        self.is_windows = platform.system() == 'Windows'
    
    def monitor(self) -> Dict:
        if self.is_windows:
            return self._monitor_windows()
        else:
            return self._monitor_linux()
    
    def _monitor_windows(self) -> Dict:
        print(f"{Colors.WARNING}Network monitoring on Windows requires additional setup.{Colors.RESET}")
        print(f"{Colors.INFO}For full functionality, install: pip install scapy{Colors.RESET}\n")
        
        # Basic implementation using netstat-like approach
        import subprocess
        
        packets = []
        
        try:
            # Use netstat to get connections
            result = subprocess.run(
                ['netstat', '-an'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            lines = result.stdout.split('\n')
            for line in lines[:self.count]:
                if 'TCP' in line or 'UDP' in line:
                    packets.append({
                        'summary': line.strip(),
                        'type': 'connection'
                    })
        
        except Exception as e:
            print(f"{Colors.ERROR}Error: {str(e)}{Colors.RESET}")
        
        return {
            'packets': packets[:self.count],
            'total_captured': len(packets),
            'platform': 'Windows',
            'note': 'Basic monitoring. Install scapy for full packet capture.'
        }
    
    def _monitor_linux(self) -> Dict:
        try:
            from scapy.all import sniff, IP, TCP, UDP, Raw  # type: ignore
            
            packets = []
            
            def process_packet(packet):
                summary = self._packet_summary(packet)
                packets.append({
                    'summary': summary,
                    'raw': str(packet)
                })
            
            print(f"{Colors.INFO}Capturing {self.count} packets...{Colors.RESET}")
            print(f"{Colors.INFO}Press Ctrl+C to stop{Colors.RESET}\n")
            
            sniff(
                iface=self.interface,
                count=self.count,
                filter=self.filter,
                prn=process_packet,
                timeout=30
            )
            
            return {
                'packets': packets,
                'total_captured': len(packets),
                'platform': 'Linux'
            }
        
        except ImportError:
            print(f"{Colors.WARNING}scapy not installed. Installing basic monitoring...{Colors.RESET}")
            return self._monitor_basic()
        except Exception as e:
            print(f"{Colors.ERROR}Error: {str(e)}{Colors.RESET}")
            return {
                'packets': [],
                'total_captured': 0,
                'error': str(e)
            }
    
    def _monitor_basic(self) -> Dict:
        return {
            'packets': [],
            'total_captured': 0,
            'note': 'Install scapy for full packet capture: pip install scapy'
        }
    
    def _packet_summary(self, packet) -> str:
        try:
            from scapy.all import IP, TCP, UDP  # type: ignore
            
            if IP in packet:
                src = packet[IP].src
                dst = packet[IP].dst
                proto = packet[IP].proto
                
                if TCP in packet:
                    sport = packet[TCP].sport
                    dport = packet[TCP].dport
                    flags = packet[TCP].flags
                    return f"TCP {src}:{sport} -> {dst}:{dport} Flags: {flags}"
                
                elif UDP in packet:
                    sport = packet[UDP].sport
                    dport = packet[UDP].dport
                    return f"UDP {src}:{sport} -> {dst}:{dport}"
                
                else:
                    return f"IP {src} -> {dst} Proto: {proto}"
        except ImportError:
            pass
        
        return str(packet.summary() if hasattr(packet, 'summary') else packet)

