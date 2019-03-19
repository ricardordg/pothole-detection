import matplotlib.pyplot as plt
import numpy as np 
import os
import math as math
import wavelet

path = "Medicoes ponte dia 07-02-2019/"
files_in_dir = []

wav_levels = 5
n_cortes = 3
fator = 4

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

    #ax.set_title("Wavelet nivel "+str(wav_levels)+" - "+str(n_cortes)+" cortes de threshold")
    ax.set_title(file_[:-4])
    ax.set_xlabel("Samples")
    ax.set_ylabel("(G)")

    ax.plot(cortes[0], label='$D_'+str(wav_levels)+'$')
    ax.plot(cortes[len(cortes) - 1], alpha=0.5, label='$D_'+str(wav_levels)+'$ - $\lambda_'+str(n_cortes)+'$', color='green')


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
    #plt.savefig(path + "atrous-"+file_[:-4]+"wav"+str(wav_levels)+".png",dpi=500)

    plt.close()