#librerias e input
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

with open("Settings/fee_settings.json", "r") as file:
    fee_data = json.load(file)
with open("Settings/call_settings.json", "r") as file:
    call_data = json.load(file)

#%% Funciones y declaraciones
data = pd.DataFrame(columns = ["Precio", "G. Bruta", "G. Neta"])
# Weighted premium
premiumNeto : float = call_data["Premium"]*call_data["Participacion"]

# Fee de apertura
openFee : float = round(min(fee_data["Open fee"]*call_data["Precio"]*call_data["Participacion"],
                        0.1*call_data["Premium"])*call_data["Contratos"], 3)

# Utilidad de la opcion
def call_payoff(close: float, strike: float, premium: float) -> float:
    return np.maximum(close-strike, 0) - premium

# Fee de cierre
def closeFee(cFee : float, numero : int, close : float, strike : float, contratos : int) -> float:
    return np.minimum(cFee*numero*close, 0.1*np.where((close-strike)<0, 0, (close-strike)))*contratos

# Valor del ejerccio
def optionVal(gBruta : float, contratos : int, participacion : float, multiplicador : float, numero : int) -> float:
    return np.where(gBruta <= 0, gBruta*contratos, (gBruta*participacion*multiplicador*numero)*contratos)

#%% Data
data["Precio"] = np.arange(call_data["Lim. Inferior"], call_data["Lim. Superior"]+1, call_data["Granularidad"])
data["G. Bruta"] = np.round(call_payoff(data["Precio"], call_data["Strike"], premiumNeto), 3)
data["G. Neta"] = np.round(optionVal(data["G. Bruta"], call_data["Contratos"],
                            call_data["Participacion"], call_data["Multiplicador"],
                            call_data["#"]) - (closeFee(fee_data["Close fee"], call_data["#"],
                            data["Precio"], call_data["Strike"], call_data["Contratos"]) + openFee), 3)
#%% Calculo de probabilidades

fig = plt.figure(figsize=(14,5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

ax1.set_title("Utilidad bruta")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.axhline(y=0, linestyle="dashed", c="black")
ax1.plot(data["Precio"], data["G. Bruta"])

ax2.set_title("Utilidad Neta")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.axhline(y=0, linestyle="dashed", c="black")
ax2.plot(data["Precio"], data["G. Neta"])
plt.show()

#%% Plot


#%% Comentarios
"""
1) Hay que automatizar el ajuste de granularidad
"""