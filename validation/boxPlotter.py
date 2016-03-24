import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

def plot(df):
    plt.clf()
    sns.set(style="whitegrid", color_codes=True)
    np.random.seed(sum(map(ord, "categorical")))
    plt.ylabel('RPKM log2', fontsize=16)
    plot = sns.boxplot(x="Name", y="RPKM log2", data=df);
    plt.savefig("/home/joris/boxPlot.svg")
