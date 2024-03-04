#Prepared by Arvind Radhakrishnen - Open Source
#Run this code on Google Colab. Upload your fidelity portfolio file 

'''
Attributes sourced from Input File - Fidelity consolidation position export file

Account Number	Number assigned to the account
Account Name	Name of the account
Symbol	Symbol of the asset
Description	Description of the asset
Quantity	Quantity of the asset held in the account
Last Price	Last traded price of the asset
Last Price Change	Change in price since the last trade
Current Value	Total value of the asset at the last traded price
Today's Gain/Loss Dollar	Dollar amount gained or lost since last trade
Today's Gain/Loss Percent	Percentage gain or loss since last trade
Total Gain/Loss Dollar	Total dollar amount gained or lost since purchase
Total Gain/Loss Percent	Total percentage gain or loss since purchase
Percent Of Account	Percentage of the asset's value in the total account
Cost Basis Total	Total cost basis of the asset
Average Cost Basis	Average cost basis of the asset
Type	Type of asset (e.g., stock, bond, ETF)


Attributes derived using Yahoo Finance to estimate price targets

Target Mean Price	Mean target price of the asset
Target Median Price	Median target price of the asset
Three-Year Average Return	Three-year average return of the asset

Attributes calculated as part of the logic

Mean Profitability (%)	Mean profitability percentage of the asset
Median Profitability (%)	Median profitability percentage of the asset
High Profitability (%)	High profitability percentage of the asset
Mean Portfolio Value	Mean value of the entire portfolio
Median Portfolio Value	Median value of the entire portfolio
High Portfolio Value	High value of the entire portfolio
Mean Portfolio Gain Possible	Mean possible gain of the entire portfolio
Median Portfolio Gain Possible	Median possible gain of the entire portfolio
High Portfolio Gain Possible	High possible gain of the entire portfolio

'''

import yfinance as yf
def get_target_price(symbol):
  stock = yf.Ticker(symbol)


  # Fetch the latest stock price
  stock_info = stock.info
      
  # Extract target mean and median prices
  target_mean_price = stock_info.get('targetMeanPrice')
  target_median_price = stock_info.get('targetMedianPrice')
  return target_mean_price, target_median_price


import pandas as pd
#update the location of your fidelity portfolio positions file here in Colab
df = pd.read_csv("/content/Portfolio_Positions_Mar-03-2024.csv")

# Define the get_target_price function
def get_target_price(symbol):
    
    try:
        
      stock = yf.Ticker(symbol)
      stock_info = stock.info
      target_mean_price = stock_info.get('targetMeanPrice')
      target_median_price = stock_info.get('targetMedianPrice')
      target_high_price = stock_info.get('targetHighPrice')
      threeYearAverageReturn = stock_info.get('threeYearAverageReturn')

    except:
      target_mean_price = 0
      target_median_price = 0
      threeYearAverageReturn = 0.1
      target_high_price = 0
    return target_mean_price, target_median_price, threeYearAverageReturn, target_high_price

