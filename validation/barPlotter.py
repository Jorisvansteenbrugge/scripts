#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import seaborn
import os


def plot(names, values, dir):
        os.chdir(dir)
        
        y_pos = np.arange(len(names))
	plt.bar(y_pos, values, align='center', alpha = 0.8)
	plt.xticks(y_pos, names)
	plt.ylabel('% of genes with H3K4me3 peak start')
	plt.title('H3K4me3 genes per annotation')
	plt.savefig('barplot.svg', format='svg', dpi=1200)


if __name__ == "__main__":
    names = ["test1", "test2"]
    nums = [5,10]
    plot(names, nums, "/home/jsteenbrugge")
