# quickrad

A Python module for generating lookup tables using [SBDART][1], a
discrete-ordinate radiative transfer model capable of estimating
incoming and outgoing flux and radiance given plane-parallel cloud
layers, aerosol properties, surface types, etc.

<p align="center">
  <img height="256" src="https://github.com/Mitchell-D/quickrad/blob/main/images/sbdart_sample_0.png" />
</p>
<p align="center">
  <img height="256" src="https://github.com/Mitchell-D/quickrad/blob/main/images/sbdart_sample_1.png" />
  <img height="256" src="https://github.com/Mitchell-D/quickrad/blob/main/images/sbdart_sample_2.png" />
</p>

## Dependencies

1. SBDART from [this repository][2] (Released for Fortran 2003)
2. python>=3.9

## Setup

Install quickrad as a package by cloning this repository into a
directory listed in `$PYTHONPATH`. Otherwise, just import relevant
methods from `get_lut.py`.

SBDART should be installed by cloning [the repository][2] and
running `make -si` to compile with gfortran.

To point quickrad to your SBDART installation, you can move the
subsequent binary file `sbdart` to a directory in $PATH, or modify
the `SBDART_PATH` variable at the top of `quickrad.py`.

## Basic Usage

The configuration for executing quickrad is the same as for SBDART,
where a string key is mapped to a numeric value, string, or list of
numeric values. The options are the same as those documented with the
original repo at [rtdoc.txt][3]. In order to assemble a config,
create a dict mapping these string keys to desired values.

```python
args = {"idatm":1, "zcloud":"10,14", "tcloud":"8,13", "iout":7}
tmp_dir = Path("tmp")
data = quickrad.parse_iout(
        iout_id=args["iout"],
        sb_out=quickrad.dispatch_sbdart(args, tmp_dir),
        print_stdout=False,
        )
```

The most basic way to use quickrad is to call `quickrad.parse_iout`
with a dict of any configured parameters that are different from the
defaults, as shown above. This will execute the radiative transfer
model one time and return the results as documented in the
corresponding parsing method.

## Large LUT Generation

There are also multiprocessed methods for generating lookup tables
for a subset of outputs, currently `quickrad.sflux_over_fields` for
spectral flux and `quickrad.flux_over_fields` for broad-band flux
over a series of user-defined orthogonal axes.

These methods allow the user to define a number of fields (SBDART
parameter keys) and a nested list of coordinate values at which each
corresponding field is evaluated. SBDART is executed at each
combination of coordinate values (in parallel if `workers>1`). The
user can also provide a dict of arguments applying to every run.

See `get_lut.py` for a worked example of generating a lookup table.

[1]: https://userpages.umbc.edu/~martins/PHYS650/SBDART%20Article.pdf
[2]: https://github.com/paulricchiazzi/SBDART/tree/master
[3]: https://github.com/paulricchiazzi/SBDART/blob/master/RunRT/rtdoc.txt
