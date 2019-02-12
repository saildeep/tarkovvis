import api
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import math
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
        x = traderSubset[xattr]
        y = traderSubset[yattr]
        if(traderSubset.size>0):
            diagram.scatter(x,y,label=trader)
        traderCount +=1

    for i, row in subset.iterrows():
        t = row['name']
        xx = row[xattr]
        yy = row[yattr]
        diagram.annotate(t,(xx,yy),size=8,ha='left',va='bottom',rotation=30)
    
    xmin = subset[xattr].min()
    xmax = subset[xattr].max()

    ymin = subset[yattr].min()
    ymax = subset[yattr].max()

    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])

    plt.xlabel(xattr)
    plt.ylabel(yattr)
    diagram.legend()
    plt.show(block=False)
    
    
    

plt.show()
