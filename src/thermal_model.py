
"""
Heat sink thermal calculation model.

This implementation follows the calculation formulas in the
original Python script supplied by Expert Thermal / XThermal.

Important source discrepancy:
The accompanying written reference report specifies Rjc = 0.1
and includes base conduction resistance. The supplied Python
script instead uses Rjc = 0.2 and does not calculate base
conduction resistance. This implementation follows the script.
"""

# ---------------------------------------------------------
# 1. FIXED GEOMETRY AND MATERIAL PROPERTIES
# ---------------------------------------------------------

# Processor die dimensions (metres)
DIE_LENGTH_M = 0.0525
DIE_WIDTH_M = 0.045
DIE_THICKNESS_M = 0.0022
DIE_AREA_M2 = DIE_LENGTH_M * DIE_WIDTH_M

# Heat sink dimensions (metres)
SINK_LENGTH_M = 0.09
SINK_WIDTH_M = 0.116
SINK_HEIGHT_M = 0.027
BASE_THICKNESS_M = 0.0025

NUMBER_OF_FINS = 60
FIN_THICKNESS_M = 0.0008
FIN_HEIGHT_M = SINK_HEIGHT_M - BASE_THICKNESS_M

# Material properties
ALUMINIUM_CONDUCTIVITY = 167.0
TIM_THICKNESS_M = 0.0001

# Air properties at 25 degrees Celsius
AIR_CONDUCTIVITY = 0.0262
AIR_KINEMATIC_VISCOSITY = 1.57e-5
AIR_PRANDTL_NUMBER = 0.71

AMBIENT_TEMPERATURE_C = 25.0

# Original supplied Python code uses 0.2 °C/W
JUNCTION_TO_CASE_RESISTANCE = 0.2


# ---------------------------------------------------------
# 2. GEOMETRY CALCULATIONS
# ---------------------------------------------------------

def calculate_fin_spacing():
    """Calculate the clear spacing between adjacent fins."""

    return (
        SINK_WIDTH_M - NUMBER_OF_FINS * FIN_THICKNESS_M
    ) / (NUMBER_OF_FINS - 1)


def calculate_convective_area():
    """
    Calculate convection area using the original supplied code.

    A_fin = N_fins * (2 * h_fin * L) + (s_f * L)

    A_base_convection = (L * W) -
                        (fin_thickness * N_fins * L)

    A_total = A_fin + A_base_convection
    """

    fin_spacing_m = calculate_fin_spacing()

    # Original supplied fin area calculation
    fin_area = (
        NUMBER_OF_FINS
        * (2 * FIN_HEIGHT_M * SINK_LENGTH_M)
        + (fin_spacing_m * SINK_LENGTH_M)
    )

    # Original supplied exposed base area calculation
    total_base_area = SINK_LENGTH_M * SINK_WIDTH_M

    base_convection_area = (
        total_base_area
        - (
            FIN_THICKNESS_M
            * NUMBER_OF_FINS
            * SINK_LENGTH_M
        )
    )

    return fin_area + base_convection_area


# ---------------------------------------------------------
# 3. MAIN THERMAL CALCULATION
# ---------------------------------------------------------

def calculate_thermal_performance(
    tdp_w,
    air_velocity_m_s,
    k_tim_w_mk
):
    """
    Calculate thermal resistance and junction temperature.

    Parameters:
        tdp_w: Processor thermal design power in watts.
        air_velocity_m_s: Air velocity in m/s.
        k_tim_w_mk: TIM thermal conductivity in W/(m K).

    Returns:
        Dictionary containing thermal and flow parameters.
    """

    # Validate inputs
    if not 30 <= tdp_w <= 250:
        raise ValueError("TDP must be between 30 and 250 W.")

    if not 0.5 <= air_velocity_m_s <= 15:
        raise ValueError("Air velocity must be between 0.5 and 15 m/s.")

    if not 1 <= k_tim_w_mk <= 12:
        raise ValueError("TIM conductivity must be between 1 and 12 W/(m K).")

    # -----------------------------------------------------
    # Step 1: Fin spacing
    # -----------------------------------------------------

    fin_spacing_m = calculate_fin_spacing()

    # -----------------------------------------------------
    # Step 2: Reynolds number
    # -----------------------------------------------------

    reynolds_number = (
        air_velocity_m_s
        * fin_spacing_m
        / AIR_KINEMATIC_VISCOSITY
    )

    # -----------------------------------------------------
    # Step 3: Nusselt number
    # -----------------------------------------------------

    if reynolds_number < 2300:

        nusselt_number = 1.86 * (
            (
                reynolds_number
                * AIR_PRANDTL_NUMBER
                * (2 * fin_spacing_m)
                / SINK_LENGTH_M
            ) ** (1 / 3)
        )

        flow_regime = "Laminar"

    else:

        nusselt_number = (
            0.023
            * reynolds_number ** 0.8
            * AIR_PRANDTL_NUMBER ** 0.3
        )

        flow_regime = "Turbulent"

    # -----------------------------------------------------
    # Step 4: Convective heat transfer coefficient
    # -----------------------------------------------------

    h_convection = (
        nusselt_number
        * AIR_CONDUCTIVITY
        / (2 * fin_spacing_m)
    )

    # -----------------------------------------------------
    # Step 5: Thermal resistance calculations
    # -----------------------------------------------------

    # Junction-to-case resistance
    r_junction_case = JUNCTION_TO_CASE_RESISTANCE

    # TIM resistance
    r_tim = (
        TIM_THICKNESS_M
        / (k_tim_w_mk * DIE_AREA_M2)
    )

    # Convection resistance
    convection_area_m2 = calculate_convective_area()

    r_convection = (
        1 / (h_convection * convection_area_m2)
    )

    # The original supplied script does not calculate
    # aluminum base conduction resistance.
    r_conduction = 0.0

    # Follow the original supplied script:
    # R_hs = R_conv + R_tim
    r_heat_sink = r_convection + r_tim

    # Original total resistance:
    # R_total = R_jc + R_hs
    r_total = r_junction_case + r_heat_sink

    # -----------------------------------------------------
    # Step 6: Junction temperature
    # -----------------------------------------------------

    junction_temperature_c = (
        AMBIENT_TEMPERATURE_C
        + tdp_w * r_total
    )

    # -----------------------------------------------------
    # Step 7: Return results
    # -----------------------------------------------------

    return {
        "tdp_w": tdp_w,
        "air_velocity_m_s": air_velocity_m_s,
        "k_tim_w_mk": k_tim_w_mk,

        "fin_spacing_m": fin_spacing_m,
        "reynolds_number": reynolds_number,
        "flow_regime": flow_regime,
        "nusselt_number": nusselt_number,
        "h_convection_w_m2k": h_convection,
        "convection_area_m2": convection_area_m2,

        "r_junction_case_c_per_w": r_junction_case,
        "r_tim_c_per_w": r_tim,
        "r_conduction_c_per_w": r_conduction,
        "r_convection_c_per_w": r_convection,
        "r_heat_sink_c_per_w": r_heat_sink,
        "r_total_c_per_w": r_total,

        "junction_temperature_c": junction_temperature_c,
    }
