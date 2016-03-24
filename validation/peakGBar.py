import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns

df = pd.read_csv("/home/joris/degroteswagfile", sep ="\t")
sns.set_style("whitegrid")
sns.barplot(x="bed",y="h3",data=df, hue="peak")
matplotlib.pyplot.savefig("/home/joris/barPlotNEW.svg")
