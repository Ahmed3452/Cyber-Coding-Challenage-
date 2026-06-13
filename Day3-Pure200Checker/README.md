# Pure200Checker 🔍

A fast, multi-threaded subdomain alive checker that filters subdomains returning specific HTTP status codes (default: `200 OK`).

Built for bug bounty hunters and recon workflows.

---

## Features

- ⚡ Multi-threaded scanning (configurable workers)
- 🔁 Optional HTTPS fallback when HTTP fails
- 🎯 Filter by any HTTP status code(s), not just 200
- 💾 Saves results to an output file automatically
- 🕐 Configurable timeout per request

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/Pure200Checker.git
cd Pure200Checker
pip install -r requirements.txt
```

---

## Usage

```bash
python pure200checker.py -f subs_raw.txt
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-f`, `--file` | Path to subdomain list (required) | — |
| `-o`, `--output` | Output file for alive subs | `alive_subs.txt` |
| `-t`, `--timeout` | Timeout per request (seconds) | `5` |
| `-w`, `--workers` | Number of concurrent threads | `20` |
| `--https` | Also try HTTPS if HTTP fails | off |
| `--status-codes` | Comma-separated codes to accept | `200` |

### Examples

```bash
# Basic usage
python pure200checker.py -f subs_raw.txt

# Custom output, 30 threads, 3s timeout
python pure200checker.py -f subs_raw.txt -o results.txt -w 30 -t 3

# Accept 200 and 301, also try HTTPS
python pure200checker.py -f subs_raw.txt --https --status-codes 200,301

# Fast scan with 50 threads
python pure200checker.py -f subs_raw.txt -w 50 -t 2
```

---

## Sample Output

```
  [200] http://admin.example.com
  [200] http://api.example.com
  [301] https://mail.example.com

-------------------------------------------------------
[+] Scan complete!
[+] Found   : 3 alive subdomain(s)
[+] Saved to: alive_subs.txt
```

---

## Input Format

Plain text file, one subdomain per line:

```
admin.example.com
api.example.com
mail.example.com
dev.example.com
```

---

## Legal Disclaimer

> This tool is intended for **authorized security testing and bug bounty programs only**.  
> Do not use against targets you do not have explicit permission to test.  
> The author is not responsible for any misuse or damage caused by this tool.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
