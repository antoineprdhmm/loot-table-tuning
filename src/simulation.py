# flake8: noqa: E501
import random
from typing import List
from loot_table import LootTable


def get_tier_index(lt: LootTable, value: float) -> int:
    for i in range(len(lt.probabilities)):
        if sum(lt.probabilities[: i + 1]) > value:
            return i
    return len(lt.probabilities) - 1


def run_simulation(lt: LootTable) -> float:
    """
    Pick a random number between 0 and 1 to find which tier the price will be in.
    Then pick a random number between the min and max of that tier.
    """
    tier_value = random.uniform(0, 1)
    tier_index = get_tier_index(lt, tier_value)
    return random.uniform(lt.prices[tier_index], lt.prices[tier_index + 1])


def run_simulations(lt: LootTable, nb_simulations: int) -> List[float]:
    return [run_simulation(lt) for _ in range(nb_simulations)]
