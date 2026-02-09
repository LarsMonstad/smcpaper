#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv

SKIP_EXACT = {
    "Er det noe mer du vil legge til om KI og musikk?",
    "comment",  # hvis den dukker opp som verdi
}

def is_digits(s: str) -> bool:
    return (s or "").strip().isdigit()

def clean_one_line(s: str) -> str:
    # Sørger for at output faktisk blir én fysisk linje
    return " ".join((s or "").replace("\r", "\n").split())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Semikolon-separert inputfil")
    ap.add_argument("--output", default="comments.csv", help="Output: én CSV-rad med komma mellom hver kommentar")
    args = ap.parse_args()

    comments = []
    skipped = 0

    with open(args.input, "r", encoding="utf-8", errors="replace", newline="") as fin:
        reader = csv.reader(fin, delimiter=";", quotechar='"')

        for row in reader:
            if not row or len(row) < 2:
                skipped += 1
                continue

            # dropp header/metarader (ID-kolonne må være tall)
            if not is_digits(row[0]):
                skipped += 1
                continue

            # vanlig case i dine data: siste kolonne er numerisk -> kommentar ligger nest sist
            comment = row[-2].strip() if (len(row) >= 2 and is_digits(row[-1])) else ""

            comment = clean_one_line(comment)
            if not comment or comment in SKIP_EXACT:
                skipped += 1
                continue

            comments.append(comment)

    # Skriv én CSV-rad: "c1","c2","c3",...
    with open(args.output, "w", encoding="utf-8", newline="") as fout:
        writer = csv.writer(fout, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(comments)

    print(f"Ferdig: {len(comments)} kommentarer skrevet (hoppet over {skipped}). Output: {args.output}")

if __name__ == "__main__":
    main()

