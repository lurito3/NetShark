# 🔒 NetShark - Multi-Purpose Security Scanner

<div align="center">


  <p>
    <img src="https://img.shields.io/badge/🐍Python-3.7+-4ecdc4?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e">
    <img src="https://img.shields.io/badge/🪟Platform-Windows%20%7C%20Linux%20%7C%20macOS-ff6b6b?style=for-the-badge&logo=windows&logoColor=white&labelColor=1a1a2e">
  </p>

</div>

## 📖 About

**NetShark** is a comprehensive command-line security scanning tool that combines multiple security analysis capabilities into a single, easy-to-use interface. Whether you're performing penetration testing, security audits, or learning about cybersecurity, NetShark provides the tools you need.

### 🎯 Why NetShark?

- 🚀 **Fast & Efficient** - Multi-threaded scanning for quick results
- 🎨 **Beautiful CLI** - Colorful output with real-time progress indicators
- 🔧 **Easy to Use** - Simple commands, powerful results
- 📦 **All-in-One** - No need for multiple tools
- 🛠️ **Extensible** - Modular architecture for easy customization
- 📊 **Multiple Formats** - Export results as JSON, CSV, or TXT

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔍 Port Scanner
- Fast TCP/UDP port scanning
- Service detection & banner grabbing
- Multi-threaded for speed
- Custom port ranges

</td>
<td width="50%">

### 🌐 Web Security Analyzer
- SSL/TLS certificate analysis
- Security headers checking
- Security score calculation
- Detailed vulnerability reports

</td>
</tr>
<tr>
<td width="50%">

### 🔎 Subdomain Enumeration
- DNS-based discovery
- Custom wordlist support
- Multi-threaded enumeration
- Fast & efficient

</td>
<td width="50%">

### 📊 Network Monitor
- Real-time traffic monitoring
- Packet capture & analysis
- BPF filter support
- Cross-platform compatible

</td>
</tr>
</table>

### 🎨 Additional Features

- ✨ **Beautiful CLI** - Colorful terminal output with progress indicators
- 📁 **Multiple Export Formats** - JSON, CSV, and TXT support
- 🔄 **Cross-Platform** - Works on Windows, Linux, and macOS
- ⚡ **High Performance** - Optimized for speed and efficiency
- 🛡️ **Safe & Legal** - Educational and authorized testing only

## 🚀 Quick Start

### 📥 Installation

<details>
<summary><b>🐧 Linux / macOS</b></summary>

```bash
# Clone the repository
git clone https://github.com/karasulib/netshark.git
cd netshark

# Install dependencies
pip install -r requirements.txt

# Run NetShark
python netshark.py --help
```

</details>

<details>
<summary><b>🪟 Windows</b></summary>

```powershell
# Clone the repository
git clone https://github.com/karasulib/netshark.git
cd netshark

# Install Python 3.7+ if not already installed
# Then install dependencies
pip install -r requirements.txt

# Run NetShark
python netshark.py --help
```

</details>

### ⚡ Quick Example

```bash
# Scan ports on a target
python netshark.py scan -t 192.168.1.1 -p 80,443,8080

# Analyze web security
python netshark.py web -u https://example.com

# Find subdomains
python netshark.py subdomain -d example.com
```

## 📖 Usage Guide

### 🔍 Port Scanning

<details>
<summary><b>Click to expand examples</b></summary>

```bash
# Scan common ports (1-1000)
python netshark.py scan -t 192.168.1.1

# Scan specific ports
python netshark.py scan -t example.com -p 80,443,8080

# Scan with banner grabbing
python netshark.py scan -t 192.168.1.1 -p 1-1000 --banner

# Scan UDP ports
python netshark.py scan -t 192.168.1.1 -p 53 -s udp

# Export results to JSON
python netshark.py scan -t 192.168.1.1 -o json -f results.json
```

</details>

### 🌐 Web Security Analysis

<details>
<summary><b>Click to expand examples</b></summary>

```bash
# Full web security analysis
python netshark.py web -u https://example.com

# SSL/TLS only
python netshark.py web -u https://example.com --ssl-only

# Export to CSV
python netshark.py web -u https://example.com -o csv -f security_report.csv
```

</details>

### 🔎 Subdomain Enumeration

<details>
<summary><b>Click to expand examples</b></summary>

```bash
# Basic enumeration
python netshark.py subdomain -d example.com

# With custom wordlist
python netshark.py subdomain -d example.com -w wordlist.txt

# With more threads (faster)
python netshark.py subdomain -d example.com -t 100
```

</details>

### 📊 Network Monitoring

<details>
<summary><b>Click to expand examples</b></summary>

```bash
# Monitor on default interface (Linux)
python netshark.py monitor -c 50

# Monitor specific interface
python netshark.py monitor -i eth0 -c 100

# With filter
python netshark.py monitor -f "tcp port 80" -c 50
```

> **Note:** Network monitoring on Windows uses basic netstat functionality. For full packet capture, use Linux with scapy installed.

</details>

## 📋 Command Reference

### Global Options

- `--version` - Show version information
- `--help` - Show help message

### Scan Command

