# flake8: noqa: E501
import random
from typing import Tuple
from loot_table import LootTable
from loot_table_with_fitness import LootTableWithFitness
from fitness import compute_fitness
from config import Config


class GeneticAlgorithm:
    """Genetic Algorithm implementation for optimizing loot tables."""

    def __init__(
        self,
        config: Config,
    ):
        self.config = config
        self.population = []
        self.generation = 0

    def initialize_population(self):
        """Initialize the population with random loot tables."""
        loot_tables = [
            LootTable.generate_random(self.config)
            for _ in range(self.config.genetic_algorithm.population_size)
        ]
        self.population = [
            LootTableWithFitness(lt, compute_fitness(lt, self.config))
            for lt in loot_tables
        ]

    def select_candidates(self) -> Tuple[LootTableWithFitness, LootTableWithFitness]:
        """
        Select two candidates using fitness-based selection.
        The more fit the candidate, the more likely it is to be selected.
        """
        candidates = random.choices(
            self.population,
            weights=[x.inverse_fitness for x in self.population],
            k=2,
        )
        return candidates[0], candidates[1]

    def crossover(
        self, candidate1: LootTable, candidate2: LootTable
    ) -> Tuple[LootTable, LootTable]:
        """Perform crossover between two candidates to create two children."""
        if random.random() > self.config.genetic_algorithm.crossover_rate:
            return candidate1.copy(), candidate2.copy()

        crossover_point = random.randint(1, 8)
        crossover_probabilities = min(len(candidate1.probabilities), crossover_point)
        crossover_prices = max(crossover_point - len(candidate1.probabilities), 0)

        child1_probabilities = (
            candidate1.probabilities[:crossover_probabilities]
            + candidate2.probabilities[crossover_probabilities:]
        )
        child2_probabilities = (
            candidate2.probabilities[:crossover_probabilities]
            + candidate1.probabilities[crossover_probabilities:]
        )

        child1_prices = (
            candidate1.prices[:crossover_prices] + candidate2.prices[crossover_prices:]
        )
        child2_prices = (
            candidate2.prices[:crossover_prices] + candidate1.prices[crossover_prices:]
        )

        child1_probabilities = LootTable.normalize_probabilities(child1_probabilities)
        child2_probabilities = LootTable.normalize_probabilities(child2_probabilities)

        return LootTable(child1_probabilities, child1_prices), LootTable(
            child2_probabilities, child2_prices
        )

    def mutate(self, lt: LootTable):
        """Mutate a loot table by randomly changing some valus."""
        for i in range(len(lt.probabilities)):
            if random.random() < self.config.genetic_algorithm.mutation_rate:
                # Add random noise to the probability
                lt.probabilities[i] += random.uniform(-0.1, 0.1)
                # make sure the probability is within the allowed range
                lt.probabilities[i] = max(
                    self.config.loot_table.min_prob,
                    min(self.config.loot_table.max_prob, lt.probabilities[i]),
                )
        lt.probabilities = LootTable.normalize_probabilities(lt.probabilities)

        for i in range(1, len(lt.prices) - 1):
            if random.random() < self.config.genetic_algorithm.mutation_rate:
                lt.prices[i] += random.randint(-1, 1)
                # make sure the price is within the allowed range
                lt.prices[i] = max(
                    self.config.loot_table.price_range_min,
                    min(self.config.loot_table.price_range_max, lt.prices[i]),
                )

    def evolve(self):
        """Evolve the population for one generation."""
        sorted_population = sorted(self.population, key=lambda x: x.fitness)

        # Elitism: keep the best genomes
        new_population = [
            genome
            for genome in sorted_population[: self.config.genetic_algorithm.elite_size]
        ]

        # Generate the rest of the population through crossover and mutation
        while len(new_population) < self.config.genetic_algorithm.population_size:
            candidate1, candidate2 = self.select_candidates()
            child1, child2 = self.crossover(
                candidate1.loot_table, candidate2.loot_table
            )

            self.mutate(child1)
            self.mutate(child2)

            new_population.append(LootTableWithFitness(child1, compute_fitness(child1, self.config)))
            if len(new_population) < self.config.genetic_algorithm.population_size:
                new_population.append(LootTableWithFitness(child2, compute_fitness(child2, self.config)))

        self.population = new_population
        self.generation += 1

    def get_best_loot_table(self) -> LootTableWithFitness:
        return min(self.population, key=lambda g: g.fitness)

    def run(self, generations: int):
        """Run the genetic algorithm for a specified number of generations."""
        if not self.population:
            self.initialize_population()

        for gen in range(generations):
            print(f"Generation {gen}")
            self.evolve()
