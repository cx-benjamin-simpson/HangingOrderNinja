# HangingOrderNinja
A tool for placing hanging orders stealthily in  IBKR
This tool reads stock order data from a CSV file and places GTC trailing stop-limit orders with logic to protect against selling below your average buy price.

Join the Bigshort.com Discord and ping Berkshire-RSI-King for questions

## Features
Connects to Interactive Brokers via TWS or IB Gateway using API
Supports delayed data fallback if real-time quotes are unavailable
Reads orders from a CSV file including:
- Symbol (e.g., AAPL, TSLA)
- Quantity
- Trailing stop percentage
- Limit price offset
- Average buy price (to prevent selling at a loss)

Dynamically calculates stop and limit prices based on live market prices

Places Good-Till-Canceled (GTC) trailing stop-limit sell orders
Logs all order activity, errors, and skipped trades
## Requirements
Python 3.7 or higher
IBKR Trader Workstation (TWS) or IB Gateway running and API enabled
Python libraries:
ib_insync
pandas
## Setup Instructions
Clone this repository
Install required Python packages
Launch IBKR TWS or IB Gateway with API enabled
Prepare your CSV file with the required columns:
Symbol, Quantity, TrailingPercent, LimitOffset, AvgBuyPrice
## How to Use
Start your TWS/IB Gateway and ensure it's connected
Run the script with your CSV file path as input
Orders will be submitted, and logs will be generated showing each action
