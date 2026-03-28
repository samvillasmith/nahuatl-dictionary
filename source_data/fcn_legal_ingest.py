#!/usr/bin/env python3
"""
FCN legal-first ingestion pipeline.

Purpose:
- Download or stage only from sources with a documented legal path
  (APIs, official dumps, public-domain scans, public Git repos, public files).
- Keep a provenance ledger for every retrieved artifact.
- Avoid brittle browser scraping by default.

Supported source types:
- wikimedia_dump: official Wikimedia dump URLs (e.g. Wiktionary XML dumps)
- internet_archive_metadata: item metadata via archive.org/metadata/<identifier>
- internet_archive_file: file download from an Internet Archive item
- github_raw: raw file download from public GitHub repositories
- url_file: generic direct-download URL when you already know it is legal to fetch

Not included by default:
- Browser scraping of AILLA/ELAR/Google Books page HTML
- Automated downloading from sources with account gates or unclear rights

Usage examples:
  python fcn_legal_ingest.py --config sources.json --out data/
  python fcn_legal_ingest.py --demo-config > sources.json

Config example:
{
  "sources": [
    {
      "name": "wiktionary-en-pages",
      "type": "wikimedia_dump",
      "url": "https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2",
      "license": "CC BY-SA / GFDL (verify current dump notice)",
      "notes": "Official dump; parse locally for Nahuatl entries."
    },
    {
      "name": "simeon-metadata",
      "type": "internet_archive_metadata",
      "identifier": "vocabularioenlen00moli_0",
      "license": "Public domain item metadata / see item rights",
      "notes": "Metadata only."
    },
    {
      "name": "ud-classical-nahuatl-readme",
      "type": "github_raw",
      "url": "https://raw.githubusercontent.com/UniversalDependencies/UD_Classical_Nahuatl-FloCo/master/README.md",
      "license": "Per-treebank license; inspect repository",
      "notes": "README for provenance and citation."
    }
  ]
}
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, Optional

USER_AGENT = "FCN-legal-ingest/0.1 (research and language documentation)"
TIMEOUT = 60
CHUNK = 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(CHUNK)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def safe_name(name: str) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in name)


def http_get(url: str, accept: Optional[str] = None) -> bytes:
    req = urllib.request.Request(url)
    req.add_header("User-Agent", USER_AGENT)
    if accept:
        req.add_header("Accept", accept)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def download_file(url: str, dest: Path) -> Dict[str, Any]:
    req = urllib.request.Request(url)
    req.add_header("User-Agent", USER_AGENT)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        content_type = resp.headers.get("Content-Type", "")
        ensure_dir(dest.parent)
        with dest.open("wb") as out:
            while True:
                block = resp.read(CHUNK)
                if not block:
                    break
                out.write(block)
    return {
        "path": str(dest),
        "sha256": sha256_file(dest),
        "size_bytes": dest.stat().st_size,
        "content_type": content_type,
    }


def save_json(data: Any, dest: Path) -> Dict[str, Any]:
    ensure_dir(dest.parent)
    with dest.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {
        "path": str(dest),
        "sha256": sha256_file(dest),
        "size_bytes": dest.stat().st_size,
        "content_type": "application/json",
    }


def handle_wikimedia_dump(source: Dict[str, Any], out_dir: Path) -> Dict[str, Any]:
    url = source["url"]
    filename = source.get("filename") or Path(urllib.parse.urlparse(url).path).name
    dest = out_dir / "wikimedia" / safe_name(source["name"]) / filename
    meta = download_file(url, dest)
    meta["retrieval_url"] = url
    return meta


def handle_internet_archive_metadata(source: Dict[str, Any], out_dir: Path) -> Dict[str, Any]:
    identifier = source["identifier"]
    url = f"https://archive.org/metadata/{urllib.parse.quote(identifier)}"
    data = json.loads(http_get(url, accept="application/json"))
    dest = out_dir / "internet_archive" / safe_name(identifier) / "metadata.json"
    meta = save_json(data, dest)
    meta["retrieval_url"] = url
    meta["identifier"] = identifier
    return meta


def handle_internet_archive_file(source: Dict[str, Any], out_dir: Path) -> Dict[str, Any]:
    identifier = source["identifier"]
    filename = source["filename"]
    url = f"https://archive.org/download/{urllib.parse.quote(identifier)}/{urllib.parse.quote(filename)}"
    dest = out_dir / "internet_archive" / safe_name(identifier) / filename
    meta = download_file(url, dest)
    meta["retrieval_url"] = url
    meta["identifier"] = identifier
    return meta


def handle_github_raw(source: Dict[str, Any], out_dir: Path) -> Dict[str, Any]:
    url = source["url"]
    filename = source.get("filename") or Path(urllib.parse.urlparse(url).path).name
    dest = out_dir / "github" / safe_name(source["name"]) / filename
    meta = download_file(url, dest)
    meta["retrieval_url"] = url
    return meta


def handle_url_file(source: Dict[str, Any], out_dir: Path) -> Dict[str, Any]:
    url = source["url"]
    filename = source.get("filename") or Path(urllib.parse.urlparse(url).path).name or "download.bin"
    dest = out_dir / "url_file" / safe_name(source["name"]) / filename
    meta = download_file(url, dest)
    meta["retrieval_url"] = url
    return meta


HANDLERS = {
    "wikimedia_dump": handle_wikimedia_dump,
    "internet_archive_metadata": handle_internet_archive_metadata,
    "internet_archive_file": handle_internet_archive_file,
    "github_raw": handle_github_raw,
    "url_file": handle_url_file,
}


def append_ledger_row(ledger_path: Path, row: Dict[str, Any]) -> None:
    ensure_dir(ledger_path.parent)
    fieldnames = [
        "timestamp_utc",
        "source_name",
        "source_type",
        "license",
        "notes",
        "retrieval_url",
        "identifier",
        "path",
        "sha256",
        "size_bytes",
        "content_type",
        "status",
        "error",
    ]
    write_header = not ledger_path.exists()
    with ledger_path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fieldnames})


def process_source(source: Dict[str, Any], out_dir: Path, ledger_path: Path) -> Dict[str, Any]:
    source_type = source["type"]
    base_row = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_name": source.get("name", ""),
        "source_type": source_type,
        "license": source.get("license", ""),
        "notes": source.get("notes", ""),
        "identifier": source.get("identifier", ""),
    }

    if source_type not in HANDLERS:
        row = {**base_row, "status": "error", "error": f"Unsupported source type: {source_type}"}
        append_ledger_row(ledger_path, row)
        return row

    try:
        meta = HANDLERS[source_type](source, out_dir)
        row = {**base_row, **meta, "status": "ok", "error": ""}
    except urllib.error.HTTPError as e:
        row = {
            **base_row,
            "retrieval_url": source.get("url", ""),
            "status": "error",
            "error": f"HTTP {e.code}: {e.reason}",
        }
    except Exception as e:  # noqa: BLE001
        row = {
            **base_row,
            "retrieval_url": source.get("url", ""),
            "status": "error",
            "error": repr(e),
        }

    append_ledger_row(ledger_path, row)
    return row


def demo_config() -> Dict[str, Any]:
    return {
        "sources": [
            {
                "name": "enwiktionary-pages-articles",
                "type": "wikimedia_dump",
                "url": "https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2",
                "license": "CC BY-SA / GFDL; verify dump/site notice",
                "notes": "Official dump; parse locally for Nahuatl entries and templates."
            },
            {
                "name": "archive-vocabulario-molina-metadata",
                "type": "internet_archive_metadata",
                "identifier": "vocabularioenlen00moli_0",
                "license": "See item rights / public-domain metadata context",
                "notes": "Get metadata before deciding which derivatives to download."
            },
            {
                "name": "ud-western-sierra-puebla-readme",
                "type": "github_raw",
                "url": "https://raw.githubusercontent.com/UniversalDependencies/UD_Western_Sierra_Puebla_Nahuatl-ITML/master/README.md",
                "license": "Per-treebank license; inspect repository and release license",
                "notes": "Useful for corpus provenance and annotation notes."
            }
        ]
    }


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="FCN legal-first ingestion pipeline")
    parser.add_argument("--config", help="Path to JSON config file")
    parser.add_argument("--out", default="data", help="Output directory")
    parser.add_argument("--demo-config", action="store_true", help="Print demo config and exit")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.demo_config:
        print(json.dumps(demo_config(), ensure_ascii=False, indent=2))
        return 0

    if not args.config:
        parser.error("--config is required unless --demo-config is used")

    out_dir = Path(args.out)
    ensure_dir(out_dir)
    ledger_path = out_dir / "ledger" / "provenance.csv"

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    sources = config.get("sources", [])
    if not isinstance(sources, list) or not sources:
        raise SystemExit("Config must contain a non-empty 'sources' list")

    results = []
    for source in sources:
        results.append(process_source(source, out_dir, ledger_path))

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
