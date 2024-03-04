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


    


    #current_portfolio_value = last_price * quantity

    # Calculate potential gains, with use threeYearAverageReturn as possibility for stocks where we do not have the 
    mean_portfolio_gain_possible = mean_portfolio_value - current_portfolio_value if mean_portfolio_value else threeYearAverageReturn*current_portfolio_value
    median_portfolio_gain_possible = median_portfolio_value - current_portfolio_value if median_portfolio_value else threeYearAverageReturn*current_portfolio_value
    high_portfolio_gain_possible = high_portfolio_value - current_portfolio_value if high_portfolio_value else threeYearAverageReturn*current_portfolio_value


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


print("Max Gain possible: ",  df['high_portfolio_gain_possible'].sum())
print("Median Gain Possible:", df['Median Portfolio Gain Possible'].sum())
print("Average Gain Possible:", df['Mean Portfolio Gain Possible'].sum())
