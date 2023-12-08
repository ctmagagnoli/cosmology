"""
NAME:
    Cosmology Analysis!
    
PURPOSE:
    Wrangle IllustrisTNG data to gain useful knowledge
    
REFERENCE:
    Christina Magagnoli
s
CALLING SEQUENCE:
    python3 "AGN.py"
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import datetime
from playsound import playsound
import math
#think this is good for what I'll need
#*******************************************************************************
starttime = datetime.datetime.now()
print("Started at",starttime)

f = open('AGN.txt','r')
AGN = f.readlines()
lum_range = []
f.close()
snapshot_ages = [.179, .271, .370, .418, .478, .517, .547, .596, .640, .687, .732, .764, .844, .932, .965, 1.036, 1.112, 1.177, 1.282, 1.366, 1.466, 1.540, 1.689, 1.812, 1.944, 2.145, 2.238, 2.384, 2.539, 2.685, 2.839, 2.981, 3.129, 3.285, 3.447, 3.593, 3.744, 3.902, 4.038, 4.206, 4.293, 4.502, 4.657, 4.816, 4.980, 5.115, 5.289, 5.431, 5.577, 5.726, 5.878, 6.073, 6.193, 6.356, 6.522, 6.692, 6.822, 6.998, 7.132, 7.314, 7.453, 7.642, 7.786, 7.932, 8.079, 8.280, 8.432, 8.587]

output = []
out2 = []
total = 0
agn44 = 0
merger44 = 0
agn2544 = 0
merger2544 = 0
agn344 = 0
merger344 = 0
agn4544 = 0
merger4544 = 0
agn5544 = 0
merger5544 = 0
agn644 = 0
merger644 = 0
agn7544 = 0
merger7544 = 0
agn8544 = 0
merger8544 = 0
agn9544 = 0
merger9544 = 0
agn45 = 0
merger45 = 0

for i in range(len(AGN)):
    line = AGN[i].strip()
    if not line.startswith('#'):
        li = line.split()
        snapnum = int(li[2])
        L_bol = float(li[3])
        M_BH = float(li[1])
        now = snapshot_ages[snapnum]
        last_merged = int(li[4])
        lum_range.append(L_bol)
        if last_merged > 0:
            merger_time = snapshot_ages[last_merged]
            time_since_merger = now - merger_time
        else:
            time_since_merger = now
        merger_ratio = float(li[5])
        if merger_ratio > 1:
            merger_ratio = 1/merger_ratio
            print(merger_ratio)
        elif merger_ratio == -99:
            merger_ratio = -.4
            print('sad')
        output.append((time_since_merger, L_bol,M_BH, merger_ratio))
    if L_bol >= 10**44 and L_bol < 2*10**44:
        agn44 +=1
        if time_since_merger < 1:
            merger44 += 1
    elif L_bol >= 2*10**44 and L_bol < 3*10**44:
        agn2544+= 1
        if time_since_merger < 1:
            merger2544 += 1
    elif L_bol >= 3*10**44 and L_bol < 4*10**44:
        agn344 += 1
        if time_since_merger < 1:
            merger344 += 1
    elif L_bol >= 4*10**44 and L_bol < 5*10**44:
        agn4544 += 1
        if time_since_merger < 1:
            merger4544 += 1
    elif L_bol >= 5*10**44 and L_bol < 6*10**44:
        agn5544 += 1
        if time_since_merger < 1:
            merger5544 += 1
    elif L_bol >= 6*10**44 and L_bol < 7*10**44:
        agn644 +=1
        if time_since_merger < 1:
            merger644 += 1
    elif L_bol >= 7*10**44 and L_bol < 8*10**44:
        agn7544 += 1
        if time_since_merger < 1:
            merger7544 += 1
    elif L_bol >= 8*10**44 and L_bol < 9*10**44:
        agn8544 += 1
        if time_since_merger <1:
            merger8544 += 1
    elif L_bol >= 9*10**44 and L_bol < 10**45:
        agn9544 += 1
        if time_since_merger < 1:
            merger9544 += 1
    elif L_bol >= 10**45:
        agn45 += 1
        if time_since_merger < 1:
            merger45 += 1
out2.append((1.5,float(merger44/agn44)))
out2.append((2.5, float(merger2544/agn2544)))
out2.append((3.5, float(merger344/agn344)))
out2.append((4.5, float(merger4544/agn4544)))
out2.append((5.5, float(merger5544/agn5544)))
out2.append((6.5, float(merger644/agn644)))
out2.append((7.5, float(merger7544/agn7544)))
out2.append((8.5, float(merger8544/agn8544)))
out2.append((9.5, float(merger9544/agn9544)))
out2.append((10.5, float(merger45/agn45)))

out2np = np.array(out2)
sf2 = open('hist_output','wb')
np.savetxt('hist_output',out2np,fmt='%s')
sf2.close()

final = np.array(output)
savefile = open('output', 'wb')
np.savetxt('output', final, fmt='%s')
savefile.close()

print(math.log10(max(lum_range)),math.log10(min(lum_range)))



