import requests
import extruct
from w3lib.html import get_base_url
import logging


def _get_html(url):
    """Get raw HTML from a URL."""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }
    req = requests.get(url, headers=headers)
    return req.text


def _get_json_ld(html, url):
    """Fetch JSON-LD structured data."""
    logger = logging.getLogger(__name__)
    try:
        metadata = extruct.extract(
            html,
            base_url=get_base_url(html, url),
            syntaxes=["json-ld"],
        )
        return metadata["json-ld"][0]
    except:
        logger.warning("Data could not be scraped for url %s" % url)
        return {}


def _formatInstructions(instructions):
    if isinstance(instructions, str):
        return instructions.split("\n")
    elif isinstance(instructions, list):
        return list(map(lambda inst: inst["text"], instructions))
    return list()


def _formatImage(img_src):
    if isinstance(img_src, str):
        return img_src
    elif isinstance(img_src, list) and len(img_src) > 0:
        return img_src[0]
    return None


def scrape_reciped(url):
    """Parse structured data from a target page."""
    html = _get_html(url)
    metadata = _get_json_ld(html, url)
    if "recipeInstructions" in metadata:
        metadata["recipeInstructions"] = _formatInstructions(
            metadata["recipeInstructions"]
        )
    if "image" in metadata:
        metadata["image"] = _formatImage(metadata["image"])
    return metadata
