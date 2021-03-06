# HBV Lumped conceptual model
The HBV model [Bergström, 1992] is usually run with daily time steps, but higher resolution (hourly) can be used if data are available. Input data are precipitation, air temperature and potential evapotranspiration.

HBV model consists of three main components:
snow accumulation and melt, soil moisture accounting, response and river routing subroutines

![HBV Component](../img/water_cycle.png)
[Bergström, 1992]

The model has number of free parameters, values of which are found by calibration, There are also parameters describing the characteristics of the basin and its climate

The soil moisture accounting calculations require data on the potential evapotranspiration.Normally monthly mean standard values are sufficient, but more detailed data can also
be used. The source of these data may either be calculations according to the Penman formula or similar, or measurements by evaporimeters. In the latter case it is important
to correct for systematic errors before entering the model.

where 14 parameters [`tt`,`sfcf`,`cfmax`,`cwh`,`cfr`,`fc`,`beta`,`lp`,`k0`,`k1`,`k2`,`uzl`,`perc`,`maxbas`]

another two parameters are added for the correction of the rainfall values `rfcf` and for the correction of the calculated evapotranspiration values `E_corr`, therefore the HBV version used inside Hapi uses 16 parameter with the following order 
[`tt`,`sfcf`,`cfmax`,`cwh`,`cfr`,`rfcf`,`fc`,`beta`,`E_corr`,`lp`,`k0`,`k1`,`k2`,`uzl`,`perc`,`maxbas`], and in case the catchment does not have a snow then the HBV model used 11 parameter (excluding the first 5 parameters)


![HBV Component](../img/HBV_buckets.png)
[Bergström, 1992]
## Snow
The snow routine controls snow accumulation and melt. The precipitation accumulates as snow when the air temperature drops below a threshold value (TT). snow accumulation is adjusted by a free parameter, Sfcf, the snowfall correction factor.
Melt starts with temperatures above the threshold, TT, according to a simple degree-day
```
MELT = Cfmax * (T - TT)
where: MELT = snowmelt (mm/day)
Cfmax = degree-day factor (mm/°C · day)
TT = temperature threshold (C).
```
The liquid water holding capacity of snow has to be exceeded before any runoff is generated. A refreezing coefficient, which is used to refreeze free water in the snow if snowmelt is interrupted.

The snow routine of the HBV model has primarily four free parameters that have to be estimated by calibration: TT, Cfmax, cfr, cwh· 

## Soil moisture
The soil moisture accounting routine computes an index of the wetness of the entire basin and integrates interception and soil moisture storage. Soil moisture subroutine is controlled by three free parameters, FC, BETA and LP. FC (Field capacity) is the maximum soil moisture storage in the basin and BETA determines the relative contribution to runoff from a millimeter of rain or snowmelt at a given soil moisture deficit. 

![Beta](../img/Beta.png)

LP controls the shape of the reduction curve for potential evaporation. At soil moisture values below LP the actual evapotranspiration will be reduced. 

To accounts for temperature anomalies a correction factor based on mean daily air temperatures and long term averages is used.
```
Ea = (1 + (T - Tm) * Ecorr)*Ep
where:
Ea is calculated actual evapotranspiration
Ecorr is evapotranspiration correction factor
T is temperature (C)
Tm is monthly long term average temperature (C)
Ep is monthly long term average potential evapotranspiration
```
![Beta](../img/Evapotranspiration.png)

## Runoff response
The runoff response routine transforms excess water from the soil moisture routine to discharge. The routine consists of two reservoirs with three free parameters: three recession coefficients, K0, K1 and :K2, a threshold UZL, and a constant percolation rate, PERC. 

Finally there is a filter for smoothing of the generated flow. This filter consists of a triangular weighting function with one free parameter, MAXBAS. There is also a Muskingum routing procedure available for flood routing.

![MaxBas](../img/maxbas.png)

## Lake

