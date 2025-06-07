from pathlib import Path

from bs4 import BeautifulSoup


def title(soup: BeautifulSoup) -> str | None:
    el = soup.find("h1", attrs={"data-testid": "bookTitle"})
    return el.get_text(strip=True) if el else None


def autor(soup: BeautifulSoup) -> str | None:
    el = soup.find("span", attrs={"data-testid": "name"})
    return el.get_text(strip=True) if el else None


def paperback(soup: BeautifulSoup) -> str | None:
    el = soup.find("p", attrs={"data-testid": "pagesFormat"})
    return el.get_text(strip=True) if el else None


def publication(soup: BeautifulSoup) -> str | None:
    el = soup.find("p", attrs={"data-testid": "publicationInfo"})
    return el.get_text(strip=True) if el else None


def ratings_count(soup: BeautifulSoup) -> str | None:
    el = soup.find("span", attrs={"data-testid": "ratingsCount"})
    return el.get_text(strip=True) if el else None


def reviews(soup: BeautifulSoup) -> str | None:
    el = soup.find("span", attrs={"data-testid": "reviewsCount"})
    return el.get_text(strip=True) if el else None


def autor_url(soup: BeautifulSoup) -> str | None:
    el = soup.find("a", class_="ContributorLink")
    return el.get("href") if el else None


def rating(soup: BeautifulSoup) -> str | None:
    el = soup.find("div", class_="RatingStatistics__rating")
    return el.get_text(strip=True) if el else None


def autor_stats(soup: BeautifulSoup) -> str | None:
    parent = soup.find("div", class_="FeaturedPerson__container")
    if parent:
        el = parent.find("span", class_="Text Text__body3 Text__subdued")
        return el.get_text(strip=True) if el else None
    return None


def author_bio(soup: BeautifulSoup) -> str | None:
    parent = soup.find("div", class_="TruncatedContent__text TruncatedContent__text--medium")
    if parent:
        el = parent.find("span", class_="Formatted")
        return el.get_text(strip=True) if el else None
    return None


def description(soup: BeautifulSoup) -> str | None:
    parent = soup.find(
        "div", class_="BookPageMetadataSection__description", attrs={"data-testid": "description"}
    )
    if parent:
        el = parent.find("span", class_="Formatted")
        return el.get_text(strip=True) if el else None
    return None


html = r"C:\Users\rapha\Documents\GitHub\portfolios-business-intelligence-data-analysis\portfolio-web-analytics\data\html\25986929-goodnight-punpun-omnibus-vol-1.html"  # noqa: E501
file_path = Path(html)
soup = BeautifulSoup(file_path.read_text(encoding="utf-8"), "html.parser")

print("Título:", title(soup))
print("Autor:", autor(soup))
print("Formato:", paperback(soup))
print("Publicação:", publication(soup))
print("Avaliações:", ratings_count(soup))
print("Resenhas:", reviews(soup))
print("URL do autor:", autor_url(soup))
print("Nota média:", rating(soup))
print("Estatísticas do autor:", autor_stats(soup))
print("Biografia:", author_bio(soup))
print("Descrição:", description(soup))
