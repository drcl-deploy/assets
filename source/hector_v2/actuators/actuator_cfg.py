from dataclasses import MISSING

from isaaclab.utils import configclass
from isaaclab.actuators import ImplicitActuatorCfg, IdealPDActuatorCfg
from . import actuator_pd


@configclass
class HectorV2ImplicitPDActuatorCfg(ImplicitActuatorCfg):
    """Configuration for the implicit PD actuator model in Hector v2.0."""

    class_type: type = actuator_pd.HectorV2ImplicitPDActuator

    knee_gear_ratio: float = 2.0
    """Gear ratio for the knee joints."""
    elbow_gear_ratio: float = 1.417
    """Gear ratio for the elbow joints."""
    knee_indices: list[int] = MISSING
    """Indices of the knee joints in the articulation."""
    ankle_indices: list[int] = MISSING
    """Indices of the ankle joints in the articulation."""
    elbow_indices: list[int] = MISSING
    """Indices of the elbow joints in the articulation."""


@configclass
class HectorV2IdealPDActuatorCfg(IdealPDActuatorCfg):
    """Configuration for the ideal PD actuator model in Hector v2.0."""

    class_type: type = actuator_pd.HectorV2IdealPDActuator

    knee_gear_ratio: float = 2.0
    """Gear ratio for the knee joints."""
    elbow_gear_ratio: float = 1.417
    """Gear ratio for the elbow joints."""
    knee_indices: list[int] = MISSING
    """Indices of the knee joints in the articulation."""
    ankle_indices: list[int] = MISSING
    """Indices of the ankle joints in the articulation."""
    elbow_indices: list[int] = MISSING
    """Indices of the elbow joints in the articulation."""
