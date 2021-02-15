# Copyright 2021 Drivetrain Hub LLC
# For non-commercial use only.  For commercial products and services, visit https://drivetrainhub.com.

"""Notebook module for planetary gear geometry."""

import numpy as np
from math import pi


PHI_CIRCLE = np.linspace(0, 2*pi)


def circle_curve(radius, phi=PHI_CIRCLE, x_center=0, y_center=0):
    x = radius * np.cos(phi) + x_center
    y = radius * np.sin(phi) + y_center

    return x, y
