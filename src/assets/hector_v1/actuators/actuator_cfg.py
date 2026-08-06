from dataclasses import MISSING

from isaaclab.actuators import IdealPDActuatorCfg, ImplicitActuatorCfg
from isaaclab.utils import configclass

from . import actuator_pd


@configclass
class HectorV1ImplicitPDActuatorCfg(ImplicitActuatorCfg):
    """Configuration for the implicit PD actuator model in Hector v1."""

    class_type: type = actuator_pd.HectorV1ImplicitPDActuator

    knee_gear_ratio: float = 2.0
    """Gear ratio for the knee joints."""
    knee_indices: list[int] = MISSING
    """Indices of the knee joints in the articulation."""
    ankle_indices: list[int] = MISSING
    """Indices of the ankle joints in the articulation."""


@configclass
class HectorV1IdealPDActuatorCfg(IdealPDActuatorCfg):
    """Configuration for the ideal PD actuator model in Hector v1."""

    class_type: type = actuator_pd.HectorV1IdealPDActuator

    knee_gear_ratio: float = 2.0
    """Gear ratio for the knee joints."""
    knee_indices: list[int] = MISSING
    """Indices of the knee joints in the articulation."""
    ankle_indices: list[int] = MISSING
    """Indices of the ankle joints in the articulation."""
