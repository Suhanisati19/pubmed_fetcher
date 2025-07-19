import typer
from pubmed_fetcher.fetcher import fetch_and_process_papers

app = typer.Typer()

@app.command()
def main(
    query: str,
    file: str = typer.Option(None, "-f", "--file"),
    debug: bool = typer.Option(False, "-d", "--debug")
):
    """
    Fetch PubMed papers and identify non-academic authors.
    """
    results = fetch_and_process_papers(query, debug)
    if file:
        import csv
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        typer.echo(f"Results written to {file}")
    else:
        for r in results:
            print(r)

if __name__ == "__main__":
    app()