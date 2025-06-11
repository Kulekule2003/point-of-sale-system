# Create the Flutter project structure and main files
import os
import json

# First, let's create the project structure
project_structure = {
    "lib": {
        "main.dart": "Main application entry point",
        "core": {
            "database": {
                "database_helper.dart": "SQLite database helper",
                "models": {
                    "product.dart": "Product model",
                    "sale.dart": "Sale model", 
                    "sale_item.dart": "Sale item model",
                    "inventory.dart": "Inventory model"
                }
            },
            "constants": {
                "app_constants.dart": "Application constants"
            },
            "theme": {
                "app_theme.dart": "Application theme"
            }
        },
        "features": {
            "sales": {
                "models": {},
                "providers": {
                    "sales_provider.dart": "Sales state management"
                },
                "screens": {
                    "sales_screen.dart": "Main sales/POS screen"
                },
                "widgets": {
                    "product_grid.dart": "Product grid widget",
                    "cart_widget.dart": "Shopping cart widget"
                }
            },
            "inventory": {
                "providers": {
                    "inventory_provider.dart": "Inventory state management"
                },
                "screens": {
                    "inventory_screen.dart": "Inventory management screen"
                },
                "widgets": {
                    "add_item_form.dart": "Add new item form",
                    "update_stock_form.dart": "Update stock form"
                }
            },
            "analytics": {
                "providers": {
                    "analytics_provider.dart": "Analytics state management"
                },
                "screens": {
                    "analytics_screen.dart": "Analytics dashboard screen"
                },
                "widgets": {
                    "sales_chart.dart": "Sales trends chart",
                    "top_selling_table.dart": "Top selling items table",
                    "inventory_status_table.dart": "Inventory status table"
                }
            }
        },
        "shared": {
            "widgets": {
                "custom_app_bar.dart": "Custom application bar",
                "navigation_rail.dart": "Navigation rail for desktop"
            }
        }
    },
    "pubspec.yaml": "Dependencies configuration"
}

print("Flutter POS System Project Structure:")
print("=====================================")

def print_structure(structure, indent=0):
    for key, value in structure.items():
        if isinstance(value, dict):
            print("  " * indent + f"📁 {key}/")
            print_structure(value, indent + 1)
        else:
            print("  " * indent + f"📄 {key} - {value}")

print_structure(project_structure)