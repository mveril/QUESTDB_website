# DatafileBuilder

DatafileBuilder.py is a script to read a $\mathrm{\LaTeX}$  `tabular`  environment to data file for the website.

## Requirement

To run the script you must have this two elements.

- [Python](https://www.python.org/)≥3
- [TexSoup](https://github.com/alvinwan/TexSoup)

## Command line usage

```
usage: datafileBuilder.py [-h] [--file FILE] [--defaultType {ABS,FLUO}]
                          [--format {LINE,COLUMN,TBE}] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --file FILE
  --defaultType {ABS,FLUO}
  --format {LINE,COLUMN,TBE}
  --debug               Debug mode
```

The default type is `ABS` (for absorbtion).

The default format is  `LINE ` described [below](#the-line-format)

## Disclaimer

There is **absolutly no guarantee** of success.

If the program crach of if the result is not correct please:

- Check if the input file respect the selected [format](#formats)
- **Simplify** the $\mathrm{\LaTeX}$ code of the input file as much as possible

## Input

### Input skeleton

```latex
% \newcommand area
\newcommand{}{}{}
% ther cusom commands definition with or without arguments
\newcommand{}{}

\begin{tabular}
% Tabular in one of the format supported by the script
\end{tabular}
```

### Example of input

```latex
\newcommand{\TDDFT}{TD-DFT}
\newcommand{\CASSCF}{CASSCF}
\newcommand{\CASPT}{CASPT2}
\newcommand{\ADC}[1]{ADC(#1)}
\newcommand{\CC}[1]{CC#1}
\newcommand{\CCSD}{CCSD}
\newcommand{\EOMCCSD}{EOM-CCSD}
\newcommand{\CCSDT}{CCSDT}
\newcommand{\CCSDTQ}{CCSDTQ}
\newcommand{\CCSDTQP}{CCSDTQP}
\newcommand{\CI}{CI}
\newcommand{\sCI}{sCI}
\newcommand{\exCI}{FCI}
\newcommand{\FCI}{FCI}


\newcommand{\AVDZ}{aug-cc-pVDZ}
\newcommand{\AVTZ}{aug-cc-pVTZ}
\newcommand{\DAVTZ}{d-aug-cc-pVTZ}
\newcommand{\AVQZ}{aug-cc-pVQZ}
\newcommand{\DAVQZ}{d-aug-cc-pVQZ}
\newcommand{\TAVQZ}{t-aug-cc-pVQZ}
\newcommand{\AVPZ}{aug-cc-pV5Z}
\newcommand{\DAVPZ}{d-aug-cc-pV5Z}
\newcommand{\PopleDZ}{6-31+G(d)}


\newcommand{\pis}{\pi^\star}
\newcommand{\Ryd}{\mathrm{R}}

\begin{tabular}{l|p{.6cm}p{1.1cm}p{1.4cm}p{1.7cm}p{.9cm}|p{.6cm}p{1.1cm}p{1.4cm}p{.9cm}|p{.6cm}p{1.1cm}p{.9cm}|p{.7cm}p{.7cm}p{.7cm}}
			 \multicolumn{16}{c}{Water}\\
			& \multicolumn{5}{c}{\AVDZ} & \multicolumn{4}{c}{\AVTZ}& \multicolumn{3}{c}{\AVQZ} & \multicolumn{3}{c}{Litt.}\\
	State 	& {\CC{3}} & {\CCSDT} & {\CCSDTQ} & {\CCSDTQP} & {\exCI} & {\CC{3}} & {\CCSDT} & {\CCSDTQ}  & {\exCI}& {\CC{3}} & {\CCSDT}   & {\exCI} & Exp.$^a$ & Th.$^b$ & Th.$^c$\\
	$^1B_1 (n \rightarrow 3s)$ 	&7.51&7.50&7.53&7.53&7.53	&7.60&7.59&7.62&7.62	&7.65	&7.64	&7.68	&7.41 &7.81&7.57\\
	$^1A_2 (n \rightarrow 3p)$ 	&9.29&9.28&9.31&9.32&9.32	&9.38&9.37&9.40&9.41	&9.43	&9.41	&9.46	&9.20 &9.30&9.33\\
	$^1A_1 (n \rightarrow 3s)$ 	&9.92&9.90&9.94&9.94&9.94	&9.97&9.95&9.98&9.99	&10.00	&9.98	&10.02	&9.67 &9.91&9.91\\
	$^3B_1 (n \rightarrow 3s)$ 	&7.13&7.11&7.14&7.14&7.14	&7.23&7.22&7.24&7.25	&7.28	&7.26	&7.30	&7.20 &7.42&7.21\\
	$^3A_2 (n \rightarrow 3p)$ 	&9.12&9.11&9.14&9.14&9.14	&9.22&9.20&9.23&9.24	&9.26	&9.25	&9.28	&8.90 &9.42&9.19\\
	$^3A_1 (n \rightarrow 3s)$ 	&9.47&9.45&9.48&9.49&9.49	&9.52&9.50&9.53&9.54	&9.56	&9.54	&9.58	&9.46 &9.78&9.50\\
\end{tabular}
```

All '\newcommand' are applied to the cell of the tabular and the tabular is parsed to extract data.

### General rules

The general rules to extract data correctly are:

- A `$` must not follow another `$` put space between them.

- The column number must be the same on each row of the `tabular`

- Please respect the format of each tabular.

- Use standard $\mathrm{\LaTeX}$ for the  `\multicolumn` command and not a wrapper.

- In general use standard $\mathrm{\LaTeX}$ instead of dirty form for example.

  ```latex
  $A''$ % Bad
  $A^"$ % Bad
  $A^{\prime\prime}$ %Good
  ```

- D'ont put comment at the end of  `tabular `  row (this cause a TexSoup bug).

- Only  `tabular` environment is supported please convert `longtable` and  other table format to  `tabular .

- Only  `\newcommand` are supported please  convert  `\def`  and  `\NewDocumentCommand`.
- After executing all commands the basis and methods name must be $\mathrm{\LaTeX}$ free (only plan text).

### Unsafe values

Unsafe value (value that must not included in the statistics table and graph) must be in emphasis or with $\sim$ symbol like

> *42*
> $\sim 42$

```latex
\emph{42} % unsafe=true
$\sim$ 42 % unsafe=true
42 % unsafe=false
```

that set the unsafe boolean value to  `true ` in the output data file

#### Formats

##### Generality

###### Transition format

```latex
$^m s[\mathrm{F}](T)$
```

Where `m` is the multiplicity `s` is the symetry and `\mathrm{F}` if it is present specifies that the vertical transition is fluorescence

T is transition type and must be in the format

```latex
initial \rightarrow final
```

All the $\mathrm{\LaTeX}$ code in this format must be standard latex except of the command define on the `\newcommand` section

##### The line format

```latex
\begin{tabular}
			& \multicolumn{n}{c}{Molecule} \\
			& basis#1 & basis#2 & basis#n \\ % You can also use the LaTeX standard \multiculumn command
	State 	& method#1 & method#2 method#n \\  % You can also use the LaTeX standard \multiculumn command
	$Transition#1$ 	& value11&value#12 & ... value#1n\\
	$Transition#2$ 	& value21&value#22 & ... value#2n\\
% All the other transition
	$Transition#m$ 	& value#m1&value#m2 & ... value#mn\\
\end{tabular}
```

##### The column format

```latex
\begin{tabular}
  &		& basis#1 & basis#2 & basis#n \\ % You can also use the LaTeX standard \multiculumn command
  Molecule &State 	& method#1 & method#2 method#n \\  % You can also use the LaTeX standard \multiculumn command
  molecule#1	&$Transition#11$			&value#111&value#112 ... &value#11n	\\
        &$Transition#12$			&value#121&value#122 &value#12n	\\
% Other transition on the molecule#1
        &$Transition#1m$			&value#1m1&value#1m1 &value#1nm	\\
% Other molecules
  molecule#k	&$Transition#k1$			&value#k11&value#k12 ... &value#k1n	\\
% Other transition on the molecule#k
        &$Transition#km$			&value#km1&value#km2 &value#kmn	\\
\end{tabular}
```

This format is very powerfull because it can be used with multiple molecules.

##### The TBE format

The `TBE` format is a variant of the `COLUMN` format but made for theoretical best estimate tabular.

> Warning:
>
> The basis is not extract from the TBE format

```latex
\begin{tabular}
                        &		&	&		& TBE(FC)&  \multicolumn{3}{c}{Corrected TBE} \\
                        & State	 & $f$ & \%$T_1$ & 	basis	& Method & Corr.	& Value \\
      molecule#1	&$transition#11$					& fvalue#11	&\%T_1value#11& fceval#11		& not used value & not used value		& eval#11	\\
                        &$transition#12$					& fvalue#12	&\%T_1value#12& fceval#12		& not used value & not used value		& eval#12	\\
% Other transition on the same molecule
                        &$transition#1n$					& fvalue#12	&\%T_1value#12& fceval#1n		& not used value & not used value		& eval#12	\\
      molecule#m	&$transition#m1$					& fvalue#m1	&\%T_1value#m1& fceval#m1		& not used value & not used value		& eval#k1	\\
                        &$transition#m2$					& fvalue#m2	&\%T_1value#m2& fceval#m2		& not used value & not used value		& eval#m2	\\
% Other transition on the same molecule
                        &$transition#mn$					& fvalue#mn	&\%T_1value#mn& fceval#mn		& not used value & not used value		& eval#mn	\\
\end{tabular}
```

## Output

### Directory strucure

```
data
├── abs
│   ├── molecule#1_method#1_basis#1.dat
│   ├── ...
│   ├── molecule#n_basis#m_method#k.dat
│   └── molecule#n_basis#m_method#k.dat
└── fluo
    ├── molecule#1_method#1_basis#1.dat
    ├── ...
    ├── molecule#n_basis#m_method#k.dat
    └── molecule#n_basis#m_method#k.dat
```

When the debug flag is used instead of `data/` the root of output directory is `data/test/`

### Output file

```
# Molecule : moleculename
# Comment  : 
# code     : codename,[version]
# method   : method,[basis]
# geom     : method,[basis]
# DOI      : DOI

# Initial state            Final state                        Transition                    Energies (eV)   %T1    Oscilator forces     unsafe
#######################  #######################  ########################################  ############# ####### ################### ##############
# Number  Spin  Symm       Number  Spin  Symm         type                                    E_abs         %T1            f            is unsafe
  n       s      symm      n       s     symm         (excitationType)                        value         %T1val         forceval     isUnsafe
```

When each value are number spin value are integer symmetry and excitation type are standard LaTeX

isUnsafe is boolean corrresponded to  `JavaScript`  boolean values `true` or  `false`


