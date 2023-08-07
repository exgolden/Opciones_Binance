#librerias e input
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

with open("Settings/fee_settings.json", "r") as file:
    fee_data = json.load(file)
with open("Settings/call_settings.json", "r") as file:
    call_data = json.load(file)

#Funciones y declaraciones
data = pd.DataFrame(columns = ["Precio", "G. Bruta", "G. Neta"])
# Weighted premium
premiumNeto : float = call_data["Premium"]*call_data["Participacion"]

# Fee de apertura
openFee : float = round(min(fee_data["Open fee"]*call_data["Precio"]*call_data["Participacion"],
                        0.1*call_data["Premium"])*call_data["Contratos"], 3)

# Utilidad de la opcion
def call_payoff(close: float, strike: float, premium: float, oFee : float) -> float:
    return np.maximum(close-strike, 0) - (premium + oFee)

# Fee de cierre
def closeFee(cFee : float, numero : int, close : float, strike : float, contratos : int) -> float:
    return np.minimum(cFee*numero*close, 0.1*np.where((close-strike)<0, 0, (close-strike)))*contratos

# Valor del ejerccio
def optionVal(gBruta : float, contratos : int, participacion : float, multiplicador : float, numero : int) -> float:
    return np.where(gBruta <= 0, gBruta*contratos, (gBruta*participacion*multiplicador*numero)*contratos)

#Data
data["Precio"] = np.arange(call_data["Lim. Inferior"], call_data["Lim. Superior"]+1, call_data["Granularidad"])
data["G. Bruta"] = np.round(call_payoff(data["Precio"], call_data["Strike"], premiumNeto, openFee), 3)
data["G. Neta"] = np.round(optionVal(data["G. Bruta"], call_data["Contratos"],
                            call_data["Participacion"], call_data["Multiplicador"],
                            call_data["#"]) - closeFee(fee_data["Close fee"], call_data["#"],
                            data["Precio"], call_data["Strike"], call_data["Contratos"]), 3)
data.to_csv("prueba.csv", index = False)
