"""
Heat sink thermal calculation model.

Equations and base dimensions are taken from the supplied
Thermal Reference PDF.

Engineering assumptions:
1. Air flows along the 90 mm heat-sink length.
2. Reynolds number uses fin spacing as the characteristic length.
3. The laminar Nusselt correlation uses the 90 mm flow length.
4. Convective area includes both fin sides, fin tips and exposed
   base surface between the fins.
5. Fin efficiency and radiation are not included.
"""

# ---------------------------------------------------------
# 1. FIXED GEOMETRY AND MATERIAL PROPERTIES
# ---------------------------------------------------------

# Processor die dimensions (metres)
DIE_LENGTH_M = 0.0525
DIE_WIDTH_M = 0.045
DIE_AREA_M2 = DIE_LENGTH_M * DIE_WIDTH_M

# Heat sink dimensions (metres)
SINK_LENGTH_M = 0.09
SINK_WIDTH_M = 0.116
BASE_THICKNESS_M = 0.0025

NUMBER_OF_FINS = 60
FIN_THICKNESS_M = 0.0008
FIN_HEIGHT_M = 0.0245

# Materials
ALUMINIUM_CONDUCTIVITY = 167.0  # W/(m K)
TIM_THICKNESS_M = 0.0001

# Air properties at 25 degrees Celsius
AIR_CONDUCTIVITY = 0.0262       # W/(m K)
AIR_KINEMATIC_VISCOSITY = 1.57e-5  # m²/s
AIR_PRANDTL_NUMBER = 0.71

AMBIENT_TEMPERATURE_C = 25.0
JUNCTION_TO_CASE_RESISTANCE = 0.1  # °C/W


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
    Estimate the exposed heat-sink area available for convection.

    Includes:
    - Both large sides of every fin
    - The top tip of every fin
    - Exposed base surface between fins

    This area calculation is an explicit modelling assumption
    because the reference PDF does not specify Atotal.
    """

    fin_side_area = (
        2
        * NUMBER_OF_FINS
        * SINK_LENGTH_M
        * FIN_HEIGHT_M
    )

    fin_tip_area = (
        NUMBER_OF_FINS
        * SINK_LENGTH_M
        * FIN_THICKNESS_M
    )

    exposed_base_width = (
        SINK_WIDTH_M - NUMBER_OF_FINS * FIN_THICKNESS_M
    )

    exposed_base_area = exposed_base_width * SINK_LENGTH_M

    return fin_side_area + fin_tip_area + exposed_base_area


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

        # Laminar, developing-flow correlation.
        # The sink length is used as the flow length.
        nusselt_number = 1.86 * (
            reynolds_number
            * AIR_PRANDTL_NUMBER
            * (2 * fin_spacing_m / SINK_LENGTH_M)
        ) ** (1 / 3)

        flow_regime = "Laminar"

    else:

        # Turbulent-flow Dittus-Boelter correlation
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

    # Heat sink base conduction resistance
    r_conduction = (
        BASE_THICKNESS_M
        / (ALUMINIUM_CONDUCTIVITY * DIE_AREA_M2)
    )

    # Convection resistance
    convection_area_m2 = calculate_convective_area()

    r_convection = (
        1 / (h_convection * convection_area_m2)
    )

    # Total heat sink resistance
    r_heat_sink = r_conduction + r_convection

    # Total junction-to-ambient resistance
    r_total = (
        r_junction_case
        + r_tim
        + r_heat_sink
    )

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