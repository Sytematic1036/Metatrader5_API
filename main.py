import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

# Initiera anslutning till MT5-terminalen
if not mt5.initialize():
    print(f"Initialisering misslyckades: {mt5.last_error()}")
    quit()

print(f"MT5 version: {mt5.version()}")

# Hämta tillgängliga symboler
symbols = mt5.symbols_get()
print(f"Antal tillgängliga instrument: {len(symbols)}")

# Hämta OHLCV-data för ett specifikt instrument
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_D1  # Daglig data
bars = 1000  # Antal bars

rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)

# Konvertera till DataFrame
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')
print(df.head())

# Stäng anslutningen
mt5.shutdown()
