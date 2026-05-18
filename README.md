# Fidelity Portfolio Target Price Analyzer

Prepared by **Arvind Radhakrishnen** — Open Source

## Overview

This Python script analyzes a Fidelity portfolio positions export file and estimates possible portfolio upside using target price data from Yahoo Finance.

It reads a Fidelity consolidated positions CSV, retrieves target mean, median, and high prices for each ticker using the `yfinance` library, calculates potential profitability and portfolio value scenarios, and exports the enriched results to `output.csv`.

The script is designed to run in **Google Colab**.

## What the Script Does

The workflow performs the following steps:

1. Loads a Fidelity portfolio positions CSV file into a pandas DataFrame.
2. Reads each holding's ticker symbol, quantity, current value, cost basis, and price information.
3. Uses Yahoo Finance through `yfinance` to retrieve:
   - Target mean price
   - Target median price
   - Target high price
   - Three-year average return
4. Calculates potential profitability for each holding under mean, median, and high target price scenarios.
5. Calculates potential portfolio value and gain possibilities.
6. Writes the enriched portfolio data to `output.csv`.
7. Prints total cost basis and estimated gain potential summaries.

## Expected Input File

The script expects a Fidelity portfolio positions export CSV file.

Update this line in the script to match the file name you upload to Google Colab:

```python
df = pd.read_csv("/content/Portfolio_Positions_Mar-03-2024.csv")
```

### Required Input Columns

The Fidelity CSV should include the following columns:

| Column | Description |
|---|---|
| Account Number | Account identifier |
| Account Name | Account name |
| Symbol | Asset ticker symbol |
| Description | Asset description |
| Quantity | Number of shares or units held |
| Last Price | Last traded price |
| Last Price Change | Change in latest price |
| Current Value | Current value of the position |
| Today's Gain/Loss Dollar | Daily gain or loss in dollars |
| Today's Gain/Loss Percent | Daily gain or loss percentage |
| Total Gain/Loss Dollar | Total dollar gain or loss |
| Total Gain/Loss Percent | Total gain or loss percentage |
| Percent Of Account | Position weight within the account |
| Cost Basis Total | Total cost basis |
| Average Cost Basis | Average cost basis |
| Type | Asset type, such as stock, bond, or ETF |

## Derived Yahoo Finance Fields

The script uses Yahoo Finance data to derive these values:

| Field | Description |
|---|---|
| Target Mean Price | Mean analyst target price |
| Target Median Price | Median analyst target price |
| Target High Price | High analyst target price |
| threeYearAverageReturn | Three-year average return when available |

## Calculated Output Fields

The script adds the following calculated columns:

| Field | Description |
|---|---|
| Mean Profitability (%) | Estimated percentage upside/downside using mean target price |
| Median Profitability (%) | Estimated percentage upside/downside using median target price |
| High Profitability (%) | Estimated percentage upside/downside using high target price |
| Mean Portfolio Value | Estimated holding value using mean target price |
| Median Portfolio Value | Estimated holding value using median target price |
| High Portfolio Value | Estimated holding value using high target price |
| Mean Portfolio Gain Possible | Potential gain using mean target price |
| Median Portfolio Gain Possible | Potential gain using median target price |
| high_portfolio_gain_possible | Potential gain using high target price |

## Setup

### 1. Open Google Colab

Create a new Google Colab notebook.

### 2. Install Required Libraries

Run the following command if `yfinance` is not already installed:

```python
!pip install yfinance pandas
```

### 3. Upload the Fidelity CSV File

Upload your Fidelity portfolio positions CSV into the Colab environment.

Example file path:

```text
/content/Portfolio_Positions_Mar-03-2024.csv
```

### 4. Update the File Path

Modify the `pd.read_csv()` line in the script so it points to your uploaded CSV file.

```python
df = pd.read_csv("/content/YOUR_FILE_NAME.csv")
```

### 5. Run the Script

Run all cells in the notebook.

## Output

The script creates an enriched CSV file:

```text
output.csv
```

This file includes the original Fidelity portfolio data plus the Yahoo Finance target prices and portfolio upside calculations.

The script also prints summary metrics such as:

```text
Max Gain possible
Median Gain Possible
Average Gain Possible
```

Each summary compares estimated possible gain against the total portfolio cost basis.

## Example Summary Output

```text
Max Gain possible:  12500.0 against a total cost basis of 100000.0 which is 12.5 %
Median Gain Possible:  8500.0 against a total cost basis of 100000.0 which is 8.5 %
Average Gain Possible:  9000.0 against a total cost basis of 100000.0 which is 9.0 %
```

## Key Functions

### `get_target_price(symbol)`

Retrieves target price and return information from Yahoo Finance for a given stock symbol.

Returns:

```python
target_mean_price, target_median_price, threeYearAverageReturn, target_high_price
```

### `analyze_stock(row)`

Processes each portfolio row and calculates:

- Target price metrics
- Profitability percentages
- Estimated target portfolio values
- Potential gain scenarios

## Error Handling

If Yahoo Finance data is unavailable for a symbol, the script assigns fallback values:

```python
target_mean_price = 0
target_median_price = 0
target_high_price = 0
threeYearAverageReturn = 0.1
```

This allows the script to continue processing even when some ticker data is missing.

## Important Notes

- Yahoo Finance target prices may not be available for every symbol.
- Some asset types, such as cash positions, mutual funds, bonds, or unsupported tickers, may return incomplete data.
- The script performs basic cleanup for dollar signs and missing values in fields such as `Cost Basis Total`.
- This analysis is only an estimate and should not be treated as financial advice.
- Validate results before using them for investment decisions.

## Suggested Improvements

Potential future enhancements include:

- Add command-line arguments or notebook widgets for the input file path.
- Improve currency and numeric parsing for all price-related fields.
- Add logging instead of print statements.
- Add validation for required CSV columns.
- Separate the logic into reusable functions or modules.
- Export a summary report in Excel or PDF format.
- Add charts for portfolio upside scenarios.
- Cache Yahoo Finance API calls to reduce repeated requests.

## License

Open source. 

## Disclaimer

This tool is for educational and analytical purposes only. It does not provide investment, financial, tax, or legal advice. Always consult a qualified professional before making investment decisions.
