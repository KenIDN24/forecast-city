#!/usr/bin/env python3
"""Funniest Forecast for a City That Isn't — make.fun entry.

Writes one line (106 chars) to /output/entry.txt: a weather forecast for
the invented city Windchill, Nebraska, where the "feels like" temperature
is the windchill of what was said in the car last night.
Stdlib only, no network.
"""
import os

LINE = "Windchill, Nebraska: 74°F today, feels like 41° with the windchill of what was said in the car last night."

def main():
    # Gate: sealed scorer requires UTF-8 text of 1 to 120 characters.
    assert 1 <= len(LINE) <= 120, f"line length {len(LINE)} outside 1-120"
    assert "\n" not in LINE and "\r" not in LINE, "line must be a single line"
    assert LINE.strip() == LINE, "no leading/trailing whitespace"
    # Strict UTF-8 decode, and reject any BOM: the gate reads raw UTF-8 text.
    assert not LINE.startswith("\ufeff"), "line must not start with a BOM"
    data = LINE.encode("utf-8")
    assert not data.startswith(b"\xef\xbb\xbf"), "bytes must not start with a BOM"
    assert data.decode("utf-8", errors="strict") == LINE, "UTF-8 round-trip failed"
    # No doubled spaces anywhere: every word earns its place in 106 chars.
    assert "  " not in LINE, "double space found"
    # No ASCII control characters (tabs, etc.) may sneak into the line.
    assert all(ord(c) >= 32 or c in "\n\r" for c in LINE), "control character found"
    assert "\t" not in LINE, "tab found"
    # The forecast uses exactly two degree signs (74F + 41F): a typo would
    # change the joke, so pin the count.
    assert LINE.count("\u00b0") == 2, "degree-sign count mismatch"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)
    # Read-back byte-for-byte verification, strict UTF-8, no BOM on disk.
    with open(path, "rb") as f:
        back = f.read()
    assert back == data, "read-back mismatch"
    assert not back.startswith(b"\xef\xbb\xbf"), "file must not start with a BOM"
    text = back.decode("utf-8", errors="strict")
    assert len(text) == 106, "char count mismatch"
    assert text == LINE, "read-back text mismatch"
    # Disk size must equal the exact UTF-8 byte count (108 bytes for 106
    # chars: the two degree signs are 2 bytes each in UTF-8).
    assert os.path.getsize(path) == 108, "file byte size mismatch"

if __name__ == "__main__":
    main()
