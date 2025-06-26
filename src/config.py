# flake8: noqa: E501
import yaml
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GeneticAlgorithmConfig:
    population_size: int = 0
    mutation_rate: float = 0.0
    crossover_rate: float = 0.0
    elite_size: int = 0
    generations: int = 0
    simulation_runs: int = 0


@dataclass
class LootTableConfig:
    nb_tiers: int = 0
    price_range_min: int = 0
    price_range_max: int = 0
    max_prob: float = 0.0
    min_prob: float = 0.0
    target_expected_value: float = 0.0


@dataclass
class Config:
    genetic_algorithm: GeneticAlgorithmConfig
    loot_table: LootTableConfig

    @classmethod
    def from_file(cls, config_path: str) -> "Config":
        """Load configuration from YAML file."""
        config_file = Path(config_path)

        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_file, "r") as f:
            data = yaml.safe_load(f)

        return cls(
            genetic_algorithm=GeneticAlgorithmConfig(
                **data.get("genetic_algorithm", {})
            ),
            loot_table=LootTableConfig(**data.get("loot_table", {})),
        )
