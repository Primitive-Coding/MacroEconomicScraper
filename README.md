# Macroeconimic Scraper

Get the most recent macroeconomic data including:

- Consumer Price Index (CPI)
- Fed Funds Rate
- 10Y - 2Y Treasury Yield Spread

---

### Setup

1. Clone git repository: `https://github.com/PrimalFinance/MacroEconomicScraper.git`
1. Configure the "config.json" file.

```
    {
        "chrome_driver_path": "D:\\PATH TO CHROME DRIVER\\chromedriver.exe",
        "data_export_path": "D:\\PATH TO EXPORT DATA"
    }

```

3. Install the projects requirements with `pip install -r requirements.txt`

---

### Instructions

- Create a class instance. If debug is set to true, various pieces of information will be logged to confirm steps of scraping were completed.

```
    m = MacroScraper()

    # m = MacroScraper(debug=True)
```

###### CPI Data

- Get CPI data. Initially it will read from a local csv file.
  - If a csv file does not exist, it will externally fetch data and create a csv file for use next time.
  - Alternatively you can force an update with this function call: `m.update_cpi()`

```
    df = m.get_cpi()

    # Output
            Value
    Date
    2024-5   3.269
    2024-4   3.357
    2024-3   3.477
    2024-2   3.153
    2024-1   3.091
    ...        ...
    1914-5   2.062
    1914-4   0.000
    1914-3   1.020
    1914-2   1.020
    1914-1   2.041
```

###### Fed Funds Data

- Get historical Federal Funds Rate data.
- Similar to CPI, it will check for data locally and write the data locally if files do not already exist.
- Force an update with `m.update_fed_funds()`

```
    m.get_fed_funds()

    # Output

             Value
    Date
    2023-9   5.33
    2023-8   5.33
    2023-7   5.12
    2023-6   5.08
    2023-5   5.06
    ...       ...
    1954-11  0.83
    1954-10  0.85
    1954-9   1.07
    1954-8   1.22
    1954-7   0.80
```

###### 10 Year - 2 Year Treasury Spread

- Get historical data related to the 10Y 2Y Treasury spread.
- Force an update with `m.update_treasury_yield_spread()`

```
    m.get_treasury_yield_spread()

    # Output

            Value
    Date
    2024-5   -0.38
    2024-3   -0.38
    2024-2   -0.33
    2024-1   -0.26
    ...        ...
    1976-10   1.43
    1976-9    1.17
    1976-8    1.14
    1976-7    0.98
    1976-6    0.80
```
