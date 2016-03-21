#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import seaborn
import os


def plot(names, values, dir):
	os.chdir(dir)
	y_pos = np.arange(len(names))
	plt.bar(y_pos, values, align='center', alpha = 0.8)
	plt.xticks(y_pos, names)
	plt.ylabel('No. of H3K4me3 genes')
	plt.title('H3K4me3 genes per bed file')
	plt.savefig('barplot.svg', format='svg', dpi=1200)
