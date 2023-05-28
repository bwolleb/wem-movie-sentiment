import srt
import os
import argparse
import json
import chardet

def main():
	parser = argparse.ArgumentParser("Convert SRT subtitles to json")
	parser.add_argument("srt")
	parser.add_argument("output")
	args = parser.parse_args()

	nb = 0
	for fn in os.listdir(args.srt):
		filepath = os.path.join(args.srt, fn)
		if os.path.isfile(filepath) and fn.endswith(".srt"):
			try:
				# Detect charset
				f = open(filepath, "rb")
				raw = f.read()
				f.close()
				encoding = chardet.detect(raw)["encoding"]

				# Read SRT
				subtitle_generator = srt.parse(raw.decode(encoding), ignore_errors=True)
				f.close()

				# Convert to list where each item is (start, end, text)
				subtitles = list(subtitle_generator)
				output_subtitles = []
				for s in subtitles:
					output_subtitles.append([s.start.total_seconds(), s.end.total_seconds(), s.content])

				# Save to json
				w = open(os.path.join(args.output, fn.replace(".srt", ".json")), "w")
				json.dump(output_subtitles, w)
				w.close()

				nb += 1
			except Exception as e:
				print("Exception on file", fn, e)

	print("Converted", nb, "files")

if __name__ == '__main__':
	main()
