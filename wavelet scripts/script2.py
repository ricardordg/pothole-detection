# TWH a trous - 2 graficos, d1 com e sem truncamento
# Autor: Ricardo Silveira Rodrigues

import matplotlib.pyplot as plt
import numpy as np 
import os
import math as math
import wavelet

path = "dados23janeiro/"
file_name = "ida2.txt"
wav_levels = 5
n_cortes = 2
fator = 4

x,y,z = wavelet.readfile_xyz(path + file_name, ' ')

z = z[672:1208] #ida2
#z = z[660:1320] #ida1
#z = z[592:900] #ida3

c = []
d = []

c, d = wavelet.cascade_wavelet(z)

cortes = []
cortes.append(list(d))
fator_local = fator
sups = []
infs = []

c_corte = d

for i in xrange(n_cortes):
    lamb_sup, lamb_inf = wavelet.threshold(fator_local, d)
    sups.append(lamb_sup)
    infs.append(lamb_inf)
    c_corte = wavelet.corte_e_complementar_atrous(lamb_sup,lamb_inf, c_corte)[0]
    cortes.append(list(c_corte))

    if(fator_local > 1):
        fator_local = fator_local - 1


fig, ax = plt.subplots(2,1)

# Grafico cima
ax[0].set_title("Standard deviation Threshold in $D_1$ signal - Lap 1",fontsize=15)
ax[0].set_xlabel("samples",fontsize=15)
ax[0].set_ylabel("(g)",fontsize=15)
ax[0].xaxis.set_tick_params(labelsize=15)
ax[0].yaxis.set_tick_params(labelsize=15)

ax[0].step(range(len(cortes[0])),cortes[0], label='Detail $D_1$')

draw_sup = [sups[0]] * len(cortes[0])
draw_inf = [infs[0]] * len(cortes[0])
ax[0].plot(draw_sup, linestyle='-.', label="$\lambda_{sup}$", color='green')
ax[0].plot(draw_inf, linestyle='-.', label="$\lambda_{inf}$", color='grey')

ax[0].legend(prop={'size': 15},shadow=True, fancybox=True,loc=1, framealpha=0.75)


# Grafico baixo
ax[1].set_xlabel("samples",fontsize=15)
ax[1].set_ylabel("(g)",fontsize=15)
ax[1].xaxis.set_tick_params(labelsize=15)
ax[1].yaxis.set_tick_params(labelsize=15)

ax[1].step(range(len(cortes[1])),cortes[1], label='Detail $D_1$')

draw_sup2 = [sups[1]] * len(cortes[0])
draw_inf2 = [infs[1]] * len(cortes[0])

ax[1].plot(draw_sup2, linestyle='-.', label="$\lambda_{sup}$", color='green')
ax[1].plot(draw_inf2, linestyle='-.', label="$\lambda_{inf}$", color='grey')

ax[1].legend(prop={'size': 15},shadow=True, fancybox=True,loc=1,  framealpha=0.75)



plt.tight_layout()
plt.show()
