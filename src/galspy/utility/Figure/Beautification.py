import numpy
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as mcolors
import matplotlib.patches as patches





# Default settings change
def SetMyStyle():
    font = {'size'   : 12}

    matplotlib.rc('font', **font)

SetMyStyle()


# List of colors for gradient
def GetGradientColorList(from_clr:tuple,to_clr:tuple,num:int=10):
    mix_pcts = [x/(num-1) for x in range(num)]
    from_clr = numpy.array(from_clr)
    to_clr = numpy.array(to_clr)
    rgb_colors = numpy.array([numpy.round(((1-mix)*from_clr + (mix*to_clr)),3) for mix in mix_pcts])
    return rgb_colors


# Add Rydberg scale from wavelength scale as twiny
def AddRydebergScale(ax:plt.Axes):
    ax_Ryd = ax.twiny()
    h=6.626e-34
    c=3e8
    V=1.6e-19
    def Ang_to_Ryd(ang):
        return ((h*c)/(ang*(1e-10)))/(13.6*V)
    
    ax_Ryd.set_xscale('log')
    lam_min,lam_max = ax.get_xlim()
    ax_Ryd.set_xlim(Ang_to_Ryd(lam_min),Ang_to_Ryd(lam_max))

    Ryd_ticks=[0.01,0.1,1,10,100]
    ax_Ryd.set_xticks(Ryd_ticks,labels=[str(r) for r in Ryd_ticks])
    # ax_Ryd.minorticks_off()
    
    ax_Ryd.set_xlabel("Rydberg",fontsize=12)

    return ax_Ryd


# Gradient below a curve
# https://stackoverflow.com/questions/29321835/is-it-possible-to-get-color-gradients-under-a-curve
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

def zfunc(x, y, fill_color='k', alpha=1.0):
    scale = 10
    x = (x*scale).astype(int)
    y = (y*scale).astype(int)
    xmin, xmax, ymin, ymax = x.min(), x.max(), y.min(), y.max()

    w, h = xmax-xmin, ymax-ymin
    z = numpy.empty((h, w, 4), dtype=float)
    rgb = mcolors.colorConverter.to_rgb(fill_color)
    z[:,:,:3] = rgb

    # Build a z-alpha array which is 1 near the line and 0 at the bottom.
    img = Image.new('L', (w, h), 0)  
    draw = ImageDraw.Draw(img)
    xy = numpy.column_stack([x, y])
    xy -= xmin, ymin
    # Draw a blurred line using PIL
    draw.line(list(map(tuple, xy)), fill=255, width=15)
    img = img.filter(ImageFilter.GaussianBlur(radius=100))
    # Convert the PIL image to an array
    zalpha = numpy.asarray(img).astype(float) 
    zalpha *= alpha/zalpha.max()
    # make the alphas melt to zero at the bottom
    n = zalpha.shape[0] // 4
    zalpha[:n] *= numpy.linspace(0, 1, n)[:, None]
    z[:,:,-1] = zalpha
    return z


def gradient_fill(x, y, fill_color=None, ax=None, zfunc=None, **kwargs):
    if ax is None:
        ax = plt.gca()

    line, = ax.plot(x, y, **kwargs)
    if fill_color is None:
        fill_color = line.get_color()

    zorder = line.get_zorder()
    alpha = line.get_alpha()
    alpha = 1.0 if alpha is None else alpha

    if zfunc is None:
        h, w = 100, 1
        z = numpy.empty((h, w, 4), dtype=float)
        rgb = mcolors.colorConverter.to_rgb(fill_color)
        z[:,:,:3] = rgb
        z[:,:,-1] = numpy.linspace(0, alpha, h)[:,None]
    else:
        z = zfunc(x, y, fill_color=fill_color, alpha=alpha)
    xmin, xmax, ymin, ymax = x.min(), x.max(), y.min(), y.max()
    im = ax.imshow(z, aspect='auto', extent=[xmin, xmax, ymin, ymax],
                   origin='lower', zorder=zorder)

    xy = numpy.column_stack([x, y])
    xy = numpy.vstack([[xmin, ymin], xy, [xmax, ymin], [xmin, ymin]])
    clip_path = patches.Polygon(xy, facecolor='none', edgecolor='none', closed=True)
    ax.add_patch(clip_path)
    im.set_clip_path(clip_path)
    ax.autoscale(True)
    return line, im


def sticky_tick_to_curve(ax_data:plt.Axes,curve_index:list[int],labels=list[str]):
    labels = numpy.array(labels,dtype=str)
    axT:plt.Axes = ax_data.twinx()

    ymini,ymaxi = ax_data.get_ylim()
    axT.set_ylim(ymini,ymaxi)
    
    if ax_data.get_yaxis().get_scale()=="log":
        axT.set_yscale("log")

    def update_ticks(ymin,ymax):
        _,xmax = ax_data.get_xlim()
        yloc = []
        for ci in curve_index:
            curve = ax_data.lines[ci]
            xind = numpy.argmin(numpy.abs(curve.get_xdata()-xmax))
            yloc.append(curve.get_ydata()[xind])
        yloc = numpy.array(yloc)

        mask = (ymin<=yloc) & (yloc<=ymax)
        axT.set_yticks(yloc[mask],labels[mask])

    update_ticks(ymini,ymaxi)

    def on_change(event):
        yminc,ymaxc = event.get_ylim()
        update_ticks(yminc,ymaxc)

    ax_data.callbacks.connect('xlim_changed', on_change)
    ax_data.callbacks.connect('ylim_changed', on_change)