import matplotlib.pyplot as plt
import numpy as np 
import os
import math as math
import wavelet

path = "Medicoes ponte dia 07-02-2019/"
files_in_dir = []

wav_levels = 10
n_cortes = 1
fator = 4



def shift(l, n):
    return l[n:] + l[:n]

for file_ in os.listdir(path):
    file_str = str(file_)
    if(file_str.endswith(".txt") or file_str.endswith(".csv")) and not file_str.endswith("readme.txt"):
        files_in_dir.append(file_)


for index, file_ in enumerate(files_in_dir):
    x,y,z = wavelet.readfile_xyz(path + file_, ' ')
    inicio, fim = wavelet.readfile_limits(path + file_, ' ')

    z = z[inicio:fim]

    c = []
    d = []

    c_temp = list(z)

    for i in xrange(wav_levels):
        ca_temp, cd_temp = wavelet.atrous_wavelet(c_temp)

        c.append(list(ca_temp))
        d.append(list(cd_temp))

        c_temp = ca_temp

    fac = math.ceil(9/2.0)
    fac = int(fac)

    last_c = list(c[wav_levels - 1])
    last_c = shift(last_c, -fac)

    new_z = []

    for i in xrange(len(last_c)):
        new_z.append(z[i] - last_c[i])

    new_c = []
    new_d = []
    new_c_temp = list(new_z)

    for i in xrange(wav_levels):
        ca_temp, cd_temp = wavelet.atrous_wavelet(new_c_temp)
        new_c.append(list(ca_temp))
        new_d.append(list(cd_temp))
        new_c_temp = ca_temp
    
    c_corte = list(new_c[wav_levels - 1])
    cortes = []
    cortes.append(list(c_corte))
    fator_local = fator
    sups = []
    infs = []
    complementares = []

    for i in xrange(n_cortes):
        lamb_sup, lamb_inf = wavelet.threshold(fator_local, c_corte)
        sups.append(lamb_sup)
        infs.append(lamb_inf)
        c_corte, complementar = wavelet.corte_e_complementar_atrous(lamb_sup, lamb_inf, c_corte)
        complementares.append(list(complementar))
        cortes.append(list(c_corte))
        fator_local = fator_local - 1
    
    fig, ax = plt.subplots(1,1)

    #ax.set_title("Wavelet nivel "+str(wav_levels)+" - "+str(n_cortes)+" cortes de threshold")
    ax.set_title(file_[:-4])
    ax.set_xlabel("Samples")
    ax.set_ylabel("(G)")

    ax.plot(c[0], alpha=0.3, label='z')
    ax.plot(last_c, alpha=0.5, label='last z')
    ax.plot(new_z, alpha=0.7,label='new z')
    ax.plot(cortes[0], label='corte 1', alpha=0.9)

    checkVar = False
    for i, v in enumerate(complementares[0]):
        if (v[0] != 0 and not checkVar):
            ax.scatter(v[1],v[0], s = 30, marker='x', color='black', label='Posicao do buraco')
            checkVar = True
        elif (v[0] != 0 and checkVar):
            ax.scatter(v[1],v[0], s = 30, marker='x', color='black')


    plt.legend()
    plt.show()
    break
    #plt.savefig(path + "atrous-"+file_[:-4]+"wav"+str(wav_levels)+".png",dpi=500)

    plt.close()