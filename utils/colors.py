class Colors:
    
    # Reset
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    
    # Status colors
    SUCCESS = BRIGHT_GREEN
    ERROR = BRIGHT_RED
    WARNING = BRIGHT_YELLOW
    INFO = BRIGHT_CYAN
    
    @staticmethod
    def print_banner():
        import sys
        import io
        
        banner = f"""
{Colors.BRIGHT_CYAN}
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║          {Colors.BOLD}NetShark - Security Scanner{Colors.RESET}{Colors.BRIGHT_CYAN}          ║
║                                                       ║
║         Multi-Purpose Security Analysis Tool          ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
{Colors.RESET}
"""
        try:
            if sys.platform == 'win32':
                sys.stdout.reconfigure(encoding='utf-8')
            print(banner)
        except:
            print("NetShark - Security Scanner\nMulti-Purpose Security Analysis Tool\n")
    
    @staticmethod
    def disable():
        Colors.RESET = ''
        Colors.BOLD = ''
        Colors.DIM = ''
        Colors.BLACK = ''
        Colors.RED = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.BLUE = ''
        Colors.MAGENTA = ''
        Colors.CYAN = ''
        Colors.WHITE = ''
        Colors.BRIGHT_RED = ''
        Colors.BRIGHT_GREEN = ''
        Colors.BRIGHT_YELLOW = ''
        Colors.BRIGHT_BLUE = ''
        Colors.BRIGHT_MAGENTA = ''
        Colors.BRIGHT_CYAN = ''
        Colors.SUCCESS = ''
        Colors.ERROR = ''
        Colors.WARNING = ''
        Colors.INFO = ''

