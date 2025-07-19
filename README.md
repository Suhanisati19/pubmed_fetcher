# PubMed Fetcher

## Description
A command-line tool to fetch PubMed papers and filter those with at least one non-academic author affiliated with a pharmaceutical or biotech company.

## Installation

```bash
git clone https://github.com/yourname/pubmed_fetcher.git
cd pubmed_fetcher
poetry install
```

## Usage

```bash
poetry run get-papers-list "cancer immunotherapy" -f results.csv --debug
```

## Tools Used

- [PubMed E-Utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [Typer](https://typer.tiangolo.com/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Poetry](https://python-poetry.org/)