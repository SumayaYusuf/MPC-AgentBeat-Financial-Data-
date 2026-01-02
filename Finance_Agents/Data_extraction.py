import json
from pathlib import Path

ATTRS = {

    "pe": ("Fundamentals", "EarningsQuality", "PriceEarningsRatio"),
    "pb": ("Fundamentals", "EarningsQuality", "PriceBookRatio"),
    "roe": ("Fundamentals", "EarningsQuality", "ReturnOnEquity"),
    "div": ("Fundamentals", "DividendYieldProfile", "DividendYield"),
    
    "exp": ("CostTaxEfficiency", "ExpenseRatio", "TotalFundOperatingExpenses"),
    "fee": ("CostTaxEfficiency", "ExpenseRatio", "ManagementFee"),
    
    "turn": ("LiquidityTrading", "PortfolioTurnover", "TurnoverRate"),
    "aum": ("LiquidityTrading", "AUMSize", "TotalNetAssets"),
    "hold": ("DiversificationConcentration", "HoldingsCount", "NumberOfSecurities"),
    
    "r1y": ("PerformanceRiskAdjusted", "AbsoluteReturn", "OneYearNAVReturn"),
    "r3y": ("PerformanceRiskAdjusted", "AbsoluteReturn", "ThreeYearNAVReturn"),
    "r5y": ("PerformanceRiskAdjusted", "AbsoluteReturn", "FiveYearNAVReturn"),
    "rinc": ("PerformanceRiskAdjusted", "AbsoluteReturn", "SinceInceptionNAVReturn"),
    "sharpe": ("PerformanceRiskAdjusted", "RiskAdjustedMeasures", "SharpeRatio"),
    "beta": ("PerformanceRiskAdjusted", "RiskAdjustedMeasures", "Beta"),
}

_raw = {}


def _dig(d, *keys):
    for k in keys:
        if not isinstance(d, dict): return None
        d = d.get(k)
    return d.get("value") if isinstance(d, dict) and "value" in d else d


def parse(path):
    data = json.loads(Path(path).read_text())["SecuritiesInformation"]
    attrs = data.get("extracted_attributes", {})
    tk = data.get("security_ticker")
    _raw[tk] = attrs
    out = {"tk": tk, "nm": data.get("security_name")}
    out.update({k: v for k, p in ATTRS.items() if (v := _dig(attrs, *p)) is not None})
    return out


def load(directory):
    return [e for f in Path(directory).rglob("*.json") if (e := parse(f))]


def get(etfs, ticker, key=None):
    etf = next((e for e in etfs if e["tk"].upper() == ticker.upper()), None)
    return etf.get(key) if etf and key else etf


def find(value):
    def search(d, path=""):
        if isinstance(d, dict):
            if d.get("value") == value:
                yield path
            for k, v in d.items():
                yield from search(v, f"{path}.{k}" if path else k)
    return [(tk, p) for tk, attrs in _raw.items() for p in search(attrs)]


def fmt(etfs):
    return "\n".join(
        f"{e['tk']}: " + " ".join(f"{k}={v}" for k, v in e.items() if k not in ("tk", "nm"))
        for e in etfs
    )


if __name__ == "__main__":
    ETF_DIR = "/home/sumay/tutorial/ETF_attributes_json"
    
    etfs = load(ETF_DIR)
    print(f"Loaded {len(etfs)} ETFs:\n")
    print(fmt(etfs))