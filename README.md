# SFO Airline Operations and Fleet Mix Analysis

A Power BI analysis of every reported landing at San Francisco International Airport (SFO) from July 1999 through October 2025: 4.67 million landings across 44,829 monthly records.

## Questions

1. Which airlines land the most at SFO?
2. How has landing activity changed over time, and how far has it recovered since COVID?
3. How much of SFO's traffic is international, and where does it come from?
4. Which aircraft account for the most landings?

## Key findings

- **United dominates.** Combining its two dataset labels (see Data checks), United accounts for 33% of all landings, followed by SkyWest at 22%. SkyWest's flying at SFO is almost entirely domestic (97%), consistent with its role as a regional feeder.
- **Recovery is real but incomplete.** Landings fell by half in 2020 (8,700 a month vs 17,700 in 2019). Through October 2025, SFO is at 90% of the same months in 2019.
- **SFO is becoming more international.** The international share of landings grew from 12% in 2000 to 19% in 2019 and 22% in 2024. Asia leads international traffic (36%), followed by Canada (24%), Europe (19%) and Mexico (13%).
- **Two aircraft families carry the airport.** The Boeing 737 family (26%) and the Airbus A320 family (22%) make up nearly half of all landings. By manufacturer, Boeing leads with 49%, then Airbus (24%) and Embraer (14%).
- **Cargo is a small slice.** Dedicated freighters account for 2% of landings.

## Dashboard

### Top 10 airlines by landings
![Top 10 Airlines](visuals/top_10_airlines_sfo.png)

The chart shows United on two rows because the source data labels United's records before July 1, 2013 separately. Combined, United leads with 1.56 million landings.

### Domestic vs international landings
![Domestic vs International](visuals/domestic_vs_international_sfo.png)

### Landings over time (1999 to 2025)
![Landings Over Time](visuals/sfo_landings_over_time.png)

1999 includes only July to December and 2025 only January to October, so the low points at each end of this chart reflect partial years, not drops in traffic.

### Top aircraft models by landings (as reported)
![Top Aircraft Models](visuals/top_aircraft_models_sfo.png)

Model codes change detail over time: early records report "737," while later ones split it into B738, B739 and MAX variants. The family totals in Key findings group these together.

## Data checks

Before trusting a chart, I checked how the data was recorded. Three quirks would mislead anyone who charts the raw table:

| Issue | Effect on a raw chart | How I handled it |
|---|---|---|
| United is split into "United Airlines" and "United Airlines - Pre 07/01/2013" | SkyWest looks like the top airline | Combined the labels for rankings |
| 1999 and 2025 are partial years (6 and 10 months) | Fake dips at both ends of the trend line | Compared average landings per month and like for like months |
| Aircraft model codes change specificity over time | The 737 family is spread across 11 codes | Grouped models into families |

`data_checks.py` reproduces every number in this README from the source CSV:

```bash
pip install pandas
python data_checks.py Air_Traffic_Landings_Statistics.csv
```

## Data

**Source:** [Air Traffic Landings Statistics](https://catalog.data.gov/dataset/air-traffic-landings-statistics), published monthly by the City and County of San Francisco on DataSF (dataset `fpux-q53t`).

Each row is aggregated monthly landing activity by operating airline, region, and aircraft type, body type, manufacturer and model, with Landing Count as the measure. There is no flight level detail and no primary key, so the table is modeled as a single fact table.

Columns used: Activity Period Start Date, Operating Airline, Operating Airline IATA Code, GEO Summary, GEO Region, Landing Aircraft Type, Aircraft Body Type, Aircraft Manufacturer, Aircraft Model, Landing Count.

## Tools

- Power BI Desktop for modeling and visuals
- Power Query for data preparation
- Python (pandas) for data validation

## Limitations

- Airlines are counted as the operating carrier at the time of landing. Regional carriers such as SkyWest are not rolled into the brands they fly for.
- The data counts landings, not passengers or seats, so a regional jet and a 777 each count as one landing.

## Next steps

- Use the Published Airline column to measure United's full network share, including flights operated by SkyWest as United Express
- Add passenger counts from SFO's companion passenger statistics dataset to compare landings with seats
- Track the international share monthly to see whether the post COVID rise holds
