"""
Task 6: Interactive Web Scraping Program
Level 3: Advanced
Internship Program: Software Development - Cognifyz Technologies

Objective:
Fetch data from a website and present it in a user-friendly way
using a simple web scraping library (BeautifulSoup + requests).

Features:
- Preset 1: Quotes to Scrape (Extracts quotes, authors, and tags)
- Preset 2: Books to Scrape (Extracts book titles, prices, star ratings, and availability)
- Preset 3: Custom URL Scraper (Extracts page title, headings, meta tags, and hyperlinks)
- Search and filter capabilities for scraped results
- Data export options to JSON and CSV formats
- Robust error handling for HTTP errors, invalid URLs, and network timeouts
"""

import csv
import json
import os
import sys
from typing import Dict, List, Optional
import urllib.parse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("⚠️ Required packages ('requests', 'beautifulsoup4') not found.")
    print("Please install them with: pip install requests beautifulsoup4")
    sys.exit(1)


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def get_html(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch raw HTML content with error handling."""
    headers = {"User-Agent": DEFAULT_USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.MissingSchema:
        print(f"❌ Invalid URL format. Did you forget 'http://' or 'https://'?")
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error. Unable to connect to '{url}'.")
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out after {timeout} seconds.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error {e.response.status_code}: {e.response.reason}")
    except Exception as e:
        print(f"❌ Unexpected scraping error: {e}")
    return None


class QuotesScraper:
    """Scrapes inspirational quotes from quotes.toscrape.com."""

    BASE_URL = "http://quotes.toscrape.com"

    @classmethod
    def scrape_quotes(cls, pages: int = 1) -> List[Dict]:
        results = []
        for p in range(1, pages + 1):
            url = f"{cls.BASE_URL}/page/{p}/"
            html = get_html(url)
            if not html:
                break

            soup = BeautifulSoup(html, "html.parser")
            quote_blocks = soup.find_all("div", class_="quote")
            if not quote_blocks:
                break

            for b in quote_blocks:
                text_elem = b.find("span", class_="text")
                author_elem = b.find("small", class_="author")
                tags_elem = b.find_all("a", class_="tag")

                text = text_elem.get_text().strip() if text_elem else ""
                author = author_elem.get_text().strip() if author_elem else "Unknown"
                tags = [t.get_text().strip() for t in tags_elem]

                results.append({
                    "quote": text,
                    "author": author,
                    "tags": tags,
                    "page": p,
                })
        return results


class BooksScraper:
    """Scrapes books catalogue from books.toscrape.com."""

    BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

    @classmethod
    def scrape_books(cls, pages: int = 1) -> List[Dict]:
        results = []
        for p in range(1, pages + 1):
            url = cls.BASE_URL.format(p)
            html = get_html(url)
            if not html:
                break

            soup = BeautifulSoup(html, "html.parser")
            articles = soup.find_all("article", class_="product_pod")
            if not articles:
                break

            for art in articles:
                h3 = art.find("h3")
                title = h3.a["title"].strip() if h3 and h3.a and h3.a.has_attr("title") else "N/A"
                price_elem = art.find("p", class_="price_color")
                price = price_elem.get_text().strip() if price_elem else "N/A"
                avail_elem = art.find("p", class_="instock availability")
                avail = avail_elem.get_text().strip() if avail_elem else "N/A"

                star_tag = art.find("p", class_="star-rating")
                rating = "N/A"
                if star_tag:
                    classes = star_tag.get("class", [])
                    rating = classes[1] if len(classes) > 1 else "N/A"

                results.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "availability": avail,
                    "page": p,
                })
        return results


class CustomWebScraper:
    """Extracts summary and metadata from any general website."""

    @classmethod
    def scrape_page(cls, url: str) -> Optional[Dict]:
        html = get_html(url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title Found"

        # Headings
        h1s = [h.get_text().strip() for h in soup.find_all("h1") if h.get_text().strip()][:5]
        h2s = [h.get_text().strip() for h in soup.find_all("h2") if h.get_text().strip()][:8]

        # Paragraphs sample
        paras = [p.get_text().strip() for p in soup.find_all("p") if len(p.get_text().strip()) > 30][:4]

        # Links
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text().strip()
            if text and not href.startswith("#") and not href.startswith("javascript"):
                full_url = urllib.parse.urljoin(url, href)
                links.append({"text": text[:40], "url": full_url})
                if len(links) >= 10:
                    break

        return {
            "url": url,
            "title": title,
            "h1_headings": h1s,
            "h2_headings": h2s,
            "paragraphs": paras,
            "links": links,
        }


def export_scraped_data(data: List[Dict], filename_base: str):
    """Export scraped records to JSON and CSV formats."""
    if not data:
        print("⚠️ No data to export.")
        return

    out_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(out_dir, f"{filename_base}.json")
    csv_path = os.path.join(out_dir, f"{filename_base}.csv")

    # Export JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    # Export CSV
    try:
        keys = list(data[0].keys())
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for row in data:
                # Stringify lists (like tags)
                cleaned = {k: (", ".join(v) if isinstance(v, list) else v) for k, v in row.items()}
                writer.writerow(cleaned)
    except Exception as e:
        print(f"⚠️ Could not write CSV: {e}")

    print(f"\n💾 Data successfully exported!")
    print(f"  • JSON: {json_path}")
    print(f"  • CSV:  {csv_path}")


def interactive_quotes():
    """Interactive quotes scraping flow."""
    print("\n--- Scraping Quotes (quotes.toscrape.com) ---")
    pages_in = input("Enter number of pages to scrape (1-5, default 1): ").strip()
    pages = int(pages_in) if pages_in.isdigit() and 1 <= int(pages_in) <= 5 else 1
    print(f"Fetching quotes across {pages} page(s)...")
    quotes = QuotesScraper.scrape_quotes(pages)

    if not quotes:
        print("No quotes retrieved.")
        return

    print(f"\n✅ Retrieved {len(quotes)} quotes:")
    print("=" * 70)
    for idx, q in enumerate(quotes[:10], 1):
        print(f"{idx}. {q['quote']}")
        print(f"   — {q['author']} | Tags: {', '.join(q['tags'][:4])}")
        print("-" * 70)
    if len(quotes) > 10:
        print(f"... and {len(quotes) - 10} more quotes.")

    save = input("\nDo you want to export this data to JSON/CSV? (y/n): ").strip().lower()
    if save == "y":
        export_scraped_data(quotes, "scraped_quotes")


def interactive_books():
    """Interactive books scraping flow."""
    print("\n--- Scraping Books (books.toscrape.com) ---")
    pages_in = input("Enter number of pages to scrape (1-3, default 1): ").strip()
    pages = int(pages_in) if pages_in.isdigit() and 1 <= int(pages_in) <= 3 else 1
    print(f"Fetching books across {pages} page(s)...")
    books = BooksScraper.scrape_books(pages)

    if not books:
        print("No books retrieved.")
        return

    print(f"\n✅ Retrieved {len(books)} books:")
    header = f"{'#':<3} | {'Title':<35} | {'Price':<10} | {'Rating':<8} | {'Availability':<15}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    for idx, b in enumerate(books[:15], 1):
        t = b["title"][:32] + "..." if len(b["title"]) > 35 else b["title"]
        print(f"{idx:<3} | {t:<35} | {b['price']:<10} | {b['rating']:<8} | {b['availability']:<15}")
    print("-" * len(header))

    save = input("\nDo you want to export this data to JSON/CSV? (y/n): ").strip().lower()
    if save == "y":
        export_scraped_data(books, "scraped_books")


def interactive_custom_url():
    """Interactive custom URL scraping flow."""
    print("\n--- Custom Website Scraper ---")
    url = input("Enter full URL to scrape (e.g. https://news.ycombinator.com or https://python.org): ").strip()
    if not url:
        print("URL cannot be empty.")
        return
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(f"Scraping '{url}'...")
    data = CustomWebScraper.scrape_page(url)
    if not data:
        return

    print("\n" + "=" * 65)
    print("🌐 WEBPAGE SCRAPING REPORT")
    print("=" * 65)
    print(f"URL:   {data['url']}")
    print(f"Title: {data['title']}")

    if data["h1_headings"]:
        print(f"\n📌 H1 Headings ({len(data['h1_headings'])}):")
        for h in data["h1_headings"]:
            print(f"  • {h}")

    if data["h2_headings"]:
        print(f"\n📌 H2 Headings ({len(data['h2_headings'])}):")
        for h in data["h2_headings"]:
            print(f"  • {h}")

    if data["paragraphs"]:
        print("\n📝 Sample Text Extracts:")
        for idx, p in enumerate(data["paragraphs"], 1):
            print(f"  [{idx}] {p[:120]}...")

    if data["links"]:
        print(f"\n🔗 Extracted Links ({len(data['links'])}):")
        for idx, l in enumerate(data["links"], 1):
            print(f"  [{idx}] {l['text']} -> {l['url']}")
    print("=" * 65)


def main():
    """Interactive CLI menu for Task 6."""
    while True:
        print("\n" + "=" * 60)
        print("  COGNIFYZ INTERNSHIP - TASK 6: INTERACTIVE WEB SCRAPER")
        print("=" * 60)
        print("1. 💬 Scrape Quotes (quotes.toscrape.com)")
        print("2. 📚 Scrape Book Store (books.toscrape.com)")
        print("3. 🌐 Scrape Any Custom Website (URL Analyzer)")
        print("4. 🚪 Return / Exit")

        choice = input("\nEnter choice (1-4): ").strip()
        if choice == "1":
            interactive_quotes()
        elif choice == "2":
            interactive_books()
        elif choice == "3":
            interactive_custom_url()
        elif choice == "4":
            print("Exiting Web Scraper. Goodbye!")
            break
        else:
            print("❌ Invalid selection! Choose 1-4.")


if __name__ == "__main__":
    main()
