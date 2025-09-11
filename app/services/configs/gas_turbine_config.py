# configs/gas_turbine_config.py
from dataclasses import dataclass

@dataclass
class GasTurbineConfig:
  """Parameter package and required dependencies for GasTurbine"""
  input: dict
  gas_fuel: object
  icph: object
  substance_repo: object
  icph_repo: object
  reactions: object
  input_air: object
  combustion_gas: object
  humidity: object
  saturation_parameters: object
