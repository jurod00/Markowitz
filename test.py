import numpy as np

from portfolio.portfolioShares import PortfolioShares
from plot.plotPortfolioShares import PlotPortfolioShares

import matplotlib.pyplot as plt
import matplotlib.path as mpath

def main():
    star = mpath.Path.unit_regular_star(6)
    circle = mpath.Path.unit_circle()
    # concatenate the circle with an internal cutout of the star
    cut_star = mpath.Path(
        vertices=np.concatenate([circle.vertices, star.vertices[::-1, ...]]),
        codes=np.concatenate([circle.codes, star.codes]))

    fig, ax = plt.subplots()
    fig.suptitle('Path markers', fontsize=14)
    fig.subplots_adjust(left=0.4)

    markers = {'star': star, 'circle': circle, 'cut_star': cut_star}

    for y, (name, marker) in enumerate(markers.items()):
        ax.text(-0.5, y, name, **text_style)
        ax.plot([y] * 3, marker=marker, **marker_style)
    format_axes(ax)
    plt.show()

from matplotlib.lines import Line2D
from matplotlib.markers import MarkerStyle
from matplotlib.transforms import Affine2D

text_style = dict(horizontalalignment='right', verticalalignment='center',
                  fontsize=12, fontfamily='monospace')
marker_style = dict(linestyle=':', color='0.8', markersize=10,
                    markerfacecolor="tab:blue", markeredgecolor="tab:blue")


def format_axes(ax):
    ax.margins(0.2)
    ax.set_axis_off()
    ax.invert_yaxis()


def split_list(a_list):
    i_half = len(a_list) // 2
    return a_list[:i_half], a_list[i_half:]
    


if __name__ == "__main__":
    main()