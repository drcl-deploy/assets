from dataclasses import MISSING

from isaaclab.utils import configclass
from isaaclab.actuators import ImplicitActuatorCfg, IdealPDActuatorCfg
from . import actuator_pd


@configclass
class Go1SEAImplicitPDActuatorCfg(ImplicitActuatorCfg):
    """Configuration for the implicit PD actuator model in Go1SEA"""

    class_type: type = actuator_pd.Go1SEAImplicitPDActuator

