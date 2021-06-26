#Librairie de fonctions

###############################################################
#
###############################################################
###############################################################
# Moments
###############################################################
def Moment_r(data,r):
    import functools
    data=[x for x in data] # transformation de données en liste
    fonc_r= lambda x : x**r
    S=functools.reduce( lambda x, y: x+y,map(fonc_r,data))
    return S/(1.0*len(data))

###############################################################
#Moments Centrés
###############################################################
def Moment_cr(data,r):
    data=[x for x in data] # transformation de données en liste
    import functools
    m=Moment_r(data,1)
    fonc_r= lambda x : (x-m)**r
    S=functools.reduce(lambda x, y: x+y,map(fonc_r,data))
    return S/(1.0*len(data))

###############################################################
# Mode(s) pour les données discrètes
###############################################################

def Mode_D(data):
    data=[x for x in data] # transformation de données en liste
    Dic={}
    for x in sorted(data):
        Dic[x]=data.count(x)
        
    Valeurs=[t for t in Dic.keys()]
    Effectifs=[t for t in Dic.values()]
    n_max=max(Effectifs)
    
    return [x for x in Valeurs if Dic[x]==n_max]


###############################################################
# Tester si les données sont discrètes ou continues
###############################################################

def discretes_continues(data):
       data=[x for x in data] # transformation de données en liste
       dic_donnees={}
       for x in sorted(data):
              dic_donnees[x]=data.count(x)

       valeurs=[k for k in dic_donnees.keys()]
       effectifs=[v for v in dic_donnees.values()]
       
       # test
       if max(effectifs) >1:
              return "discrete"
       else:
              return "continue"

###############################################################
# nombre d'occurrences pour les données discrètes
###############################################################
def comptage_occurrences(data):
    data1=[x for x in data] # transformation de données en liste (ordonnée)
    Dic_compt={}
    for valeur in data1:
        Dic_compt[valeur]=data1.count(valeur)
    return Dic_compt

       
###############################################################
# Histogramme des données discrètes
###############################################################

def histo_discretes(data,nom=None):

    # nom : le nom (sans extension)  pour la figure

    import datetime
    import numpy
    import matplotlib.pyplot as plt
    
    plt.rcParams['hatch.color'] = [0.9,0.9,0.9]
    
    
    D=comptage_occurrences(data)
    valeurs=[k for k in D.keys()]
    effectifs=[v for v in D.values()]
    
    i_mode=numpy.argmax(effectifs)  # indice max
    ### multi_mode
    indice_mode=[i for i in range(len(effectifs)) if effectifs[i]==effectifs[i_mode]]

    fig1 = plt.figure(figsize=(10,7))
    ax1 =fig1.add_subplot(111)
    # cacher le cadre (haut,bas , à gauche)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ##
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_ticks_position('left')
   
    ax1.set_yticks([])
    
    ax1.set_xticks(valeurs)  ## positions des extrémités des valeurs
    ax1.set_xticklabels(valeurs ,fontsize=10, rotation=25)
    ax1.set_xlabel("Valeurs",fontsize=13)
    ax1.set_ylabel("Effectifes",fontsize=13)
    
    for k in range(len(valeurs)):
        if k not in indice_mode:
            plt.bar(valeurs[k], height= effectifs[k],edgecolor="white")
        else:
            plt.bar(valeurs[k], height= effectifs[k],edgecolor="white",
                    color = [0.15,0.15,0.85],hatch="X", lw=1., zorder = 0)
        for i in range(len(valeurs)):
            ax1.text(valeurs[i], effectifs[i], "%d"%(effectifs[i]),fontsize=9,
                     horizontalalignment='center',verticalalignment='bottom',style='italic')

    # le nom de la figure va  porter la date du jour de création
    aujourdhui=datetime.datetime.today()
    jour="{}{}{}".format(aujourdhui.timetuple()[2],aujourdhui.timetuple()[1],aujourdhui.timetuple()[0])
    
    if nom is None:
        plt.show()
    else:
        nom_fig="{}_histo_{}.png".format(nom,jour)
        print(nom_fig)
        plt.savefig(nom_fig, format="png")
        plt.close()
            

###############################################################
# histogramme pour les Données Continues
###############################################################

