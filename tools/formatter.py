import json

def format_numeric_values(data):
    if isinstance(data, dict):
        return {k: format_numeric_values(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [format_numeric_values(v) for v in data]
    elif isinstance(data, str):
        try:
            if '.' in data:
                val = float(data)
                if abs(val) >= 0.01:
                    return f"{val:.2f}"
        except ValueError:
            pass
    elif isinstance(data, float):
        if abs(data) >= 0.01:
            return round(data, 2)
    return data

def serialize(data):
    return json.dumps(format_numeric_values(data), indent=2)
