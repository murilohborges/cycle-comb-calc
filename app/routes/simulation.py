from fastapi import APIRouter
from ..models.input import Input
from ..models.output import Output

router = APIRouter()


@router.post("/simulation", tags=["Simulation"], response_model=Output)
async def create_simulation(input: Input):
    return Output(
        PCI_fuel=1.0,
        air_mass_flow=1.0,
        exhaustion_gas_tempature=1.0,
        exhaustion_gas_mass_flow=1.0,
        thermal_charge=1.0,
        saturated_water_mass_flow=1.0,
        make_up_water_mass_flow=1.0,
        cooling_water_mass_flow=1.0,
        quality_exhaustion_steam_turbine=1.0,
        high_steam_mass_flow=1.0,
        medium_steam_mass_flow=1.0,
        low_steam_mass_flow=1.0,
        pump_variation_pressure=1.0,
        net_power_gas_turbine=1.0,
        gross_power_steam_turbine=1.0,
        net_power_steam_turbine=1.0,
        power_consumed_pump=1.0,
        gross_power_cycle_combined=1.0,
        net_power_cycle_combined=1.0,
        gross_cycle_combined=50.0,  # entre 0 e 100
        net_cycle_combined=50.0     # entre 0 e 100
    )
