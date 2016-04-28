# 2016.03.22 11:46:26 CET
# Embedded file name: /home/joris/tools/scripts/validation/barPlotter.py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn
import os

def plot(names, values, dir):
    os.chdir(dir)
    names = cleanNames(names)
    y_pos = np.arange(len(names))
    plt.barh(y_pos, values, align='center', alpha=0.8)
    plt.yticks(y_pos, names, linespacing=1)
    axes = plt.gca()
    axes.set_xlim([0, 100])
    plt.gcf().subplots_adjust(left=0.2)
    plt.xlabel('% of genes with H3K4me3 peak start')
    plt.title('H3K4me3 genes per annotation')
    plt.savefig('/home/joris/barplot.svg', format='svg', dpi=1200)


def cleanNames(names):
    out = []
    for i in names:
        out.append(i.replace('_intersections.bed', ''))

    return out


if __name__ == '__main__':
    names = ['test1', 'test2']
    nums = [5, 10]
    plot(names, nums, '/home/jsteenbrugge')
# okay decompyling barPlotter.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.03.22 11:46:26 CET
