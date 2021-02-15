# Copyright 2021 Drivetrain Hub LLC
# For non-commercial use only.  For commercial products and services, visit https://drivetrainhub.com.

"""Notebook module for planetary gear geometry."""

import numpy as np
from math import pi, cos, sin
from typing import Tuple


Point = Tuple[float, float]
Coord = Tuple[np.ndarray, np.ndarray]
PHI_CIRCLE = np.linspace(0, 2*pi)


def circle_curve(radius: float, phi:np.ndarray = PHI_CIRCLE, x_center: float = 0, y_center: float = 0) -> Coord:
    x = radius * np.cos(phi) + x_center
    y = radius * np.sin(phi) + y_center

    return x, y


def polar_to_cartesian(radius: float, phi: float) -> Point:
    x = radius * cos(phi)
    y = radius * sin(phi)

    return x, y
