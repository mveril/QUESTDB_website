---
title: "Subsets"
date: 2020-09-10 15:00
draft: false
---

The QUEST database provides theoretical best estimates (TBEs) for more than 500 highly-accurate excitation energies of various natures (valence, Rydberg, {{< tex "n \rightarrow \pi^\star" >}}, {{< tex "\pi \rightarrow \pi^\star" >}}, singlet, doublet, triplet, and double excitations) for molecules ranging from diatomics to molecules as large as naphthalene.
This set is also chemically diverse, with organic and inorganic systems, open- and closed-shell compounds, acyclic and cyclic systems, pure hydrocarbons and various heteroatomic structures, etc.
The molecules included in the QUEST dataset have been systematically optimized at the CC3/aug-cc-pVTZ level of theory, except for a very few cases.
The QUEST dataset of vertical excitations is composed by 5 subsets:

{{< figure src="/img/subsets.png" title="Composition of each of the five subsets making up the present QUEST dataset of highly-accurate vertical excitation energies" >}}

{{< figure src="/img/molecules.png" title="Molecules each of the five subsets making up the present QUEST dataset of highly-accurate vertical excitation energies: QUEST#1 (red), QUEST#2 (magenta and/or underlined), QUEST#3 (black), QUEST#4 (green), and QUEST#5 (blue)." >}}

### [QUEST#1](/references#QUEST%231)
The QUEST#1 benchmark set consists of 110 vertical excitation energies (as well as oscillator strengths) from 18 molecules with sizes ranging from one to three non-hydrogen atoms (water, hydrogen sulfide, ammonia, hydrogen chloride, dinitrogen, carbon monoxide, acetylene, ethylene, formaldehyde, methanimine, thioformaldehyde, acetaldehyde, cyclopropene, diazomethane, formamide, ketene, nitrosomethane, and the smallest
streptocyanine). For this set, we provided two sets of TBEs: i) one obtained within the frozen-core approximation and the aug-cc-pVTZ basis set, and ii) another one including further corrections for basis set incompleteness and "all electron" effects.
For the former set, we systematically selected FCI/aug-cc-pVTZ values to define the TBEs except in very few cases.
For the latter set, both the "all electron" correlation and the basis set corrections were systematically obtained at the CC3 level of theory and with the d-aug-cc-pV5Z basis for the nine smallest molecules, and slightly more compact basis sets for the larger compounds.

### [QUEST#2](/references#QUEST%232)
The QUEST#2 benchmark set reports reference energies for double excitations.
This set gathers 20 vertical transitions from 14 small- and medium-size molecules (acrolein, benzene, beryllium atom, butadiene, carbon dimer and trimer, ethylene, formaldehyde, glyoxal, hexatriene, nitrosomethane, nitroxyl, pyrazine, and tetrazine).
The TBEs of the QUEST#2 set are obtained with SCI and/or multiconfigurational [CASSCF, CASPT2, (X)MS-CASPT2, and NEVPT2] calculations depending on the size of the molecules and the level of theory that we could afford.
An important addition to this second study was the inclusion of various flavors of multiconfigurational methods (CASSCF, CASPT2, and NEVPT2) in addition to high-order CC methods including, at least, perturbative triples (CC3, CCSDT, CCSDTQ, etc).

