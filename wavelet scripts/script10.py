import matplotlib.pyplot as plt
import numpy as np 
import os
import math as math
import wavelet

path = "Medicoes ponte dia 07-02-2019/"
files_in_dir = []

wav_levels = 2
n_cortes = 3
fator = 4

for file_ in os.listdir(path):
    file_str = str(file_)
    if(file_str.endswith(".txt") or file_str.endswith(".csv")) and not file_str.endswith("readme.txt"):
        files_in_dir.append(file_)







fig, ax = plt.subplots(1,1)

ax.set_title("Todas posicoes de buracos detectados usando TWH cascata $D_{" + str(wav_levels)+"}$ e $\lambda_1$ - Volta")
ax.set_xlabel("Amostras")
ax.set_ylabel("(G)")

list_of_hits = []
count = 0

for index, file_ in enumerate(files_in_dir):
    x,y,z = wavelet.readfile_xyz(path + file_, ' ')
    inicio, fim = wavelet.readfile_limits(path + file_, ' ')

    z = z[inicio:fim]

    c = []
    d = []

    d_temp = list(z)

    for i in xrange(wav_levels):
        ca_temp, cd_temp = wavelet.cascade_wavelet(d_temp)

        c.append(list(ca_temp))
        d.append(list(cd_temp))

        d_temp = cd_temp

    #ultimo nivel
    d_corte = c[wav_levels - 1]
    cortes = []
    cortes.append(list(d_corte))
    fator_local = fator
    sups = []
    infs = []
    complementares = []

    for i in xrange(n_cortes):
        lamb_sup, lamb_inf = wavelet.threshold(fator_local, d_corte)
        sups.append(lamb_sup)
        infs.append(lamb_inf)
        d_corte, complementar = wavelet.corte_e_complementar_cascade(lamb_sup, lamb_inf, d_corte)
        complementares.append(list(complementar))
        cortes.append(list(d_corte))
        fator_local = fator_local - 1

    complementar = complementares[0]

    for i, v in enumerate(complementar):
        if(v[0] != 0) and file_.startswith('volta'):
            ax.scatter(v[1],v[0], s = 15, marker='x', color='red')
            tu = (v[1],v[0])
            list_of_hits.append(tu)
            count+=1

t = list_of_hits[0]
ax.scatter(t[0],t[1], s = 15, marker ='x', color='red', label='hit')
plt.legend()
plt.gcf().text(0.01, 0.95, "Total: "+str(count) +" hits", fontsize=12)
plt.gcf().text(0.01, 0.90, "18 arquivos", fontsize=12)
plt.show()
plt.close()
        