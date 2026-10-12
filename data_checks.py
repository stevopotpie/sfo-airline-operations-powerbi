"""Data checks for the SFO landings dashboard.

Verifies the figures quoted in the README and flags the reporting quirks that
can mislead a chart built straight from the raw table.

Usage:
    python data_checks.py Air_Traffic_Landings_Statistics.csv
"""

import sys

import pandas as pd

FAMILY_737 = {"737", "739", "B733", "B734", "B735", "B736", "B737", "B738", "B739", "B38M", "B39M"}
FAMILY_A320 = {"A318", "A319", "A320", "A321", "A20N", "A21N"}


def family(model: str) -> str:
    m = str(model).upper()
    if m in FAMILY_737:
        return "737 family"
    if m in FAMILY_A320:
        return "A320 family"
    return m


def main(path: str) -> None:
    d = pd.read_csv(path, usecols=["Activity Period Start Date", "Operating Airline", "GEO Summary",
                                   "GEO Region", "Landing Aircraft Type", "Aircraft Manufacturer",
                                   "Aircraft Model", "Landing Count"])
    d["date"] = pd.to_datetime(d["Activity Period Start Date"])
    d["year"] = d["date"].dt.year
    d["month"] = d["date"].dt.month
    total = d["Landing Count"].sum()
    print(f"Rows: {len(d):,}   Landings: {total:,}   Months: {d['date'].min():%b %Y} to {d['date'].max():%b %Y}\n")

    # 1. Partial years distort an annual total chart
    months = d.groupby("year")["date"].nunique()
    partial = months[months < 12]
    print("1. Partial years (annual totals understate these):")
    for y, n in partial.items():
        print(f"   {y}: {n} months of data")
    yearly = d.groupby("year")["Landing Count"].sum()
    avg = (yearly / months).round(0).astype(int)
    print("   Average landings per month, selected years:")
    for y in [2000, 2019, 2020, 2024, months.index.max()]:
        print(f"   {y}: {avg[y]:,}")

    # Like for like recovery, same months of the year
    last = months.index.max()
    last_m = d.loc[d["year"] == last, "month"].max()
    same = d["month"] <= last_m
    rec = d[same & (d["year"] == last)]["Landing Count"].sum() / d[same & (d["year"] == 2019)]["Landing Count"].sum()
    print(f"   {last} through month {last_m} vs the same months of 2019: {rec:.0%}\n")

    # 2. United is split across two labels
    d["airline"] = d["Operating Airline"].str.replace(" - Pre 07/01/2013", "", regex=False)
    print("2. Airline labels with a 'Pre 07/01/2013' suffix:")
    for a in sorted(d.loc[d["Operating Airline"].str.contains("Pre 07/01/2013"), "Operating Airline"].unique()):
        print(f"   {a}")
    top = d.groupby("airline")["Landing Count"].sum().sort_values(ascending=False).head(5)
    print("   Top 5 after combining labels:")
    for a, v in top.items():
        print(f"   {a:<22}{v:>12,}  {v / total:.0%}")
    print()

    # 3. Aircraft model labels change specificity over time
    d["family"] = d["Aircraft Model"].map(family)
    fam = d.groupby("family")["Landing Count"].sum().sort_values(ascending=False).head(5)
    print("3. Top aircraft after grouping model codes into families:")
    for f, v in fam.items():
        print(f"   {f:<22}{v / total:.0%}")
    man = d.groupby("Aircraft Manufacturer")["Landing Count"].sum().sort_values(ascending=False).head(3)
    print("   By manufacturer: " + ", ".join(f"{k} {v / total:.0%}" for k, v in man.items()))
    print()

    # 4. International share over time
    intl = d[d["GEO Summary"] == "International"].groupby("year")["Landing Count"].sum() / yearly
    print("4. International share of landings:")
    for y in [2000, 2010, 2019, 2024]:
        print(f"   {y}: {intl[y]:.0%}")
    reg = d[d["GEO Summary"] == "International"].groupby("GEO Region")["Landing Count"].sum()
    reg = (reg / reg.sum()).sort_values(ascending=False).head(4)
    print("   Top international regions: " + ", ".join(f"{k} {v:.0%}" for k, v in reg.items()))
    cargo = d.loc[d["Landing Aircraft Type"] == "Freighter", "Landing Count"].sum() / total
    print(f"   Freighter share of all landings: {cargo:.1%}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
