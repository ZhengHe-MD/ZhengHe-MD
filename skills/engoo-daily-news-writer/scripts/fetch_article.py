#!/usr/bin/env python3
"""
Fetch and parse article content from a URL.
Outputs JSON with only the essential content for ESL lesson creation.

Usage:
    python3 fetch_article.py <url> [output.json]

If output file is not specified, prints to stdout.

Dependencies: beautifulsoup4, requests (pip install beautifulsoup4 requests)
"""

import json
import re
import sys

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.", file=sys.stderr)
    print("Install with: pip install beautifulsoup4 requests", file=sys.stderr)
    sys.exit(1)


def fetch_article(url):
    """Fetch and extract essential article content."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP {e.response.status_code}: {e.response.reason}", "url": url}
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "url": url}

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract title
    title = ""
    # Try og:title first
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        title = og_title['content']
    # Try <title> tag
    elif soup.title and soup.title.string:
        title = soup.title.string.strip()

    # Clean title (remove site name suffix)
    if title:
        title = re.split(r'\s+[-|–—]\s+(?=[^-|–—]*$)', title)[0].strip()

    # Extract description
    description = ""
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        description = meta_desc['content']
    else:
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            description = og_desc['content']

    # Remove unwanted elements
    for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside',
                         'form', 'iframe', 'svg', 'noscript', 'figure', 'picture']):
        element.decompose()

    # Try to find main content area
    main_content = None
    selectors = [
        'article',
        'main',
        '[role="main"]',
        '.article-body',
        '.article-content',
        '.post-content',
        '.entry-content',
        '.story-body',
        '.main-content',
        '#article-body',
        '#content',
    ]

    for selector in selectors:
        main_content = soup.select_one(selector)
        if main_content:
            break

    # Fallback to body
    if not main_content:
        main_content = soup.body if soup.body else soup

    # Extract paragraphs and headings
    content = []
    seen_texts = set()

    # Standard content tags + font (for older sites like Paul Graham's)
    for element in main_content.find_all(['p', 'h1', 'h2', 'h3', 'blockquote', 'font']):
        text = element.get_text(separator=' ', strip=True)

        # Skip empty or very short text
        if len(text) < 50:
            continue

        # Skip navigation/UI patterns
        text_lower = text.lower()
        skip_patterns = [
            r'^(home|about|contact|search|menu|skip to)',
            r'(click here|read more|sign up|log in|subscribe)',
            r'(follow us|share this|related posts|you might also)',
            r'^(previous|next)\s*(post|article|page|$)',
            r'^\d+\s*(comments?|shares?|views?)',
            r'(cookie|privacy policy|terms of)',
        ]
        if any(re.search(p, text_lower) for p in skip_patterns):
            continue

        # Must contain sentence-ending punctuation
        if not re.search(r'[.!?]', text):
            continue

        # Deduplicate
        normalized = re.sub(r'\s+', ' ', text_lower[:100])
        if normalized in seen_texts:
            continue
        seen_texts.add(normalized)

        # Determine type (font -> p)
        elem_type = element.name if element.name in ['p', 'h1', 'h2', 'h3', 'blockquote'] else 'p'

        content.append({
            "type": elem_type,
            "text": text
        })

    # Limit content to ~600 words (but always include at least first paragraph)
    max_words = 600
    total_words = 0
    limited_content = []

    for i, item in enumerate(content):
        word_count = len(item['text'].split())
        # Always include at least the first item, even if it exceeds limit
        if i == 0:
            limited_content.append(item)
            total_words = word_count
        elif total_words + word_count <= max_words:
            limited_content.append(item)
            total_words += word_count
        else:
            break

    return {
        "url": url,
        "title": title,
        "description": description,
        "word_count": total_words,
        "content": limited_content
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_article.py <url> [output.json]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    result = fetch_article(url)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    json_output = json.dumps(result, indent=2, ensure_ascii=False)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"Saved: {result['title']}", file=sys.stderr)
        print(f"Words: {result['word_count']}", file=sys.stderr)
        print(f"Paragraphs: {len(result['content'])}", file=sys.stderr)
    else:
        print(json_output)


if __name__ == "__main__":
    main()
