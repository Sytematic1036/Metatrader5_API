import MetaTrader5 as mt5
from datetime import datetime

if not mt5.initialize():
    print(f"Initialisering misslyckades: {mt5.last_error()}")
    quit()

symbol = "EURUSD"

timeframes = [
    ("M1", mt5.TIMEFRAME_M1, 50000),
    ("M5", mt5.TIMEFRAME_M5, 50000),
    ("M15", mt5.TIMEFRAME_M15, 50000),
    ("H1", mt5.TIMEFRAME_H1, 50000),
    ("H4", mt5.TIMEFRAME_H4, 20000),
    ("D1", mt5.TIMEFRAME_D1, 10000),
    ("W1", mt5.TIMEFRAME_W1, 5000),
    ("MN1", mt5.TIMEFRAME_MN1, 1000),
]

print(f"Datatillgaenglighet foer {symbol}:\n")
print(f"{'Timeframe':<10} {'Foersta datum':<20} {'Antal bars':<12} {'Aar bakaat':<10}")
print("-" * 55)

for name, tf, max_bars in timeframes:
    rates = mt5.copy_rates_from_pos(symbol, tf, 0, max_bars)
    if rates is not None and len(rates) > 0:
        first_date = datetime.fromtimestamp(rates[0]['time'])
        years_back = (datetime.now() - first_date).days / 365.25
        print(f"{name:<10} {first_date.strftime('%Y-%m-%d'):<20} {len(rates):<12} {years_back:.1f}")
    else:
        error = mt5.last_error()
        print(f"{name:<10} Ingen data - Error: {error}")

mt5.shutdown()
