#2020-08-18 12:28
#0, use awk to pre-process the BAND_S**_A****.OUT to CHOOSE BANDS NEED. After process data should be like: data[:,0]=kpt, data[:,1], data[:,3] ... is the energy; data[:, 2], data[:, 4]... is the spin or l,m projections. 
#1, this script is to make the line with weight by color.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcoll
import pandas as pd
from matplotlib.collections import LineCollection

def multicolored_lines():


    #df_pt=pd.read_table("Mo_new.dat", sep="\s+", usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], header=None)
    df_pt=pd.read_table("Mo_new.dat", sep="\s+", header=None)
    #df_pt.columns=['kp', 'E0', 'w0', 'E1', 'w1', 'E2', 'w2', 'E3', 'w3', 'E4', 'w4', 'E5', 'w5', 'E6', 'w6', 'E7', 'w7']

    x = df_pt.iloc[:,0]
#    YY = [df_pt.iloc[:,i] for i in range(1,16,2)]
#    ZZ = [df_pt.iloc[:,j] for j in range(2,17,2)]
    fig, ax = plt.subplots(figsize=(16,10))
    #lc = [colorline(x, YY[i], ZZ[i], cmap='bwr') for i in range(0,8,1)]
    lc = [colorline(x, df_pt.iloc[:,i], df_pt.iloc[:,i+1], cmap='bwr') for i in range(1,16,2)]
    #lc0 = colorline(x, y0, z0, cmap='bwr')
    #lc1 = colorline(x, y1, z1, cmap='bwr')
    #lc2 = colorline(x, y2, z2, cmap='bwr')
    #lc3 = colorline(x, y3, z3, cmap='bwr')
    #lc4 = colorline(x, y4, z4, cmap='bwr')
    #lc5 = colorline(x, y5, z5, cmap='bwr')
    #lc6 = colorline(x, y6, z6, cmap='bwr')
    #lc7 = colorline(x, y7, z7, cmap='bwr')

    

    plt.colorbar(lc[0])
    plt.xlim(x.min(), x.max())
    plt.xticks([0.0, 0.583, 1.256, 1.593], ['M', '$\Gamma$', 'K', 'M'], fontsize=26)
    ax.tick_params(direction='in')
    plt.ylim(df_pt.iloc[:,1].min()-0.005, df_pt.iloc[:,15].max()+0.005)

    #line_segments = LineCollection([np.column_stack([x, y]) for y in YY],
    line_segments = LineCollection([np.column_stack([x, df_pt.iloc[:,i]]) for i in range(1,16,2)],
                               linewidth=0.02, #linewidths=(0.5, 1, 1.5, 2),
                               linestyles='solid')
    line_segments.set_array(x)
    ax.add_collection(line_segments)
    #axcb = fig.colorbar(line_segments)
    #axcb.set_label('Line Number')
    #ax.set_title('Line Collection with mapped colors')
    plt.sci(line_segments)  # This allows interactive changing of the colormap.
    subtitlefont = {'family': 'serif',
        'color':  'black', #'darkred',
        'weight': 'normal',
        'size': 16,
        }   


    plt.title("red for up, and blue for down of Mo", loc='center', fontdict=subtitlefont)

    #import matplotlib
    #matplotlib.use('ps')
    #from matplotlib import rc
    #rc('text',usetex=True)
    #rc('text.latex', preamble='\usepackage{color}')

    #import matplotlib as matplotlib
    #from matplotlib import rc
    #matplotlib.use('pgf')
    #matplotlib.rc('pgf', texsystem='pdflatex')  # from running latex -v
    #preamble = matplotlib.rcParams.setdefault('pgf.preamble', [])
    #preamble.append(r'\usepackage{color}')
    #plt.title(r'\textcolor{red}{red for up spin }'+r'\textcolor{blue}{blue for down spin}'+r' of W', fontsize=16)
    plt.suptitle("MoSe2/WSe2 bands", x=0.45, fontsize=32)

    #plt.text(0.45, 1, 'the third line', fontsize=13, ha='center')
    plt.ylabel("Energy (au)", fontsize=26)
    plt.savefig("Mo_test.png")
    #plt.show()


def colorline(
        x, y, z, cmap='bwr', norm=plt.Normalize(-1.0, 1.0),
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
    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
                              linewidth=linewidth, alpha=alpha)

    ax = plt.gca()
    ax.add_collection(lc)

    return lc

def make_segments(x, y):

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments

multicolored_lines()
