from pybit.unified_trading import HTTP
import numpy as np
import time
from signalParser import instrum
from signalParser import direction
from signalParser import take_values

constI = 'USDT'
apiKey = ''
apiSecret = ''
_Symbol = instrum + constI

session = HTTP(
    api_key = apiKey,
    api_secret = apiSecret
)
req=session.get_wallet_balance(accountType="CONTRACT")
print(req)

print("1",session.place_order(
    category="spot",
    symbol=_Symbol,
    side=direction,
    orderType="Limit",
    qty= 11.35,
    price = 2.1400
))