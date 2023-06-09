import numpy as np
import os
import argparse
import json
import warnings

def loadJson(path):
	f = open(path)
	data = json.load(f)
	f.close()
	return data

def writeJson(data, path):
	w = open(path, "w")
	json.dump(data, w, ensure_ascii=False)
	w.close()

def moving_average(x, width):
	return np.convolve(x, np.ones(width), 'valid') / width

def computeNormAvg(movie, avgWidth):
	neg = [entry[1] for entry in movie]
	pos = [entry[2] for entry in movie]
	avgNeg = moving_average(neg, avgWidth)
	avgPos = moving_average(pos, avgWidth)
	diff = []
	for i in range(len(avgPos)):
		diff.append(avgPos[i] - avgNeg[i])
	x = [entry[0] for entry in movie[:len(avgPos)]]
	factor = 100 / x[-1]
	normx = [r * factor for r in x]
	return normx, avgNeg, avgPos, diff

def main():
	parser = argparse.ArgumentParser("Compute the dramatic signature on precomputed sentiment analysis")
	parser.add_argument("movies", help="Json movies files")
	parser.add_argument("sentiment", help="Sentiment analysis dir")
	parser.add_argument("avg", help="Moving average width", type=int)
	parser.add_argument("poly", help="Polynomial degree", type=int)
	parser.add_argument("output", help="Output json file")
	parser.add_argument("-v", help="Verbose", dest="verbose", action="store_true")
	args = parser.parse_args()

	warnings.simplefilter('ignore', np.RankWarning)
	movies = loadJson(args.movies)
	signatures = loadJson(args.output) if os.path.isfile(args.output) else {}
	i = 0
	ign = []

	for m in movies:
		uuid = m["uuid"]
		analysisFile = os.path.join(args.sentiment, uuid + ".json")
		if os.path.isfile(analysisFile):
			analysis = loadJson(analysisFile)
			if len(analysis) < args.avg: # Not enough subtitles to compute anything
				ign.append((uuid, m["title"]))
				continue
			x, neg, pos, diff = computeNormAvg(analysis, args.avg)
			fitNeg = list(np.polyfit(x, neg, args.poly))
			fitNeg.reverse()
			fitPos = list(np.polyfit(x, pos, args.poly))
			fitPos.reverse()
			fitDiff = list(np.polyfit(x, diff, args.poly))
			fitDiff.reverse()
			if uuid not in signatures:
				signatures[uuid] = {}
			signatures[uuid]["signature"] = (fitNeg, fitPos, fitDiff)
		# Progress
		i += 1
		if args.verbose and i % 100 == 0:
			print("Progress", i, "/", len(movies))

	print("Computed signatures on", len(signatures), "/", len(movies))
	if len(ign) > 0:
		print("Ignored", len(ign), "movies:")
		print(str.join("\n", [m[1] + " (" + m[0] + ")" for m in ign]))
	writeJson(signatures, args.output)

if __name__ == '__main__':
	main()