### [QUEST#3](/references#QUEST%233)
The QUEST#3 benchmark set is, by far, the largest set, and consists of highly accurate vertical transition energies and oscillator strengths obtained for 27 molecules encompassing 4, 5, and 6 non-hydrogen atoms (acetone, acrolein, benzene, butadiene, cyanoacetylene, cyanoformaldehyde, cyanogen, cyclopentadiene, cyclopropenone, cyclopropenethione, diacetylene, furan, glyoxal, imidazole, isobutene, methylenecyclopropene, propynal, pyrazine, pyridazine, pyridine, pyrimidine, pyrrole, tetrazine, thioacetone, thiophene, thiopropynal, and triazine) for a total of 238 vertical transition energies and 90 oscillator strengths with a reasonably good balance between singlet, triplet, valence, and Rydberg excited states.
For these 238 transitions, we have estimated that 224 are chemically accurate for the considered geometry.
To define the TBEs of the QUEST#3 set, we employed CC methods up to the highest technically possible order (CC3, CCSDT, and CCSDTQ), and, when affordable SCI calculations with very large reference spaces (up to hundred million determinants in certain cases), as well as the most reliable multiconfigurational method, NEVPT2, for double excitations.
Most of the TBEs are based on CCSDTQ (4 non-hydrogen atoms) or CCSDT (5 and 6 non-hydrogen atoms) excitation energies.
For all the transitions of the QUEST#3 set, we reported at least CCSDT/aug-cc-pVTZ (sometimes with basis set extrapolation) and CC3/aug-cc-pVQZ transition energies as well as CC3/aug-cc-pVTZ oscillator strengths for each dipole-allowed transition.

### [QUEST#4](/references#QUEST%234)
The QUEST#4 benchmark set consists of two subsets of excitations and oscillator strengths.
An "exotic" subset of 30 excited states for closed-shell molecules containing {{< tex "\ce{F}">}}, {{< tex "\ce{Cl}">}}, {{< tex "\ce{P}">}}, and {{< tex "\ce{Si}">}} atoms (carbonyl fluoride, {{< tex "\ce{CCl2}">}}, {{< tex "\ce{CClF}">}}, {{< tex "\ce{CF2}">}}, difluorodiazirine, formyl fluoride, {{< tex "\ce{HCCl}">}}, {{< tex "\ce{HCF}">}}, {{< tex "\ce{HCP}">}}, {{< tex "\ce{HPO}">}}, {{< tex "\ce{HPS}">}}, {{< tex "\ce{HSiF}">}}, {{< tex "\ce{SiCl2}">}}, and silylidene) and a "radical" subset of 51 doublet-doublet transitions in small radicals (allyl, {{< tex "\ce{BeF}">}}, {{< tex "\ce{BeH}">}}, {{< tex "\ce{BH2}">}}, {{< tex "\ce{CH}">}}, {{< tex "\ce{CH3}">}}, {{< tex "\ce{CN}">}}, {{< tex "\ce{CNO}">}}, {{< tex "\ce{CON}">}}, {{< tex "\ce{CO+}">}}, {{< tex "\ce{F2BO}">}}, {{< tex "\ce{F2BS}">}}, {{< tex "\ce{H2BO}">}}, {{< tex "\ce{HCO}">}}, {{< tex "\ce{HOC}">}}, {{< tex "\ce{H2PO}">}}, {{< tex "\ce{H2PS}">}}, {{< tex "\ce{NCO}">}}, {{< tex "\ce{NH2}">}}, nitromethyl, {{< tex "\ce{NO}">}}, {{< tex "\ce{OH}">}}, {{< tex "\ce{PH2}">}}, and vinyl) characterized by open-shell electronic configurations and an unpaired electron.
This represents a total of 81 high-quality TBEs, the vast majority being obtained at the FCI level with at least the aug-cc-pVTZ basis set.
We further performed high-order CC calculations to ascertain these estimates.

### [QUEST#5](/references#QUEST%235)

The QUEST#5 subset is composed by additional accurate excitation energies that we have produced for the present article. This new set gathers 13 new systems composed by small molecules as well as larger molecules: aza-naphthalene, benzoquinone, cyclopentadienone, cyclopentadienethione, diazirine, hexatriene, maleimide, naphthalene, nitroxyl, octatetraene, streptocyanine-C3, streptocyanine-C5, and thioacrolein. For these new transitions, we generated quality vertical energies, the vast majority being obtained at the CCSDT level, and we consider that, out of these 80 new transitions, 55 of them can be labeled 
as "safe", i.e., considered as chemically accurate or within 0.05 eV of the FCI limit for the given geometry and basis set.
are made with literature data.



