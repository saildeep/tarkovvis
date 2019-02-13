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
for categoryID in range(len(categories)):
    category = categories[categoryID]
    fig = plt.figure()
    diagram = plt.subplot(1,1,1)
    subset = ammoinfo[ammoinfo.category == category]
    diagram.set_title(category)
    xattr='penetration'
    yattr='damage'

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
                is_subsonic ='v' if row['velocity'] < 343 else '.'
                print(is_subsonic)
                diagram.scatter(x,y,label=trader,marker=is_subsonic)

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

    axes = plt.gca()
    axes.set_xlim([xmin-scaleX,xmax+scaleX])
    axes.set_ylim([ymin-scaleY,ymax+scaleY])

    plt.xlabel(xattr)
    plt.ylabel(yattr)


    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
   

    plt.show(block=False)
    
    
    

plt.show()
