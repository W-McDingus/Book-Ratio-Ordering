#!/usr/bin/env python3
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sys.dont_write_bytecode = True
sys.path.insert(0, "../lib")
sys.path.insert(0, "/Users/Weston/code/lib")
sys.dont_write_bytecode = True
from botconfigparser import BotConfigParser
from logger import LOGINIT,LOG,LOGE

def analyze_data(row):
    LOG('PROC: running book ratio ordering analysis')
    bookratios = [col for col in row.index.tolist() if 'bookratio' in col]
    x,y,z = row[bookratios[0]], row[bookratios[1]], row[bookratios[2]]
    if (x < y) and (y < z): #xyz
        return 0
    elif (y < x) and (x < z): #yxz
        return 1
    elif (x < z) and (z < y): #xzy
        return 2
    elif (y < z) and (z < x): #yzx
        return 3
    elif (z < x) and (x < y): #zxy
        return 4
    elif (z < y) and (y < x): #zyx
        return 5

def load_data(path, depth):
    LOG('LOAD: loading data into pandas dataframe')
    df = pd.read_csv(path + 'bitcoinity_data_{0}_pct.csv'.format(depth), engine='c')
    return df

def clean_data(df):
    LOG('PROC: cleaning raw data in dataframe')
    df[['asks', 'bids','price']] = df[['asks', 'bids','price']].apply(pd.to_numeric)
    df.index = pd.to_datetime(df['Time'])
    del df['Time']
    return df

def process_data(df, depth):
    LOG('PROC: producing bid/ask pct')
    df['bookratio_{0}_pct'.format(depth)] = np.log(df['bids'] / df['asks'])
    return df

def combine_dfs(dfs, depths):
    LOG('PROC: combining all bookratio dataframes into one')
    df = dfs[0]
    for i in range(1, len(depths)):
        depth = depths[i]
        df = df.join(dfs[i]['bookratio_{0}_pct'.format(depth)], on='Time')
    df.index = df.index.strftime('%Y%m%d%H%M%S')
    return df

def plot_color(row):
    order = row['order']
    num2color = {0:"green",1:"blue", 2:"blue", 3:"blue", 4:"blue", 5:"red"}
    return num2color[order]

def plot_analysis(df):
    colors = df.apply (lambda row: plot_color(row), axis=1)
    fig = go.Figure(data=go.Scatter(x=df.index, y=df['price'], mode='lines+markers',
            marker=dict(
            color=colors,
            line_width=1)
            ))
    fig.show()

if __name__ == '__main__':
    LOGINIT('bookratios')
    full_cfg = BotConfigParser()
    full_cfg.loadcfg()
    cfg = full_cfg.getsection('process')
    depths = sorted([int(item) for item in cfg['depths'].split(',')])
    bookratio_dfs = []
    for depth in depths:
        LOG('INFO: begin depth:' + str(depth))
        raw_data_df = load_data(cfg['datapath'], depth)
        cleaned_data_df = clean_data(raw_data_df)
        bookratio_df = process_data(cleaned_data_df, depth)
        bookratio_dfs.append(bookratio_df)
    analysis_df = combine_dfs(bookratio_dfs, depths)
    analysis_df['order'] = analysis_df.apply(lambda row: analyze_data(row), axis=1)
    LOG('OUT: saving analysis dataframe as CSV to path:', cfg['output'])
    buy_sell_signals = analysis_df['order'].tolist()
    print('Signals:\n', buy_sell_signals[-10:])
    analysis_df.to_csv(cfg['output'] + 'bookratios_analysis.csv')

