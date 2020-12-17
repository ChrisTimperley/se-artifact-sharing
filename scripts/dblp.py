#!/usr/bin/env python3
"""
Obtains a list of technical publications at ICSE, FSE, ASE, and EMSE
between 2014 and 2018 using a .tar.gz snapshot of the DBLP database
(https://dblp.org).

Writes the resulting set of publications to a YAML document,
papers.dblp.yml, in the current working directory.
"""
import argparse
import gzip
import re
import os
import typing as t

import attr
import lxml.etree
import yaml

YEARS = range(2008, 2019)

PAGE_REGEX = r'(\d+)-(\d+)'

CROSSREF_TO_VENUE = {
    'conf/icse/2018': 'ICSE',
    'conf/icse/2017': 'ICSE',
    'conf/icse/2016': 'ICSE',
    'conf/icse/2015-1': 'ICSE',
    'conf/icse/2015-2': 'ICSE',
    'conf/icse/2014': 'ICSE',
    'conf/icse/2013': 'ICSE',
    'conf/icse/2012': 'ICSE',
    'conf/icse/2011': 'ICSE',
    'conf/icse/2010': 'ICSE',
    'conf/icse/2009': 'ICSE',
    'conf/icse/2008': 'ICSE',

    'conf/kbse/2018': 'ASE',
    'conf/kbse/2017': 'ASE',
    'conf/kbse/2016': 'ASE',
    'conf/kbse/2015': 'ASE',
    'conf/kbse/2014': 'ASE',
    'conf/kbse/2013': 'ASE',
    'conf/kbse/2012': 'ASE',
    'conf/kbse/2011': 'ASE',
    'conf/kbse/2010': 'ASE',
    'conf/kbse/2009': 'ASE',
    'conf/kbse/2008': 'ASE',

    'conf/sigsoft/2018': 'FSE',
    'conf/sigsoft/2017': 'FSE',
    'conf/sigsoft/2016': 'FSE',
    'conf/sigsoft/2015': 'FSE',
    'conf/sigsoft/2014': 'FSE',
    'conf/sigsoft/2013': 'FSE',
    'conf/sigsoft/2012': 'FSE',
    'conf/sigsoft/2011': 'FSE',
    'conf/sigsoft/2010': 'FSE',
    'conf/sigsoft/2009': 'FSE',
    'conf/sigsoft/2008': 'FSE'
}

DIR_DATA = os.path.join(os.path.dirname(__file__), '../data')
FN_PAPER_NAMES = os.path.join(DIR_DATA, 'papers.txt')
FN_DOIS = os.path.join(DIR_DATA, 'dois.txt')

with open(FN_DOIS, 'r') as f:
    RESTRICT_TO_PAPERS = [p.rstrip('\n') for p in f]
    RESTRICT_TO_PAPERS = [p for p in RESTRICT_TO_PAPERS if p != '']


def str_to_pages(s: str) -> t.Tuple[int, int]:
    m = re.match(PAGE_REGEX, s)
    assert m
    return int(m.group(1)), int(m.group(2))


def pages_to_str(pages: t.Tuple[int, int]):
    return '-'.join([str(p) for p in pages])


def _fast_iter(context, func, *args, **kwargs):
    """
    https://stackoverflow.com/questions/12160418/why-is-lxml-etree-iterparse-eating-up-all-my-memory
    http://lxml.de/parsing.html#modifying-the-tree
    Based on Liza Daly's fast_iter
    http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    See also http://effbot.org/zone/element-iterparse.htm
    """
    for event, elem in context:
        func(elem, *args, **kwargs)
        # It's safe to call clear() here because no descendants will be
        # accessed
        elem.clear()
        # Also eliminate now-empty references from the root node to elem
        for ancestor in elem.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
    del context


@attr.s(slots=True, auto_attribs=True, frozen=True)
class Author:
    name: str
    affiliations: t.Optional[t.Sequence[str]] = attr.ib(default=None)

    @staticmethod
    def from_dict(d: t.Dict[str, t.Any]) -> 'Author':
        return Author(name=d['name'],
                      affiliations=d.get('affiliations'))

    def to_dict(self) -> t.Dict[str, t.Any]:
        d = {'name': self.name}
        if self.affiliations is not None:
            d['affiliations'] = self.affiliations
        return d


