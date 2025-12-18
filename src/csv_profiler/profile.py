import numbers


def basic_profile(rows: list[dict[str, str]]) -> dict:
    row_count = len(rows)
    columns = list(rows[0].keys())
    columns_profile: dict[str, dict] = {}

    for col in columns:
        values = column_values(rows,col)
        type = infer_type(values)

        if type == "number":
            stats = numeric_stats(values)
        else:
            stats = text_stats(values, top_k=5)

        columns_profile[col] = {
            "type": type,
            "stats": stats,
        }

    return{
        'summary' : {
            'rows':row_count,
            'columns_count' : len(columns),
        },
        'columns' : columns_profile

    }

MISSING = {"", "na", "n/a", "null", "none", "nan"}
def is_missing(value: str | None) -> bool:
    if value is None:
     return True
    cleaned = value.strip().casefold()
    return cleaned in MISSING


def infer_type(values:list[str]) -> str:
     usable = [v for v in values if not is_missing(v)]
     if not usable:
        return "text"
     for v in usable:
         if try_float(v) is None:
            return "text"
     return "number"

def try_float(input):
    try:
        return float(input)
    except ValueError:
         return None
    except BaseException:
        raise (f"Non-numeric value found: {input!r}")



def column_values(rows: list[dict[str,str]], col:str) -> list[str]:
    if len(rows) == 0:
        return []
    else:
        return [row.get(col,"") for row in rows]


def numeric_stats(values:list[str]) -> dict:
    """Compute stats for numeric column values (strings)."""

    usable = [v for v in values if not is_missing(v)] # {"", "na", "n/a", "null", "none", "nan"}
    nums = [try_float(v) for v in usable]

    nums2 = []
    for num in nums:
        if num is None:
            continue

        else:
            nums2.append(num)

    nums = nums2
    missing = len(values) - len(usable)
    count = len(nums)
    unique = len(set(nums))

    result = {
        "count" : count,
        "unique" : unique,
        "min" : min(nums),
        "max" : max(nums),
        "mean" : sum(nums) / count,
        "missing" : missing
    }
    return result

def text_stats(values: list[str], top_k: int = 5) -> dict:
    
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1
    
    top_items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    top = [{"value": v, "count": c} for v, c in top_items]
    unique = len(counts)
    return{
        'count' : len(usable) ,
        'missing' : missing,
        'top' : top,
        'unique' : unique
    }

