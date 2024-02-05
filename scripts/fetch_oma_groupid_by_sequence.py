from typing import Any
import requests
import sys
import warnings
from Bio import SeqIO

def fetch_seq(url: str):
    res = requests.get(url)
    if not res.ok:
        print(f"HTTP error. Code: {res.status_code}")
        return (False, dict())
    json: dict[str, Any] = res.json()
    return (True, json)


def main() -> None:
    # scream if no arguments passed
    if len(sys.argv) < 2:
        raise ValueError("Not enough arguments. Usage: fetch_oma_groupid_by_sequence.py [id]")
    
    # read the fasta (if it is a fasta)
    try:
        fasta = list(SeqIO.parse(sys.argv[1], "fasta"))
    except:
        raise ValueError(f"Could not read sequence file {sys.argv[1]}")
    
    if len(fasta) > 1:
        warnings.warn("Multiple sequences passed, ignoring all except the first.")
    
    success, json = fetch_seq(f"https://omabrowser.org/api/sequence/?query={fasta[0].seq}")

    if not success:
        raise ValueError("Fetch failed, aborting")

    entry: dict = dict()
    for it in json["targets"]:
            if it["is_main_isoform"]:
                entry = it
                break
    if entry == dict():
        if len(json["targets"][0]["alternative_isoforms_urls"]) > 0:
            isoform = json["targets"][0]["alternative_isoforms_urls"][0]
            success, json = fetch_seq(isoform)
            if not success:
                raise ValueError("Isoform fetch failed, aborting")
            if json["is_main_isoform"]:
                entry = json
            else:
                raise ValueError("Isoform not found")
    print(entry["oma_group"])


if __name__ == "__main__":
    main()
