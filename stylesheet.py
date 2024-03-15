import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns

### Stylesheet. Contrast with https://matplotlib.org/stable/users/explain/customizing.html#the-matplotlibrc-file
def customize_matplotlib_rcParams():
    """_summary_

    Args:
        _arg_ (_type_): _description_

    Returns:
        _type_: _description_
        
    Examples:
    --------------
    # Apply the customizations
    customize_matplotlib_rcParams()
    
    # Create a plot
    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.title('Title')
    plt.show()

    """

    ## General
    # Font face and sizes
    mpl.rcParams['font.family'] = 'sans-serif'
    # mpl.rcParams['font.sans-serif'] = "Helvetica"
    mpl.rcParams['font.size'] = 8             # default font sizes
    mpl.rcParams['axes.titlesize'] = 12       # large
    mpl.rcParams['axes.labelsize'] = 9        # medium
    mpl.rcParams['xtick.labelsize'] = 8       # medium
    mpl.rcParams['ytick.labelsize'] = 8       # medium
    mpl.rcParams['legend.fontsize'] = 9       # medium
    mpl.rcParams['legend.title_fontsize'] = 9 # None (same as default axes)
    mpl.rcParams['figure.titlesize'] = 15     # large (suptitle size)
    mpl.rcParams['figure.labelsize'] = 12     # large (sup[x|y]label size)


    # Spines and ticks
    mpl.rcParams['axes.spines.top'] = True
    mpl.rcParams['axes.spines.right'] = True
    mpl.rcParams['axes.linewidth'] = .6
    mpl.rcParams['axes.edgecolor'] = 'black'
    mpl.rcParams['xtick.major.size'] = 0 # 3.5
    mpl.rcParams['ytick.major.size'] = 0 # 3.5
    # mpl.rcParams['xtick.major.width'] =  0.8
    # mpl.rcParams['ytick.major.width'] =  0.8

    # Grid
    mpl.rcParams['axes.grid.which'] = 'major' # lines at {major, minor, both} ticks
    mpl.rcParams['grid.linestyle'] = '--'
    mpl.rcParams['grid.color'] = '#CCCCCC'
    mpl.rcParams['grid.linewidth'] = 0.2
    # mpl.rcParams['grid.alpha'] = 1

    # Label placement
    mpl.rcParams['axes.titlelocation'] = 'center' # {left, right, center}
    mpl.rcParams['axes.titlepad'] = 7.5 # 6
    mpl.rcParams['axes.labelpad'] = 7.5 # 4
    # mpl.rcParams['xtick.major.pad'] = 3.5 # dist to major tick label in pts
    # mpl.rcParams['ytick.major.pad'] = 3.5

    # Discrete color cycle (and continuous map)
    # mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=sns.color_palette("PiYG", n_colors=6))

    # Legend properties
    mpl.rcParams['legend.loc'] = 'best'
    mpl.rcParams['legend.frameon'] = False
    mpl.rcParams['legend.loc'] = 'best'

    # Legend padding
    # mpl.rcParams['legend.borderpad'] =  0.4     # border whitespace
    # mpl.rcParams['legend.labelspacing'] = 0.5   # vert space between legend entries
    # mpl.rcParams['legend.handlelength'] = 2.0   # length of the legend lines
    # mpl.rcParams['legend.handleheight'] = 0.7   # height of the legend handle
    # mpl.rcParams['legend.handletextpad'] = 0.8  # space btwn leg line leg txt
    # mpl.rcParams['legend.borderaxespad'] = 0.5  # border btwn axs and leg edge
    # mpl.rcParams['legend.columnspacing'] = 2.0  # column separation

    # Space-filling object properties (e.g., polygons/circles, bars/scatter)
    mpl.rcParams['patch.edgecolor'] = 'black' # if forced, else patch not filled
    mpl.rcParams['patch.force_edgecolor'] = 1
    mpl.rcParams['patch.linewidth'] = 0 # edgewidth (.5)

    ## Specific objects
    # Scatter properties
    # mpl.rcParams['scatter.edgecolors'] = 'black' # 'face' = match edge colours

    # Line properties
    mpl.rcParams['lines.markersize'] = 5
    mpl.rcParams['lines.linewidth'] = 2

    # Bar properties
    # mpl.rcParams['bar.width'] = 0.8 # / no global styling parameter

    # Error properties
    mpl.rcParams['errorbar.capsize'] = 3
    # mpl.rcParams['errorbar.color'] = 'black' # / no global styling parameter
    # mpl.rcParams['errorbar.linewidth'] = 1.5 # / no global styling parameter

    # Contour properties
    mpl.rcParams['contour.linewidth'] = 1 # None: falls back to line.linewidth

    # Histogram properties
    # hist.bins: 10  # the default number of histogram bins or 'auto'

    # Box properties
    # box
    mpl.rcParams['boxplot.boxprops.linewidth'] = 0 # box outline (0.5)
    # mpl.rcParams['boxplot.boxprops.color'] = 'none' # 'black' (?)

    # box line to cap
    mpl.rcParams['boxplot.whiskerprops.linewidth'] = .65
    mpl.rcParams['boxplot.whiskerprops.linestyle'] = '--'
    # mpl.rcParams['boxplot.whiskerprops.color'] = 'black' # (?)

    # box cap line
    mpl.rcParams['boxplot.capprops.linewidth'] = .75
    # mpl.rcParams['boxplot.capprops.color'] = 'black' # (?)

    # box median line
    mpl.rcParams['boxplot.medianprops.linewidth'] = 1
    mpl.rcParams['boxplot.medianprops.linestyle'] = '-'
    # mpl.rcParams['boxplot.medianprops.color'] = 'black' # (?)

    mpl.rcParams['boxplot.meanprops.linewidth'] = 1
    mpl.rcParams['boxplot.meanprops.linestyle'] = '-'
    # mpl.rcParams['boxplot.meanprops.color'] = 'black' # (?)

    # box scatter
    mpl.rcParams['boxplot.flierprops.markerfacecolor'] = 'none'
    mpl.rcParams['boxplot.flierprops.markeredgewidth'] = .65
    mpl.rcParams['boxplot.flierprops.marker'] = 'o'
    # mpl.rcParams['boxplot.flierprops.markersize'] = 6 # (?)
    # mpl.rcParams['boxplot.flierprops.linewidth'] = 0 # (?)
    # mpl.rcParams['boxplot.flierprops.markeredgecolor'] = 'black' # (?)
    # mpl.rcParams['boxplot.flierprops.color'] = 'black' # (?)

    ## Figure padding
    # Figure layout
    mpl.rcParams['figure.autolayout'] = True # auto- make plot elements fit on fig
    mpl.rcParams['figure.constrained_layout.use'] = True # apply tight layout

    # Subplot padding (all dims are a fraction of the fig width and height).
    # Not compatible with constrained_layout.
    # mpl.rcParams['figure.subplot.left'] = .125    # left side of fig subplots
    # mpl.rcParams['figure.subplot.right'] = 0.9    # right side of fig subplots
    # mpl.rcParams['figure.subplot.bottom'] = 0.11  # bottom of subplots of fig
    # mpl.rcParams['figure.subplot.top'] = 0.88     # top of fig subplots
    # mpl.rcParams['figure.subplot.wspace'] = 0.2   # w reserved space btwn subplots
    # mpl.rcParams['figure.subplot.hspace'] = 0.2   # h reserved space btwn subplots

    # Constrained layout padding. Not compatible with autolayout.
    # mpl.rcParams['figure.constrained_layout.h_pad'] = 0.04167
    # mpl.rcParams['figure.constrained_layout.w_pad'] = 0.04167

    # Constrained layout spacing between subplots, relative to the subplot sizes. 
    # Much smaller than for tight_layout (figure.subplot.hspace, figure.subplot.wspace) 
    # as constrained_layout already takes surrounding text (titles, labels, # ticklabels)
    # into account. Not compatible with autolayout.
    # mpl.rcParams['figure.constrained_layout.hspace'] = 0.02
    # mpl.rcParams['figure.constrained_layout.wspace'] = 0.02

    ## Other
    # Figure size and quality
    mpl.rcParams['figure.dpi'] = 100 # [NOTE] alters figure size
    mpl.rcParams['figure.figsize'] = (5, 5) # (6, 4), (6.4, 4.8)

    # Figure saving settings
    mpl.rcParams['savefig.transparent'] = True
    mpl.rcParams['savefig.format'] = 'png' # {png, ps, pdf, svg}
    mpl.rcParams['savefig.dpi'] = 330

    #%config InlineBackend.figure_format = 'svg' # set inline figure format/quality
    
    return