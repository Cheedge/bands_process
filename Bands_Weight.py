# sys used in readdata()
import sys
# used for check file exist
import os.path
from os import path
# use pandas to read data
import pandas as pd
# used in plot
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcoll
from matplotlib.collections import LineCollection

# calculate time cost
import timeit
start_time= timeit.default_timer()


def process_data():
    # read "filename" and BANDLINES.OUT, if spin bands, or l,m bands read from input.
    if len(sys.argv) == 1:
        print ("Band with weight should give this filename, if only bands don't give anything just enter:")
        filename = input("Enter Filename: ")
    else:
        filename = sys.argv[1]

    # need Nb(num of bands), Nkp(num of kpoints), Nhk(num of high sysmetry points).
    print ("Please give the high sysmetry kpoints number Nhk, number of kpoints Nkp, and the number of bands Nb:")
    Nhk = 4 #int(input("Enter Nhk: "))
    Nkp = 300 #int(input("Enter Nkp: "))
    Nb  = 348 #int(input("Enter Nb: "))

    #if filename == None:
    #    df_bands = pd.read_table("BAND.OUT", sep="\s+", header=None)
    #else:
    #    df_bands = pd.read_table(filename, sep="\s+", usecols=[0,1], header=None)
    #    df_weight = pd.read_table(filename, sep="\s+", usecols=[2,3], header=None)

    df_bands = pd.read_table(filename, sep="\s+", usecols=[0,1], header=None)
    df_weight = pd.read_table(filename, sep="\s+", usecols=[2,3], header=None)

    if path.exists("BANDLINES.OUT"):
        df_highsysp = pd.read_table("BANDLINES.OUT", sep="\s+", usecols=[0], header=None)
        # pass high sysmetry points to list hk
        hk = [df_highsysp.iloc[i,0] for i in range(0,2*Nhk,2)]
    
    # pass the data to variables.
    x = df_bands.iloc[0:Nkp,0]
    # loop over every block of kpts
    y = []
    w = []
    for j in range(0,(Nb-1)*Nkp+1,Nkp):
        y.append(df_bands.iloc[j:j+Nkp,1])
        z1= df_weight.iloc[j:j+Nkp,0]
        z2= df_weight.iloc[j:j+Nkp,1]
        # process data: like spin up - spin downas the w (weight).
        z=[a_i - b_i for a_i, b_i in zip(z1, z2)]
        w.append(z)

    #check data
    #print (type(hk))
    #with open('checkfile.dat', 'w') as f:
    #    for item in w:
    #        f.write("%s\n" % item)
    #f.close()

    return x, y, w, Nb, hk, Nhk
#process_data()

def bands_weights():

    x, y, w, Nb, hk, Nhk = process_data()
    kpt = x
    Energy = y
    Weight = w

    print ("if choose several bands please input the order number of bands (same as xmgrace number):")
    try:
        Nb1  = int(input("Enter Nb1: "))
    except ValueError:
        Nb1 = 1
    try:
        Nb2  = int(input("Enter Nb2: "))
    except ValueError:
        Nb2=Nb

    fig, ax = plt.subplots(figsize=(16,10))
    #wl = [weightline(kpt, Energy[i], Weight[i], cmap='bwr') for i in range(0,Nb,1)]
    wl = [weightline(kpt, Energy[i], Weight[i], cmap='bwr') for i in range(Nb1-1,Nb2,1)]


    # make the color lines: line_segments = LineCollection([np.column_stack([x, y]) for y in YY],
    #line_segments = LineCollection([np.column_stack([kpt, Energy[i]]) for i in range(0,Nb,1)],
    line_segments = LineCollection([np.column_stack([kpt, Energy[i]]) for i in range(Nb1-1,Nb2,1)],
                               linewidth=1, #linewidths=(0.5, 1, 1.5, 2),
                               linestyles='solid')
    line_segments.set_array(x)
    ax.add_collection(line_segments)

    plt.sci(line_segments)  # This allows interactive changing of the colormap.

##### these section all the window settings like axis, lable, ticks, titles#######
    plt.colorbar(wl[0])
    plt.xlim(kpt.min(), kpt.max())
 #   plt.xlim(hk[0], hk[3])
    plt.xticks(hk, ['M', '$\Gamma$', 'K', 'M'], fontsize=26)
    ax.tick_params(direction='in')
    [plt.axvline(x=hk[i]) for i in range(0,Nhk,1)]
    #plt.axvline(x=hk[0])
    #plt.axvline(x=hk[1])
    #plt.axvline(x=hk[2])
    #plt.axvline(x=hk[3])

    # Here can change the y limit to adjust the window to see different energy range bands.
    #plt.ylim(Energy[0].min(), Energy[-1].max())
    #plt.ylim(Energy[Nb1-1].min(), Energy[Nb2-1].max())
    plt.ylim(-0.1, 0.1)

    subtitlefont = {'family': 'serif',
        'color':  'black', #'darkred',
        'weight': 'normal',
        'size': 16,
        }   

    plt.title("red for up, and blue for down of Mo", loc='center', fontdict=subtitlefont)

    plt.suptitle("MoSe2/WSe2 bands", x=0.45, fontsize=32)

    plt.ylabel("Energy (au)", fontsize=26)
    plt.savefig("Mo_all.png")
    #plt.show()
#################################################################################


def weightline(x, y, z, cmap='bwr', norm=plt.Normalize(-1.0, 1.0),
        linewidth=5, alpha=1.0):

    # Default colors equally spaced on [0,1]:
    #if z is None:
    #    z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    # to check for numerical input -- this is a hack
    #if not hasattr(z, "__iter__"):
    #    z = df_pt.w
    
    z = np.asarray(z)

    segments = make_segments(x, y)
    wl = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
                              linewidth=linewidth, alpha=alpha)

    ax = plt.gca()
    ax.add_collection(wl)

    return wl

def make_segments(x, y):

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments

bands_weights()

# calculate time cost
stop_time = timeit.default_timer()
print ("total time cost: %lf s" % (stop_time - start_time))
#print ("total time cost: ", stop_time - start_time)
