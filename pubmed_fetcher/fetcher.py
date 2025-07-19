from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from pubmed_fetcher.utils import is_non_academic_affiliation, extract_email

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_and_process_papers(query: str, debug: bool = False) -> List[Dict]:
    ids = fetch_pubmed_ids(query)
    papers = fetch_pubmed_details(ids)
    results = []

    for paper in papers:
        non_academic_authors = []
        company_affiliations = []
        corresponding_email = ""

        for author in paper.get("authors", []):
            affil = author.get("affiliation", "")
            name = author.get("name", "")
            if is_non_academic_affiliation(affil):
                non_academic_authors.append(name)
                company_affiliations.append(affil)
                email = extract_email(affil)
                if email:
                    corresponding_email = email

        if non_academic_authors:
            results.append({
                "PubmedID": paper["pmid"],
                "Title": paper["title"],
                "Publication Date": paper["pub_date"],
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(set(company_affiliations)),
                "Corresponding Author Email": corresponding_email,
            })
            if debug:
                print(f"DEBUG: {paper['pmid']} - Non-academic authors found.")

    return results

def fetch_pubmed_ids(query: str) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 50,
        "retmode": "json"
    }
    response = requests.get(BASE_URL + "esearch.fcgi", params=params)
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]

def fetch_pubmed_details(ids: List[str]) -> List[Dict]:
    params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }
    response = requests.get(BASE_URL + "efetch.fcgi", params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    articles = soup.find_all("pubmedarticle")
    results = []
    for article in articles:
        pmid = article.pmid.text
        title = article.find("articletitle").text
        pub_date = article.find("pubdate").text if article.find("pubdate") else "N/A"
        authors = []
        for author in article.find_all("author"):
            name = f"{author.find('lastname', '').text if author.find('lastname') else ''} {author.find('forename', '').text if author.find('forename') else ''}"
            affiliation = author.find("affiliation")
            authors.append({
                "name": name.strip(),
                "affiliation": affiliation.text if affiliation else ""
            })
        results.append({
            "pmid": pmid,
            "title": title,
            "pub_date": pub_date,
            "authors": authors
        })
    return results