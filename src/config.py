from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
RESULTS_DIR = OUTPUT_DIR / "results"

CSV_PATH = DATA_DIR / "electricity_market_data.csv"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

BATTERY_CAPACITY = 35
MAX_POWER = 11
INTERVAL_MINS = 15

POWER_STRATEGIES = [
    "Ramp Up",
    "Ramp Down",
    "Max Power",
    "Delayed Max",
    "Uniform"
]