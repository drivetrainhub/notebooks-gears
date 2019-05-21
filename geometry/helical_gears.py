# Copyright 2019 Drivetrain Hub LLC
# For non-commercial use only.  For commercial products and services, visit https://www.drivetrainhub.com.

"""Notebook module for helical gear geometry."""

from math import pi, sin, cos, tan, acos, atan
import numpy as np


# region HELPERS

def involute_function(pressure_angle):
    """Involute function of an arbitrary pressure angle."""

    return tan(pressure_angle) - pressure_angle


def inverse_involute_function(involute_fcn):
    """Solve the involute function for phi, where involute_function(phi) = tan(phi) - phi.

    Implements the direct approximation by Cheng, see references.
    Accurate to six significant figures up to phi = 60 degrees.
    """

    q = involute_fcn
    phi = (3 * q) ** (1 / 3) - \
          (2 * q) / 5 + \
          (9 / 175) * (3) ** (2 / 3) * (q) ** (5 / 3) - \
          (2 / 175) * (3) ** (1 / 3) * (q) ** (7 / 3) - \
          (144 / 67375) * (q) ** (9 / 3) + \
          (3258 / 3128125) * (3) ** (2 / 3) * (q) ** (11 / 3) - \
          (49711 / 153278125) * (3) ** (1 / 3) * (q) ** (13 / 3)

    return phi


def diameter_to_roll_angle(base_diameter, diameter):
    """Convert involute diameter to roll angle."""

    return tan(acos(base_diameter / diameter))


def roll_angle_to_diameter(base_diameter, roll_angle):
    """Convert involute roll angle to diameter."""

    return base_diameter / cos(atan(roll_angle))


# endregion


# region HELICAL GEAR

# region HELIX

def helix_curve(radius, helix_angle, length):
    """Cartesian coordinates of a helix curve."""

    c = radius / tan(helix_angle)
    pitch = helix_pitch_fcn(radius, helix_angle)

    z = np.linspace(0, length, num=abs(int(pitch * 50)))
    t = z / c

    x = radius * np.cos(t)
    y = radius * np.sin(t)

    return x, y, z


def helix_pitch_fcn(radius, helix_angle):
    """Pitch of a helix curve."""

    return 2 * pi * radius / tan(abs(helix_angle))


def helix_angle_arbitrary_fcn(diameter_arbitrary, helix_angle_ref, diameter_ref):
    """Helix angle at an arbitrary diameter."""

    return atan(diameter_arbitrary * tan(helix_angle_ref) / diameter_ref)


# endregion


# region TOOTH SIZE

def module_transverse_fcn(module_normal, helix_angle):
    return module_normal / cos(helix_angle)


def theoretical_pitch_diameter_fcn(module_transverse, number_of_teeth):
    return module_transverse * number_of_teeth


def pitch_transverse_fcn(diameter, number_of_teeth):
    """Transverse pitch at an arbitrary diameter.

    To calculate transverse base pitch, specify the base circle diameter as an input arg.
    """

    return pi * diameter / number_of_teeth


def pitch_normal_fcn(module_normal):
    """Normal pitch of helical gear teeth."""

    return pi * module_normal


def pitch_axial_fcn(module_normal, helix_angle):
    """Axial pitch of helical gear teeth."""

    return pi * module_normal / sin(helix_angle)


def base_pitch_normal_fcn(module_normal, pressure_angle_normal):
    """Normal base pitch of helical gear teeth."""

    return pi * module_normal * cos(pressure_angle_normal)


def base_pitch_axial_fcn(module_normal, pressure_angle_normal, helix_angle_base):
    """Axial base pitch of helical gear teeth.

    Since the gear helix pitch length is the same regardless of diameter, axial base pitch is equal to axial pitch at
    the theoretical pitch diameter.
    """

    return pi * module_normal * cos(pressure_angle_normal) / sin(helix_angle_base)


def diametral_pitch_fcn(module):
    return 25.4 / module


# endregion


# region PRESSURE ANGLE

def pressure_angle_transverse_fcn(pressure_angle_normal, helix_angle):
    """Transverse pressure angle at the theoretical pitch diameter."""

    return atan(tan(pressure_angle_normal) / cos(helix_angle))


