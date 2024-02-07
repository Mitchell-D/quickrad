import numpy as np
import pickle as pkl
from pathlib import Path

from quickrad import sflux_over_fields

"""
Configure and run the model by providing static arguments to sbdart_args,
and arguments with values to be iterated over in the fields and coords
variables below.

Documentation for all SBDART parameter options can be found here:
https://github.com/paulricchiazzi/SBDART/blob/master/Documents/rtdoc.txt
"""
sbdart_args = {
        "btemp":300,
        #"idatm":2, ## Mid-latitude summer
        #"idatm":1, ## Tropical
        #"pbar":0, ## no atmospheric scattering or absorption
        #"pbar":-1, ## Default atmospheric scattering and absorption
        "isalb":0, ## User-selected albedo
        "albcon":.33, ## Constant surface albedo

        ## Single cloud layer
        #"nre":9,
        #"zcloud":4,
        #"sza":20,
        #"tcloud":1,

        ## Wavelength range
        "wlinf":.2,
        "wlsup":5,
        "wlinc":.02,
        #"wlinf":5,
        #"wlsup":50,
        #"wlinc":0.25,

        ## Aerosol properties
        #"wlinc":0.1,
        #"iaer":5, ## User-defined
        #"wlbaer":.64,#",".join(map(str,[.42,.64,.86,.12])), ## single scatter albedo
        #"wbaer":.945,#",".join(map(str,[.95,.94,.93,.92])), ## single scatter albedo
        #"gbaer":.58,#",".join(map(str,[.68,.59,.55,.54])), ## Assymetry parameter
        #"qbaer":.58,
        }

"""
list the new axes' labels and coordinate points in order.  This serves
as the configuration for coordinate values that are iterated over.
"""
fields,coords = zip(*(
        ## Atmosphere profile
        ("idatm", [1,2,3,4,5,6]),
        ## Cloud height
        ("zcloud", list(range(1,13,3))),
        ## Cloud optical depth
        ("tcloud", np.logspace(np.log10(0.01), np.log10(40), 12)),
        ## Cloud particle effective radius
        ("nre", np.concatenate((range(-20,2,2),range(2,21,2)))),
        ## Solar zenith angle
        ("sza", list(range(0, 90, 20))),
        ))
print(fields)
print(coords)

## Directory where sbdart can spawn temporary subdirectories
tmp_dir = Path("test/sbdart")
## pkl file where the lookup table will be stored.
lut_file = Path("test/test_flux.pkl")

""" Run SBDART to calculate layer-wise spectral flux """
labels,coords,sflux = sflux_over_fields(
        fields=fields,
        new_coords=coords,
        sbdart_args=sbdart_args,
        tmp_dir_parent=tmp_dir,
        workers=15,
        dtype=np.float32
        )

"""
Store lookup table and axis info as a 3-tuple like (labels, coords, sflux)
where labels contains strings naming each list of coordinate points. The coords
similarly correspond to each axis of the 'sflux' array with the same index.
"""
pkl.dump((labels,coords,sflux), lut_file.open("wb"))
print(f"NaN Count: {np.count_nonzero(np.isnan(sflux))}")
print(f"Coord Labels: {labels}")
print([len(c) for c in coords])
print(sflux.shape)
