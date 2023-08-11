## Call largo
Principalmente me base en el modelo que se ve en el video adjunto en las referencias pero este contiene muchos errores. En este modela un strangle y hace parecer que las opciones son casi siempre una apuesta segura *no lo son*. Algunos de los errores que encontre y recuerdo son:
1. Omite la comision de cierre
2. Omite el cobro de premium en la utilidad bruta
3. Omite la cantidad de subyacentes en cada opcion
4. No topa las comisiones 
5. Usa mal los strikes en la utilidad bruta
6. Ejerce la opcion antes del breakeven


## Nuevo modelo
Parti del modelo anterior y lo dividi en sus compnentes principales, un call largo y un put largo. resolvi el tema de las comisiones -*no fue sencillo*- y arregle el calculo del payoff. Ahora las utilidades son mas realistas. El modelo funciona de la siguiente manera:

Primero calculemos la comision de apertura y cierre:
$$
Open \ fee = min(fee*precio \ subyacente*num \ subyacentes, \ 0.1*premium)*num \ contratos
$$

$$
Close \ fee = min(S_{t}*fee*num \ subyacentes, \ 0.1*(S_{t}-K))*num \ contratos
$$

Como no siempre se ejerce la opcion entonces no siempre se cobra esta comision por lo que hay que modificarla un poco para que funcione en el modelo, $S_{t}-K$ es el valor intrinsico de la opcion, y esta solo tiene valor cuando estamos in the money osea $(S_{t}-K)>0$ en caso contrario se toma como $0$
$$
Close \ fee' = min(S_{t}*fee*num \ subyacentes, \ 0.1*if(S_{t}-K)<0, \ 0, \ (S_{t}-K))*num \ contratos
$$

Ahora el payoff bruto esta dado por:
$$
Call_{B} = max(S_{t}-K, \ 0) - premium*weight 
$$

Y finalmente la utilidad neta se calcula asi:
$$
Call_{N} \ = \ (if(Call_{B}<=0, \ Call_{B}*contratos, \ Call_{B}*participacion*leverage*num \ subyayecentes)*num \ contratos) \ - \ (Close \ fee \ + \ Open \ fee)
$$




### Referencias
* https://docs.google.com/spreadsheets/d/1aC04DyfDFYNIq7DyonNic8fJ0-y9CVJn3kdCaCkNCEw/edit?usp=sharing
* https://www.macroption.com/calculating-option-payoff-in-excel/
* https://www.binance.com/en/support/faq/binance-options-trading-fees-5326e5de61c34fed98abe28d2f175a23
* https://stackoverflow.com/questions/36921951/truth-value-of-a-series-is-ambiguous-use-a-empty-a-bool-a-item-a-any-o
* https://www.youtube.com/watch?v=trOpiNjL2s0&t=1189s




# Estoy cobrando la comision de apertura en la utilidad bruta, se debe de cobrar en la utilidad neta