@attr.s(hash=False, slots=True, auto_attribs=True)
class Paper:
    doi: str
    venue: str
    year: int
    title: str
    pages: t.Tuple[int, int]
    authors: t.Sequence[Author]

    def __hash__(self) -> int:
        return hash(self.doi)

    @staticmethod
    def from_dict(d: t.Dict[str, t.Any]) -> 'Paper':
        authors = tuple(Author.from_dict(dd) for dd in d['authors'])
        return Paper(doi=d['doi'],
                     venue=d['venue'],
                     year=int(d['year']),
                     title=d['title'],
                     pages=str_to_pages(d['pages']),
                     authors=authors)

    def to_dict(self) -> t.Dict[str, t.Any]:
        d = {'doi': self.doi,
             'venue': self.venue,
             'year': self.year,
             'title': self.title,
             'pages': pages_to_str(self.pages),
             'authors': [a.to_dict() for a in self.authors]}
        return d


class PaperDatabase:
    @staticmethod
    def build_from_dblp_file(
        filename: str
    ) -> 'PaperDatabase':
        papers: List[Paper] = []

        def ca(name: str) -> str:
            return ' '.join([p for p in name.split(' ') if not p.isnumeric()])

        def process_journal_article(elem) -> None:
            try:
                venue = elem.xpath('./journal//text()')[0]
            except IndexError:
                return
            if venue == 'Empirical Software Engineering':
                _process_paper('EMSE', elem)

        def process_conference_paper(elem) -> None:
            try:
                crossref = elem.xpath('./crossref//text()')[0]
            except IndexError:
                return

            if crossref not in CROSSREF_TO_VENUE:
                return

            venue = CROSSREF_TO_VENUE[crossref]
            _process_paper(venue, elem)

        def _process_paper(venue: str, elem):
            try:
                year_s = elem.xpath('./year//text()')[0]
                if not year_s.isnumeric():
                    return
                year = int(year_s)
                if year not in YEARS:
                    return

                title = str(elem.xpath('./title//text()')[0])

                doi = [url for url in elem.xpath('./ee//text()')
                       if url.startswith('https://doi.org')
                       or url.startswith('http://doi.acm.org')][0]
                _, _, doi = doi.partition('.org/')

                # restrict our attention to technical papers
                if doi not in RESTRICT_TO_PAPERS:
                    return

                author_names = [ca(t) for t in elem.xpath('./author//text()')]
                authors = [Author(name) for name in author_names]

                pages = str_to_pages(elem.xpath('./pages//text()')[0])

                paper = Paper(title=title,
                              doi=doi,
                              pages=pages,
                              venue=venue,
                              year=year,
                              authors=authors)
                papers.append(paper)
            except IndexError:
                pass

        with gzip.open(filename, mode='rb') as f:
            context = lxml.etree.iterparse(f, load_dtd=True, tag='inproceedings')
            _fast_iter(context, process_conference_paper)

        with gzip.open(filename, mode='rb') as f:
            context = lxml.etree.iterparse(f, load_dtd=True, tag='article')
            _fast_iter(context, process_journal_article)

        db = PaperDatabase(papers)
        return db

    @staticmethod
    def load(filename: str) -> 'PaperDatabase':
        with open(filename, 'r') as f:
            yml = yaml.safe_load(f)
        return PaperDatabase([Paper.from_dict(d) for d in yml])

    def __init__(self, contents: t.Collection[Paper]) -> None:
        self.__contents = contents
        self.__indexed_by_title_venue_year = {
            (p.title, p.venue, p.year): p for p in contents
        }

    def __iter__(self) -> t.Iterator[Paper]:
        yield from self.__contents

    def save(self, filename: str) -> None:
        yml = [p.to_dict() for p in self]
        with open(filename, 'w') as f:
            yaml.dump(yml, f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filename',
        help='path to a .xml.gz dump from DBLP'
    )
    args = parser.parse_args()

    db = PaperDatabase.build_from_dblp_file(args.filename)
    db.save('papers.dblp.yml')


if __name__ == '__main__':
    main()
