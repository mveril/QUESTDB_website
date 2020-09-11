# QUEST Website

## Introduction

The QUEST website is the website build to analyze the date from the [QUEST project](https://doi.org/10.1021/acs.jpclett.0c00014). it provide statistics for the QUEST vertical excitations set by targeting data corresponding to the parameters which the user has selected.

## Quick start

To clone this website and use it locally please run the following commands.

```bash
git clone --recurse-submodules https://git.irsamc.ups-tlse.fr/mveril/exdatabaseLCPQ
cd exdatabaseLCPQ
hugo serve
```

Now you car use your favorite browser to navigate to the website using the URL showed by hugo in your terminal (normally <localhost:1313>)

## Repository content

### The website

The main part of this repository is the website. It is build using the [hugo](https://gohugo.io/) static website generator with the [beautifulhugo](https://themes.gohugo.io/beautifulhugo/) theme.

All the data are stored in the [data](exdatabaseLCPQ/src/branch/master/static/data) directory.

### The tools.

The second part is the  [tools](exdatabaseLCPQ/src/branch/master/tools/) a series of python and bash scripts used to generate data.

#### datafileBuilder

A python script to generate data from custom \LaTeX input file see  [examples](exdatabaseLCPQ/src/branch/master/docs/examples).

#### metarecover

the metarecover bash script is used to regenerate the metadata from the previous git history state.
So you can remove a data file to regenerate it from a LaTeX input file with datafileBuilder and recover the metadata from the previous version using metarecover.