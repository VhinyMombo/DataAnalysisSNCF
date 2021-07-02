def getData(ID):
    import pandas as pd
    link = "https://ressources.data.sncf.com/explore/dataset/" + ID + "/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B"
    df = pd.read_csv(link, sep = ";")
    for name in df.columns:
        if  name.startswith('nombre'):
            df[name] = df[name].apply(pd.to_numeric)
    #df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d',exact = False)
    return df
