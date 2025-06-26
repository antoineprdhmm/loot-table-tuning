# flake8: noqa: E501
from loot_table import LootTable


class LootTableWithFitness:
    def __init__(self, loot_table: LootTable, fitness: float):
        self.loot_table = loot_table
        self.fitness = fitness
        # if perfect score, avoid div by 0 and set +inf
        self.inverse_fitness = 1 / fitness if fitness > 0 else float('inf')
