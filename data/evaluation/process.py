# clean.py
# script to clean data

# Remove undesirable categories from data
def clean_raw(filepath, new_filepath):

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

def clean_query(filepath, new_filepath):

    n = open(new_filepath, 'w')
    with open(filepath) as f:

        removeCat = False
        for line in f:
            if line.startswith('.X') or line.startswith('.C') or line.startswith('.K') or line.startswith('.N') or line.startswith('.B') or line.startswith('.A') or line.startswith('.T'):
                removeCat = True

            if line.startswith('.I') or line.startswith('.W'):
                removeCat = False
            
            if not removeCat:
                n.write(line)

def clean_rel(filepath, new_filepath):

    n = open(new_filepath, 'w')
    with open(filepath) as f:

        for line in f:
            line = line.split()
            #print(len(line) - len(line.strip()))
            n.write(line[0] + ' ' + line[1] + '\n')


def main():
    clean_raw('raw/cisi/CISI.ALL', 'processed/cisi/CISI.ALL')
    clean_query('raw/cisi/CISI.QRY', 'processed/cisi/CISI.QRY')
    clean_rel('raw/cisi/CISI.REL', 'processed/cisi/CISI.REL')


    clean_raw('raw/cacm/cacm.all', 'processed/cacm/cacm.all')
    clean_query('raw/cacm/query.text', 'processed/cacm/query.text')
    clean_rel('raw/cacm/qrels.text', 'processed/cacm/qrels.text')


    clean_raw('raw/med/MED.ALL', 'processed/med/MED.ALL')

    remove_empty('raw/time/TIME.RAW', 'raw/time/TIME.ALL')
    clean_time('raw/time/TIME.ALL', 'processed/time/TIME.ALL')


if __name__ == '__main__':
    main()

