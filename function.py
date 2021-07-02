def getData(ID):
    import pandas as pd
    import numpy as np
    link = "https://ressources.data.sncf.com/explore/dataset/" + ID + "/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B"
    df = pd.read_csv(link, sep=";")
    if(ID=="nombre-de-materiels-roulants-sncf-voyageurs-exploitables-par-serie-activite"):
        dd = df[['Année', 'Mois']]
        dd = dd.assign(day=np.ones(len(dd.index)))
        dd.columns = ["year", "month", "day"]
        df.assign(Date=pd.to_datetime(dd))
    else:
        for name in df.columns:
            if name.startswith('nombre'):
                df[name] = df[name].apply(pd.to_numeric)
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', exact=False)
    return df
