# flake8: noqa: E501
import os
from genetic_algorithm import GeneticAlgorithm
from fitness import debug_fitness
from config import Config


def main():
    config = Config.from_file("config/dev.yaml")

    ga = GeneticAlgorithm(
        config=config,
    )

    ga.run(
        generations=config.genetic_algorithm.generations,
    )

    best_loot_table = ga.get_best_loot_table()

    debug_fitness(best_loot_table.loot_table, config)

    print(f"Best Fitness: {best_loot_table.fitness}")
    print(f"Probabilities: {best_loot_table.loot_table.probabilities}")
    print(f"Prices: {best_loot_table.loot_table.prices}")


if __name__ == "__main__":
    main()
