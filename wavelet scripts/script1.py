# TWH a trous - 1 arquivo - N niveis e M cortes
# Autor: Ricardo Silveira Rodrigues

import matplotlib.pyplot as plt
import numpy as np 
import os
import math as math
import wavelet

path = "Medicoes ponte dia 07-02-2019/"
file_name = "ida27.txt"
wav_levels = 5
n_cortes = 3
fator = 4

x,y,z = wavelet.readfile_xyz(path + file_name, ' ')

#z = z[524:1100]

c = []
d = []

c_temp = list(z)

for i in xrange(wav_levels):
    ca_temp, cd_temp = wavelet.atrous_wavelet(c_temp)

    c.append(list(ca_temp))
    d.append(list(cd_temp))

    c_temp = ca_temp

#ultimo nivel
c_corte = c[wav_levels - 1]
cortes = []
cortes.append(list(c_corte))
fator_local = fator
sups = []
infs = []

for i in xrange(n_cortes):
    lamb_sup, lamb_inf = wavelet.threshold(fator_local, c_corte)
    sups.append(lamb_sup)
    infs.append(lamb_inf)
    c_corte = wavelet.corte_e_complementar_atrous(lamb_sup, lamb_inf, c_corte)[0] # soh pega o sinal cortado, sem complementar
    cortes.append(list(c_corte))
    fator_local = fator_local - 1

fig, ax = plt.subplots(1,1)

ax.set_title("Wavelet nivel "+str(wav_levels)+" - "+str(n_cortes)+" cortes de threshold")
ax.set_xlabel("Samples")
ax.set_ylabel("(G)")

#ax.plot(z, label='z')
ax.plot(cortes[0], label='$D_'+str(wav_levels)+'$')
#ax.plot(cortes[len(cortes) - 1], alpha=0.75, label='$D_'+str(wav_levels)+'$ - $\lambda_'+str(n_cortes)+'$', color='green')


for i in xrange(len(sups)):
    draw_sup = [sups[i]] * len(cortes[0])
    draw_inf = [infs[i]] * len(cortes[0])

    if i == 0:
        ax.plot(draw_sup, linestyle='-.', color='red', label='$\lambda_{sup}$')
        ax.plot(draw_inf, linestyle='-.', color='grey', label='$\lambda_{inf}$')
    else:
        ax.plot(draw_sup, linestyle='-.', color='red')
        ax.plot(draw_inf, linestyle='-.', color='grey')
    
plt.legend()
plt.show()

plt.close()