def pressure_angle_transverse_arbitrary_fcn(base_diameter, diameter):
    """Transverse pressure angle at an arbitrary diameter."""

    return acos(base_diameter / diameter)


def pressure_angle_transverse_to_diameter(base_diameter, pressure_angle_transverse_arbitrary):
    """Diameter at an arbitrary transverse pressure angle."""

    return base_diameter / cos(pressure_angle_transverse_arbitrary)


# endregion


# region DIAMETERS

def base_diameter_fcn(theoretical_pitch_diameter, pressure_angle_transverse):
    """Diameter of involute base circle."""

    return theoretical_pitch_diameter * cos(pressure_angle_transverse)


def root_diameter_fcn(theoretical_pitch_diameter, basic_rack_dedendum, profile_shift):
    return theoretical_pitch_diameter - 2 * (basic_rack_dedendum - profile_shift)


def tip_diameter_fcn(theoretical_pitch_diameter, basic_rack_addendum, profile_shift):
    return theoretical_pitch_diameter + 2 * (basic_rack_addendum + profile_shift)


# endregion


# region TOOTH THICKNESS

def tooth_thickness_transverse_fcn(module_normal, pressure_angle_normal, helix_angle, profile_shift_coefficient):
    """Circular tooth thickness in the transverse plane, at the theoretical pitch diameter."""

    return module_normal / cos(helix_angle) * (pi / 2 + 2 * profile_shift_coefficient * tan(pressure_angle_normal))


def tooth_thickness_transverse_arbitrary_fcn(diameter, module_normal, pressure_angle_normal,
                                             number_of_teeth, helix_angle, profile_shift_coefficient):
    """Circular tooth thickness in the transverse plane, at an arbitrary diameter."""

    pa_transverse = pressure_angle_transverse_fcn(pressure_angle_normal, helix_angle)
    module_transverse = module_transverse_fcn(module_normal, helix_angle)
    theoretical_pitch_diameter = theoretical_pitch_diameter_fcn(module_transverse, number_of_teeth)
    base_diameter = base_diameter_fcn(theoretical_pitch_diameter, pa_transverse)
    pa_transverse_at_diameter = pressure_angle_transverse_arbitrary_fcn(base_diameter, diameter)

    return diameter * (pi / (2 * number_of_teeth) +
                       2 * profile_shift_coefficient * tan(pressure_angle_normal) / number_of_teeth +
                       involute_function(pa_transverse) -
                       involute_function(pa_transverse_at_diameter))


def tooth_thickness_normal_fcn(tooth_thickness_transverse, helix_angle):
    """Circular tooth thickness in the normal plane."""

    return tooth_thickness_transverse * cos(helix_angle)


def tooth_thickness_half_angle_fcn(diameter, tooth_thickness_transverse_at_diameter):
    """Tooth thickness half angle in the transverse plane, at an arbitrary diameter."""

    return tooth_thickness_transverse_at_diameter / diameter


# endregion


# region ROOT

def form_diameter_fcn(module_normal, pressure_angle_normal, helix_angle, number_of_teeth,
                      cutter_addendum_coefficient, profile_shift_coefficient, tip_radius_coefficient):
    """Diameter of boundary point at root fillet and involute profile for a helical gear without undercut.

    None is returned if undercut is detected.
    """

    # tool params
    m_n = module_normal
    x_c = profile_shift_coefficient
    h_f = cutter_addendum_coefficient * m_n
    rho = tip_radius_coefficient * m_n
    alpha_n = pressure_angle_normal
    alpha_t = pressure_angle_transverse_fcn(alpha_n, helix_angle)
    m_t = module_transverse_fcn(m_n, helix_angle)

    # involute params
    d = theoretical_pitch_diameter_fcn(m_t, number_of_teeth)
    d_b = base_diameter_fcn(d, alpha_t)
    r_b = d_b / 2

    # involute profile transverse pressure angle of root fillet boundary point
    numerator = h_f - rho + rho * sin(alpha_n) - x_c * m_n  # tool height calculation
    pressure_angle_transverse_ff = atan(tan(alpha_t) - numerator / (r_b * sin(alpha_t)))

    if pressure_angle_transverse_ff >= 0:
        # root fillet boundary is valid
        fillet_boundary_diameter = pressure_angle_transverse_to_diameter(d_b, pressure_angle_transverse_ff)
    else:
        # root fillet boundary cannot be less than base diameter
        # ==> indicates that gear tooth root is undercut
        fillet_boundary_diameter = None

    return fillet_boundary_diameter


