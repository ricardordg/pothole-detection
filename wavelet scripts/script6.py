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

    fig, ax = plt.subplots(1,1)

    #ax.set_title("Wavelet nivel "+str(wav_levels)+" - "+str(n_cortes)+" cortes de threshold")
    ax.set_title("TWH cascata - $D_{"+str(wav_levels)+"}$ $\lambda_1$ - " + file_[:-4])
    ax.set_xlabel("Amostras")
    ax.set_ylabel("(G)")

    ax.step(range(len(cortes[0])), cortes[0], label='$D_{'+str(wav_levels)+'}$', alpha=0.4 )
    ax.step(range(len(cortes[1])), cortes[1], label='$D_{'+str(wav_levels)+'}$ - $\lambda_1$', color='green')

    complementar = complementares[0]

    check_var = True
    for i, v in enumerate(complementar):
        if(v[0] != 0 and check_var):
            ax.scatter(v[1],v[0], s = 15, marker='x', color='black', label='Posicao do buraco')
            ax.text(v[1]+5,v[0], str(v[1]) + ', ' + str(v[0])[0:4])
            check_var = False
        elif v[0] != 0 and not check_var:
            ax.scatter(v[1],v[0], s = 15, marker='x', color='black')
            ax.text(v[1]+5,v[0], str(v[1]) + ', ' + str(v[0])[0:4])

    for i in xrange(len(sups)):
        draw_sup = [sups[i]] * len(cortes[0])
        draw_inf = [infs[i]] * len(cortes[0])

        if i == 0:
            ax.plot(draw_sup, linestyle='-.', color='red', label='$\lambda_{sup1}$',alpha=0.7)
            ax.plot(draw_inf, linestyle='-.', color='grey', label='$\lambda_{inf1}$', alpha=0.7)
        # else:
        #     ax.plot(draw_sup, linestyle='-.', color='red')
        #     ax.plot(draw_inf, linestyle='-.', color='grey')
        
    plt.legend()
    #plt.show()
    plt.savefig(path + "cascata-"+file_[:-4]+"wav"+str(wav_levels)+".png",dpi=500)

    plt.close()