lakes can be included explicitly using a storage discharge curve relationship which requires dividing the catchment into sub-basins defined by outlet of lakes.
In case of the existence of a lake in the catchment, the outflow from basins upstream of the lake will be summed and be used as an inflow to the lake. 
Storage in the lake will be computed according to water stage/storage curve or water stage/lake surface area table and outflow can be obtained from a rating curve (IHMS 2010).
Lakes have a significant impact on the dynamics of runoff process and the routing and therefore modelled explicitly, and for that the presence of a lake in the catchment is an important factor for choosing substructure based on sub basins. (Lindström et al. 1997)

![MaxBas](../img/lake.png)

Bergström, Sten. 1992. “The HBV Model - Its Structure and Applications.” Smhi Rh 4(4): 35.

# Hapi Lumped Model

to run the HBV lumped model inside Hapi you need to prepare the meteorological inputs (rainfall, temperature and potential evapotranspiration), HBV parameters, and the HBV model (you can load Bergström, 1992 version of HBV from Hapi )

- First load the prepared lumped version of the HBV module inside Hapi, the triangular routing function and the wrapper function that runs the lumped model `RUN`.
```
import Hapi.hbv_bergestrom92 as HBVLumped
import Hapi.run as RUN
from Hapi.routing import TriangularRouting
```
- read the meteorological data, data has be in the form of numpy array with the following order [rainfall, ET, Temp, Tm], ET is the potential evapotranspiration, Temp is the temperature (C), and Tm is the long term monthly average temperature.
```
import numpy as np
import pandas as pd

data=pd.read_csv("meteo_data.txt",header=0 ,delimiter=',', index_col=0)
data=data.values
```
- Loat the pre-estimated parameters with the following order ["rfcf","tt","sfcf","cfmax","cwh","cfr","fc","beta","lp","k0","k1","k2","uzl","perc","maxbas"] if the catchment has snow, if not ["rfcf","fc","beta","lp","k0","k1","k2","uzl","perc","maxbas"] and convert it to list

```
parameters = pd.read_csv("parameter.txt", index_col = 0, header = None)
parameters = parameters[1].tolist()
```
- prepare the initial conditions, snow option (if you want to simulate snow accumulation and snow melt or not), temporal resolution, and cathcment area.
```
### Basic_inputs
ConceptualModel = HBVLumped
# p2 = [temporal resolution, catchment area]
p2=[24, 1530]
init_st=[0,10,10,10,0]
# no snow subroutine
snow = 0
```
- prepare the routing options (whether you want to route the generated discharge or not, if yes the routing function).
```
### Routing
Routing=1
RoutingFn=TriangularRouting
```
- now all the data required for the model are prepared in the right form, now you can call the `RunLumped` wrapper to initiate the calculation
```
st, q_sim=RUN.RunLumped(ConceptualModel,data,parameters,p2,init_st,snow,Routing, RoutingFn)
```
the `RunLumped` returns two numpy arrays first is the state variables [snow pack, soil moisture, upper zone, lower zone, water content], and second array is the calculated discharge.

to calculate some metrics for the quality assessment of the calculate discharge the `performancecriteria` contains some metrics like `RMSE`, `NSE`, `KGE` and `WB` , you need to load it, a measured time series of doscharge for the same period of the simulation is also needed for the comparison.

all methods in `performancecriteria` takes two numpy arrays of the same length and return real number.
```
import Hapi.performancecriteria as PC

# observed flow
Qobs =np.loadtxt("measuredQ.txt")

Metrics = dict()

Metrics['RMSE'] = PC.RMSE(Qobs, q_sim)
Metrics['NSE'] = PC.NSE(Qobs, q_sim)
Metrics['NSEhf'] = PC.NSEHF(Qobs, q_sim)
Metrics['KGE'] = PC.KGE(Qobs, q_sim)
Metrics['WB'] = PC.WB(Qobs, q_sim)
```
to plot the calculated and measured discharge import matplotlib

```
import matplotlib.pyplot as plt

plt.figure(1, figsize=(12,8))
plt.plot(q_sim)
plt.plot(Qobs)
plt.xlabel("Time (daily)")
plt.ylabel("Flow Hydrograph m3/s")
```