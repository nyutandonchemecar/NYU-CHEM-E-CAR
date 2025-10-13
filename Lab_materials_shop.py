# lab_materials_shop.py
# Simple supermarket cashier register using JSON for storage.
# Features:
# - Add, remove, and update item prices
# - List items
# - Query an item's price
# - Persistent storage in catalog.json (JSON file)

import json
import os
from typing import Dict, Any

CATALOG_FILE = "catalog.json"


def _normalize_key(name: str) -> str:
    """Normalize item name for case-insensitive keys."""
    return name.strip().casefold()


def load_catalog(filename: str = CATALOG_FILE) -> Dict[str, Dict[str, Any]]:
    """Load the catalog JSON; return empty dict if missing or invalid."""
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Ensure expected shape
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


def save_catalog(catalog: Dict[str, Dict[str, Any]], filename: str = CATALOG_FILE) -> None:
    """Save the catalog JSON with pretty formatting."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)


def add_item(catalog: Dict[str, Dict[str, Any]], name: str, price: float) -> None:
    """Add a new item or overwrite if it exists."""
    key = _normalize_key(name)
    catalog[key] = {"name": name.strip(), "price": float(price)}


def remove_item(catalog: Dict[str, Dict[str, Any]], name: str) -> bool:
    """Remove an item by name (case-insensitive). Returns True if removed."""
    key = _normalize_key(name)
    return catalog.pop(key, None) is not None


def update_price(catalog: Dict[str, Dict[str, Any]], name: str, price: float) -> bool:
    """Update price of an existing item. Returns True if updated."""
    key = _normalize_key(name)
    if key in catalog:
        catalog[key]["price"] = float(price)
        return True
    return False


def get_price(catalog: Dict[str, Dict[str, Any]], name: str):
    """Return price if found, else None."""
    key = _normalize_key(name)
    item = catalog.get(key)
    return item["price"] if item else None


def list_items(catalog: Dict[str, Dict[str, Any]]) -> None:
    """Pretty-print catalog items sorted by display name."""
    if not catalog:
        print("Catalog is empty.")
        return
    items = sorted(catalog.values(), key=lambda x: x["name"].casefold())
    print("\nCurrent Catalog")
    print("-" * 40)
    for it in items:
        print(f"{it['name']:<20} ${it['price']:.2f}")
    print("-" * 40)


def menu() -> None:
    catalog = load_catalog()
    while True:
        print(
            "\n=== Supermarket Cashier Register ===\n"
            "1) List items\n"
            "2) Add item\n"
            "3) Remove item\n"
            "4) Update price\n"
            "5) Get price\n"
            "6) Save & Exit\n"
        )
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            list_items(catalog)

        elif choice == "2":
            name = input("Enter item name to add: ").strip()
            try:
                price = float(input("Enter price: ").strip())
            except ValueError:
                print("Invalid price. Please enter a number.")
                continue
            add_item(catalog, name, price)
            print(f"Added/updated '{name}' at ${price:.2f}.")

        elif choice == "3":
            name = input("Enter item name to remove: ").strip()
            if remove_item(catalog, name):
                print(f"Removed '{name}'.")
            else:
                print(f"'{name}' not found.")

        elif choice == "4":
            name = input("Enter item name to update: ").strip()
            try:
                price = float(input("Enter new price: ").strip())
            except ValueError:
                print("Invalid price. Please enter a number.")
                continue
            if update_price(catalog, name, price):
                print(f"Updated '{name}' to ${price:.2f}.")
            else:
                print(f"'{name}' not found. Use 'Add item' instead.")

        elif choice == "5":
            name = input("Enter item name to look up: ").strip()
            price = get_price(catalog, name)
            if price is None:
                print(f"'{name}' not found.")
            else:
                print(f"The price of {name} is ${price:.2f}.")

        elif choice == "6":
            save_catalog(catalog)
            print(f"Saved to {CATALOG_FILE}. Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    menu()
