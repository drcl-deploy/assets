from __future__ import annotations

import torch
from collections.abc import Sequence
from typing import TYPE_CHECKING

from isaacsim.core.utils.types import ArticulationActions

from isaaclab.actuators import ImplicitActuator, IdealPDActuator

if TYPE_CHECKING:
    from .actuator_cfg import (
        HectorV2ImplicitPDActuatorCfg,
        HectorV2IdealPDActuatorCfg,
    )


def update_coupling_gear_ratios(
    control_action: ArticulationActions,
    joint_pos: torch.Tensor,
    joint_vel: torch.Tensor,
    knee_gear_ratio: float,
    elbow_gear_ratio: float,
    knee_indices: list[int],  # left and right knee indices
    ankle_indices: list[int],  # left and right ankle indices
    elbow_indices: list[int],  # left and right elbow indices
):

    # assume the command is in motor space (policy pov) , now transform it to joint space (sim pov)
    for knee_idx, ankle_idx in zip(knee_indices, ankle_indices):
        # scale knee
        control_action.joint_positions[:, knee_idx] = (
            control_action.joint_positions[:, knee_idx] / knee_gear_ratio
        )
        control_action.joint_velocities[:, knee_idx] = (
            control_action.joint_velocities[:, knee_idx] / knee_gear_ratio
        )
        # read current knee joint state
        knee_joint_pos = joint_pos[:, knee_idx]
        knee_joint_vel = joint_vel[:, knee_idx]
        # clip ankle commands
        control_action.joint_positions[:, ankle_idx] = torch.clip(
            control_action.joint_positions[:, ankle_idx], min=-0.5846853, max=0.977384
        )
        # coupled ankle commands with knee state
        control_action.joint_positions[:, ankle_idx] -= (knee_joint_pos + 1.5708)
        control_action.joint_velocities[:, ankle_idx] -= knee_joint_vel

    for elbow_idx in elbow_indices:
        # scale elbow
        control_action.joint_positions[:, elbow_idx] = (
            control_action.joint_positions[:, elbow_idx] / elbow_gear_ratio
        )
        control_action.joint_velocities[:, elbow_idx] = (
            control_action.joint_velocities[:, elbow_idx] / elbow_gear_ratio
        )

    return control_action


class HectorV2ImplicitPDActuator(ImplicitActuator):
    """Implicit actuator model for Hector V2 robot.

    This class implements an implicit actuator model for the Hector V2 robot. The model is based on the
    joint stiffness and damping parameters provided in the configuration instance passed to the class.

    """

    cfg: HectorV2ImplicitPDActuatorCfg
    """The configuration for the actuator model."""

    def reset(self, env_ids: Sequence[int]):
        pass

    def compute(
        self,
        control_action: ArticulationActions,
        joint_pos: torch.Tensor,
        joint_vel: torch.Tensor,
    ) -> ArticulationActions:

        control_action = update_coupling_gear_ratios(
            control_action,
            joint_pos,
            joint_vel,
            self.cfg.knee_gear_ratio,
            self.cfg.elbow_gear_ratio,
            knee_indices=self.cfg.knee_indices,
            ankle_indices=self.cfg.ankle_indices,
            elbow_indices=self.cfg.elbow_indices,
        )
        # approximate torques for reward computation
        error_pos = control_action.joint_positions - joint_pos
        error_vel = control_action.joint_velocities - joint_vel

        self.computed_effort = (
            self.stiffness * error_pos
            + self.damping * error_vel
            + control_action.joint_efforts
        )

        # clip the torques based on the motor limits
        self.applied_effort = self._clip_effort(self.computed_effort)

        return control_action


class HectorV2IdealPDActuator(IdealPDActuator):

    cfg: HectorV2IdealPDActuatorCfg
    """The configuration for the actuator model."""

    def reset(self, env_ids: Sequence[int]):
        pass

    def compute(
        self,
        control_action: ArticulationActions,
        joint_pos: torch.Tensor,
        joint_vel: torch.Tensor,
    ) -> ArticulationActions:

        control_action = update_coupling_gear_ratios(
            control_action,
            joint_pos,
            joint_vel,
            self.cfg.knee_gear_ratio,
            elbow_gear_ratio=self.cfg.elbow_gear_ratio,
            knee_indices=self.cfg.knee_indices,
            ankle_indices=self.cfg.ankle_indices,
            elbow_indices=self.cfg.elbow_indices,
        )
        # store approximate torques for reward computation
        error_pos = control_action.joint_positions - joint_pos
        error_vel = control_action.joint_velocities - joint_vel

        self.computed_effort = (
            self.stiffness * error_pos
            + self.damping * error_vel
            + control_action.joint_efforts
        )

        # clip the torques based on the motor limits
        self.applied_effort = self._clip_effort(self.computed_effort)

        control_action.joint_efforts = self.applied_effort
        control_action.joint_positions = None
        control_action.joint_velocities = None

        return control_action
