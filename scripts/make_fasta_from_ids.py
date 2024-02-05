import requests
import sys
import warnings

def main() -> None:
    if len(sys.argv) < 2:
        raise ValueError("Not enough arguments. Usage: fetch_oma_group_by_id.py [id]")
    
    with open(sys.argv[1]) as f:
        for line in f:
            id = line.strip().split('.')[0]
            res = requests.get(f"https://omabrowser.org/api/protein/{id}")
            if not res.ok:
                warnings.warn(f"Could not fetch sequence {id}")
                continue
            json = res.json()

            print(f">{json['canonicalid']} | {json['species']['species']} | {json['species']['taxon_id']} | {json['sequence_length']}")
            print(json["sequence"])


if __name__ == "__main__":
    main()
