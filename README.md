# VAULTSCOPE
Simple payment surface scanner reads URLs from a text file, crawls a small set of common paths, flags payment‑related keywords, and (optionally) exports JSON or CSV results.
VaultScope is a lightweight Python tool that crawls public pages on a list of target
domains, flags payment‑related keywords, and assigns a simple risk rating
(`Low | Medium | High`).  
Perfect for quick reconnaissance during security reviews, OSINT sweeps, or
compliance inventories.

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-yellow.svg" />
</p>

-------------

## Features
- **Passive scanning** – just `requests` + `BeautifulSoup`; no login, no form‑submits  
- **Browser mimicry** – rotates real User‑Agent strings to stay under the radar  
- **Configurable paths** – checks `/`, `/privacy`, `/billing`, etc.*  
- **Risk grading** – simple heuristic based on keyword severity  
- **Exports** – print‑only _or_ `--output results.{json,csv}` for easy ingest  
- **One‑file install** – add a `requirements.txt`, run `pip install -r …`, done

\* Edit `extra_paths`, `keywords`, etc. at the top of `vaultscope.py`.

-------------

## Quick Start

```bash
# 1) clone repo
git clone https://github.com/<you>/vaultscope.git
cd vaultscope

# 2) install deps
pip install -r requirements.txt

# 3) drop a urls.txt in ./data/
echo "https://example.com" >> data/urls.txt

# 4) run a scan (console only)
python VaultScope.py urls.txt

# 5) run & export to JSON
python VaultScope.py urls.txt -o results.json
