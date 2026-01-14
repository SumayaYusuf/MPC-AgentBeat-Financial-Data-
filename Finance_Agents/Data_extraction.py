import json
from pathlib import Path

ATTRS = {
    #15 of these
    # Fundamentals
    "pe": ("Fundamentals", "EarningsQuality", "PriceEarningsRatio"),
    "pb": ("Fundamentals", "EarningsQuality", "PriceBookRatio"),
    "roe": ("Fundamentals", "EarningsQuality", "ReturnOnEquity"),
    "div": ("Fundamentals", "DividendYieldProfile", "DividendYield"),
    "distfreq": ("Fundamentals", "DividendYieldProfile", "DistributionFrequency"),
    
    # Cost
    "exp": ("CostTaxEfficiency", "ExpenseRatio", "TotalFundOperatingExpenses"),
    "fee": ("CostTaxEfficiency", "ExpenseRatio", "ManagementFee"),
    
    # Liquidity
    "turn": ("LiquidityTrading", "PortfolioTurnover", "TurnoverRate"),
    "aum": ("LiquidityTrading", "AUMSize", "TotalNetAssets"),
    
    # Diversification
    "hold": ("DiversificationConcentration", "HoldingsCount", "NumberOfSecurities"),
    
    # Performance
    "r1y": ("PerformanceRiskAdjusted", "AbsoluteReturn", "OneYearNAVReturn"),
    "r3y": ("PerformanceRiskAdjusted", "AbsoluteReturn", "ThreeYearNAVReturn"),
    "r5y": ("PerformanceRiskAdjusted", "AbsoluteReturn", "FiveYearNAVReturn"),
    "sharpe": ("PerformanceRiskAdjusted", "RiskAdjustedMeasures", "SharpeRatio"),
    "beta": ("PerformanceRiskAdjusted", "RiskAdjustedMeasures", "Beta"),
}

_raw = {}


def _dig(d, *keys):
    """Safely extract nested attribute values."""
    for k in keys:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d.get("value") if isinstance(d, dict) and "value" in d else d


def parse(path):
    """Parse a single ETF JSON file."""
    data = json.loads(Path(path).read_text())["SecuritiesInformation"]
    attrs = data.get("extracted_attributes", {})
    tk = data.get("security_ticker")
    _raw[tk] = attrs
    
    out = {"tk": tk, "nm": data.get("security_name")}
    
    for k, p in ATTRS.items():
        v = _dig(attrs, *p)
        if v is not None:
            out[k] = v
    
    return out


def load(directory):
    """Load all ETF JSON files from directory."""
    return [e for f in Path(directory).rglob("*.json") if (e := parse(f))]


def get(etfs, ticker, key=None):
    """Get ETF by ticker, optionally get specific key."""
    etf = next((e for e in etfs if e["tk"].upper() == ticker.upper()), None)
    return etf.get(key) if etf and key else etf


def filter_by(etfs, key, condition):
    """Filter ETFs by a condition on a key."""
    return [e for e in etfs if key in e and e[key] is not None and condition(e[key])]


def count_non_null(etfs, key):
    """Count ETFs with non-null value for a key."""
    return len([e for e in etfs if key in e and e[key] is not None])


def count_where(etfs, key, condition):
    """Count ETFs where condition is true for key."""
    return len(filter_by(etfs, key, condition))


def stats(etfs, key):
    """Get min, max, avg for a numeric key."""
    vals = [e[key] for e in etfs if key in e and e[key] is not None and isinstance(e[key], (int, float))]
    if not vals:
        return None
    return {"min": min(vals), "max": max(vals), "avg": sum(vals) / len(vals), "count": len(vals)}


def fmt(etfs):
    """Format ETFs for display."""
    lines = []
    for e in etfs:
        parts = [f"{e['tk']}:"]
        for k, v in e.items():
            if k not in ("tk", "nm"):
                if isinstance(v, float):
                    parts.append(f"{k}={v:.2f}")
                else:
                    parts.append(f"{k}={v}")
        lines.append(" ".join(parts))
    return "\n".join(lines)


if __name__ == "__main__":
    ETF_DIR = "/home/sumay/tutorial/ETF_attributes_json"
    
    etfs = load(ETF_DIR)
    print(f"Loaded {len(etfs)} ETFs:\n")
    print(fmt(etfs))