# Apply the function to each Symbol in the DataFrame
def analyze_stock(row):
    symbol = row['Symbol']
    last_price = row['Average Cost Basis']
    quantity = row['Quantity']
    current_portfolio_value=row['Current Value']
    last_price = row['Last Price']
    cost_basis_total = row['Cost Basis Total']
    total_gain_loss = row['Total Gain/Loss Dollar']


    #print(symbol, last_price, quantity)
    target_mean_price, target_median_price, threeYearAverageReturn, targetHighPrice = get_target_price(symbol)
    
    # Convert target prices to float for comparison and calculations
    try:
        target_mean_price = float(target_mean_price)
    except (TypeError, ValueError):
        target_mean_price = None

    # Convert target prices to float for comparison and calculations
    try:
        targetHighPrice = float(targetHighPrice)
    except (TypeError, ValueError):
        targetHighPrice = None

      # Convert threeYearAverageReturn to float for comparison and calculations
    try:
        threeYearAverageReturn = float(threeYearAverageReturn)
    except (TypeError, ValueError):
        threeYearAverageReturn = 0.1

    try:
        target_median_price = float(target_median_price)
    except (TypeError, ValueError):
        target_median_price = None

    # Calculate profitability based on target mean and median prices
    if target_mean_price is not None:
        try:
          last_price = last_price.replace("$", "")
        except:
          last_price = float(last_price)

        last_price = float(last_price)
        mean_profitability = ((target_mean_price - last_price) / last_price) * 100
        mean_portfolio_value = target_mean_price * quantity

    else:
        mean_profitability = None
        mean_portfolio_value = None
        
    if target_median_price is not None:
        median_profitability = ((target_median_price - last_price) / last_price) * 100
        median_portfolio_value = target_median_price * quantity

    else:
        median_profitability = None
        median_portfolio_value= None
  
    if targetHighPrice is not None:
          high_profitability = ((targetHighPrice - last_price) / last_price) * 100
          high_portfolio_value = targetHighPrice * quantity

    else:
          high_profitability = None
          high_portfolio_value= None
    

    try:
      last_price = last_price.replace("$", "")
    except:
      last_price = float(last_price)
      
    try:
      last_price = float(last_price)
    except:
      last_price = 0

    try:
      current_portfolio_value = current_portfolio_value.replace("$", "")
    except:
      current_portfolio_value = float(current_portfolio_value)
    
    current_portfolio_value = float(current_portfolio_value)

    try:
      total_gain_loss = total_gain_loss.replace("$", "")
      total_gain_loss = total_gain_loss.replace("--", "0")

    except:
      total_gain_loss = float(total_gain_loss)

    total_gain_loss = float(total_gain_loss)

    

    #current_portfolio_value = last_price * quantity

    # Calculate potential gains, with use threeYearAverageReturn as possibility for stocks where we do not have the 
    mean_portfolio_gain_possible = mean_portfolio_value - current_portfolio_value if mean_portfolio_value else (threeYearAverageReturn*current_portfolio_value) + total_gain_loss
    median_portfolio_gain_possible = median_portfolio_value - current_portfolio_value if median_portfolio_value else (threeYearAverageReturn*current_portfolio_value)  + total_gain_loss
    high_portfolio_gain_possible = high_portfolio_value - current_portfolio_value if high_portfolio_value else (threeYearAverageReturn*current_portfolio_value) +   total_gain_loss


    return pd.Series([
        target_mean_price, target_median_price, threeYearAverageReturn, mean_profitability, median_profitability,high_profitability,
        mean_portfolio_value, median_portfolio_value,high_portfolio_value,  mean_portfolio_gain_possible, median_portfolio_gain_possible, high_portfolio_gain_possible
    ])

    #return pd.Series([target_mean_price, target_median_price, mean_profitability, median_profitability])


# Add new columns to the DataFrame
df[['Target Mean Price', 'Target Median Price', 'threeYearAverageReturn', 'Mean Profitability (%)', 'Median Profitability (%)', 'High Profitability (%)',
    'Mean Portfolio Value', 'Median Portfolio Value', 'High Portfolio Value',  'Mean Portfolio Gain Possible', 'Median Portfolio Gain Possible', 'high_portfolio_gain_possible']] = df.apply(analyze_stock, axis=1)

# Add new columns to the DataFrame
#df[['Target Mean Price', 'Target Median Price', 'Mean Profitability (%)', 'Median Profitability (%)']] = df.apply(analyze_stock, axis=1)

# Show the updated DataFrame
#print(df)
df.to_csv("output.csv")

df['Cost Basis Total'] = df['Cost Basis Total'].str.replace('$', '')
df['Cost Basis Total'] = df['Cost Basis Total'].str.replace('--', '0')

# Convert NaN values to 0
df['Cost Basis Total'] = df['Cost Basis Total'].fillna('0')

print(df['Cost Basis Total'])


# Convert values to float
df['Cost Basis Total'] = df['Cost Basis Total'].astype(float)
cost_basis_total = df['Cost Basis Total'].sum()

print(cost_basis_total)
max_gain_possible = df['high_portfolio_gain_possible'].sum()/cost_basis_total
median_gain_possible = df['Median Portfolio Gain Possible'].sum()/cost_basis_total
avg_gain_possible = df['Mean Portfolio Gain Possible'].sum()/cost_basis_total


print("Max Gain possible: ",  df['high_portfolio_gain_possible'].sum() , " against a total cost basis of ", df['Cost Basis Total'].sum(), " which is ", float(max_gain_possible*100), "%")
print("Median Gain Possible:", df['Median Portfolio Gain Possible'].sum() , " against a total cost basis of ", df['Cost Basis Total'].sum(), " which is ", float(median_gain_possible*100), "%")
print("Average Gain Possible:", df['Mean Portfolio Gain Possible'].sum() , " against a total cost basis of ", df['Cost Basis Total'].sum(), " which is ", float(avg_gain_possible*100), "%")

