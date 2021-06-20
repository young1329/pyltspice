# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 13:39:05 2020
µ
@author: min13
"""

from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=True)
from PyLTSpice.LTSpiceBatch import SimCommander
from PyLTSpice.LTSpice_RawRead import LTSpiceRawRead
import ltspice

from si_prefix import si_parse

# LTC=SimCommander('./ltc/rc_ltspice0.asc')
LTC=SimCommander('./ltc/rc_ltspice1.net')
# LTC=SimCommander('./ltc/rc_ltspice3.net')
if len(LTC.netlist)==0:
    print('Fail to read the netlist file')

LTC.set_component_value('Rs', '1k')
LTC.set_component_value('CL', 1e-6)
Rs = si_parse(LTC.get_component_value('Rs'))
CL = si_parse(LTC.get_component_value('CL'))

tau = Rs*CL
wo = 1/tau
fo = wo/2/np.pi

#1.0 Transient Analysis
LTC.add_instruction(".tran 4ms")
LTC.run(run_filename='./ltc_run/runfile.net')
LTC.wait_completion()

data=LTSpiceRawRead('./ltc_run/runfile.raw')
print('Trance names are')
print(data.get_trace_names())
Tnames=data.get_trace_names()

ts=data.get_time_axis()*1e3 # in ms unit
ys=data.get_trace(Tnames[1]).get_wave(step=0)
xs=data.get_trace(Tnames[2]).get_wave()

data1=ltspice.Ltspice('./ltc_run/runfile.raw')
data1.parse()
ts1=data1.get_time()
ys1=data1.get_data('V(outp)')
xs1=data1.get_data('V(inp)s')

#2.0 AC analysis
LTC.add_instruction( ".ac dec 21 10 1meg" )

fname='./ltc_run/ac_runfile'
LTC.run(fname+'.net')
LTC.wait_completion()
data2=LTSpiceRawRead(fname+'.raw')

freq = np.real(data2.get_trace('frequency').get_wave())
mVo = np.abs(data2.get_trace('V(outp)').get_wave())
pVo = np.angle(data2.get_trace('V(outp)').get_wave())*180/np.pi


fig=plt.figure(figsize=(10,7))
ax1 = fig.add_subplot(2,1,1)
ax1.plot(ts,ys,color='tab:blue')
ax1.plot(ts,xs,color='cyan')
ax1.plot(ts1,ys1,color='red')
ax1.set_title('transient')

ax2 = fig.add_subplot(2,1,2)
ax2p = ax2.twinx()


ax2.set_title('Bode Plot')
ax2.plot(freq, 20*np.log10(mVo),'red')
ax2.set_xscale('log')
ax2.set_ylim(top=0, bottom=-60)
ax2.vlines(fo,ymin=-60, ymax=0,color='tab:red', linestyle='dotted')
ax2.hlines(-3,xmin=100, xmax=1e6, color='tab:red',linestyle='dotted')
ax2.text(fo,-3,'-3dB',ha='left',va='bottom', color='tab:red')

ax2p.plot(freq, pVo,'blue')
ax2p.set_ylabel('∠ $\mathcal{Vo}\degree$',color='tab:blue')
ax2p.tick_params(axis='y',labelcolor='tab:blue')
ax2p.set_ylim(top=0, bottom=-90)
ax2p.vlines(fo,ymin=-90, ymax=0, color='tab:blue',linestyle='dashed')
ax2p.hlines(-45,xmin=10,xmax=1e6, color='tab:blue', linestyle='dotted')
ax2p.text(fo,-45,"-45 $\degree$",ha='left',va='baseline', c='tab:blue')

plt.show()