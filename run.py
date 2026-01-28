import json
from tqdm import tqdm
from extract import extract_email

EMAILS_FILE = "data/emails.json"
PORTS_FILE = "data/ports.json"
OUTPUT_FILE = "output.json"

def load_ports():
    with open(PORTS_FILE, "r", encoding="utf-8") as f:
        ports = json.load(f)
    return "\n".join(
        f"{p['code']} - {p['name']} ({p['country']})" for p in ports
    )

def main():
    with open(EMAILS_FILE, "r", encoding="utf-8") as f:
        emails = json.load(f)

    ports_reference = load_ports()
    results = []

    for email in tqdm(emails):
        result = extract_email(email, ports_reference)
        results.append(result)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
