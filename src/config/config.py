from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class DataConfig:
    """数据配置"""
    window_size: int = 30
    update_frequency: int = 7
    min_data_points: int = 10
    validation_ratio: float = 0.2


@dataclass
class ModelConfig:
    """模型配置"""
    # VBGF参数
    vbgf_initial_guess: Tuple[float, float, float] = (40.0, 0.015, 0.0)
    vbgf_bounds: Tuple[Tuple, Tuple] = ((20, 0.001, -15), (100, 0.1, 10))

    # 体重公式参数
    weight_initial_guess: Tuple[float, float] = (0.01, 3.0)
    weight_bounds: Tuple[Tuple, Tuple] = ((0.001, 2.5), (0.1, 3.5))


@dataclass
class ExperimentConfig:
    """实验配置"""
    random_seed: int = 42
    n_trials: int = 10
    confidence_level: float = 0.95