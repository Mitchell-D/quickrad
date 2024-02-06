# quickrad

A Python module for generating lookup tables using [SBDART][1], a
discrete-ordinate radiative transfer model capable of estimating
incoming and outgoing flux and radiance given plane-parallel cloud
layers, aerosol properties, surface types, etc.

<p align="center">
  <img height="256" src="https://github.com/Mitchell-D/quickrad/blob/main/images/sbdart_sample_0.png" />
  <img height="256" src="https://github.com/Mitchell-D/quickrad/blob/main/images/sbdart_sample_1.png" />
  <img height="256" src="https://github.com/Mitchell-D/quickrad/blob/main/images/sbdart_sample_2.png" />
</p>

## Dependencies

1. SBDART from [this repository][2] (Released for Fortran 2003)
2. python>=3.9

[1]: https://userpages.umbc.edu/~martins/PHYS650/SBDART%20Article.pdf
[2]: https://github.com/paulricchiazzi/SBDART/tree/master
