# Copyright 2019 Drivetrain Hub LLC
# For non-commercial use only.  For commercial products and services, visit https://www.drivetrainhub.com.

"""Notebook module for basic rack."""

from math import pi, sin, cos, tan, radians
import numpy as np


def pitch_fcn(module):
    return pi * module


def base_pitch_fcn(module, pressure_angle):
    return pi * module * cos(pressure_angle)


def bottom_clearance_fcn(addendum, dedendum):
    """Calculate the basic rack bottom clearance."""

    return dedendum - addendum


def bottom_clearance_root_radius(addendum, dedendum, pressure_angle):
    """Calculate the basic rack root radius limited by bottom clearance."""

    bottom_clearance = bottom_clearance_fcn(addendum, dedendum)

    return bottom_clearance / (1 - sin(pressure_angle))


def max_root_radius(module, pressure_angle, addendum, dedendum):
    """Calculate the basic rack maximum allowable root radius.  Only valid without undercut."""

    bottom_clearance_root_radius_limit = bottom_clearance_root_radius(addendum, dedendum, pressure_angle)

    # calculate full root radius
    e_p = pi * module / 2
    tan_a = tan(pressure_angle)
    sec_a = 1 / cos(pressure_angle)
    y_fillet = (e_p * tan_a - e_p * sec_a + 2 * dedendum) / (2 * (tan_a * sec_a - tan_a ** 2 - 1))
    full_root_radius = (dedendum + y_fillet) / (1 - sin(pressure_angle))

    # conditional check against the root radius limited by bottom clearance
    if bottom_clearance_root_radius_limit < full_root_radius:
        maximum_root_radius = bottom_clearance_root_radius_limit
    else:
        maximum_root_radius = full_root_radius

    return maximum_root_radius


# region CURVES

def circle_curve(radius, phi_i, phi_f, x_center, y_center):
    """Cartesian coordinates for a circular arc.

    :param radius: Radius of circle.
    :param phi_i: Starting polar angle.
    :param phi_f: Ending polar angle.
    :param x_center: x-coordinate center of circle.
    :param y_center: y-coordinate center of circle.
    :return: xy coordinate data of circular arc.
    """

    phi = np.linspace(phi_i, phi_f)

    x = list(radius * np.cos(phi) + x_center)
    y = list(radius * np.sin(phi) + y_center)

    return x, y


def basic_rack_coordinates(module, pressure_angle_deg, addendum_coefficient, dedendum_coefficient,
                           root_radius_coefficient):
    """Cartesian coordinates for a basic rack without undercut.

    Coordinates are computed from left to right, with the origin on the datum line at mid-spacewidth.
    """

    pitch = pitch_fcn(module)
    addendum = addendum_coefficient * module
    dedendum = dedendum_coefficient * module
    root_radius = root_radius_coefficient * module
    pressure_angle = radians(pressure_angle_deg)

    root_radius_height = root_radius - root_radius * sin(pressure_angle)
    dedendum_profile_height = dedendum - root_radius_height

    yc_rho = - dedendum + root_radius
    xc_rho_rl = pitch / 4 - dedendum_profile_height * tan(pressure_angle) - root_radius * cos(pressure_angle)
    # ==> calculated for the right tooth, left root; indicated by _rl suffix
    # ==> x-value >= 0 for valid values of root radius; bottom clearance limit may further constrain

    if xc_rho_rl < 0:
        print("\x1b[31mWARNING: Root geometry is not feasible!\x1b[0m")  # red color formatting

    # left tooth, left root
    xc = - pitch + xc_rho_rl
    x_lt_lr, y_lt_lr = circle_curve(root_radius, -pi / 2, -pressure_angle, xc, yc_rho)

    # left tooth, tip land
    x_lt_tip = [- 3 * pitch / 4 + addendum * tan(pressure_angle), - pitch / 4 - addendum * tan(pressure_angle)]
    y_lt_tip = [addendum] * 2

    # left tooth, right root
    xc = - xc_rho_rl
    x_lt_rr, y_lt_rr = circle_curve(root_radius, -pi + pressure_angle, -pi / 2, xc, yc_rho)

    # root land
    x_root = [-xc_rho_rl, xc_rho_rl]
    y_root = [-dedendum] * 2

    # right tooth, left root
    xc = xc_rho_rl
    x_rt_lr, y_rt_lr = circle_curve(root_radius, -pi / 2, -pressure_angle, xc, yc_rho)

    # right tooth, tip land
    x_rt_tip = [pitch / 4 + addendum * tan(pressure_angle), 3 * pitch / 4 - addendum * tan(pressure_angle)]
    y_rt_tip = [addendum] * 2

    # right tooth, right root
    xc = pitch - xc_rho_rl
    x_rt_rr, y_rt_rr = circle_curve(root_radius, -pi + pressure_angle, -pi / 2, xc, yc_rho)

    # combine coordinate data
    x_left_tooth_data = x_lt_lr + x_lt_tip + x_lt_rr
    y_left_tooth_data = y_lt_lr + y_lt_tip + y_lt_rr

    x_right_tooth_data = x_rt_lr + x_rt_tip + x_rt_rr
    y_right_tooth_data = y_rt_lr + y_rt_tip + y_rt_rr

    x_coord = x_left_tooth_data + x_root + x_right_tooth_data
    y_coord = y_left_tooth_data + y_root + y_right_tooth_data

    return x_coord, y_coord


