import requests
import sys

def main() -> None:
    if len(sys.argv) < 2:
        raise ValueError("Not enough arguments. Usage: fetch_oma_ids_by_groupid.py [id]")
    
    id = sys.argv[1]
    res = requests.get(f"https://omabrowser.org/api/group/{id}")
    for it in res.json()["members"]:
        print(it["canonicalid"])

if __name__ == "__main__":
    main()
