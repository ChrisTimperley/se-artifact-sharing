# Replication Package: Understanding and Improving Artifact Sharing in Software Engineering Research

This repository provides the associated publication analysis dataset and survey instrument
for the research paper,
[Understanding and Improving Artifact Sharing in Software Engineering Research](http://dx.doi.org/10.1007/s10664-021-09973-5),
published in [Empirical Software Engineering](https://www.springer.com/journal/10664).
(http://dx.doi.org/10.1007/s10664-021-09973-5).
A preprint for the paper is available on arXiv: https://arxiv.org/abs/2008.01046.

This artifact is archived on Zenodo (https://doi.org/10.5281/zenodo.4737346) and hosted
on GitHub (https://github.com/ChrisTimperley/se-artifact-sharing).

The study was designed, conducted, and reported by the following investigators:

* [Christopher S. Timperley](https://christimperley.co.uk) (Carnegie Mellon University)
* [Lauren Herckis](http://www.laurenherckis.com) (Carnegie Mellon University)
* [Claire Le Goues](https://clairelegoues.com) (Carnegie Mellon University)
* [Michael Hilton](http://www.cs.cmu.edu/~mhilton) (Carnegie Mellon University)

If you have any questions about the research or this replication package, you should
contact Christopher or Michael.


## Contents

Below is a description of the contents of this repository:

* [`data/publication-analysis.yml`](data/publication-analysis.yml):
  contains the results of our publication analysis.
  A description of the format of this file is given below.
* [`data/aec.csv`](data/aec.csv):
  contains data on the number of artifacts submitted to and accepted by the
  artifact evaluation committee at FSE between 2015 and 2018, inclusive.
  We also include a count of the number of papers that we determined to contain
  artifacts, based on the results of our publication analysis.
* [`data/author-survey-quantitative.csv`](data/author-survey-quantitative.csv):
  contains the quantitative results from our author survey.
  A description of the format of this file is given below.
* [`survey-questionnaire.pdf`](./survey-questionnaire.pdf):
  outlines the questionnaire that was given to
  participants and describes the branching logic that was used to target
  specific subpopulations (e.g., past AEC members).
* [`recruitment-email.pdf`](./recruitment-email.pdf):
  provides the recruitment email that was sent to 744
  validated participants, all of whom had published at least one technical-track
  paper at ICSE, FSE, ASE, or EMSE in 2018.
* [`consent-form.pdf`](./consent-form.pdf):
  provides the form that was used by participants to
  give their consent for the investigators to use their responses as part of the
  study.
* [`se-artifacts.ipynb`](./se-artifacts.ipynb):
  provides the [Jupyter notebook](https://jupyter.org/) used to produce the
  figures in the paper.
* [`scripts/dblp.py`](scripts/dblp.py):
  provides the script that was used to obtain a list of technical papers at
  ICSE, FSE, ASE, and EMSE between 2014 and 2018, inclusive.
* [`scripts/grab-urls.py`](scripts/grab-urls.py):
  provides the script that was used to obtain a list of potential artifact
  URLs from a given PDF.
* [`data/dblp-2018-11-01.xml.gz`](data/dblp-2018-11-01.xml.gz):
  the DBLP snapshot that was used to construct the publication dataset.
* [`data/dois.txt`](data/dois.txt):
  a newline-delimited list of the DOIs of the technical papers published at
  ICSE, FSE, ASE, and EMSE between 2014 and 2018, inclusive.
* [`paper.pdf`](./paper.pdf):
  provides a preprint of the paper.

Note that, due to the risk of reidentification, we do not provide the qualitative
results from our survey of authors as part of our replication package.


### Publication Analysis

The publication analysis, represented as a YAML document, describes all technical
track publications at [ICSE](http://www.icse-conferences.org/),
[ASE](https://dl.acm.org/conference/ase),
[FSE](https://dl.acm.org/conference/fse),
and [EMSE](https://www.springer.com/journal/10664)
between 2014 and 2018, inclusive.
Each paper is described as an object with the following fields:

* `authors`: a list of the authors of the paper, given by their `name` and
  `affiliations` according to the paper.
* `title`: the title of the paper.
* `venue`: the venue at which the paper was published
  (i.e., `ICSE`, `FSE`, `ASE`, or `EMSE`).
* `pages`: the pages at which the paper appears in the associated journal
  edition or conference proceedings, given as `start-end`, where `end`
  is inclusive (e.g., `2900-2909`).
* `year`: the year in which the paper was published.
* `doi`: the DOI (digital object identifier) for the paper.
* `artifact-links`: a list of the artifacts included in the paper that
  are associated with that paper (i.e., we do not count artifacts produced
  by another author/study). Each link is described by its `url`, a
  boolean flag indicating whether or not the artifact was accessible upon
  inspection `is-alive`, and, in the case that the URL redirects to another,
  `redirects-to` gives the destination URL.

**Provenance:**
The contents of the document were obtained through a combination of (a)
scraping [dblp](https://dblp.uni-trier.de/), and (b) manually identifying and
checking the liveness of the links contained in each paper.


### Author Survey Quantitative Responses

We provide responses to the quantitative components of our author survey in the form
of a CSV file. Single choice questions are represented by a single column (e.g., `Q2`),
whereas multiple choice questions are given a separate column for each predefined
response (e.g., `Q5_2`). The first row contains the number of the associated question,
and the second row states the question itself.
To preserve anonymity, we removed participant numbers and shuffled responses.


### Jupyter Notebook

The dependencies required to use our notebook can be installed using
[pipenv](https://pypi.org/project/pipenv/), a popular tool for managing Python
virtual environments.

```
$ pipenv install
```

To open our notebook using the classic Jupyter Notebook:

```
$ pipenv run jupyter notebook se-artifacts.ipynb
```

To open our notebook using Jupyter Lab:

```
$ pipenv run jupyter-lab se-artifacts.ipynb
```
