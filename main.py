from src.config import CSV_PATH
from src.data_loader import load_price_data
from src.simulation import simulate_charging_events
from src.visualization import plot_simulation_results


def main():
    print("EV Charging Cost Optimization")
    print("=" * 40)

    print(f"Loading electricity price data from: {CSV_PATH}")
    df_prices = load_price_data(CSV_PATH)

    print(f"Loaded {len(df_prices)} price records.")

    num_events = 30000
    print(f"Running simulation for {num_events} charging events...")

    results, success_rate, valid_events = simulate_charging_events(
        num_events=num_events,
        df_prices=df_prices
    )

    print(f"Valid simulated events: {valid_events}")

    print("Generating figures and result summary...")
    summary_df = plot_simulation_results(
        results,
        success_rate,
        valid_events
    )

    print("\nStrategy Summary:")
    print(summary_df)

    print("\nDone.")
    print("Figures saved in: outputs/figures")
    print("Results saved in: outputs/results")


if __name__ == "__main__":
    main()