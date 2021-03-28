#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obtains a list of potential artifact URLs from a given PDF and writes them
to the stdout.
"""
import argparse
import re
import typing as t

import pdfx
from pdfx.extractor import URL_REGEX

BLOCKLIST = [
    'reddit.com',
    'wikipedia.org',
    'stackoverflow.com',
    '.acm.org',
    'scitools.com',
    'debian.org',
    'heroku.com',
    'bower.io',
    'arxiv.org',
    'android.com',
    'haskell.org',
    'docker.io',
    'cloudbees.com',
    'jenkins.io',
    'travis-ci.org',
    'yaml.org',
    'crunchbase.com',
    'circleci.com',
    'appveyor.com',
    'google.com',
    'lamdu.org',
    'unisonweb.org',
    'doi.org',
]
REF_REGEX = re.compile(r'\[\d+\]')


def url_is_blocklisted(url: str) -> bool:
    return any(term in url for term in BLOCKLIST)


def url_is_valid(url: str) -> bool:
    return url.startswith("http") and re.match(URL_REGEX, url)


def extract_urls_from_text(text: str) -> t.Set[str]:
    urls = pdfx.extract_urls(text)
    url_to_locations: t.Dict[str, t.Set[t.Tuple[int, int]]] = {}

    for url_original in urls:

        # find the maximal URL for each match of the URL
        for url_match in re.finditer(url_original, text):
            (start_at, end_at) = url_match.span()
            while True:
                while not text[end_at].isspace():
                    end_at += 1
                if text[end_at] == '\n':
                    end_at += 1
                else:
                    break

            url_canonical = url_original
            url_maximal = text[start_at:end_at]
            parts = [p for p in url_maximal.split('\n') if p != '']
            for i, suffix in enumerate(parts):
                if i > 0 and suffix.startswith("http:"):
                    break
                if REF_REGEX.match(suffix):
                    break
                if suffix.isdigit():
                    continue

                url_partial = ''.join(parts[0 : i + 1])
                if url_is_valid(url_partial):
                    url_canonical = url_partial
                if url_partial[-1] in [',', '.'] and url_is_valid(url_partial[:-1]):
                    url_canonical = url_partial[:-1]

            if not url_is_valid(url_canonical):
                continue
            if url_canonical not in url_to_locations:
                url_to_locations[url_canonical] = set()

    return set(url for url in url_to_locations if not url_is_blocklisted(url))


def extract_urls_from_pdf(filename: str) -> t.Set[str]:
    pdf = pdfx.PDFx(filename)
    text = pdf.get_text()
    return extract_urls_from_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="extracts a list of URLs from a given PDF",
    )
    parser.add_argument("filename", help="path to a .PDF file")
    args = parser.parse_args()
    urls_in_file = extract_urls_from_pdf(args.filename)
    for url in urls_in_file:
        print(url)


if __name__ == "__main__":
    main()
