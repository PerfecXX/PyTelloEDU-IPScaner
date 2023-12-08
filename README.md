# PyTelloEDU-IPScanner
Tool for scanning Tello IPs on the same LAN

## Installation

```python
pip install telloipscanner
```

## Dependency

You Need to install Nmap before using this package 

Download Link : https://nmap.org/download

## Usage

```python

from telloipscanner import TelloIPScanner

scanner = TelloIPScanner()
scanner.run_scan()

```

