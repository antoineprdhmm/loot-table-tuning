# flake8: noqa: E501
import math
import random
from typing import List
from config import Config


class LootTable:
    def __init__(self, probabilities: List[float], prices: List[float]):
        self.probabilities = probabilities
        self.prices = prices

    def __str__(self):
        return f"LootTable(probabilities={self.probabilities}, prices={self.prices})"

    @staticmethod
    def normalize_probabilities(probabilities: List[float]) -> List[float]:
        total = sum(probabilities)
        return [p / total for p in probabilities]

    @staticmethod
    def generate_random(config: Config) -> "LootTable":
        probabilities = [
            random.uniform(config.loot_table.min_prob, config.loot_table.max_prob)
            for _ in range(config.loot_table.nb_tiers)
        ]
        probabilities = LootTable.normalize_probabilities(probabilities)

        prices = [config.loot_table.price_range_min]
        prices.extend(
            random.uniform(
                config.loot_table.price_range_min, config.loot_table.price_range_max
            )
            for _ in range(config.loot_table.nb_tiers - 1)
        )
        prices.append(config.loot_table.price_range_max)
        prices = [math.floor(price) for price in prices]
        prices = sorted(prices)

        return LootTable(probabilities, prices)

    def get_expected_value(self) -> float:
        return sum(
            [
                (self.prices[i + 1] - self.prices[i]) * self.probabilities[i]
                for i in range(len(self.prices) - 1)
            ]
        )

    def copy(self) -> "LootTable":
        return LootTable(self.probabilities.copy(), self.prices.copy())
