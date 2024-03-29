"""
=========================
Default SBDART atmosphere
=========================

 - LOWTRAN7 solar irradiance spectrum
 - SZA and SAZA of 0 (directly overhead)
 - sub-arctic summer
 - henyey-greenstein phase function
 - cloud and aerosol layers match ambient humidity
 - Thermal emission only for wl>2um
 - Match k-fit transmissions to LOWTRAN solar beam transmission
 - Gridded with the default atmospheric profile
 - Output at 0 ant 100km AGL

================
inputs to SBDART
================

-- data files --
atms.dat     # atmospheric profile      (idatm =  0)
aerosol.dat  # aerosol information      (iaer  = -1)
albedo.dat   # spectral surface albedo  (isalb = -1)
filter.dat   # sensor filter function   (isat  =  0)
solar.dat    # solar spectrum           (nf    = -1)
usrcld.dat   # cloud vertical profile   (tcloud)
CKATM,CKTAU  # k tau values and weights (kdist = -1)

-- solar irradiance --

:@param nf: Select solar spectral irradiance source. (-2) CKTAU file iff
    kdist=-1, (-1) Read from solar.dat file from cwd, (0) spectrally uniform,
    (1) 5s solar spectrum, (2) LOWTRAN7 spectrum (default), (3) MODTRAN3.
:@param sza: Solar zenith angle in degrees. Ignored if iday!=0 or csza>=0
:@param csza: Cosine of solar zenith angle (alternative to sza)
:@param saza: Solar azimuth angle. Ignored if iday is nonzero
:@param iday: Integer day of year, used to calculate sza and saza
:@param time: UTC time in decimal hours
:@param alat: Latitude position of point on Earth's surface
:@param alon: East longitude of point on Earth's surface
:@param solfac: Solar distance factor (to account for seasonal variation)

-- surface reflectance --

:@param isalb: Surface albedo ID: int in [-1, 10]. (-1):reads from albedo.dat;
    (0):uses albcom, for specific surface types [1,10] see documenation.
:@param albcon: If isalb=0, this sets a spectrally-uniform surface albedo
:@param sc: Surface albedo parameters for isalb in {7,8,10}

-- atmospheric parameters --

:@param idatm: Model atmosphere ID: int in [0,6]. (0):reads atms.dat, [1,6]
    are model atmospheres, see documentation.
:@param amix: Weighting factor that mixes a model atmosphere specified with
    idatm with a provided profile in atms.dat. If negative, no mixing (default)
:@param ztrp: Altitude of the tropopause.
:@param pbar: Surface pressure (mb) If pbar<0, original pressure profile used
    (default), (0):No atmospheric absorption, pbar>0 is interpreted as pressure
:@param zpres: Surface altitude; alternative to pbar
:@param sclh2o: Scale height for logarithmic distribution of water vapor if
    sclh2o>0. Otherwise, original water vapor profile is used (default).
:@param xrsc: Rayleigh scattering sensitivity factor
:@param xo4: Oxygen collisional complex sensitivity factor

-- atmospheric constituents --

:@param uw: Integrated column vapor amount (g/cm^2)
:@param uo3: Integrated column ozone above altitude ztrp (atm-cm)
:@param o3trp: Integrated ozone concentration in troposphere (atm-cm)
:@param XN2: Volume mixing ratio of N2 (ppm) (default 781000.00 )
:@param XO2: Volume mixing ratio of O2 (ppm) (default 209000.00 )
:@param XCO2: Volume mixing ratio of CO2 (ppm) (default 360.00 )
:@param XCH4: Volume mixing ratio of CH4 (ppm) (default 1.74 )
:@param XN2O: Volume mixing ratio of N2O (ppm) (default 0.32 )
:@param XCO: Volume mixing ratio of CO (ppm) (default 0.15 )
:@param XNH3: Volume mixing ratio of NH3 (ppm) (default 5.0e-4)
:@param XSO2: Volume mixing ratio of SO2 (ppm) (default 3.0e-4)
:@param XNO: Volume mixing ratio of NO (ppm) (default 3.0e-4)
:@param XHNO3: Volume mixing ratio of HNO3 (ppm) (default 5.0e-5)
:@param XNO2: Volume mixing ratio of NO2 (ppm) (default 2.3e-5)


-- instrument RSRs / filters --

:@param isat: Choose response functions. IDs in range [-4,-2] are filters,
    (-1):reads filter.dat, (0):no filter (default), [1,29] are sensor RSRs
:@param wlinf: sets lower wl limit when isat=0, or central wavelength if
    isat in range [-4, -2].
:@param wlsup: sets upper wl limit when isat=0, or the filter area-equivalent
    width if isat in range [-4, -2].
:@param wlinc: Spectral resolution of the run. If wlinc<0, it defines the rate
    of change of wl step sizes in terms of wl. If wlinc=0, wavelength is 5e-3um
    or (wlsup-wlinf)/10, whichever is smaller. If wlinc in (0,1], then it is
    the step size in cm^(-1).

-- cloud specification --

:@param zcloud: cloud layer boundaries in terms of altitude in km
:@param tcloud: optical depth (at 0.55um) of corresponding cloud layers. .55um
    is a reference wavelength used to abstract
:@param lwp: Alternative to tcloud for specifying optical thickness in terms of
    liquid (or ice, if negative) water path.
:@param rhcld: float in [0,1] defining relative humidity in corresponding
    cloud layers. If negative, defaults to general atmospheric profile.
:@param krhclr: if rhcld is specified for at least one cloud layer, krhclr=1
    will attempt to adjust the cloudless layers' mixing ratios to account for
    the change in LWP due to the modified relative humidity.

-- stratospheric aerosols --

:@param jaer: 5-element array of stratospheric aerosol types for each layer.
    Options include 1:no_aerosol, 2:bkg_stratosphere, 3:aged_volcano,
    4:fresh_volcano, 5:meteor_dust.
:@param zaer: List of altitudes in km AGL of stratospheric aerosol layers.
:@param taerst: List of optical depths of stratospheric aerosol layers.

-- boundary-layer aerosols --

:@param nosct: Boundary layer aerosol mode. int in [0,3]. Doesn't affect iaer=5
    boundary layer aerosol model, or stratospheric models.
:@param iaer: Boundary layer type selection; int in [-1, 5]. 1-4 are models
    for rural, urban, oceanic, and tropospheric aerosols, and iaer=5 uses
    parameters (wlbaer, tbaer, wbaer, gbaer) to define BLA scattering params.
    List of integers if multiple layers specified with zbaer
:@param rhaer: Specify the relative humidity in the boundary layer, similar to
    rhcld. This overrides the default environmental atmospheric profile.
:@param vis: Horizontal meteorological visibility in (km) at 0.55um. This
    quantity can be converted to an aerosol profile estimate, which affects
    the vertical structure when iaer=5. If tbaer is specified, vis still
    controls profile, but total optical depth is overridden by tbaer values.
:@param zbaer: altitude grid (in km AGL) for custom aerosol model.
:@param dbear: Aerosol density at the grid points specified by zbaer. Units
    are arbitrary since only the ratio to zbaer intervals matters, as the
    total optical depth of aerosol layers are specified with tbaer.
:@param tbaer: Optical depth of corresponding aerosol layers at 0.55um
:@param qbaera: Extinction efficiency, used to set the spectral dependence
    of optical depth wrt wavelength if tbaer is provided. Otherwise, if wlbaer
    is defined, floats corresponding to each wavelength are interpreted as
    extinction optical depth values for that wavelength
:@param imoma: Boundary layer aerosol phase function ID (int in [1,5]).
    1:isotropic, 2:rayleigh, 3:henyey_greenstein(g(Re)), 4:haze, 5:cloud.
    This is ignored if iaer=5 & pmaer!=0
:@param spowder: If True, a sub-surface layer with z in [-1,0] km is added to
    the bottom of the grid, which has optical properties that can be specified
    in terms of aerosols or clouds using negative 'z' values.
-- only if iaer=5 --
:@param wlbaer: User-defined wavelength bin(s)
:@param wbaer: Single-scattering albedo corresponding to each wlbaer bin
:@param gbaer: Asymmetry parameter corresponding to each wlbaer bin. This
    value is ignored if pmaer is set or imoma!=3
:@param pmaer: Legendre moments of the scattering phase function. See docs.
:@param abaer: Angstrom exponent used to extrapolate extinction efficiencies
    to wavelengths other than those specified in wlbaer. [Qe ~ wl^(-abaer)]

-- emission and absorption --

:@param nothrm: Thermal emission setting -1:emission for wl>2.0um,
    0:emission for all wl, 1: no thermal emission
:@param kdist: Correlated-k settings. -1:read k params from CKATM/CKTAU and
    ignore gas input parameters, 0:sets absorption optical depth with LOWTRAN
    transmission (efficient approximation), 1:use LOWTRAN7 k-distribution
    method (3-term exp), 2:match LOWTRAN transmission, 3:alternative LOWTRAN
    transmission correction (default).

-- atmosphere model grid settings --

:@param zgrid1: Resolution near bottom of grid
:@param zgrid2: Maximum top-of-grid step size (interval)
:@param ngrid: Number of grid points

-- output --
:@param idb: Diagnostic output selector. See docs for options.
:@param iout: STDOUT output selector. See docs for options.

-- DISORT options --

:@param deltam: If True, uses delta-m method for multiple-stream approximation.
:@param nstr: Number of computational zenith angles (must be multiple of 2)
:@param corint: If True, intensities are corrected for delta-m scaling.

-- radiance output --

:@param nzen: Number of 'user' zenith angles between bounds set with uzen/vzen.
:@param uzen: 2-element array boundaries in [0,180] for calculated zenith
    angles. 0deg is upward-propagating radiation; 180 degrees is downward.
:@param vzen: Alternative 2-element array for viewer zenith angles (180-uzen)
:@param nphi: Number of 'user' azimuth angles. If this is specified, phi sets
    the inclusive boundaries for the specified nphi bins.
:@param phi: 'User' azimuth angles boundaries (if nphi specified), otherwise
    list of azimuth angles to calculate for.
:@param zout: Bottom and top altitude in km for iout outputs. [0,100] by def.

-- radiation boundary conditions --

:@param ibcnd: if 1, uses isotropic illumination from top and bottom. See docs.
:@param fisot: Top-boundary isotropic illumination (W/m^2)
:@param temis: Top-layer emissivity
:@param btemp: Surface temperature in Kelvin

================
outputs from SBDART
================
:@param iout: STDOUT format selector

  0 No STDOUT, but diagnostics (from idb) are called.
    ()

  1 One output record for every wavelength in range including the following
    variables: [WL,FFV,TOPDN,TOPUP,TOPDIR,BOTDN,BOTUP,BOTDIR]
    (wl,ffv,topdn,topup,topdir,botdn,botup,botdir)

  5 Outputs TOA radiance at each (wavelength,zenith,azimuth) combination
    (wl,ffv,topdn,topup,topdir,botdn,botup,botdir,phi[nphi],uzen[nzen],
     uurs[nzen,nphi])

  6 Same as 5 but for bottom of atmosphere (zout[0])

  7 Radiative flux at each layer for each wavelength (very large output)
    (nz, nw, (wl, (z[nz], fdird[nz], fdifd[nz], flxdn[nz], flxup[nz])))

 10 One output, with fluxes integrated over all wavelength
    (wlinf, wlsup, ffew, topdn, topup, topdir, botdn, botup, botdir)

 11 Layerwise radient fluxes integrated over all wavelengths
    (nz, phidw, z, p, fxdn, fxup, fxdir, dfdz, heat)

 20 Radiance output at top of zout range. First record is like IOUT=10, then
    subsequent records contain labels and data points for (nphi,nzen) radiances
    (wlinf, wlsup, ffew, topdn, topup, topdir, botdn, botup, botdir,
     nphi, nzen, phi[nphi], uzen[nzen], rad[uzen,phi]))

 21 Same as 20 but for bottom of zout range

 22 Wavelength-integrated radiative flux AND radiance (in W/m^2/sr) for each
    atmospheric layer (each zenith and azimuth at every layer)
    (nphi, nzen, nz, ffew, phi[nphi], uzen[nzen], z[nz], fxdn[nz], fxup[nz],
     fxdir[nz], rad[z,uzen,phi])

 23 Same as 20 except upper/lower radiance outputs correspond to
    zout[0]/zout[1], which enables you to get radiation from above and below
    a scattered layer

================
Surface albedo options
================

:@param isalb: surface albedo type. Defaults to 0
    -1  spectral surface albedo read from "albedo.dat"
     0  user specified, spectrally uniform albedo set with ALBCON
     1  snow
     2  clear water
     3  lake water
     4  sea  water
     5  sand           (data range 0.4 - 2.3um)
     6  vegetation     (data range 0.4 - 2.6um)
     7  ocean water brdf, includes bio-pigments, foam, and sunglint
        additional input parameters provided in SC.
     8  Hapke analytic brdf model. additional input parameters
        provided in SC.
     9  Ross-thick Li-sparse brdf model. additional input
        parameters in SC.
     10 combination of snow, seawater, sand and vegetation
        partition factors set by input quantity SC
:@param albcon: If isalb==0 sets constant surface albedo. (Def 0; BB)
:@param btemp: Surface (skin) temperature in Kelvin. This includes the
    temperature of the entire dust layer when spowder=True
    (def -1; uses atmospheric profile sfc temp)
:@param temis: Emissivity of the top layer
"""

