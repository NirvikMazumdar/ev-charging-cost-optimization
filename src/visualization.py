import pandas as pd
import matplotlib.pyplot as plt

from src.config import FIGURES_DIR, RESULTS_DIR


def plot_simulation_results(results, success_rate, valid_events):
    strategies = list(results.keys())

    avg_costs = [
        sum(results[strategy]) / len(results[strategy])
        if len(results[strategy]) > 0 else 0
        for strategy in strategies
    ]

    success_percentages = [
        (success_rate[strategy] / valid_events) * 100
        if valid_events > 0 else 0
        for strategy in strategies
    ]

    summary_df = pd.DataFrame({
        "strategy": strategies,
        "average_cost_eur": avg_costs,
        "success_rate_percent": success_percentages
    })

    summary_path = RESULTS_DIR / "strategy_summary.csv"
    summary_df.to_csv(summary_path, index=False)

    plt.figure(figsize=(11, 6))
    plt.bar(strategies, avg_costs)
    plt.ylabel("Average Cost (€)")
    plt.title("Average Charging Cost per Strategy")
    plt.xticks(rotation=20)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "average_cost_per_strategy.png", dpi=300)
    plt.close()

    plt.figure(figsize=(11, 6))
    plt.boxplot([results[strategy] for strategy in strategies], labels=strategies)
    plt.ylabel("Cost (€)")
    plt.title("Cost Distribution per Strategy")
    plt.xticks(rotation=20)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "cost_distribution_per_strategy.png", dpi=300)
    plt.close()

    plt.figure(figsize=(11, 6))
    plt.bar(strategies, success_percentages)
    plt.ylabel("Success Rate (%)")
    plt.title("SOC Target Achievement per Strategy")
    plt.xticks(rotation=20)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "success_rate_per_strategy.png", dpi=300)
    plt.close()

    return summary_df