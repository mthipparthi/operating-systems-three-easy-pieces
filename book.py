#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pathlib
import threading
from pathlib import Path

import bs4
import requests
from PyPDF2 import PdfFileMerger


def scrape_urls():

    url = "http://pages.cs.wisc.edu/~remzi/OSTEP/#book-chapters"
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    base_url = "http://pages.cs.wisc.edu/~remzi/OSTEP/{}"
    with open("./urls.txt", "w+") as f:
        for link in soup.find_all("a", {"style": "color:black"}):
            print(base_url.format(link.attrs["href"]), file=f)


def scrape_urls2():

    url = "http://pages.cs.wisc.edu/~remzi/OSTEP/#book-chapters"
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    base_url = "http://pages.cs.wisc.edu/~remzi/OSTEP/{}"
    rslt = {}
    for link in soup.find_all("td"):
        el = link.find("small")
        small = link.find("small").get_text() if el else ""
        el = link.find("a")
        url = el.attrs["href"] if el and "href" in el.attrs else ""
        try:
            small = int(small)
            small = 100 + small
        except:
            small = None
        if small and url:
            rslt[small] = base_url.format(url)

    with open("./urls.txt", "w+") as f:
        for k in sorted(rslt.keys()):
            print(k, rslt[k], file=f)


def download_book():
    def download(i, url):
        url = url.strip()
        print(f" {i} downloading {url}")
        res = requests.get(url, timeout=120)
        print(f"{res}")
        if res.ok:
            last_name = url.split("/")[-1]
            file_name = f"./output/{i}-{last_name}"
            print(f"{last_name}{file_name}")
            with open(f"{file_name}", "wb") as f:
                f.write(res.content)

    threads = []

    with open("./urls.txt") as f:
        for line in f:
            i, url = line.split(" ")
            print(f"{i}{url}")
            t = threading.Thread(target=download, args=(i, url))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()


def merge_pdf():
    output_dir = Path("./output")
    files = [file.resolve() for file in sorted(output_dir.glob("*.pdf"))]

    files = files[-2:] + files[0:-2]

    # print(files)
    merger = PdfFileMerger()

    for pdf in files:
        merger.append(open(pdf, "rb"))

    with open("book.pdf", "wb") as fout:
        merger.write(fout)


def read_file():
    f = open("./urls3.txt")
    for i in f:
        index, url = i.split(" ")
        print(f"{index}{url}")


if __name__ == "__main__":
    # scrape_urls2()
    # download_book()
    merge_pdf()
    # read_file()