```
python netshark.py scan [OPTIONS]

Options:
  -t, --target TEXT      Target IP address or hostname [required]
  -p, --ports TEXT       Port range (e.g., 1-1000, 80,443,8080) [default: 1-1000]
  -T, --timeout FLOAT    Connection timeout in seconds [default: 1.0]
  -s, --scan-type TEXT   Scan type: tcp, udp, or both [default: tcp]
  -o, --output TEXT      Output format: json, csv, or txt
  -f, --file TEXT        Output file path
  --banner               Grab service banners
```

### Web Command

```
python netshark.py web [OPTIONS]

Options:
  -u, --url TEXT         Target URL [required]
  -o, --output TEXT      Output format: json, csv, or txt
  -f, --file TEXT        Output file path
  --ssl-only             Only check SSL/TLS configuration
```

### Subdomain Command

```
python netshark.py subdomain [OPTIONS]

Options:
  -d, --domain TEXT      Target domain [required]
  -w, --wordlist TEXT    Custom wordlist file path
  -t, --threads INTEGER  Number of threads [default: 50]
  -o, --output TEXT      Output format: json, csv, or txt
  -f, --file TEXT        Output file path
```

### Monitor Command

```
python netshark.py monitor [OPTIONS]

Options:
  -i, --interface TEXT   Network interface (e.g., eth0, wlan0)
  -c, --count INTEGER    Number of packets to capture [default: 100]
  -f, --filter TEXT      BPF filter (e.g., tcp port 80)
  -o, --output TEXT      Output format: json, csv, or txt
  --file TEXT            Output file path
```

## 🎯 Real-World Examples

### 🔥 Example 1: Quick Security Audit

```bash
# Perform a complete security check
python netshark.py web -u https://example.com -o json -f audit.json
```

### 🔥 Example 2: Network Discovery

```bash
# Scan common ports on a network
python netshark.py scan -t 192.168.1.1 -p 1-1000 --banner
```

### 🔥 Example 3: Subdomain Discovery Workflow

```bash
# Find all subdomains
python netshark.py subdomain -d example.com -t 100 -o txt -f subdomains.txt

# Then scan ports on discovered subdomains
# (Use subdomains.txt to iterate)
```

### 🔥 Example 4: Complete Security Assessment

```bash
# 1. Find subdomains
python netshark.py subdomain -d example.com -o json -f subs.json

# 2. Analyze web security for each subdomain
python netshark.py web -u https://www.example.com -o csv -f security.csv

# 3. Scan open ports
python netshark.py scan -t example.com -p 80,443,8080,8443
```

## 🔧 Requirements

| Component | Version | Description |
|-----------|---------|-------------|
| **Python** | 3.7+ | Tested with 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13 |
| **click** | ≥8.0.0 | CLI framework |
| **requests** | ≥2.28.0 | HTTP library |
| **dnspython** | ≥2.3.0 | DNS operations |
| **scapy** | ≥2.5.0 | Network packet manipulation (Linux only, optional) |

## 📁 Project Structure

```
netshark/
├── 📄 netshark.py              # Main CLI entry point
├── 📂 modules/
│   ├── __init__.py
│   ├── 🔍 port_scanner.py     # Port scanning module
│   ├── 🌐 web_security.py     # Web security analysis
│   ├── 🔎 subdomain_enum.py   # Subdomain enumeration
│   └── 📊 network_monitor.py  # Network monitoring
├── 📂 utils/
│   ├── __init__.py
│   ├── 🎨 colors.py           # Terminal colors
│   └── 📤 output.py           # Output formatting
├── 📋 requirements.txt        # Python dependencies
├── 📄 LICENSE                 # MIT License
└── 📖 README.md              # This file
```

## ⚠️ Legal Disclaimer

This tool is for **educational and authorized security testing purposes only**. 

- Only scan systems you own or have explicit permission to test
- Unauthorized scanning is illegal in many jurisdictions
- The authors are not responsible for misuse of this tool
- Always comply with local laws and regulations

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. ⭐ **Star the repository** - Show your support!
2. 🍴 **Fork the project** - Create your own copy
3. 🌿 **Create a branch** - `git checkout -b feature/AmazingFeature`
4. 💾 **Commit changes** - `git commit -m 'Add some AmazingFeature'`
5. 📤 **Push to branch** - `git push origin feature/AmazingFeature`
6. 🔄 **Open a Pull Request** - Let's discuss your changes!

### 🎯 Contribution Ideas

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- ⚡ Performance optimizations
- 🧪 Test coverage

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🎯 Inspired by tools like **Nmap**, **Masscan**, and **Subfinder**
- 🐍 Built with **Python** and the amazing open-source community
- 💡 Thanks to all contributors and users!

## 📧 Support

<div align="center">

**Need help? Have questions? Found a bug?**

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-lightgrey?style=flat-square&logo=github)](https://github.com/karasulib/netshark/issues)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-lightgrey?style=flat-square&logo=github)](https://github.com/karasulib/netshark/discussions)

</div>

---

<div align="center">

### ⭐ Star this repo if you find it useful!

**Made with ❤️ for the security community**

</div>

