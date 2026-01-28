import json

FIELDS = [
    "product_line",
    "origin_port_code",
    "origin_port_name",
    "destination_port_code",
    "destination_port_name",
    "incoterm",
    "cargo_weight_kg",
    "cargo_cbm",
    "is_dangerous",
]

def equal(a, b):
    if a is None and b is None:
        return True
    if isinstance(a, float):
        return round(a, 2) == round(b, 2)
    return str(a).strip().lower() == str(b).strip().lower()

def evaluate(pred_file, gold_file):
    pred = json.load(open(pred_file))
    gold = json.load(open(gold_file))

    total = 0
    correct = 0

    for p, g in zip(pred, gold):
        for field in FIELDS:
            total += 1
            if equal(p.get(field), g.get(field)):
                correct += 1

    accuracy = correct / total
    print(f"Accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    evaluate("output.json", "data/ground_truth.json")
