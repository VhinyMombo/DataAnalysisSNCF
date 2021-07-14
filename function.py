def getData(ID):
    import pandas as pd
    link = "https://ressources.data.sncf.com/explore/dataset/" + ID + "/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B"
    df = pd.read_csv(link, sep=";")
    for name in df.columns:
        if name.startswith('nombre'):
            df[name] = df[name].apply(pd.to_numeric)
    if ID == 'regularite-mensuelle-ter':
        df = df.drop(columns=["Commentaires"])
    elif ID == "regularite-mensuelle-intercites":
        df = df.drop(columns=["empty"])
    elif ID == "regularite-mensuelle-tgv-aqst":
        df = df.rename(columns={'Période': 'Date'})
        df = df.drop(columns=["Année",
                              "Mois",
                              "Commentaire (facultatif) annulations",
                              "Commentaire (facultatif) retards au départ",
                              "Commentaire (facultatif) retards à l'arrivée"])
    elif ID == "regularite-mensuelle-tgv-axes":
        df = df.rename(columns={'Période': 'Date'})
        df = df.drop(columns=["Année",
                              "Mois"])
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', exact=False)
    return df



def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    import pandas as pd
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.groupby(levels[i:]).sum()
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i + 1]].copy()
        else:
            df_tree['parent'] = 'total'
        df_tree['value'] = dfg[value_column]
        df_tree['color'] = dfg[color_columns[0]] / dfg[color_columns[1]]
        df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
    total = pd.Series(dict(id='total', parent='',
                           value=df[value_column].sum(),
                           color=df[color_columns[0]].sum() / df[color_columns[1]].sum()))
    df_all_trees = df_all_trees.append(total, ignore_index=True)
    return df_all_trees


def ecdf(tab):
    import numpy as np
    N = len(tab)
    X = np.sort(tab)
    F = np.array(range(N)) / float(N - 1)
    return X, F


def f_repartition(X, n=10):
    import numpy as np
    x_min, x_max = min(X), max(X)
    N = len(X)
    dx = (x_max - x_min) / N
    x_m, x_M = x_min - n * dx, x_max + n * dx
    F = []
    Xr = np.linspace(x_m, x_M, N + 2 * n)
    for x in Xr:
        F.append(sum(1.0 * (X < x)) / N)
    return Xr, F


def compute_MR(data):
    import numpy as np
    data_sort = np.sort(data)
    n = len(data)
    MR = []
    for i in range(1, len(data) + 1):
        MR.append((i - 0.3) / (n + 0.4))
    return data_sort, np.array(MR)


# Calcul les paramètres des lois de Weibull
# return un triplet contenant le paramètre a,b des loi de Weibull et l'erreur
def estimation_loi_weibull(data):
    import scipy.stats as st
    import numpy as np
    X, cdf = compute_MR(data)  # calcul la fonction de repartition
    cdf = cdf[X != 0]
    X = X[X != 0]
    lnX = np.log(X)
    Y = np.log(-np.log(1 - cdf))
    linreg = st.linregress(lnX, Y)
    a = linreg.slope
    b = np.exp(-linreg.intercept / a)
    err = np.power((Y - (linreg.intercept + linreg.slope * lnX)), 2)
    return a, b, np.sum(err)/len(err)


def ProbaDensityFunc(data, n=100):
    import numpy as np
    from scipy import stats
    bins = np.linspace(min(data), max(data), n)
    histogram, bins = np.histogram(data, bins=bins, density=True)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    pdf = stats.norm.pdf(bin_centers)
    return bin_centers, pdf, histogram


def weib(x, a, b):
    import numpy as np
    return (a / b) * (x / b) ** (a - 1) * np.exp(-(x / b) ** a)


def plotWeibParams(data, a, b):
    import numpy as np
    count, bins = np.histogram(data, density=True, bins=10)
    dx = (count.max() - bins.min()) / 100
    x = np.linspace(bins.min() + 5 * dx, bins.max() - 5 * dx, 100)
    scale = count.max() / weib(x, a, b).max()
    cdf = weib(x, a, b) * scale
    return x, cdf