def minimum_profile_shift_coefficient_to_avoid_undercut(basic_rack_addendum_coefficient, pressure_angle_normal,
                                                        number_of_teeth, helix_angle):
    """Minimum profile shift coefficient to avoid undercut with rack generation, such as hobbing."""

    pressure_angle_transverse = pressure_angle_transverse_fcn(pressure_angle_normal, helix_angle)
    numerator = number_of_teeth * sin(pressure_angle_transverse) ** 2
    denominator = 2 * cos(helix_angle)

    return basic_rack_addendum_coefficient - numerator / denominator


def minimum_teeth_to_avoid_undercut(basic_rack_addendum_coefficient, pressure_angle_normal,
                                    profile_shift_coefficient, helix_angle):
    """Minimum number of gear teeth to avoid undercut with rack generation, such as hobbing."""

    alpha_t = pressure_angle_transverse_fcn(pressure_angle_normal, helix_angle)
    sine_squared = sin(alpha_t) ** 2

    return 2 * cos(helix_angle) * (basic_rack_addendum_coefficient - profile_shift_coefficient) / sine_squared


# endregion

# endregion


# region HELICAL GEAR MESH

# region PRESSURE ANGLE

def working_pressure_angle_fcn(center_distance, base_diameter1, base_diameter2):
    """Working pressure angle in transverse plane of a gear pair."""

    return acos((base_diameter1 + base_diameter2) / (2 * center_distance))


def working_pressure_angle_theoretical_fcn(
        profile_shift_coefficient1, profile_shift_coefficient2,
        number_of_teeth1, number_of_teeth2,
        pressure_angle_normal, pressure_angle_transverse):
    """*Theoretical* working pressure angle in transverse plane of a gear pair.

    **Corresponds to the condition of zero backlash.**

    Returns none if an invalid working pressure angle is identified.
    """

    x1 = profile_shift_coefficient1
    x2 = profile_shift_coefficient2
    z1 = number_of_teeth1
    z2 = number_of_teeth2
    a_n = pressure_angle_normal
    a_t = pressure_angle_transverse

    inv_a_w = involute_function(a_t) + 2 * tan(a_n) * (x1 + x2) / (z1 + z2)

    if inv_a_w >= 0:
        # large negative (-) sum of profile shift can cause a negative involute function, thus invalid
        return inverse_involute_function(inv_a_w)


# endregion


# region CENTER DISTANCE

def center_distance_reference_fcn(module_normal, number_of_teeth1, number_of_teeth2, helix_angle):
    """Center distance of a gear pair without any profile shifts or backlash.  Also called null center distance."""

    return module_normal * (number_of_teeth1 + number_of_teeth2) / (2 * cos(helix_angle))


def center_distance_theoretical_fcn(reference_center_distance, working_pressure_angle_transverse,
                                    pressure_angle_transverse):
    """Center distance of a gear pair with zero backlash.  Gears may have profile shift.

    WARNING: The specified working pressure angle must be for the condition of zero backlash.
    """

    return reference_center_distance * cos(pressure_angle_transverse) / cos(working_pressure_angle_transverse)


# endregion


# region CLEARANCES & BACKLASH

def bottom_clearance_fcn(center_distance_actual, root_diameter, mating_tip_diameter):
    """Diametral clearance between root diameter and mating tip diameter."""

    return (center_distance_actual - mating_tip_diameter / 2) - root_diameter / 2


def tip_clearance_fcn(center_distance_actual, tip_diameter, mating_root_diameter):
    """Diametral clearance between tip diameter and mating root diameter."""

    return (center_distance_actual - tip_diameter / 2) - mating_root_diameter / 2


