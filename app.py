from collections import Counter

def analyze(data):
    reference = data["reference"]
    splits = data["splits"]
    if not isinstance(splits, dict) or not splits:
        raise ValueError("Provide named evaluation splits")
    def counts(labels):
        if not isinstance(labels, list) or not labels or any(not isinstance(x, str) or not x.strip() for x in labels):
            raise ValueError("Every set needs a nonempty list of labels")
        return Counter(labels)
    base = counts(reference)
    observed = {name: counts(labels) for name, labels in splits.items()}
    labels = sorted(set(base).union(*(set(values) for values in observed.values())))
    def shares(counter):
        total = sum(counter.values())
        return {label: counter[label] / total for label in labels}
    expected = shares(base)
    report = {}
    for name, counter in observed.items():
        actual = shares(counter)
        distance = sum(abs(expected[label] - actual[label]) for label in labels) / 2
        report[name] = {"distance": round(distance, 6), "shares": actual}
    return {"reference": expected, "splits": report}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
