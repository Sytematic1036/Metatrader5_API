import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import os

if not mt5.initialize():
    print(f"Initialisering misslyckades: {mt5.last_error()}")
    quit()

# Hamta alla tillgangliga symboler
symbols = mt5.symbols_get()
print(f"Antal tillgangliga instrument: {len(symbols)}")

# Skapa Download-mappen om den inte finns
output_dir = "Download"
os.makedirs(output_dir, exist_ok=True)

# Samla all data
all_data = []
success_count = 0
failed_symbols = []

print(f"\nLaddar ner 3 dagars D1-data for {len(symbols)} instrument...")
print("-" * 50)

for i, symbol in enumerate(symbols):
    symbol_name = symbol.name

    # Hamta 3 bars (3 dagar)
    rates = mt5.copy_rates_from_pos(symbol_name, mt5.TIMEFRAME_D1, 0, 3)

    if rates is not None and len(rates) > 0:
        for rate in rates:
            all_data.append({
                'symbol': symbol_name,
                'time': datetime.fromtimestamp(rate['time']),
                'open': rate['open'],
                'high': rate['high'],
                'low': rate['low'],
                'close': rate['close'],
                'tick_volume': rate['tick_volume'],
                'spread': rate['spread'],
                'real_volume': rate['real_volume']
            })
        success_count += 1
    else:
        failed_symbols.append(symbol_name)

    # Visa progress var 1000:e symbol
    if (i + 1) % 1000 == 0:
        print(f"Progress: {i + 1}/{len(symbols)} instrument...")

print("-" * 50)
print(f"\nResultat:")
print(f"  Lyckade: {success_count} instrument")
print(f"  Misslyckade: {len(failed_symbols)} instrument")

# Spara till CSV
if all_data:
    df = pd.DataFrame(all_data)
    output_file = os.path.join(output_dir, "all_instruments_3days_D1.csv")
    df.to_csv(output_file, index=False)
    print(f"\nData sparad till: {output_file}")
    print(f"Totalt antal rader: {len(df)}")
    print(f"\nForsta 10 raderna:")
    print(df.head(10))

mt5.shutdown()
