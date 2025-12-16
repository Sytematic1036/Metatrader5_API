import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import os

if not mt5.initialize():
    print(f"Initialisering misslyckades: {mt5.last_error()}")
    quit()

# Hamta alla symboler
symbols = mt5.symbols_get()

# Filtrera pa kategori
selected_categories = ["Forex", "Metals", "Indexes"]
selected_symbols = []

for symbol in symbols:
    path = symbol.path
    if '\\' in path:
        category = path.split('\\')[0]
    else:
        category = path

    if category in selected_categories:
        selected_symbols.append((category, symbol.name))

print(f"Laddar ner data for {len(selected_symbols)} instrument...")
print(f"  Forex: {sum(1 for c, _ in selected_symbols if c == 'Forex')}")
print(f"  Metals: {sum(1 for c, _ in selected_symbols if c == 'Metals')}")
print(f"  Indexes: {sum(1 for c, _ in selected_symbols if c == 'Indexes')}")
print("-" * 50)

# Skapa Download-mappen
output_dir = "Download"
os.makedirs(output_dir, exist_ok=True)

# Samla data per kategori
all_data = []
success_count = 0

for category, symbol_name in selected_symbols:
    rates = mt5.copy_rates_from_pos(symbol_name, mt5.TIMEFRAME_D1, 0, 3)

    if rates is not None and len(rates) > 0:
        for rate in rates:
            all_data.append({
                'category': category,
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

print(f"\nResultat:")
print(f"  Lyckade: {success_count} instrument")
print(f"  Misslyckade: {len(selected_symbols) - success_count} instrument")

# Spara till CSV
if all_data:
    df = pd.DataFrame(all_data)
    output_file = os.path.join(output_dir, "forex_metals_indexes_3days_D1.csv")
    df.to_csv(output_file, index=False)
    print(f"\nData sparad till: {output_file}")
    print(f"Totalt antal rader: {len(df)}")

    # Visa sammanfattning per kategori
    print(f"\nSammanfattning per kategori:")
    print(df.groupby('category')['symbol'].nunique())

    print(f"\nForsta 15 raderna:")
    print(df.head(15).to_string())

mt5.shutdown()
