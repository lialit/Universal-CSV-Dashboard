import math
def compact_number(value):
    if value is None: return "—"
    n=float(value)
    if math.isnan(n): return "—"
    a=abs(n)
    if a>=1_000_000_000: return f"{n/1_000_000_000:.1f}B"
    if a>=1_000_000: return f"{n/1_000_000:.1f}M"
    if a>=1_000: return f"{n/1_000:.1f}K"
    return f"{n:,.2f}".rstrip("0").rstrip(".")
