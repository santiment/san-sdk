import datetime
import pandas as pd
import numpy as np
import san
import matplotlib.pyplot as plt


def fancy_plot(df, left_metrics:list, right_metric=None, signals=None):
    ''' Quick visualization tool. '''
    fig, ax1 = plt.subplots(figsize=(18,9))
    for metric in left_metrics:
        p1, = ax1.plot(df.index, df[metric], label=metric, linewidth=2)
        plt.grid('x')
        plt.legend(loc='upper right', fontsize=14)

    ax2 = ax1.twinx()
    if right_metric:
        p1, = ax2.plot(df.index, df[right_metric], color='red', label=right_metric, linewidth=1.8)
        plt.legend(loc='upper left', fontsize=14)

    if signals:
        plt.vlines(
            signals, 
            df.min().min(),
            df.max().max(),
            color = '#424242', linewidth=1
        )
        

def get_san_metric(start, end, metric, asset, interval, iterate_over_days=120, convert_index=True):
    ''' Iterates over days and gets the metric data. '''
    start = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    end = datetime.datetime.strptime(end, '%Y-%m-%d').date()
    df = pd.DataFrame(None)

    for i in range(int(np.ceil((end - start).days / iterate_over_days))):
        start_date = str(start + datetime.timedelta(days=iterate_over_days * i))
        end_date = str(min(end, start + datetime.timedelta(days=iterate_over_days * (i + 1) - 1)))

        df_batch = san.get(
            f'{metric}/{asset}',
            from_date=start_date,
            to_date=end_date,
            interval=interval
        )
        df = df.append(df_batch)
        if convert_index:
            df.index = df.index.astype('datetime64[ns]')

    return df