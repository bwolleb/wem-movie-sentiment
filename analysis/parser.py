import mwparserfromhell
import mwxml
import re
import uuid
import sys
import argparse
import json

yearRe = re.compile("(19|20)[0-9]{2}")

def main():
	parser = argparse.ArgumentParser("Wikipedia film parser")
	parser.add_argument("dump", help="Wikipedia dump")
	parser.add_argument("movies", help="Movies json to write")
	args = parser.parse_args()

	dump = mwxml.Dump.from_file(args.dump)
	movies = []

	exc = 0
	for page in dump:
		if page.title.lower().endswith("film)"):
			try:
				rev = next(page)
				if rev.page.namespace != 0: continue # Parse articles only
				wikicode = mwparserfromhell.parse(rev.text)
				infoboxes = [n for n in wikicode.nodes if "Infobox" in n]
				if len(infoboxes) == 0:
					continue
				infobox = infoboxes[0]
				movie = {}
				movie["uuid"] = uuid.uuid1().hex

				title = page.title
				if infobox.has("name"):
					nameNode = infobox.get("name").value
					title = str(nameNode.strip_code()).strip()
					movie["title"] = title
				else:
					movie["title"] = page.title.replace("(film)", "").strip()

				if not infobox.has("released"):
					continue
				releaseNode = infobox.get("released").value
				parts = releaseNode.filter_text()
				year = None
				for part in parts:
					asStr = str(part)
					if yearRe.match(asStr):
						year = int(asStr)
						break
				if year is None:
					continue
				movie["year"] = year

				if infobox.has("image"):
					img = infobox.get("image").value.strip()
					movie["image"] = img

				if infobox.has("starring"):
					starring = infobox.get("starring").value
					actors = [x.value for x in starring.filter_text() if x not in [" ","\n"]][1:]
					movie["actors"] = actors

				sections = wikicode.get_sections()
				for sect in sections:
					if type(sect.nodes[0]) == mwparserfromhell.nodes.heading.Heading and sect.nodes[0].title == "Plot":
						code = mwparserfromhell.wikicode.Wikicode(sect.nodes[1:])
						plot = code.strip_code().replace("\n", " ")
						movie["plot"] = plot
						break

				movies.append(movie)
			except Exception as e:
				exc += 1
				print("EXCEPT", exc, page.title, e)

	print("Parsed", len(movies), "movies, excepted", exc)
	w = open(args.movies, "w")
	json.dump(movies, w, ensure_ascii=False)
	w.close()

if __name__ == '__main__':
	main()
