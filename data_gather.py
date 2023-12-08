"""
NAME:
    Cosmology Project!
    
PURPOSE:
    Wrangle IllustrisTNG and hope the data spits out useful knowledge
    
REFERENCE:
    Christina Magagnoli

CALLING SEQUENCE:
    python3 "take2.py"
"""
import illustris_python as il
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import datetime
from playsound import playsound
#think this is good for what I'll need
#*******************************************************************************
starttime = datetime.datetime.now()
print("Started at",starttime)
basePath = '/media/christina/Ilos/TNG100/output'
#shID = 3127
AGN = []
x = []
sn = 59
while sn < 68:
    x.append(sn)
#    sub = il.groupcat.loadSingle(basePath, sn, subhaloID=shID)
    group = il.groupcat.loadSubhalos(basePath, sn, fields = ['SubhaloBHMass','SubhaloBHMdot','SubhaloMass','SubhaloMassType'])
    fields = ['SubhaloMass','SubfindID','SnapNum', 'SubhaloID','NextProgenitorID','MainLeafProgenitorID','FirstProgenitorID','SubhaloMassType','DescendantID','SubhaloIDRaw']
    #subs = il.groupcat.loadSubhalos(basePath, sn, fields = ['SubhaloBHMass', 'SubhaloBHMdot','SubhaloFlag'])
    black_holes = il.snapshot.loadSubset(basePath, sn, 5, fields=['BH_Mass', 'BH_Mdot', 'ParticleIDs'])
    total = len(black_holes['ParticleIDs'])
    print("There are",total,"Black Holes")
    for i in range(1,total):
        snapshot = -99
        mr = -99
        this_subhalo = il.snapshot.loadSubhalo(basePath, sn, i, 5, fields=['BH_Mass', 'BH_Mdot', 'ParticleIDs'])
        try:
            mdot_bh = this_subhalo['BH_Mdot']
        except KeyError:
            mdot_bh = [0]
        L_bol = .1*mdot_bh[0]*(29979245800**2)*(2*10**37)/(975*31536000)
        if L_bol > 10**44: #should be 10^44...
            bhid = this_subhalo['ParticleIDs'][0]
            present = il.snapshot.loadSubset(basePath, 99, 5, fields=['ParticleIDs','Coordinates'])
            for k in range(len(present['ParticleIDs'])):
                if int(present['ParticleIDs'][k]) == bhid:
                    found = k
                    coords = present['Coordinates'][found]
                    subhalos = il.groupcat.loadSubhalos(basePath, 99, fields=['SubhaloPos','SubhaloCM'])
                    print(coords,subhalos['SubhaloPos'][0],subhalos['SubhaloCM'][0])
                else:
                    pass
            shID = i
            GroupFirstSub = il.groupcat.loadHalos(basePath,sn,fields=['GroupFirstSub'])
            tree = il.sublink.loadTree(basePath,sn,shID,fields=fields,onlyMPB=True)
            try:
                plt.plot(tree['SnapNum'],tree['SubhaloMass'],'-',label=bhid)
                tree = il.sublink.loadTree(basePath,sn,shID,fields=fields)
                numMergers, merger_snapnums, mass_ratios = il.sublink.numMergers(tree)

                for j in range(len(merger_snapnums)):
                    plt.arrow(merger_snapnums[j],600,0,-600)
                    snapshot = merger_snapnums[0]
                    mr = mass_ratios[0]
                plt.yscale('log')
                plt.xlabel('Snapshot Number')
                plt.ylabel('Total Subhalo Mass [code units]')
                plotname = str(this_subhalo['ParticleIDs'][0])+'_'+str(sn)+'_mass.png'
                plt.savefig(plotname)
                plt.clf()
            except TypeError or IndexError:
                pass
            AGN.append((str(this_subhalo['ParticleIDs'][0]),this_subhalo['BH_Mass'][0],sn,L_bol,snapshot,mr))#,this_subhalo['

            #except ValueError:
            #    pass

    print('Finished snap',sn,'at',datetime.datetime.now())
    sn += 1

savearray = np.array(AGN)
savefile = open('AGN.txt','wb')
np.savetxt('AGN.txt',savearray,fmt='%s')
savefile.close()

playsound('garrus-awaitingorders.mp3')
print("Done at",datetime.datetime.now(),"Total Runtime is",(datetime.datetime.now()-starttime))

