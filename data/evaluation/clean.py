# clean.py
# script to clean data

# Remove undesirable categories from data
def clean_cat(filepath, new_filepath):

	n = open(new_filepath, 'w')
	with open(filepath) as f:

		removeCat = False
		for line in f:
			if line.startswith('.X') or line.startswith('.C') or line.startswith('.K') or line.startswith('.N') or line.startswith('.B') or line.startswith('.A'):
				removeCat = True

			if line.startswith('.I') or line.startswith('.T') or line.startswith('.W'):
				removeCat = False
			
			if not removeCat:
				n.write(line)

# Split time into ID and body (.W)
def clean_time(filepath, new_filepath):
	
	n = open(new_filepath, 'w')
	with open(filepath) as f:

		previous = ''
		for line in f:

			if line.startswith('*TEXT'):
				# line.split() # for some reason not recognizing split on spaces 
				ID = int(line[6] + line[7] + line[8])
				n.write('.I ')
				n.write(str(ID)+'\n')

			elif previous.startswith('*TEXT'):
				n.write('.W\n')

			else:
				n.write(line.lower())

			previous = line


# Remove empty lines
def remove_empty(filepath, new_filepath):

	n = open(new_filepath, 'w')
	with open(filepath) as f:

		for line in f:
			# ignore empty lines
			if line not in ['\n', '\r\n']:
				n.write(line)


def main():
	clean_cat('raw/cisi/CISI.ALL', 'clean/cisi/CISI.ALL')
	clean_cat('raw/cacm/cacm.all', 'clean/cacm/cacm.all')
	clean_cat('raw/med/MED.ALL', 'clean/med/MED.ALL')

	remove_empty('raw/time/TIME.RAW', 'raw/time/TIME.ALL')
	clean_time('raw/time/TIME.ALL', 'clean/time/TIME.ALL')


if __name__ == '__main__':
	main()

