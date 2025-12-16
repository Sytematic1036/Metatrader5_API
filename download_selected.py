import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import os

if not mt5.initialize():
    print(f"Initialisering misslyckades: {mt5.last_error()}")
    quit()

# Lista med valda symboler
SELECTED_SYMBOLS = [
    "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDSEK", "AUDSGD", "AUDUSD",
    "CADCHF", "CADJPY", "CADSGD",
    "CHFDKK", "CHFHUF", "CHFJPY", "CHFNOK", "CHFPLN", "CHFSEK", "CHFSGD",
    "DKKSEK",
    "EURAUD", "EURCAD", "EURCHF", "EURCNH", "EURCZK", "EURDKK", "EURGBP",
    "EURHKD", "EURHUF", "EURJPY", "EURMXN", "EURNOK", "EURNZD", "EURPLN",
    "EURRUR", "EURSEK", "EURSGD", "EURTRY", "EURUSD", "EURZAR",
    "GBPAUD", "GBPCAD", "GBPCHF", "GBPCZK", "GBPDKK", "GBPHUF", "GBPJPY",
    "GBPMXN", "GBPNOK", "GBPNZD", "GBPPLN", "GBPSEK", "GBPSGD", "GBPTRY",
    "GBPUSD", "GBPZAR",
    "HKDJPY", "NOKJPY", "NOKSEK",
    "NZDCAD", "NZDCHF", "NZDDKK", "NZDJPY", "NZDSEK", "NZDSGD", "NZDUSD",
    "SEKJPY", "SGDHKD", "SGDJPY", "TRYJPY",
    "USDCAD", "USDCHF", "USDCNH", "USDCZK", "USDDKK", "USDHKD", "USDHUF",
    "USDILS", "USDJPY", "USDMXN", "USDNOK", "USDPLN", "USDRMB", "USDSEK",
    "USDSGD", "USDTHB", "USDTRY", "USDZAR",
    "XAUUSD", "XAUEUR", "XAUAUD", "XAGUSD", "XAGEUR", "XPDUSD", "XPTUSD",
    "XAGAUD", "XAUCHF", "XAUGBP",
    "AUS200", "EUSTX50", "FRA40", "HK50", "JPN225", "US500", "US30M",
    "US500M", "USTECH100M", "GER30M", "DE40", "US30", "USTEC", "CHINA50",
    "CHINAH", "US2000", "ZARJPY"
]

# Konfiguration
YEARS_TO_DOWNLOAD = 1  # Antal kalenderaar (1 = fran 1 jan i ar, 2 = fran 1 jan forra aret, osv)
TIMEFRAME = mt5.TIMEFRAME_D1

# Berakna datumintervall baserat pa kalenderaar
current_year = datetime.now().year
start_year = current_year - YEARS_TO_DOWNLOAD + 1
start_date = datetime(start_year, 1, 1)
end_date = datetime.now()

# Hamta alla symboler fran MT5
all_symbols = mt5.symbols_get()
available_symbols = {s.name: s.path for s in all_symbols}

# Filtrera till endast valda som finns
valid_symbols = []
missing_symbols = []

for symbol in SELECTED_SYMBOLS:
    if symbol in available_symbols:
        path = available_symbols[symbol]
        if '\\' in path:
            category = path.split('\\')[0]
        else:
            category = path
        valid_symbols.append((category, symbol))
    else:
        missing_symbols.append(symbol)

print(f"Valda symboler: {len(SELECTED_SYMBOLS)}")
print(f"Tillgangliga: {len(valid_symbols)}")
print(f"Saknas hos maklaren: {len(missing_symbols)}")
print(f"Period: {start_date.strftime('%Y-%m-%d')} till {end_date.strftime('%Y-%m-%d')} ({YEARS_TO_DOWNLOAD} kalenderaar)")

if missing_symbols:
    print(f"\nSaknade symboler: {', '.join(missing_symbols[:10])}")

print("-" * 50)

# Skapa Download-mappen
output_dir = "Download"
os.makedirs(output_dir, exist_ok=True)

# Ladda ner och spara varje symbol separat
success_count = 0
failed_symbols = []

for i, (category, symbol_name) in enumerate(valid_symbols):
    rates = mt5.copy_rates_range(symbol_name, TIMEFRAME, start_date, end_date)

    if rates is not None and len(rates) > 0:
        # Skapa DataFrame
        data = []
        for rate in rates:
            data.append({
                'time': datetime.fromtimestamp(rate['time']).strftime('%Y-%m-%d'),
                'open': rate['open'],
                'high': rate['high'],
                'low': rate['low'],
                'close': rate['close'],
                'tick_volume': rate['tick_volume'],
                'spread': rate['spread']
            })

        df = pd.DataFrame(data)

        # Spara till Excel med symbol_category som filnamn
        output_file = os.path.join(output_dir, f"{symbol_name}_{category}.xlsx")
        df.to_excel(output_file, sheet_name='Data', index=False, engine='openpyxl')

        success_count += 1

        # Visa progress
        if (i + 1) % 20 == 0 or (i + 1) == len(valid_symbols):
            print(f"Progress: {i + 1}/{len(valid_symbols)} ({symbol_name}: {len(df)} rader)")
    else:
        failed_symbols.append(symbol_name)

print("-" * 50)
print(f"\nResultat:")
print(f"  Lyckade: {success_count} filer skapade")
print(f"  Misslyckade: {len(failed_symbols)} instrument")

if failed_symbols:
    print(f"  Misslyckade symboler: {', '.join(failed_symbols)}")

print(f"\nFiler sparade i: {os.path.abspath(output_dir)}")

mt5.shutdown()
