from sys import argv

sol_ids = [i.split('.')[0] for i in argv[2:]]



with open(argv[1]) as gff:
    for line in gff:
        if line.startswith("#"):
            continue

        line = line.strip().split()
        if line[2] != 'gene':
            continue

        alias = "".join([x for x in line[-1].split(';') if 'Alias' in x]).replace('Alias=','')
        
        if alias in sol_ids:
            print("\t".join(line))
        
