

def slugify(text : str) -> str:
    """Turn 'Report Name' → 'report-name'."""
    t = text.strip().casefold()
    # print(type(t))
    clean = t.split()
    # print(type(clean))
    return "-".join(clean)
