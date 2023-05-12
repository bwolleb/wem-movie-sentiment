import io
import os
import sys
import re
import argparse
import requests
import zipfile
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

domain = "https://www.opensubtitles.org"
searchPath = "/fr/search2/sublanguageid-eng/moviename-"

def getMovie(title, year, yearDelta=0, verbose=False):
	url = domain + searchPath + title
	if verbose: print("GET", url, file=sys.stderr)
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")

	props = soup.find_all("p", itemprop=["aggregateRating", "director", "creator", "actor"])
	if len(props) > 0:
		if verbose: print("Found exact match", file=sys.stderr)
		return page.url

	candidates = soup.find_all("a", class_="bnone")

	if verbose: print("Searching through", len(candidates), "candidates", file=sys.stderr)
	match = []
	for c in candidates:
		cTitle, cYear = c.getText().split("\n")
		cYear = int(re.sub("[^\w]", "", cYear))
		if abs(year - cYear) > yearDelta:
			continue
		titleSimilarity = SequenceMatcher(None, title, cTitle).ratio()
		link = domain + c.get("href")
		match.append((titleSimilarity, link))

	if len(match) == 0:
		if verbose: print("Movie not found", file=sys.stderr)
		return ""

	match = sorted(match, key=lambda x: x[0], reverse=True)
	if verbose: print("Matches:", match, file=sys.stderr)
	return match[0][1]

def getSubs(movieurl, verbose=False):
	url = movieurl + "/sort-7/asc-0"
	if verbose: print("GET", url, file=sys.stderr)
	moviePage = requests.get(url) # 
	movieSoup = BeautifulSoup(moviePage.content, "html.parser")
	subsTable = movieSoup.find(id="search_results")
	subRow = subsTable.find_all("tr")[1]
	subCol = subRow.find_all("td")[4]
	subLink = subCol.find("a")
	return domain + subLink.get("href")

def getSrt(fileurl, verbose=False):
	if verbose: print("GET", fileurl, file=sys.stderr)
	subZipData = requests.get(fileurl)
	buf = io.BytesIO(subZipData.content)
	subZip = zipfile.ZipFile(buf)

	for fn in subZip.namelist():
		if fn.endswith(".srt"):
			if verbose: print("Found subs", fn, file=sys.stderr)
			srtRaw = subZip.read(fn)
			return srtRaw
	return ""

def getSubtitles(title, year, yearDelta, verbose=False):
	movieUrl = getMovie(title, year, yearDelta, verbose)
	if movieUrl == "":
		return ""
	subUrl = getSubs(movieUrl, verbose)
	srt = getSrt(subUrl, verbose)
	return srt

def main():
	parser = argparse.ArgumentParser("GetSubs")
	parser.add_argument("-t", help="Title of the movie", type=str, required=True, dest="title")
	parser.add_argument("-y", help="Year of the movie", type=int, required=True, dest="year")
	parser.add_argument("-d", help="Year delta", type=int, required=False, default=0, dest="yearDelta")
	parser.add_argument("-v", help="Verbose", required=False, action="store_true", dest="verbose")
	parser.add_argument("-o", help="Output file", required=False, default=None, dest="output")
	args = parser.parse_args()

	cleanTitle = re.sub('[^\w ]', '', args.title)
	subs = getSubtitles(cleanTitle, args.year, args.yearDelta, args.verbose)
	if len(subs) > 0:
		if args.output is not None:
			w = open(args.output, "wb")
			w.write(subs)
			w.close()
		else:
			sys.stdout.buffer.write(subs)

if __name__ == "__main__":
	main()