def backlash_radial_fcn(center_distance_actual, center_distance_theoretical):
    """Backlash in the radial direction, along the center line, in the transverse plane."""

    return center_distance_actual - center_distance_theoretical


def backlash_circumferential_fcn(backlash_radial, working_pressure_angle_transverse):
    """Pitch circle arc length of backlash in the circumferential direction in the transverse plane."""

    return 2 * backlash_radial * tan(working_pressure_angle_transverse)


def backlash_angular_fcn(backlash_circumferential, working_pitch_diameter):
    """Angular backlash corresponding to the circumferential backlash, specific to a gear."""

    return 2 * backlash_circumferential / working_pitch_diameter


def backlash_profile_fcn(backlash_circumferential, working_pressure_angle_transverse):
    """Backlash in the line of action, i.e. normal to involute profile, in the transverse plane."""

    return backlash_circumferential * cos(working_pressure_angle_transverse)


def backlash_normal_fcn(backlash_profile, helix_angle_base):
    """Backlash in the plane of action, normal to helicoid tooth surface.  Shortest distance between tooth surfaces."""

    return backlash_profile * cos(helix_angle_base)


# endregion


# region CONTACT

def pressure_angle_transverse_contact_fcn(working_pressure_angle_transverse, number_of_teeth,
                                          mating_number_of_teeth, mating_pressure_angle_transverse_contact_point):
    """Transverse pressure angle at a point of contact.

    Useful for calculating the start of active profile (SAP) and end of active profile (EAP).
    """

    z = number_of_teeth
    z_mate = mating_number_of_teeth
    alpha_w = working_pressure_angle_transverse
    alpha_contact_mating = mating_pressure_angle_transverse_contact_point

    return atan(tan(alpha_w) - z_mate / z * (tan(alpha_contact_mating) - tan(alpha_w)))


def contact_plane_length_fcn(working_pressure_angle_transverse,
                             base_diameter1, base_diameter2,
                             pressure_angle_transverse_eap1, pressure_angle_transverse_eap2):
    """Length of the contact plane for a spur or helical gear pair."""

    tan_w = tan(working_pressure_angle_transverse)
    tan_eap1 = tan(pressure_angle_transverse_eap1)
    tan_eap2 = tan(pressure_angle_transverse_eap2)

    return base_diameter2 / 2 * (tan_eap2 - tan_w) + base_diameter1 / 2 * (tan_eap1 - tan_w)


def contact_ratio_transverse_fcn(working_pressure_angle_transverse,
                                 number_of_teeth1, number_of_teeth2,
                                 pressure_angle_transverse_eap1, pressure_angle_transverse_eap2):
    """Contact ratio of helical gear pair in the transverse plane."""

    tan_w = tan(working_pressure_angle_transverse)
    tan_eap1 = tan(pressure_angle_transverse_eap1)
    tan_eap2 = tan(pressure_angle_transverse_eap2)

    return (number_of_teeth1 * (tan_eap1 - tan_w) + number_of_teeth2 * (tan_eap2 - tan_w)) / (2 * pi)


def contact_ratio_axial_fcn(facewidth_effective, helix_angle, module_normal):
    """Contact ratio of helical gear pair in the axial plane.  Also known as overlap ratio."""

    return facewidth_effective * sin(abs(helix_angle)) / (pi * module_normal)


def contact_ratio_total_fcn(contact_ratio_transverse, contact_ratio_axial):
    """Total contact ratio of spur or helical gear pair."""

    return contact_ratio_transverse + contact_ratio_axial


def contact_lines_length_mean_fcn(facewidth_effective, contact_ratio_transverse, helix_angle_base):
    """Mean of total length of contact lines.  Total length of contact lines varies through mesh cycle."""

    return facewidth_effective * contact_ratio_transverse / cos(helix_angle_base)


