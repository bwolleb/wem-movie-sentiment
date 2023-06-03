from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import torch
import matplotlib.pyplot as plt
import datetime
import torch
import os
import argparse
import json

def loadJson(path):
	f = open(path)
	data = json.load(f)
	f.close()
	return data

def writeJson(data, path):
	w = open(path, "w")
	json.dump(data, w, ensure_ascii=False)
	w.close()

def analyzeTxt(tokenizer, model, device, text):
	encoded_input = tokenizer(text, max_length=512, truncation=True, return_tensors='pt').to(device)
	output = model(**encoded_input)
	scores = output[0][0].detach().cpu().numpy()
	scores = softmax(scores)
	return scores

def analyzeSubs(tokenizer, model, device, subtitles, window):
	result = [] # Entries are (start, neg, pos)
	subs = []
	for sub in subtitles:
		subs.append(sub)
		start = sub[0]
		while start - subs[0][0] > window:
			txt = str.join(" ", [s[2] for s in subs[:-1]])
			scores = analyzeTxt(tokenizer, model, device, txt)
			entry = (subs[0][0], scores[0].item(), scores[2].item()) # Convert to  native float for serialization
			result.append(entry)
			subs.pop(0)
	return result

def main():
	parser = argparse.ArgumentParser("Perform sentiment analysis on movies")
	parser.add_argument("movies", help="Json movies files")
	parser.add_argument("sub", help="Subtitles dir")
	parser.add_argument("window", help="Window width in seconds", type=int)
	parser.add_argument("output", help="Path to output dir")
	args = parser.parse_args()

	# cuda setup if available
	if torch.cuda.is_available(): 
		dev = "cuda:0" 
	else: 
		dev = "cpu" 
	device = torch.device(dev)

	# model setup
	modelName = "cardiffnlp/twitter-roberta-base-sentiment-latest"
	tokenizer = AutoTokenizer.from_pretrained(modelName)
	config = AutoConfig.from_pretrained(modelName)
	# PT
	model = AutoModelForSequenceClassification.from_pretrained(modelName)
	model.to(device)

	movies = loadJson(args.movies)

	# Stats
	nb = 0
	totTime = 0

	for m in movies:
		uuid = m["uuid"]
		subFile = os.path.join(args.sub, uuid + ".json")
		if not os.path.isfile(subFile):
			continue
		# Skip if result already exists
		resultFile = os.path.join(args.output, uuid + ".json")
		if os.path.isfile(resultFile):
			continue
		tStart = datetime.datetime.now()
		subs = loadJson(subFile)
		analysis = analyzeSubs(tokenizer, model, device, subs, args.window)
		writeJson(analysis, resultFile)

		# Stats
		nb += 1
		tEnd = datetime.datetime.now()
		secs = (tEnd - tStart).total_seconds()
		totTime += secs
		remaining = len(movies) - nb
		meanTime = int(totTime / nb)
		estHours = round(remaining * meanTime / 3600, 2)
		print("Processed", m["title"], "in", secs, "seconds, mean seconds per film:", meanTime, ",", nb, "/", remaining, ", estimated:", estHours, "hours")

if __name__ == '__main__':
	main()
