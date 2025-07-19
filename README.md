# PubMed Fetcher

## Description
PubMed Fetcher is a command-line Python tool designed to streamline literature research by querying PubMed for scientific papers based on a user-specified search term. It filters and extracts papers that include at least one author affiliated with a pharmaceutical or biotech company, helping researchers quickly identify industry-relevant publications. The results are saved in CSV format for easy analysis and reference.
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
