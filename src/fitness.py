# flake8: noqa: E501
import statistics
from typing import List
from loot_table import LootTable
from simulation import run_simulations
from config import Config


def get_expected_value_absolute_deviation(lt: LootTable, config: Config) -> float:
    """
    Calculate the absolute deviation from the target expected value.
    """
    return config.loot_table.target_expected_value - lt.get_expected_value()


def get_simulation_results_absolute_deviation(
    simulation_results: List[float],
    config: Config,
) -> float:
    """
    Even if the theorical expected value is 8.5, the simulation results might be different.
    Calculate the absolute deviation from the target expected value from the simulation results.
    """
    return config.loot_table.target_expected_value - sum(simulation_results) / len(
        simulation_results
    )


def get_are_prices_sorted(lt: LootTable) -> bool:
    """
    Check if the prices are sorted.
    """
    return sorted(lt.prices) == lt.prices


def get_are_probabilities_within_range(lt: LootTable, config: Config) -> bool:
    """
    Check if the probabilities are within the range.
    """
    return all(
        config.loot_table.min_prob <= probability <= config.loot_table.max_prob
        for probability in lt.probabilities
    )


def get_is_highest_tier_lowest_probability(lt: LootTable) -> bool:
    """
    Check if the highest tier has the lowest probability.
    """
    return lt.probabilities[-1] == min(lt.probabilities)


def get_contains_duplicate_prices(lt: LootTable) -> bool:
    """
    Check if the loot table contains duplicate prices.
    """
    return len(lt.prices) != len(set(lt.prices))


def get_are_ranges_wide_enough(lt: LootTable) -> bool:
    """
    Check if the ranges are wide enough.
    """
    for i in range(1, len(lt.prices) - 1):
        if lt.prices[i] - lt.prices[i - 1] < 2:
            return False
    return True


def debug_fitness(lt: LootTable, config: Config) -> float:

    print(f"FITNESS DEBUG:")

    print(f"- EV deviation: {get_expected_value_absolute_deviation(lt, config)}")
    print(f"- Prices sorted: {get_are_prices_sorted(lt)}")
    print(
        f"- Probabilities within range: {get_are_probabilities_within_range(lt, config)}"
    )
    print(
        f"- Highest tier lowest probability: {get_is_highest_tier_lowest_probability(lt)}"
    )
    print(f"- Contains duplicate prices: {get_contains_duplicate_prices(lt)}")
    print(f"- Ranges wide enough: {get_are_ranges_wide_enough(lt)}")

    print(f"SIMULATIONS:")
    for _ in range(10):
        print(
            f"- Simulation results deviation: {get_simulation_results_absolute_deviation(run_simulations(lt, config.genetic_algorithm.simulation_runs), config)}"
        )


def compute_fitness(lt: LootTable, config: Config) -> float:
    score = 0

    ev = get_expected_value_absolute_deviation(lt, config)

    sim_evs = [
        get_simulation_results_absolute_deviation(
            run_simulations(lt, config.genetic_algorithm.simulation_runs), config
        )
        for _ in range(20)
    ]

    sim_evs_mean = sum(sim_evs) / len(sim_evs)
    sim_dev = abs(abs(ev) - abs(sim_evs_mean))
    score += abs(sim_dev) * 1000

    sim_std = statistics.stdev(sim_evs)
    score += sim_std * 1000

    score += abs(ev) * 1000

    if not get_are_prices_sorted(lt):
        score += 1000
    if not get_are_probabilities_within_range(lt, config):
        score += 1000
    if not get_is_highest_tier_lowest_probability(lt):
        score += 1000
    if not get_are_ranges_wide_enough(lt):
        score += 1000
    if get_contains_duplicate_prices(lt):
        score += 1000

    return score
