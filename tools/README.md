This directory contains a series of Python scripts used to generate data:

- `datafileBuilder`: A python  script to  generate data  from custom LaTeX input
  file. See [examples](/docs/examples).
- `metarecover`: A python script  is used  to regenerate  the metadata from the
  previous git history state.  So you can remove a data file to regenerate  it
  from  a  LaTeX input  file  with `datafileBuilder`  and recover the metadata
  from the previous version using `metarecover`.
- `ADC25generator`: script used  to build  `ADC(2.5)`  data files  from `ADC(2)` and `ADC(3)` data files.
- `generate_data`: script used to  wrap all  data file  into one `database.json` file.

