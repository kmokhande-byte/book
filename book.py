import urllib.request
import urllib.parse
import re
import time

headers = {"User-Agent": "Mozilla/5.0"}

def get_html(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode("utf-8", errors="ignore")
    except:
        return ""

def search_sites(query):
    query = urllib.parse.quote(query + " pdf")
    url = f"https://duckduckgo.com/html/?q={query}"

    html = get_html(url)

    links = re.findall(r'class="result__a" href="(.*?)"', html)

    sites = []
    for link in links:
        link = urllib.parse.unquote(link)

        if "uddg=" in link:
            link = link.split("uddg=")[1]

        sites.append(link)

    return sites


def extract_pdfs(site):
    html = get_html(site)

    links = re.findall(r'href="(.*?)"', html)

    pdfs = []

    for link in links:
        if ".pdf" in link.lower():

            if not link.startswith("http"):
                link = urllib.parse.urljoin(site, link)

            pdfs.append(link)

    return pdfs


def crawl(book):

    print("\nSearching internet...\n")

    sites = search_sites(book)

    found = set()

    for site in sites[:15]:

        print("Scanning:", site)

        pdfs = extract_pdfs(site)

        for pdf in pdfs:
            found.add(pdf)

        time.sleep(1)

    return list(found)


book = input("Enter book name: ")

results = crawl(book)

print("\nPDF files found:\n")

if results:
    for r in results:
        print(r)
else:
    print("No PDFs found.")