def undercut_basic_rack_coordinates(module, pressure_angle_deg, addendum_coefficient, dedendum_coefficient,
                                    root_radius_coefficient, undercut_angle_deg, undercut_size):
    """Cartesian coordinates for a basic rack with undercut.

    Coordinates are computed from left to right, with the origin on the datum line at mid-spacewidth.
    """

    pitch = pitch_fcn(module)
    addendum = addendum_coefficient * module
    dedendum = dedendum_coefficient * module
    root_radius = root_radius_coefficient * module
    pressure_angle = radians(pressure_angle_deg)
    undercut_angle = radians(undercut_angle_deg)

    # height of root radius, undercut, and dedendum tooth profile
    root_radius_height = root_radius - root_radius * sin(undercut_angle)
    x_qf = root_radius * (1 - cos(pressure_angle - undercut_angle))
    l_u = (undercut_size - x_qf) / sin(pressure_angle - undercut_angle)
    undercut_profile_height = l_u * cos(undercut_angle)
    undercut_height_from_bottom = root_radius_height + undercut_profile_height
    dedendum_profile_height = dedendum - undercut_height_from_bottom

    yc_rho = - dedendum + root_radius
    y_undercut = - dedendum + undercut_height_from_bottom

    xc_rho_rl = pitch / 4 - dedendum_profile_height * tan(pressure_angle) - undercut_profile_height * tan(
        undercut_angle) - root_radius * cos(undercut_angle)
    # ==> calculated for the right tooth, left root; indicated by _rl suffix
    # ==> x-value >= 0 for valid values of root radius; bottom clearance limit may further constrain

    if xc_rho_rl < 0:
        print("\x1b[31mWARNING: Root geometry is not feasible!\x1b[0m")  # red color formatting

    # left tooth, left root
    xc = - pitch + xc_rho_rl
    x_lt_lr, y_lt_lr = circle_curve(root_radius, -pi / 2, -undercut_angle, xc, yc_rho)

    # left tooth, left undercut point
    x_lt_lu = [- 3 * pitch / 4 - dedendum_profile_height * tan(pressure_angle)]
    y_lt_lu = [y_undercut]

    # left tooth, tip land
    x_lt_tip = [- 3 * pitch / 4 + addendum * tan(pressure_angle), - pitch / 4 - addendum * tan(pressure_angle)]
    y_lt_tip = [addendum] * 2

    # left tooth, right undercut point
    x_lt_ru = [- pitch / 4 + dedendum_profile_height * tan(pressure_angle)]
    y_lt_ru = [y_undercut]

    # left tooth, right root
    xc = - xc_rho_rl
    x_lt_rr, y_lt_rr = circle_curve(root_radius, -pi + undercut_angle, -pi / 2, xc, yc_rho)

    # root land
    x_root = [-xc_rho_rl, xc_rho_rl]
    y_root = [-dedendum] * 2

    # right tooth, left root
    xc = xc_rho_rl
    x_rt_lr, y_rt_lr = circle_curve(root_radius, -pi / 2, -undercut_angle, xc, yc_rho)

    # right tooth, left undercut point
    x_rt_lu = [pitch / 4 - dedendum_profile_height * tan(pressure_angle)]
    y_rt_lu = [y_undercut]

    # right tooth, tip land
    x_rt_tip = [pitch / 4 + addendum * tan(pressure_angle), 3 * pitch / 4 - addendum * tan(pressure_angle)]
    y_rt_tip = [addendum] * 2

    # right tooth, right undercut point
    x_rt_ru = [3 * pitch / 4 + dedendum_profile_height * tan(pressure_angle)]
    y_rt_ru = [y_undercut]

    # right tooth, right root
    xc = pitch - xc_rho_rl
    x_rt_rr, y_rt_rr = circle_curve(root_radius, -pi + undercut_angle, -pi / 2, xc, yc_rho)

    # combine coordinate data
    x_left_tooth_data = x_lt_lr + x_lt_lu + x_lt_tip + x_lt_ru + x_lt_rr
    y_left_tooth_data = y_lt_lr + y_lt_lu + y_lt_tip + y_lt_ru + y_lt_rr

    x_right_tooth_data = x_rt_lr + x_rt_lu + x_rt_tip + x_rt_ru + x_rt_rr
    y_right_tooth_data = y_rt_lr + y_rt_lu + y_rt_tip + y_rt_ru + y_rt_rr

    x_coord = x_left_tooth_data + x_root + x_right_tooth_data
    y_coord = y_left_tooth_data + y_root + y_right_tooth_data

    return x_coord, y_coord

# endregion