""" Configured values """
default_params = [
    ('idatm',  4, 'Atmospheric profile ID'),
    ('amix',  0.0, 'Mixing factor between custom (atms.dat) and selected idatm profile'),
    ('isat',  0, 'Spectral response (filter) function ID'),
    ('wlinf',  0.550, 'Lower wavelength limit in um'),
    ('wlsup',  0.550, 'Upper wavelength limit in um'),
    ('wlinc',  0.0, 'Spectral resolution'),
    ('sza',  0.0, 'Solar zenith angle in deg'),
    ('csza',  -1.0, 'Cosine of solar zenith angle in deg'),
    ('solfac',  1.0, 'Solar distance factor'),
    ('nf',  2, 'Solar spectrum ID'),
    ('iday',  0, 'Day of year (for SZA calculation)'),
    ('time',  16.0, 'UTC time in decimal hours'),
    ('alat', -64.7670, 'Latitude of point on Earth\'s surface'),
    ('alon', -64.0670, 'Longitude of point on Earth\'s surface'),
    ('zpres',  -1.0, 'Surface altitude in km; alternative to PBAR'),
    # negative -> use original pressure profile
    ('pbar',  -1.0, 'Surface pressure in mb'),
    # negative -> use vertical profile
    ('sclh2o',  -1.0, 'Water vapor scale height (km)'),
    ('uw',  -1.0, 'Integrated water vapor (g/cm^2)'),
    ('uo3',  -1.0, 'Integrated ozone concentration (atm-cm)'),
    ('o3trp',  -1.0, 'Integrated tropospheric ozone concentration (atm-cm)'),
    # By default, UW sets integrated ozone for whole atmosphere with ZTRP=0.0
    ('ztrp',  0.0, 'Tropopause altitude'),
    ('xrsc',  1.0, 'Rayleigh scattering sensitivity'),
    ('xn2',  -1.0, 'N_2 volume mixing ratio (PPM)'),
    ('xo2',  -1.0, 'O_2 volume mixing ratio (PPM)'),
    ('xco2',  -1.0, 'CO_2 volume mixing ratio (PPM)'),
    ('xch4',  -1.0, 'CH_4 volume mixing ratio (PPM)'),
    ('xn2o',  -1.0, 'N_2O volume mixing ratio (PPM)'),
    ('xco',  -1.0, 'CO volume mixing ratio (PPM)'),
    ('xno2',  -1.0, 'NO_2 volume mixing ratio (PPM)'),
    ('xso2',  -1.0, 'SO_2 volume mixing ratio (PPM)'),
    ('xnh3',  -1.0, 'NH_3 volume mixing ratio (PPM)'),
    ('xno',  -1.0, 'NO volume mixing ratio (PPM)'),
    ('xhno3',  -1.0, 'HNO_3 volume mixing ratio (PPM)'),
    ('xo4',  1.0, 'Oxygen collisional complex absorption sensitivity'),
    ('isalb',  0, 'Surface albedo feature'),
    ('albcon',  0.0, 'Spectrally-uniform surface albedo'),
    ('sc', '1.0,3*0.0', 'Surface albedo params for ISALB in {7,8,10}'),
    ('zcloud',  '5*0.0', 'Cloud layer altitude in km (up to 5 values)'),
    ('tcloud',  '5*0.0', 'Cloud optical depth at 0.55um'),
    ('lwp',  '5*0.0', 'Liquid water path (g/m^2)'),
    ('nre',  '5*8.0', 'Cloud effective radius (um)'),
    # If RHCLD<0, relative humidity inside clouds follows profile
    ('rhcld',  -1.0, 'Relative humidity within cloud layers'),
    ('krhclr',  0, 'Clear-layer water vapor adjustment (if TCLOUD>0 or RHCLD>=0)'),
    ('jaer',  '5*0', '5-element array of stratospheric aerosol types'),
    ('zaer',  '5*0.0', 'Altitudes of stratospheric aerosol layers (km)'),
    ('taerst',  '5*0.0', 'Optical depth at 0.55um of stratospheric aerosol layers'),
    ('iaer', 0, 'Boundary layer aerosol ID'),
    ('vis',  23.0, 'Horizontal visibility due to aerosols at 0.55um (km)'),
    ('rhaer',  -1.0, 'Relative humidity for BL aerosol model (IAER)'),
    ('wlbaer',  '47*0.0', 'Wavelength points when IAER is 5 (um)'),
    # Significant for IAER=1,2,3,4
    ('tbaer',  '47*0.0', 'Vertical optical depth of BL aerosols at 0.55um'),
    ('abaer',  -1.0, 'Angstrom exp for BL aerosol extinction (if IAER is 5)'),
    ('wbaer',  '47*0.950', 'Single-scatter albedo (if IAER is 5)'),
    ('gbaer',  '47*0.70', 'Asymmetry factor (if IAER is 5)'),
    ('pmaer',  '940*0.0', 'Legendere moments of BL phase function (if IAER is 5)'),
    # Valid for positive IAER values
    ('zbaer',  '50*-1.0', 'Altitude grid for custom aerosol profile (km)'),
    # Valid for ZBAER grid points with arbitrary relative units
    ('dbaer',  '50*-1.0', 'Aerosol density at ZBAER points'),
    ('nothrm', -1, 'Thermal emission ID (-1, 0, or 1)'),
    ('nosct',  0, 'BL Aerosol scattering method ID'),
    ('kdist',  3, 'Transmission scheme ID'),
    ('zgrid1',  0.0, 'Lower-atmosphere resolution (km)'),
    ('zgrid2',  30.0, 'Upper-atmosphere resolution (km)'),
    ('ngrid',  50, 'Number of vertical grid points'),
    ('zout',  0.0,100.0, 'Bottom and top altitudes for IOUT (km)'),
    ('iout',  10, 'Output format ID'),
    ('deltam', 't', 'If True, Uses Delta-m method (Wiscombe, 1977)'),
    ('corint',  'f', 'Use (Nakajima & Tanaka, 1988) Delta-M correction'),
    ('lamber',  't', ''),
    ('ibcnd',  0, 'Boundary illumination; 1 if isotropic illumination from bottom'),
    ('saza',  180.0, 'Solar azimuth angle (deg)'),
    ('prnt',  '7*f', 'DISORT output option ID'),
    ('ipth',  1, ''),
    ('fisot',  0.0, 'Top isotropic illumination (W/m^2)'),
    ('temis',  0.0, 'Top-layer emissivity'),
    ('nstr',  4, 'Number of internal radiation streams used'),
    ('nzen',  0, 'Number of viewing zenith angles'),
    ('uzen',  20*-1.0, 'Specific viewing zenith angles'),
    ('vzen',  20*90, 'User NADIR angles (ie 180-UZEN)'),
    ('nphi',  0, 'Number of viewing azimuth angles'),
    ('phi',  20*-1.0, 'Specific viewer azimuth angles'),
    ('imomc',  3, 'Cloud model phase function ID'),
    ('imoma',  3, 'BL Aerosol phase function ID'),
    ('ttemp',  -1.0, 'Top-layer thermal emission'),
    ('btemp',  -1.0, 'Bottom-layer thermal emission'),
    ('spowder',  'f', 'Additional surface layer scattering'),
    ('idb',  20*0, 'Diagnostic output ID'),
    ]

out_labels = {
    "rad":"Radiance (in W/m^2/sr) for each phi/uzen combo",
    "srad":"Spectral radiance (in W/m^2/um/sr)",
    "flux":"Flux (in W/m^2)",
    "sflux":"Spectral flux (in W/m^2/um)",
    "flux_labels":"String labels for flux values",
    "sflux_labels":"String labels for spectral flux values",
    "srad_labels":"String labels for spectral radiance values",
    "phi":"Azimuth angle in degrees",
    }
{
    "ffew":"filter function equivalent width (um)",
    "topdn":"total downward flux at ZOUT(2) km (w/m^2) ",
    "topup": "total upward flux at ZOUT(2) km (w/m^2)",
    "topdir": "direct downward flux at ZOUT(2) km (w/m^2)",
    "botdn": "total downward flux at ZOUT(1) km (w/m^2)",
    "botup": "total upward flux at  ZOUT(1) km (w/m^2)",
    "botdir": "direct downward flux at ZOUT(1) km (w/m^2)",
    }
