import MetaTrader5 as mt5
from collections import defaultdict

if not mt5.initialize():
    print(f"Initialisering misslyckades: {mt5.last_error()}")
    quit()

symbols = mt5.symbols_get()
print(f"Totalt antal instrument: {len(symbols)}\n")

# Gruppera efter path (kategori)
categories = defaultdict(list)

for symbol in symbols:
    # Path innehaller kategorin, t.ex. "Forex\EURUSD" -> "Forex"
    path = symbol.path
    if '\\' in path:
        category = path.split('\\')[0]
    else:
        category = path
    categories[category].append(symbol.name)

# Visa kategorier sorterade efter antal instrument
print(f"{'Kategori':<40} {'Antal instrument':<15}")
print("=" * 60)

sorted_categories = sorted(categories.items(), key=lambda x: -len(x[1]))

for category, symbols_list in sorted_categories:
    print(f"{category:<40} {len(symbols_list):<15}")

print("\n" + "=" * 60)
print(f"Totalt: {len(sorted_categories)} kategorier")

# Visa exempel fran varje kategori
print("\n\nExempel fran varje kategori:")
print("-" * 60)
for category, symbols_list in sorted_categories[:15]:  # Top 15
    examples = symbols_list[:5]  # 5 exempel per kategori
    print(f"\n{category}:")
    print(f"  {', '.join(examples)}")

mt5.shutdown()
