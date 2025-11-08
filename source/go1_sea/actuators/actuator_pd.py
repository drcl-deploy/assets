from __future__ import annotations

import torch
from collections.abc import Sequence
from typing import TYPE_CHECKING

from isaacsim.core.utils.types import ArticulationActions

from isaaclab.actuators import ImplicitActuator, IdealPDActuator

if TYPE_CHECKING:
    from .actuator_cfg import (
        Go1SEAImplicitPDActuatorCfg,
    )

class Go1SEAImplicitPDActuator(ImplicitActuator):
    """Implicit actuator model for Hector V2 robot.

    This class implements an implicit actuator model for the Hector V2 robot. The model is based on the
    joint stiffness and damping parameters provided in the configuration instance passed to the class.

    """

    cfg: Go1SEAImplicitPDActuatorCfg
    """The configuration for the actuator model."""

    def reset(self, env_ids: Sequence[int]):
        pass

    def compute(
        self, control_action: ArticulationActions, joint_pos: torch.Tensor, joint_vel: torch.Tensor
    ) -> ArticulationActions:
        """Process the actuator group actions and compute the articulation actions.

        In case of implicit actuator, the control action is directly returned as the computed action.
        This function is a no-op and does not perform any computation on the input control action.
        However, it computes the approximate torques for the actuated joint since PhysX does not compute
        this quantity explicitly.

        Args:
            control_action: The joint action instance comprising of the desired joint positions, joint velocities
                and (feed-forward) joint efforts.
            joint_pos: The current joint positions of the joints in the group. Shape is (num_envs, num_joints).
            joint_vel: The current joint velocities of the joints in the group. Shape is (num_envs, num_joints).

        Returns:
            The computed desired joint positions, joint velocities and joint efforts.
        """
        # store approximate torques for reward computation
        # I want to replace the 12, 13, 14, 15 control_action.joint_positions to 0

        # zero out joint positions for indices 12-15
        # print("Joint pos is:", joint_pos)
        pos = control_action.joint_positions.clone()
        # pos[:, 12:16] = 0.0
        try:
            control_action.joint_positions = pos
        except Exception:
            # if attribute assignment is not supported, use pos for computations below
            pass
            
        error_pos = pos - joint_pos
        error_vel = control_action.joint_velocities - joint_vel
        self.computed_effort = self.stiffness * error_pos + self.damping * error_vel + control_action.joint_efforts
        # clip the torques based on the motor limits
        self.applied_effort = self._clip_effort(self.computed_effort)
        return control_action