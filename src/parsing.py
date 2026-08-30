"""parse SEC filing HTML into clean text """
from pathlib import Path
from bs4 import BeautifulSoup

def extract_text(html_path):
    with open (html_path, encoding = "utf-8") as f:
        soup =  BeautifulSoup(f, "html.parser")
    
    # Strip non-visible/non-prose content: scripts, styles, and
    # inline XBRL metadata blocks that aren't meant to be read as text. 

    for tag in soup(["script","style"]):
        tag.decompose()

    for tag in soup.find_all(["ix:header","ix:resources","ix:references"]):
        tag.decompose()

    for tag in soup.find_all(style = lambda v: v and "display:none" in v.replace(" ","")):
        tag.decompose()

    text = soup.get_text(separator="\n")

    cutoff = text.upper().find("SIGNATURES")
    if cutoff != -1:
        text=text[:cutoff]
    
    return text.strip()

