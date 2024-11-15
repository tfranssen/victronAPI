import requests
import json

def fetch_data(api_url, token):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'X-Authorization': f'Token {token}'
    }
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()

def calculate_metrics(data):
    totals = data["totals"]

    # Extract values
    Gc = totals["Gc"]
    Bc = totals["Bc"]
    Gb = totals["Gb"]
    Bg = totals["Bg"]
    Pc = totals["Pc"]
    Pb = totals["Pb"]
    Pg = totals["Pg"]

    # Power production
    total_yield = Gc + Gb + Pc + Pb + Pg
    total_solar_production = Pc + Pb + Pg
    total_grid_production = Gb + Gc
    percentage_production_solar = (total_solar_production / total_yield) * 100
    percentage_production_grid = (total_grid_production / total_yield) * 100

    # Power consumption
    total_consumption = Gc + Bc + Pc
    total_solar_consumption = Pc
    total_grid_consumption = Gc
    total_battery_consumption = Bc
    percentage_solar_consumption = (total_solar_consumption / total_consumption) * 100
    percentage_grid_consumption = (total_grid_consumption / total_consumption) * 100
    percentage_battery_consumption = (total_battery_consumption / total_consumption) * 100

    # Battery
    battery_charge = Gb + Pb
    battery_discharge = Bc + Bg

    # Create JSON object with rounded values
    result = {
        "Power Production": {
            "total_yield": round(total_yield, 1),
            "total_solar_production": round(total_solar_production, 1),
            "total_grid_production": round(total_grid_production, 1),
            "percentage_production_solar": round(percentage_production_solar, 1),
            "percentage_production_grid": round(percentage_production_grid, 1)
        },
        "Power Consumption": {
            "total_consumption": round(total_consumption, 1),
            "total_solar_consumption": round(total_solar_consumption, 1),
            "total_grid_consumption": round(total_grid_consumption, 1),
            "total_battery_consumption": round(total_battery_consumption, 1),
            "percentage_solar_consumption": round(percentage_solar_consumption, 1),
            "percentage_grid_consumption": round(percentage_grid_consumption, 1),
            "percentage_battery_consumption": round(percentage_battery_consumption, 1)
        },
        "Battery": {
            "battery_charge": round(battery_charge, 1),
            "battery_discharge": round(battery_discharge, 1)
        }
    }

    return result

# API call parameters
api_url = "https://vrmapi.victronenergy.com/v2/installations/116491/stats?end=1730323200&interval=days&start=1727731200&type=kwh"
token = "b1f7d2763ac033a64e4875721b2bcfb77a99cbeb18387c2a48b3bb3ad0b1157e"

try:
    # Fetch data
    data = fetch_data(api_url, token)

    # Calculate metrics
    metrics = calculate_metrics(data)

    # Print results as JSON
    print(json.dumps(metrics, indent=4))

except requests.exceptions.RequestException as e:
    print(f"Error during API call: {e}")
except KeyError as e:
    print(f"Missing expected data in response: {e}")