def histo_Continue(data,k,nom=None):
    # k=nombre de classes
    # nom : le nom (sans extension)  pour la figure

    import datetime
    import numpy
    import matplotlib.pyplot as plt
    
    plt.rcParams['hatch.color'] = [0.9,0.9,0.9] # hachure
    
    
    data=numpy.array([x for x in data])
    Ext=[min(data)+(max(data)-min(data))*i/(1.0*k) for i in range(k+1)]
    
    C=[0.5*(Ext[i]+Ext[i+1]) for i in range(k)]  # Centres des classes

    NN=[] # Effectifs des classes
    for i in range(k):
        NN.append(((Ext[i] <= data) & (data<=Ext[i+1])).sum())
        
    # pour la classe modale
    indice_max=[i for i in range(k) if NN[i]==numpy.max(NN)]
    
    TT=[str("{:.4f}".format(t)) for t in Ext]  ## pour afficher les extrémités des classes

    CC=[str("{:.4f}".format(t)) for t in C]    ## pour afficher les centres des classes
    

    fig = plt.figure(figsize=(10,7))
    ax1 = fig.add_subplot(111)
    # cacher le cadre
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.xaxis.set_ticks_position('bottom')
    
    ax1.set_yticks([])
    largeur=Ext[1]-Ext[0]  #  largeur des classes
    
    for i in range(k):
        
        if i in indice_max: 
            ax1.bar(C[i], NN[i],largeur,  color = [0.15,0.15,0.80], edgecolor="white", hatch="/", 
                    lw=1., zorder = 0,alpha=0.9)
        else:
            ax1.bar(C[i], NN[i],largeur, align='center', edgecolor="white")
        
        ax1.text(C[i], NN[i], "%d"%(NN[i]),fontsize=8, style='italic', 
                 horizontalalignment='center',verticalalignment='bottom')

            
    #ax1.set_xticks(C)      ## positions des centres
    ax1.set_xticks(Ext)  ## positions des extrémités des classes
    
    ax1.set_xticklabels(TT ,fontsize=8, rotation=45)
    #ax1.set_xticklabels(CC ,fontsize=8, rotation=45)

    
    ax1.set_xlim(numpy.min(data)-0.75*largeur, numpy.max(data)+0.75*largeur)
    ax1.set_ylim(0.0, numpy.max(NN)+3.0)
    ax1.set_xlabel("Valeurs",fontsize=12)
    ax1.set_ylabel("Effectifs",fontsize=14)
    
    # le nom de la figure va  porter la date du jour de création
    aujourdhui=datetime.datetime.today()
    jour="{}{}{}".format(aujourdhui.timetuple()[2],aujourdhui.timetuple()[1],aujourdhui.timetuple()[0])
    
    if nom is None:
        plt.show()
    else:
        nom_fig="{}_histo_{}.png".format(nom,jour)
        print(nom_fig)
        plt.savefig(nom_fig, format="png")
        plt.close()
        
###########################################################################""

def histo_Continue_plotly(data,k,nom=None):
    # k=nombre de classes
    # nom : le nom (sans extension)  pour la figure

    import datetime
    import numpy
    import matplotlib.pyplot as plt
    from plotly.tools import mpl_to_plotly
    
    plt.rcParams['hatch.color'] = [0.9,0.9,0.9] # hachure
    
    
    data=numpy.array([x for x in data])
    Ext=[min(data)+(max(data)-min(data))*i/(1.0*k) for i in range(k+1)]
    
    C=[0.5*(Ext[i]+Ext[i+1]) for i in range(k)]  # Centres des classes

    NN=[] # Effectifs des classes
    for i in range(k):
        NN.append(((Ext[i] <= data) & (data<=Ext[i+1])).sum())
        
    # pour la classe modale
    indice_max=[i for i in range(k) if NN[i]==numpy.max(NN)]
    
    TT=[str("{:.4f}".format(t)) for t in Ext]  ## pour afficher les extrémités des classes

    CC=[str("{:.4f}".format(t)) for t in C]    ## pour afficher les centres des classes
    

    fig = plt.figure(figsize=(10,7))
    ax1 = fig.add_subplot(111)
    # cacher le cadre
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.xaxis.set_ticks_position('bottom')
    
    ax1.set_yticks([])
    largeur=Ext[1]-Ext[0]  #  largeur des classes
    
    for i in range(k):
        
        if i in indice_max: 
            ax1.bar(C[i], NN[i],largeur,  color = [0.15,0.15,0.80], edgecolor="white", hatch="/", 
                    lw=1., zorder = 0,alpha=0.9)
        else:
            ax1.bar(C[i], NN[i],largeur, align='center', edgecolor="white")
        
        ax1.text(C[i], NN[i], "%d"%(NN[i]),fontsize=8, style='italic', 
                 horizontalalignment='center',verticalalignment='bottom')

            
    #ax1.set_xticks(C)      ## positions des centres
    ax1.set_xticks(Ext)  ## positions des extrémités des classes
    
    ax1.set_xticklabels(TT ,fontsize=8, rotation=45)
    #ax1.set_xticklabels(CC ,fontsize=8, rotation=45)

    
    ax1.set_xlim(numpy.min(data)-0.75*largeur, numpy.max(data)+0.75*largeur)
    ax1.set_ylim(0.0, numpy.max(NN)+3.0)
    ax1.set_xlabel("Valeurs",fontsize=12)
    ax1.set_ylabel("Effectifs",fontsize=14)
    
    # le nom de la figure va  porter la date du jour de création
    aujourdhui=datetime.datetime.today()
    jour="{}{}{}".format(aujourdhui.timetuple()[2],aujourdhui.timetuple()[1],aujourdhui.timetuple()[0])
    
    plotly_fig = mpl_to_plotly(fig)
    
    if nom is None:
        plt.show()
    else:
        nom_fig="{}_histo_{}.png".format(nom,jour)
        print(nom_fig)
        plt.savefig(nom_fig, format="png")
        plt.close()
    return plotly_fig


