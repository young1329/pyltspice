# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

'''
8.6.1 LPF RC
'''
import math
import numpy as np
import matplotlib.pyplot as plt


import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()


from PySpice.Plot.BodeDiagram import bode_diagram
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


circuit = Circuit('Low-Pass RC Filter')

Vin = circuit.SinusoidalVoltageSource('input', 'inp', circuit.gnd, amplitude=1@u_V)
R1 = circuit.R(1, 'inp', 'out', 1@u_kΩ)
C1 = circuit.C(1, 'out', circuit.gnd, 1@u_uF)

tau=R1.resistance*C1.capacitance
wo=1/tau
fo=wo/2/np.pi

break_frequency = 1 / (2 * math.pi * float(R1.resistance * C1.capacitance))
print("Break frequency = {:.1f} Hz".format(break_frequency))

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.ac(start_frequency=1@u_Hz, stop_frequency=1@u_MHz, number_of_points=10,  variation='dec')
# print(analysis.out)


fig = plt.figure(figsize=(10,7))
ax1 = fig.add_subplot(1, 1, 1)
ax1t=ax1.twinx()


ax1.plot(analysis.frequency, 20*np.log10(np.abs(analysis.out)),color='blue')
ax1.set_xscale('log')
ax1.set_xscale('log')
ax1.set_xlabel('freq(Hz)')
ax1.set_ylabel('dB(Vo)',color='tab:red')
ax1.tick_params(axis='y',labelcolor='tab:red')
ax1.set_ylim(top=0, bottom=-60)
ax1.vlines(fo,ymin=-60, ymax=0,color='tab:red', linestyle='dotted')
ax1.hlines(-3,xmin=100, xmax=1e6, color='tab:red',linestyle='dotted')
ax1.text(fo,-3,'-3dB',ha='left',va='bottom', color='tab:red')


ax1t.set_ylabel('∠ $\mathcal{Vo}\degree$',color='tab:blue')
ax1t.tick_params(axis='y',labelcolor='tab:blue')
ax1t.plot(analysis.frequency,np.angle(analysis.out)*180/np.pi,color='tab:blue')
ax1t.set_ylim(top=0, bottom=-90)
ax1t.vlines(fo,ymin=-90, ymax=0, color='tab:blue',linestyle='dashed')
ax1t.hlines(-45,xmin=10,xmax=1e6, color='tab:blue', linestyle='dotted')
ax1t.text(fo,-45,"-45 $\degree$",ha='left',va='baseline', c='tab:blue')

plt.show()




