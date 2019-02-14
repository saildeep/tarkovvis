import api
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import math
from collections import OrderedDict
ammoinfo = api.cached('ammo.json',api.get_ammo_info)
ammoinfo = pd.DataFrame(ammoinfo)
print(ammoinfo)
alltraders = list(filter(lambda x:x.startswith('Trader:'),list(ammoinfo.columns)))
print(alltraders)
categories = list(set(ammoinfo["category"]))
sqrtcats = math.ceil(math.sqrt(len(categories)))


russian_ar =plt.figure(0)
us_ar = plt.figure(0)
other = plt.figure(0)
pumpgun = plt.figure(0)
sniper = plt.figure(0)
russian_pistol_smg = plt.figure(0)
us_pistol_smg = plt.figure(0)
fig_lookup = {
    ".366_TKM_ammunition":russian_ar,
    "5.45x39mm_ammunition":russian_ar,
    "7.62x39mm_ammunition":russian_ar,
    "9x39mm_ammunition":other,
    "7.62x51mm_NATO_ammunition":us_ar,
    "5.56x45mm_NATO_ammunition":us_ar,
    "20x70mm_ammunition":pumpgun,
    "12x70mm_ammunition":pumpgun,
    "4.6x30mm_HK_ammunition":us_pistol_smg,
    "9x19mm_Parabellum_ammunition":us_pistol_smg,
    "7.62x54mmR_ammunition":sniper,
    "9x18mm_Makarov_ammunition":russian_pistol_smg,
    "9x21mm_Gyurza_ammunition":russian_pistol_smg,
    "7.62x25mm_Tokarev_ammunition":russian_pistol_smg


}
colmap = cm.get_cmap('Accent')
for categoryID in range(len(categories)):
    category = categories[categoryID]
    fig = fig_lookup[category]
    if fig is None:
        raise Exception()
    diagram = fig.gca()
    subset = ammoinfo[ammoinfo.category == category]
    diagram.set_title(category)
    xattr='penetration'
    yattr='damage'
    zattr='armor damage'
    subset[xattr] = pd.to_numeric(subset[xattr])
    subset[yattr] = pd.to_numeric(subset[yattr])

    traderCount = 0
    print(subset)
    for trader in alltraders:
        traderSubset = subset[subset[trader] == True]
        
        if(traderSubset.size>0):
            for i,row in traderSubset.iterrows():
                t = row['name']
                x = row[xattr]
                y = row[yattr]
                s = row[zattr]
                is_subsonic ='v' if row['velocity'] < 343 else '.'
           
                diagram.scatter(x,y,s=[s*4],label=categoryID,color=colmap(categoryID),marker=is_subsonic)

                xx = row[xattr]
                yy = row[yattr]
                diagram.annotate(t,(xx,yy),size=8,ha='left',va='bottom',rotation=30)

        traderCount +=1

    xmin = subset[xattr].min()
    xmax = subset[xattr].max()

    ymin = subset[yattr].min()
    ymax = subset[yattr].max()


    scaleX = .2 * (xmax - xmin)
    scaleY = .2 * (ymax - ymin)

    axes = fig.gca()
    #axes.set_xlim([xmin-scaleX,xmax+scaleX])
    #axes.set_ylim([ymin-scaleY,ymax+scaleY])

    axes.xlabel(xattr)
    axes.ylabel(yattr)


    handles, labels = fig.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
   

    fig.show(block=False)
    
    
    

plt.show()
