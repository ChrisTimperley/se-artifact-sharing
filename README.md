# Replication Package: Understanding and Improving Artefact Sharing in Software Engineering Research

This repository provides the associated publication analysis dataset and survey instrument
for the research paper,
"Understanding and Improving Artefact Sharing in Software Engineering Research",
submitted to [Empirical Software Engineering](https://www.springer.com/journal/10664).
An unrefereed preprint for the paper will be uploaded to arXiv.

The study was designed, conducted, and reported by the following investigators:

* [Christopher S. Timperley](https://christimperley.co.uk) (Carnegie Mellon University)
* [Lauren Herckis](http://www.laurenherckis.com) (Carnegie Mellon University)
* [Claire Le Goues](https://clairelegoues.com) (Carnegie Mellon University)
* [Michael Hilton](http://www.cs.cmu.edu/~mhilton) (Carnegie Mellon University)

If you have any questions about the research or this replication package, you should
email any of the investigators listed above.


## Citation Guidelines

If this replication package or the results of the associated study has informed
your research, consider citing our paper as follows:

```
(I will add this after we upload to arXiv.)
```


## Contents

Below is a description of the contents of this repository:

* `publication-analysis.yml`: contains the results of our publication analysis.
  A description of the format of this file is given below.
* `survey-questionnaire.pdf`: outlines the questionnaire that was given to
  participants and describes the branching logic that was used to target
  specific subpopulations (e.g., past AEC members).
* `recruitment-email.pdf`: provides the recruitment email that was sent to 744
  validated participants, all of whom had published at least one technical-track
  paper at ICSE, FSE, ASE, or EMSE in 2018.
* `consent-form.pdf`: provides the form that was used by participants to
  give their consent for the investigators to use their responses as part of the
  study.


Note that, due to the risk of reidentification, we do not provide our survey data
as part of our replication package.


### Data Format: Publication Analysis

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
  are associated with that paper (i.e., we do not count artefacts produced
  by another author/study). Each link is described by its `url`, a
  boolean flag indicating whether or not the artefact was accessible upon
  inspection `is-alive`, and, in the case that the URL redirects to another,
  `redirects-to` gives the destination URL.

**Provenance:**
The contents of the document were obtained through a combination of (a)
scraping [dblp](https://dblp.uni-trier.de/), and (b) manually identifying and
checking the liveness of the links contained in each paper.
