# Copyright 2019 Drivetrain Hub LLC
# For non-commercial use only.  For commercial products and services, visit https://drivetrainhub.com.

"""Notebook module for involute geometry."""

import numpy as np
from math import pi


# region CURVES

def involute_curve(radius_base, roll_angle):
    x = radius_base * (np.cos(roll_angle) + roll_angle * np.sin(roll_angle))
    y = radius_base * (np.sin(roll_angle) - roll_angle * np.cos(roll_angle))

    return x, y


def circle_curve(radius, phi, x_center=0, y_center=0):
    x = radius * np.cos(phi) + x_center
    y = radius * np.sin(phi) + y_center

    return x, y

# endregion


def involute_curvature(radius_base, roll_angle):
    # radius of curvature
    radius_curvature = radius_base * roll_angle
    phi_curvature = roll_angle - pi / 2

    # polar to cartesian
    x_curvature = radius_curvature * np.cos(phi_curvature)
    y_curvature = radius_curvature * np.sin(phi_curvature)

    # involute curve
    x, y = involute_curve(radius_base, roll_angle)

    # center of curvature
    x_center_curvature = x - x_curvature
    y_center_curvature = y - y_curvature

    return radius_curvature, phi_curvature, x_center_curvature, y_center_curvature


def involute_pressure_angle(radius_base, roll_angle):
    x, y = involute_curve(radius_base, roll_angle)
    r = np.hypot(x, y)

    return np.arccos(radius_base / r)


def involute_function(pressure_angle):
    return np.tan(pressure_angle) - pressure_angle

