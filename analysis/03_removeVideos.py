import magic
import os
import argparse

def main():
	parser = argparse.ArgumentParser("Remove videos")
	parser.add_argument("path")
	args = parser.parse_args()

	m = magic.Magic(mime=True)
	nb = 0

	for f in os.listdir(args.path):
		filepath = os.path.join(args.path, f)
		if os.path.isfile(filepath) and m.from_file(filepath).startswith("video"):
			os.remove(filepath)
			nb += 1

	print("Removed", nb, "files in ", args.path)

if __name__ == '__main__':
	main()
