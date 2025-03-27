import galspy as gs
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits


root=gs.NavigationRoot(gs.NINJA.L150N2040)
PIG=root.PIG(43)

spm=gs.PIGSpectrophotometry(PIG)
imgs=spm.get_photometry_images(2)
img_F070W = imgs["F070W"].T
img_F090W = imgs["F090W"].T
img_F115W = imgs["F115W"].T
img_F150W = imgs["F150W"].T
img_F200W = imgs["F200W"].T
img_F277W = imgs["F277W"].T
img_F356W = imgs["F356W"].T
img_F444W = imgs["F444W"].T

# b=b/np.max(b)
# g=g/np.max(g)
# r=r/np.max(r)
# rgb = np.stack([r, g, b], axis=-1)


# --------- FITS
hdu_primary = fits.PrimaryHDU()

def load(img,name,normalise=False):
    hdu = fits.ImageHDU(img,name=name)
    if normalise: hdu = hdu/np.max(hdu)
    return hdu

hdu_F070W = load(img_F070W,name="F070W") 
hdu_F090W = load(img_F090W,name="F090W")
hdu_F115W = load(img_F115W,name="F115W")
hdu_F150W = load(img_F150W,name="F150W")
hdu_F200W = load(img_F200W,name="F200W")
hdu_F277W = load(img_F277W,name="F277W")
hdu_F356W = load(img_F356W,name="F356W")
hdu_F444W = load(img_F444W,name="F444W")

hdul = fits.HDUList([hdu_primary, hdu_F070W,hdu_F090W,hdu_F115W,hdu_F150W,hdu_F200W,hdu_F277W,hdu_F356W,hdu_F444W])


SAVE_FILEPATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/test_gid2.fits"
hdul.writeto(SAVE_FILEPATH, overwrite=True)
print("FITS file saved")








