import imageio
from os import path
from glob import glob

LAYOUT = "/home/joris/nemaNAS/jaapjan/Tray layout.csv"

folder = '/home/joris/nemaNAS/jaapjan/Images/'

loc_map = {}

with open(LAYOUT) as layout_file:
	header = layout_file.readline()

	for line in layout_file:
		if line.startswith(','):
			continue 
		line = line.strip().split(',')

		try:
			loc_map[line[2]] = f"{line[0]}_{line[1]}_{line[2]}_{line[3]}"
		except IndexError:
			pass



for cam_folder in glob(folder+"*"):
	images = sorted(list(glob(cam_folder+"/*")))
	locations = [image.split("_")[0] for image in images]

	locations = [path.basename(loc) for loc in locations]
	uniq_locations = list(set(locations))

	for loc in uniq_locations:
		loc_images = []

		for img in images:
			bn = path.basename(img)
			if bn.startswith(loc):
				loc_images.append(img)

		loc_images = sorted(loc_images)
		loc_images = [imageio.imread(img) for img in loc_images]


		name = f"{loc_map[loc]}.gif"
		imageio.mimsave(f'~/nemaNAS/jaapjan/share/{name}', loc_images)


