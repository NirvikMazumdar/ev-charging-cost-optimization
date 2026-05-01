import numpy as np

from src.config import (
    BATTERY_CAPACITY,
    MAX_POWER,
    INTERVAL_MINS,
    POWER_STRATEGIES
)


def calculate_required_energy(start_soc, end_soc):
    return (end_soc - start_soc) * BATTERY_CAPACITY


def generate_strategy_power(strategy, n_slots, required_energy):
    power = np.zeros(n_slots)

    if strategy == "Max Power":
        power[:] = MAX_POWER

    elif strategy == "Ramp Up":
        power = np.linspace(MAX_POWER * 0.2, MAX_POWER, n_slots)

    elif strategy == "Ramp Down":
        power = np.linspace(MAX_POWER, MAX_POWER * 0.2, n_slots)

    elif strategy == "Delayed Max":
        delay_slots = n_slots // 3
        power[:delay_slots] = 0
        power[delay_slots:] = MAX_POWER

    elif strategy == "Uniform":
        power[:] = required_energy / (n_slots * (INTERVAL_MINS / 60))

    return np.clip(power, 0, MAX_POWER)


def optimized_mixed_strategy(time_stamps, prices, required_energy):
    n_slots = len(time_stamps)
    dt_hours = INTERVAL_MINS / 60

    energy_needed = required_energy
    power_opt = np.zeros(n_slots)

    strategies_power = {
        strategy: generate_strategy_power(strategy, n_slots, required_energy)
        for strategy in POWER_STRATEGIES
    }

    for i in range(n_slots):
        if energy_needed <= 0:
            break

        remaining_slots = n_slots - i
        max_possible_energy = remaining_slots * MAX_POWER * dt_hours

        if energy_needed > max_possible_energy:
            deliverable_energy = min(MAX_POWER * dt_hours, energy_needed)
            power_opt[i] = deliverable_energy / dt_hours
            energy_needed -= deliverable_energy
            continue

        slot_costs = []

        for strategy in POWER_STRATEGIES:
            candidate_power = strategies_power[strategy][i]
            candidate_energy = min(candidate_power * dt_hours, energy_needed)
            slot_costs.append(candidate_energy * prices[i])

        best_strategy_idx = np.argmin(slot_costs)
        best_strategy = POWER_STRATEGIES[best_strategy_idx]

        chosen_power = strategies_power[best_strategy][i]
        deliverable_energy = min(chosen_power * dt_hours, energy_needed)

        power_opt[i] = deliverable_energy / dt_hours
        energy_needed -= deliverable_energy

    return power_opt


def fourier_optimize_profile(optimized_power, prices, required_energy, n_components=5):
    n = len(optimized_power)
    dt_hours = INTERVAL_MINS / 60

    fft_result = np.fft.rfft(optimized_power)
    magnitude = np.abs(fft_result)

    top_indices = magnitude.argsort()[-n_components:]

    mask = np.zeros_like(fft_result, dtype=bool)
    mask[top_indices] = True

    filtered_fft = np.where(mask, fft_result, 0)
    reconstructed = np.fft.irfft(filtered_fft, n=n)
    reconstructed = np.clip(reconstructed, 0, MAX_POWER)

    fourier_power = reconstructed.copy()

    cheap_threshold = np.percentile(prices, 30)
    cheap_indices = np.where(prices <= cheap_threshold)[0]
    fourier_power[cheap_indices] = np.maximum(
        fourier_power[cheap_indices],
        MAX_POWER * 0.9
    )

    expensive_threshold = np.percentile(prices, 90)
    expensive_indices = np.where(prices >= expensive_threshold)[0]
    fourier_power[expensive_indices] = np.minimum(
        fourier_power[expensive_indices],
        MAX_POWER * 0.2
    )

    current_energy = np.sum(fourier_power) * dt_hours

    if current_energy > 0:
        fourier_power *= required_energy / current_energy

    fourier_power = np.clip(fourier_power, 0, MAX_POWER)

    return fourier_power


def compute_cost(power, prices):
    dt_hours = INTERVAL_MINS / 60
    return np.sum(power * dt_hours * prices)


def compute_energy(power):
    dt_hours = INTERVAL_MINS / 60
    return np.sum(power) * dt_hours