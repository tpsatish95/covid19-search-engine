# process.py
# script to clean Glasgow Datasets


# Format data into .I .T .W
def clean_raw(filepath, new_filepath):

    n = open(new_filepath, 'w')
    with open(filepath) as f:

        if 'TIME' in filepath:
            previous = ''
            for line in f:
                if line.startswith('*TEXT'):
                    ID_line = line.split()
                    ID = int(ID_line[1])
                    n.write('.I ')
                    n.write(str(ID)+'\n')

                elif previous.startswith('*TEXT'):
                    n.write('.W\n')
                    n.write(line.lower())

                else:
                    n.write(line.lower())

                previous = line

        else:
            removeCat = False
            for line in f:
                if line.startswith('.X') or line.startswith('.C') or line.startswith('.K') or line.startswith('.N') or line.startswith('.B') or line.startswith('.A'):
                    removeCat = True

                if line.startswith('.I') or line.startswith('.T') or line.startswith('.W'):
                    removeCat = False
                
                if not removeCat:
                    n.write(line)


# Remove empty lines
def remove_empty_lines(filepath, new_filepath):

    n = open(new_filepath, 'w')
    with open(filepath) as f:

        for line in f:
            if line not in ['\n', '\r\n']:
                n.write(line)


# Format queries into .I .W
def clean_query(filepath, new_filepath):

    n = open(new_filepath, 'w')
    with open(filepath) as f:

        if 'TIME' in filepath:
            previous = ''
            for line in f:
                if line.startswith('*FIND'):
                    ID_line = line.split()
                    n.write('.I ')
                    n.write(ID_line[1] + '\n')

                elif previous.startswith('*FIND'):
                        n.write('.W\n')
                        n.write(line.lower())

                else:
                    n.write(line.lower())

                previous = line

        else:    
            removeCat = False
            for line in f:
                if line.startswith('.X') or line.startswith('.C') or line.startswith('.K') or line.startswith('.N') or line.startswith('.B') or line.startswith('.A') or line.startswith('.T'):
                    removeCat = True

                if line.startswith('.I') or line.startswith('.W'):
                    removeCat = False
                
                if not removeCat:
                    n.write(line)


# Format rels into [query ID][doc ID] list
def clean_rel(filepath, new_filepath):

    n = open(new_filepath, 'w')
    with open(filepath) as f:

        if 'MED' in filepath:
            for line in f:
                line = line.split()
                n.write(line[0] + ' ' + line[2] + '\n')

        elif 'TIME' in filepath:
            for line in f:
                line = line.split()

                for doc_id in line[1:]:
                    n.write(line[0] + ' ' + doc_id + '\n')

        else:
            for line in f:
                line = line.split()
                n.write(line[0] + ' ' + line[1] + '\n')


# Find missing numbers in a sequence
def find_missing(lst):
    return [i for x, y in zip(lst, lst[1:])  
        for i in range(x + 1, y) if y - x > 1] 


# Remove queries that have no relevant docs
def remove_query(r_filepath, q_filepath, t_r_filepath, t_q_filepath):

    # Identify queries missing in rel
    n = open(t_r_filepath, 'w')
    with open(r_filepath) as f:

        prev = 0
        cur = 0
        present = []
        for line in f:
            n.write(line)
            line = line.split()
            prev = cur
            cur = line[0]
            if(cur != prev):
                present.append(int(cur))

    f.close()
    n.close()

    missing = find_missing(present)
    # print('Missing = ')
    # print(missing)

    # Remove queries which are missing in rel
    toRemove = False
    n = open(t_q_filepath, 'w')
    with open(q_filepath) as f:
        for line in f:
            if line.startswith('.I'):
                IDline = line.split()
                if int(IDline[1]) in missing:
                    toRemove = True

                else:
                    toRemove = False

            if toRemove == False:
                n.write(line)
    f.close()
    n.close()


# Re-number queries in query and rel
def relabel_query(t_r_filepath, t_q_filepath, new_r_filepath, new_q_filepath):
    
    n = open(new_r_filepath, 'w')
    with open(t_r_filepath) as f:
        prev = 0
        cur = 0
        i = 0
        for line in f:
            line = line.split()
            prev = cur
            cur = line[0]

            if (cur != prev):
                i += 1

            n.write(str(i) + " " + line[1] + '\n')

    n.close()
    f.close()

    n = open(new_q_filepath, 'w')
    with open(t_q_filepath) as f:
        i = 1
        for line in f:
            if line.startswith('.I'):
                line = line.split()
                n.write(line[0] + " " + str(i) + '\n')
                i+=1

            else:
                n.write(line)

    n.close()
    f.close()


def relabel_ID():
    return 0


def main():

    # CISI Dataset
    clean_raw('raw/cisi/CISI.ALL', 'cisi/CISI.ALL')
    clean_query('raw/cisi/CISI.QRY', 'cisi/CISI.QRY')
    clean_rel('raw/cisi/CISI.REL', 'cisi/CISI.REL')
    remove_query('cisi/CISI.REL', 'cisi/CISI.QRY', 'cisi/reltemp', 'cisi/querytemp')
    relabel_query('cisi/reltemp', 'cisi/querytemp', 'cisi/CISI.REL', 'cisi/CISI.QRY')

    # CACM Dataset
    clean_raw('raw/cacm/cacm.all', 'cacm/cacm.all')
    clean_query('raw/cacm/query.text', 'cacm/query.text')
    clean_rel('raw/cacm/qrels.text', 'cacm/qrels.text')
    remove_query('cacm/qrels.text', 'cacm/query.text', 'cacm/reltemp', 'cacm/querytemp')
    relabel_query('cacm/reltemp', 'cacm/querytemp', 'cacm/qrels.text', 'cacm/query.text')

    # MED Dataset
    clean_raw('raw/med/MED.ALL', 'med/MED.ALL')
    clean_query('raw/med/MED.QRY', 'med/MED.QRY')
    clean_rel('raw/med/MED.REL', 'med/MED.REL')
    remove_query('med/MED.REL', 'med/MED.QRY', 'med/reltemp', 'med/querytemp') # No queries to remove

    # TIME Dataset
    # remove_empty_lines('raw/time/TIME.RAW', 'raw/time/TIME.ALL')
    # remove_empty_lines('raw/time/TIME.QUE', 'raw/time/TIME.QUE_')
    # remove_empty_lines('raw/time/TIME.REL', 'raw/time/TIME.REL_')

    # clean_raw('raw/time/TIME.ALL', 'time/TIME.ALL')
    # clean_query('raw/time/TIME.QUE_', 'time/TIME.QUE')
    # clean_rel('raw/time/TIME.REL_', 'time/TIME.REL')
    # remove_query('time/TIME.REL', 'time/TIME.QUE', 'time/reltemp', 'time/querytemp') # No queries to remove


if __name__ == '__main__':
    main()

