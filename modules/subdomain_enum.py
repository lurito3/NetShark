import socket
import dns.resolver
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.colors import Colors

class SubdomainEnum:
    
    COMMON_SUBDOMAINS = [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
        'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test',
        'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3',
        'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static',
        'docs', 'beta', 'web', 'media', 'email', 'images', 'img', 'www1', 'intranet',
        'portal', 'video', 'sip', 'dns2', 'api', 'cdn', 'stats', 'dns1', 'ns4', 'www3',
        'dns', 'search', 'staging', 'server', 'mx1', 'chat', 'wap', 'my', 'svn', 'mail1',
        'sites', 'proxy', 'ads', 'online', 'gw', 'firewall', 'server2', 'mx2', 'api2',
        'www4', 'secure', 'shop', 'demo', 'ns5', 'remote', 'blog2', 'vps', 'ns6', 'mail3',
        'smtp2', 'www5', 'ftp2', 'web2', 'www6', 'panel', 'dns3', 'www7', 'www8', 'www9',
        'www10', 'www11', 'www12', 'www13', 'www14', 'www15', 'www16', 'www17', 'www18',
        'www19', 'www20', 'www21', 'www22', 'www23', 'www24', 'www25', 'www26', 'www27',
        'www28', 'www29', 'www30', 'www31', 'www32', 'www33', 'www34', 'www35', 'www36',
        'www37', 'www38', 'www39', 'www40', 'www41', 'www42', 'www43', 'www44', 'www45',
        'www46', 'www47', 'www48', 'www49', 'www50', 'www51', 'www52', 'www53', 'www54',
        'www55', 'www56', 'www57', 'www58', 'www59', 'www60', 'www61', 'www62', 'www63',
        'www64', 'www65', 'www66', 'www67', 'www68', 'www69', 'www70', 'www71', 'www72',
        'www73', 'www74', 'www75', 'www76', 'www77', 'www78', 'www79', 'www80', 'www81',
        'www82', 'www83', 'www84', 'www85', 'www86', 'www87', 'www88', 'www89', 'www90',
        'www91', 'www92', 'www93', 'www94', 'www95', 'www96', 'www97', 'www98', 'www99',
        'www100', 'www101', 'www102', 'www103', 'www104', 'www105', 'www106', 'www107',
        'www108', 'www109', 'www110', 'www111', 'www112', 'www113', 'www114', 'www115',
        'www116', 'www117', 'www118', 'www119', 'www120', 'www121', 'www122', 'www123',
        'www124', 'www125', 'www126', 'www127', 'www128', 'www129', 'www130', 'www131',
        'www132', 'www133', 'www134', 'www135', 'www136', 'www137', 'www138', 'www139',
        'www140', 'www141', 'www142', 'www143', 'www144', 'www145', 'www146', 'www147',
        'www148', 'www149', 'www150', 'www151', 'www152', 'www153', 'www154', 'www155',
        'www156', 'www157', 'www158', 'www159', 'www160', 'www161', 'www162', 'www163',
        'www164', 'www165', 'www166', 'www167', 'www168', 'www169', 'www170', 'www171',
        'www172', 'www173', 'www174', 'www175', 'www176', 'www177', 'www178', 'www179',
        'www180', 'www181', 'www182', 'www183', 'www184', 'www185', 'www186', 'www187',
        'www188', 'www189', 'www190', 'www191', 'www192', 'www193', 'www194', 'www195',
        'www196', 'www197', 'www198', 'www199', 'www200'
    ]
    
    def __init__(self, domain: str, wordlist: Optional[str] = None, threads: int = 50):
        self.domain = domain
        self.wordlist = wordlist
        self.threads = threads
        self.found_subdomains: List[str] = []
    
    def enumerate(self) -> Dict:
        if self.wordlist:
            try:
                with open(self.wordlist, 'r') as f:
                    subdomains = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                print(f"{Colors.WARNING}Wordlist not found, using default{Colors.RESET}")
                subdomains = self.COMMON_SUBDOMAINS
        else:
            subdomains = self.COMMON_SUBDOMAINS
        
        print(f"{Colors.INFO}Testing {len(subdomains)} subdomains ({self.threads} threads)...{Colors.RESET}\n")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self._check_subdomain, sub): sub for sub in subdomains}
            
            completed = 0
            total = len(subdomains)
            
            for future in as_completed(futures):
                completed += 1
                try:
                    result = future.result()
                    if result:
                        self.found_subdomains.append(result)
                        print(f"{Colors.SUCCESS}✓ {result}{Colors.RESET}")
                except:
                    pass
                
                if completed % 10 == 0 or completed == total:
                    progress = (completed / total) * 100
                    print(f"\r{Colors.INFO}Progress: {progress:.1f}% ({completed}/{total}){Colors.RESET}", 
                          end='', flush=True)
        
        print()
        
        unique = sorted(set(self.found_subdomains))
        return {
            'domain': self.domain,
            'subdomains': unique,
            'total_found': len(unique)
        }
    
    def _check_subdomain(self, subdomain: str) -> Optional[str]:
        full_domain = f"{subdomain}.{self.domain}"
        
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 2
            resolver.lifetime = 2
            answers = resolver.resolve(full_domain, 'A')
            if answers:
                return full_domain
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
            pass
        except:
            pass
        
        try:
            socket.gethostbyname(full_domain)
            return full_domain
        except:
            pass
        
        return None

