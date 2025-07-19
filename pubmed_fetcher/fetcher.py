from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from pubmed_fetcher.utils import is_non_academic_affiliation, extract_email

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_pubmed_ids(query: str) -> List[str]:
    """
    Fetch PubMed IDs for a given query.
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 100,
        "retmode": "json"
    }
    response = requests.get(BASE_URL + "esearch.fcgi", params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_pubmed_details(ids: List[str]) -> List[Dict]:
    """
    Fetch detailed PubMed article data using a list of PubMed IDs.
    """
    if not ids:
        print("⚠️ No PubMed IDs provided. Skipping fetch.")
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }
    response = requests.get(BASE_URL + "efetch.fcgi", params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "xml")

    articles = soup.find_all("PubmedArticle")
    results = []

    for article in articles:
        try:
            pmid_tag = article.find("PMID")
            pmid = pmid_tag.text.strip() if pmid_tag else "N/A"

            title_tag = article.find("ArticleTitle")
            title = title_tag.text.strip() if title_tag else "No Title"

            pub_date_tag = article.find("PubDate")
            pub_date = pub_date_tag.text.strip() if pub_date_tag else "N/A"

            authors = []
            for author in article.find_all("Author"):
                last_name_tag = author.find("LastName")
                forename_tag = author.find("ForeName")
                name = f"{forename_tag.text.strip() if forename_tag else ''} {last_name_tag.text.strip() if last_name_tag else ''}".strip()

                affiliation_info = author.find("AffiliationInfo")
                affiliation = ""
                if affiliation_info:
                    aff_tag = affiliation_info.find("Affiliation")
                    affiliation = aff_tag.text.strip() if aff_tag else ""

                email = extract_email(affiliation)

                authors.append({
                    "name": name,
                    "affiliation": affiliation,
                    "email": email
                })

            results.append({
                "pmid": pmid,
                "title": title,
                "pub_date": pub_date,
                "authors": authors
            })
        except Exception as e:
            print(f"⚠️ Skipping one article due to error: {e}")
            continue

    return results

def fetch_and_process_papers(query: str, debug: bool = False) -> List[Dict]:
    """
    Fetch and process PubMed papers for a given query.
    Returns only those papers with at least one non-academic affiliation.
    """
    ids = fetch_pubmed_ids(query)
    if debug:
        print(f"🔍 Found {len(ids)} papers for query: '{query}'")

    papers = fetch_pubmed_details(ids)

    # Filter papers with at least one author having a non-academic affiliation
    filtered = []
    for paper in papers:
        for author in paper["authors"]:
            if is_non_academic_affiliation(author["affiliation"]):
                filtered.append(paper)
                break

    if debug:
        print(f"✅ Filtered down to {len(filtered)} papers with at least one non-academic affiliation")

    return filtered
