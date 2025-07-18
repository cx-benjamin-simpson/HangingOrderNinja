import pandas as pd
from ib_insync import *

# Connect to TWS or IB Gateway
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Request delayed data if real-time is unavailable
ib.reqMarketDataType(1)  # 3 = delayed, 1 = real-time, 2 = frozen

# Load the CSV
df = pd.read_csv('orders.csv')

for index, row in df.iterrows():
    symbol = row['Symbol']
    qty = int(row['Quantity'])
    trailing_pct = float(row['TrailingPercent'])
    limit_offset = float(row['LimitOffset'])
    avg_buy_price = float(row['AvgBuyPrice'])

    print(f"\n[INFO] Processing {symbol}")

    # Define contract
    contract = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(contract)

    # Request market data
    ticker = ib.reqMktData(contract, '', False, False)
    ib.sleep(2)

    # Get market price
    current_ask = ticker.ask()


# Calculate midprice
# bid = ticker.bid
# ask = ticker.ask
# midprice = (bid + ask) / 2 if bid and ask else None

    # Fallback to CSV value if market price is unavailable
    if current_ask is None or pd.isna(current_ask):
        if 'MarketPrice' in row and not pd.isna(row['MarketPrice']):
            current_ask = float(row['MarketPrice'])
            print(f"[INFO] Using CSV price for {symbol}: {current_ask}")
        else:
            print(f"[SKIP] No market price for {symbol} (possibly due to no delayed data)")
            continue

    if current_ask <= avg_buy_price:
        print(f"[SKIP] {symbol}: Market price {current_ask:.2f} <= Avg Buy Price {avg_buy_price:.2f}")
        continue

    # Calculate stop and limit price
    stop_price = round(current_ask * (1 - trailing_pct / 100), 2)
    limit_price = round(stop_price - limit_offset, 2)

    if limit_price <= avg_buy_price:
        print(f"[SKIP] {symbol}: Limit price {limit_price:.2f} is below average buy price {avg_buy_price:.2f}")
        continue

    # Create stop limit order
    order = Order(
        action='SELL',
        orderType='STP LMT',
        totalQuantity=qty,
        auxPrice=stop_price,   # Stop trigger price
        lmtPrice=limit_price,  # Limit price
        tif='GTC'
    )

    # Place order
    trade = ib.placeOrder(contract, order)
    ib.sleep(1)

    # Check result
    if trade.orderStatus.status in ['Submitted', 'PreSubmitted']:
        print(f"[OK] Order submitted for {symbol} at stop {stop_price}, limit {limit_price}")
    else:
        print(f"[FAIL] Order failed for {symbol}: {trade.orderStatus.status}")

ib.disconnect()
