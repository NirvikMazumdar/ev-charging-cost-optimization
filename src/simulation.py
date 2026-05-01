import random
from datetime import timedelta

import numpy as np
import pandas as pd

from src.config import (
    BATTERY_CAPACITY,
    INTERVAL_MINS,
    POWER_STRATEGIES
)

from src.optimizer import (
    generate_strategy_power,
    optimized_mixed_strategy,
    fourier_optimize_profile,
    compute_cost,
    compute_energy
)


def simulate_charging_events(
    num_events,
    df_prices,
    start_date="2024-01-13 08:00",
    end_date="2024-10-15 12:00"
):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    strategies = POWER_STRATEGIES + [
        "Optimized Mixed",
        "Fourier Optimized"
    ]

    results = {strategy: [] for strategy in strategies}
    success_rate = {strategy: 0 for strategy in strategies}

    valid_events = 0

    total_minutes = int((end_date - start_date).total_seconds() / 60)

    for _ in range(num_events):
        session_start = start_date + timedelta(
            minutes=random.randint(0, total_minutes)
        )

        session_duration_slots = random.randint(4, 20)
        session_end = session_start + timedelta(
            minutes=session_duration_slots * INTERVAL_MINS
        )

        start_soc = random.uniform(0.1, 0.5)
        end_soc = random.uniform(0.7, 0.95)

        required_energy = (end_soc - start_soc) * BATTERY_CAPACITY

        df_event = df_prices[
            (df_prices["timestamp"] >= session_start)
            & (df_prices["timestamp"] <= session_end)
        ]

        if df_event.empty:
            continue

        valid_events += 1

        time_stamps = pd.date_range(
            session_start,
            session_end,
            freq=f"{INTERVAL_MINS}min"
        )

        prices = np.interp(
            pd.to_numeric(time_stamps),
            pd.to_numeric(df_event["timestamp"]),
            df_event["price"]
        )

        for strategy in POWER_STRATEGIES:
            power = generate_strategy_power(
                strategy,
                len(time_stamps),
                required_energy
            )

            cost = compute_cost(power, prices)
            energy_delivered = compute_energy(power)

            results[strategy].append(cost)

            if energy_delivered >= required_energy:
                success_rate[strategy] += 1

        opt_power = optimized_mixed_strategy(
            time_stamps,
            prices,
            required_energy
        )

        opt_cost = compute_cost(opt_power, prices)
        opt_energy = compute_energy(opt_power)

        results["Optimized Mixed"].append(opt_cost)

        if opt_energy >= required_energy:
            success_rate["Optimized Mixed"] += 1

        fourier_power = fourier_optimize_profile(
            opt_power,
            prices,
            required_energy
        )

        fourier_cost = compute_cost(fourier_power, prices)
        fourier_energy = compute_energy(fourier_power)

        results["Fourier Optimized"].append(fourier_cost)

        if fourier_energy >= required_energy:
            success_rate["Fourier Optimized"] += 1

    return results, success_rate, valid_events