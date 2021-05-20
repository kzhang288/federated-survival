import pandas as pd

# calculates a cumulative count of the target column based on a date column
# first project only targets and date column
# collapse to remove duplicates

def get_cumulative(table, groupby, date, name, key=None):
    
    df = table.copy()
    start = df.shape[0]

    if type(groupby) is not list:
        groupby = [groupby]
    
    # collapse the dataframe based on keys
    if key is not None:
        if type(key) is not list:
            key = [key]
    temp = df.drop_duplicates(key)[groupby + [date]]

    # normal cumulative count hence disregards other values that should share position
    temp['temp1'] = temp.sort_values(by=date, ascending=True).groupby(groupby).cumcount() + 1 
    df = pd.concat([df, temp['temp1']], axis=1)

    # counts duplicates 
    temp = df.groupby(groupby+[date]).size().reset_index(name='temp2')
    df = pd.merge(df, temp, on=groupby+[date])

    # take max of duplicate and normal cumulative count 
    df[name] = df[['temp1', 'temp2']].max(axis=1)
    
    df = df.drop(columns=['temp1', 'temp2'])

    end = df.shape[0]
    print("lost: ", start - end)
    return df

def get_indicator(table, target, groupby, date, name, key=None):

    df = table.copy()
    start = df.shape[0]

    if type(groupby) is not list:
        groupby = [groupby]
    
    # collapse the dataframe based on keys
    if key is not None:
        if type(key) is not list:
            key = [key]
        df = df.drop_duplicates(key)

    # normal cumulative sum hence disregards other values that should share position
    df['temp1'] = df.sort_values(by=date, ascending=True).groupby(groupby)[target].cumsum()
    
    # counts positives 
    temp = df.loc[df.temp1 > 0].groupby(groupby+[date]).size().reset_index(name='temp2')

    df = pd.merge(df, temp, on=groupby+[date], how='left')
    
    # take max of duplicate and normal cumulative count 
    df[name] = df[['temp1', 'temp2']].max(axis=1) > 0
    
    df = df.drop(columns=['temp1', 'temp2'])

    end = df.shape[0]
    print("lost: ", start - end)
    return df