def contact_lines_length_min_fcn(contact_lines_length_mean, contact_ratio_transverse, contact_ratio_axial):
    """Minimum of total length of contact lines.  Total length of contact lines varies through mesh cycle."""

    cr_t = contact_ratio_transverse
    cr_a = contact_ratio_axial

    # remainder of contact ratios
    n_t = cr_t % 1
    n_a = cr_a % 1
    n_sum = n_t + n_a

    if cr_a == 0:
        # spur
        contact_lines_length_min = contact_lines_length_mean * (1 - n_t / cr_t)
    else:
        # helical
        if n_sum <= 1:
            contact_lines_length_min = contact_lines_length_mean * (1 - n_t * n_a / (cr_t * cr_a))
        else:
            contact_lines_length_min = contact_lines_length_mean * (1 - (1 - n_t) * (1 - n_a) / (cr_t * cr_a))

    return contact_lines_length_min


# endregion


# region KINEMATICS

def transmission_ratio_fcn(number_of_teeth1, number_of_teeth2):
    """Transmission ratio of a gear pair.

    Also known as the gear speed ratio, defined as :math:`\omega_1 / \omega_2`.
    """

    return number_of_teeth2 / number_of_teeth1


def pitch_diameters_fcn(center_distance_actual, number_of_teeth1, number_of_teeth2):
    """Working pitch diameters of a helical gear mesh.

    Pitch point is at the intersection of these two pitch circles for the specified center distance.
    """

    i = transmission_ratio_fcn(number_of_teeth1, number_of_teeth2)
    pitch_diameter1 = 2 * center_distance_actual / (i + 1)
    pitch_diameter2 = pitch_diameter1 * i

    return pitch_diameter1, pitch_diameter2


def pitch_line_velocity_fcn(pitch_diameter, angular_velocity):
    """Linear velocity at the pitch point of a meshing gear tooth.

    Pitch line velocity is equal in magnitude and direction for both gears in a helical gear pair.
    """

    return pitch_diameter * angular_velocity


def tangential_velocity_fcn(base_diameter, pressure_angle_transverse_contact, angular_velocity):
    """Velocity tangential to the tooth profile at the specified contact point.

    Returns the magnitude of velocity, always a positive value.
    """

    return abs(angular_velocity) * tan(pressure_angle_transverse_contact) * base_diameter / 2


def sliding_velocity_fcn(base_diameter1, base_diameter2,
                         pressure_angle_transverse_contact1, pressure_angle_transverse_contact2,
                         angular_velocity1, angular_velocity2):
    """Sliding velocity at the contact point of an involute profile.

    Relative velocity of the contact point in the direction tangential to the tooth profiles.

    Returns the sliding velocity of both gears: (value1, value2)
    """

    alpha_ty1 = pressure_angle_transverse_contact1
    alpha_ty2 = pressure_angle_transverse_contact2

    tangential_velocity1 = tangential_velocity_fcn(base_diameter1, alpha_ty1, angular_velocity1)
    tangential_velocity2 = tangential_velocity_fcn(base_diameter2, alpha_ty2, angular_velocity2)

    sliding_velocity1 = tangential_velocity1 - tangential_velocity2
    sliding_velocity2 = tangential_velocity2 - tangential_velocity1

    return sliding_velocity1, sliding_velocity2


def specific_sliding_fcn(base_diameter1, base_diameter2,
                         pressure_angle_transverse_contact1, pressure_angle_transverse_contact2,
                         angular_velocity1, angular_velocity2):
    """Specific sliding at the contact point of meshing involute profiles.

    Returns the specific sliding of both gears: (value1, value2)
    """

    alpha_ty1 = pressure_angle_transverse_contact1
    alpha_ty2 = pressure_angle_transverse_contact2

    tangential_velocity1 = tangential_velocity_fcn(base_diameter1, alpha_ty1, angular_velocity1)
    tangential_velocity2 = tangential_velocity_fcn(base_diameter2, alpha_ty2, angular_velocity2)

    sliding_velocity1, sliding_velocity2 = sliding_velocity_fcn(
        base_diameter1, base_diameter2,
        alpha_ty1, alpha_ty2,
        angular_velocity1, angular_velocity2
    )

    specific_sliding1 = sliding_velocity1 / tangential_velocity1
    specific_sliding2 = sliding_velocity2 / tangential_velocity2

    return specific_sliding1, specific_sliding2

# endregion

# endregion
