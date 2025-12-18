import json
import csv
from typing import Dict, Optional
from utils.colors import Colors

class OutputFormatter:
    
    @staticmethod
    def display_scan_results(results: Dict, output_format: Optional[str] = None, 
                           file_path: Optional[str] = None):
        if output_format == 'json':
            output = json.dumps(results, indent=2)
        elif output_format == 'csv':
            output = OutputFormatter._scan_to_csv(results)
        else:
            output = OutputFormatter._scan_to_text(results)
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n{Colors.SUCCESS}Results saved to {file_path}{Colors.RESET}")
        else:
            print(output)
    
    @staticmethod
    def _scan_to_text(results: Dict) -> str:
        text = f"\n{Colors.BOLD}Scan Results:{Colors.RESET}\n"
        text += "=" * 60 + "\n\n"
        
        if results.get('open_ports'):
            text += f"{Colors.SUCCESS}Open Ports:{Colors.RESET}\n"
            for port_info in results['open_ports']:
                port = port_info['port']
                state = port_info['state']
                service = port_info.get('service', 'unknown')
                banner = port_info.get('banner', '')
                
                text += f"  {Colors.GREEN}✓{Colors.RESET} Port {Colors.BOLD}{port}{Colors.RESET} - {state.upper()} - {service}"
                if banner:
                    text += f" - {banner}"
                text += "\n"
        else:
            text += f"{Colors.WARNING}No open ports found{Colors.RESET}\n"
        
        text += f"\n{Colors.INFO}Summary:{Colors.RESET}\n"
        text += f"  Total ports scanned: {results.get('total_scanned', 0)}\n"
        text += f"  Open ports: {len(results.get('open_ports', []))}\n"
        text += f"  Closed ports: {results.get('closed_count', 0)}\n"
        text += f"  Filtered ports: {results.get('filtered_count', 0)}\n"
        text += f"  Scan duration: {results.get('duration', 0):.2f}s\n"
        
        return text
    
    @staticmethod
    def _scan_to_csv(results: Dict) -> str:
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Port', 'State', 'Service', 'Banner'])
        for port_info in results.get('open_ports', []):
            writer.writerow([
                port_info['port'],
                port_info['state'],
                port_info.get('service', 'unknown'),
                port_info.get('banner', '')
            ])
        
        return output.getvalue()
    
    @staticmethod
    def display_web_results(results: Dict, output_format: Optional[str] = None,
                           file_path: Optional[str] = None):
        if output_format == 'json':
            output = json.dumps(results, indent=2)
        elif output_format == 'csv':
            output = OutputFormatter._web_to_csv(results)
        else:
            output = OutputFormatter._web_to_text(results)
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n{Colors.SUCCESS}Results saved to {file_path}{Colors.RESET}")
        else:
            print(output)
    
    @staticmethod
    def _web_to_text(results: Dict) -> str:
        text = f"\n{Colors.BOLD}Web Security Analysis:{Colors.RESET}\n"
        text += "=" * 60 + "\n\n"
        
        # URL Info
        text += f"{Colors.INFO}Target:{Colors.RESET} {results.get('url', 'N/A')}\n"
        text += f"{Colors.INFO}IP Address:{Colors.RESET} {results.get('ip', 'N/A')}\n\n"
        
        # SSL/TLS Info
        if 'ssl' in results:
            ssl = results['ssl']
            text += f"{Colors.BOLD}SSL/TLS Configuration:{Colors.RESET}\n"
            text += f"  Certificate Valid: {Colors.GREEN if ssl.get('valid') else Colors.RED}{ssl.get('valid', False)}{Colors.RESET}\n"
            text += f"  Issuer: {ssl.get('issuer', 'N/A')}\n"
            text += f"  Subject: {ssl.get('subject', 'N/A')}\n"
            text += f"  Valid Until: {ssl.get('expires', 'N/A')}\n"
            text += f"  Protocol: {ssl.get('protocol', 'N/A')}\n"
            text += f"  Cipher: {ssl.get('cipher', 'N/A')}\n\n"
        
        # Security Headers
        if 'headers' in results:
            headers = results['headers']
            text += f"{Colors.BOLD}Security Headers:{Colors.RESET}\n"
            
            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'X-Frame-Options': 'X-Frame-Options',
                'X-Content-Type-Options': 'X-Content-Type-Options',
                'X-XSS-Protection': 'X-XSS-Protection',
                'Content-Security-Policy': 'CSP',
                'Referrer-Policy': 'Referrer-Policy'
            }
            
            for header, name in security_headers.items():
                if header in headers:
                    text += f"  {Colors.GREEN}✓{Colors.RESET} {name}: {headers[header]}\n"
                else:
                    text += f"  {Colors.RED}✗{Colors.RESET} {name}: Missing\n"
        
        # Security Score
        if 'security_score' in results:
            score = results['security_score']
            color = Colors.GREEN if score >= 80 else Colors.YELLOW if score >= 50 else Colors.RED
            text += f"\n{Colors.BOLD}Security Score:{Colors.RESET} {color}{score}/100{Colors.RESET}\n"
        
        return text
    
    @staticmethod
    def _web_to_csv(results: Dict) -> str:
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Category', 'Item', 'Value'])
        writer.writerow(['URL', 'Target', results.get('url', 'N/A')])
        writer.writerow(['URL', 'IP', results.get('ip', 'N/A')])
        
        if 'ssl' in results:
            ssl = results['ssl']
            writer.writerow(['SSL', 'Valid', ssl.get('valid', False)])
            writer.writerow(['SSL', 'Issuer', ssl.get('issuer', 'N/A')])
            writer.writerow(['SSL', 'Protocol', ssl.get('protocol', 'N/A')])
        
        if 'headers' in results:
            for header, value in results['headers'].items():
                writer.writerow(['Header', header, value])
        
        return output.getvalue()
    
    @staticmethod
    def display_subdomain_results(results: Dict, output_format: Optional[str] = None,
                                 file_path: Optional[str] = None):
        if output_format == 'json':
            output = json.dumps(results, indent=2)
        elif output_format == 'csv':
            output = OutputFormatter._subdomain_to_csv(results)
        else:
            output = OutputFormatter._subdomain_to_text(results)
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n{Colors.SUCCESS}Results saved to {file_path}{Colors.RESET}")
        else:
            print(output)
    
    @staticmethod
    def _subdomain_to_text(results: Dict) -> str:
        text = f"\n{Colors.BOLD}Subdomain Enumeration Results:{Colors.RESET}\n"
        text += "=" * 60 + "\n\n"
        
        subdomains = results.get('subdomains', [])
        
        if subdomains:
            text += f"{Colors.SUCCESS}Found {len(subdomains)} subdomains:{Colors.RESET}\n\n"
            for subdomain in subdomains:
                text += f"  {Colors.GREEN}✓{Colors.RESET} {subdomain}\n"
        else:
            text += f"{Colors.WARNING}No subdomains found{Colors.RESET}\n"
        
        text += f"\n{Colors.INFO}Total found: {len(subdomains)}{Colors.RESET}\n"
        
        return text
    
    @staticmethod
    def _subdomain_to_csv(results: Dict) -> str:
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Subdomain'])
        for subdomain in results.get('subdomains', []):
            writer.writerow([subdomain])
        
        return output.getvalue()
    
    @staticmethod
    def display_network_results(results: Dict, output_format: Optional[str] = None,
                               file_path: Optional[str] = None):
        if output_format == 'json':
            output = json.dumps(results, indent=2)
        elif output_format == 'csv':
            output = OutputFormatter._network_to_csv(results)
        else:
            output = OutputFormatter._network_to_text(results)
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n{Colors.SUCCESS}Results saved to {file_path}{Colors.RESET}")
        else:
            print(output)
    
    @staticmethod
    def _network_to_text(results: Dict) -> str:
        text = f"\n{Colors.BOLD}Network Monitoring Results:{Colors.RESET}\n"
        text += "=" * 60 + "\n\n"
        
        packets = results.get('packets', [])
        
        if packets:
            text += f"{Colors.INFO}Captured {len(packets)} packets:{Colors.RESET}\n\n"
            for i, packet in enumerate(packets[:20], 1):  # Show first 20
                text += f"  {i}. {packet.get('summary', 'N/A')}\n"
            
            if len(packets) > 20:
                text += f"\n  ... and {len(packets) - 20} more packets\n"
        else:
            text += f"{Colors.WARNING}No packets captured{Colors.RESET}\n"
        
        return text
    
    @staticmethod
    def _network_to_csv(results: Dict) -> str:
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Packet', 'Summary'])
        for i, packet in enumerate(results.get('packets', []), 1):
            writer.writerow([i, packet.get('summary', 'N/A')])
        
        return output.getvalue()

