from collections import defaultdict
from sys import stdout

infile =  'faculty.csv'
outfile = 'by_year.tsv'
deltafile = 'changes.txt'

cs_tt =  defaultdict(int)
ece_tt =  defaultdict(int)

cs_teaching =  defaultdict(int)
ece_teaching =  defaultdict(int)

leave =  defaultdict(int)
cs_leave =  defaultdict(int)
ece_leave =  defaultdict(int)

delta = defaultdict(list)

year_min = 2525
year_max = 2014

def load_data():
    global year_max, year_min
    for line in open(infile):
        (fn,ln,status,prog,start,last,leave) = line.strip().split(',')[:7]
        name = '%s_%s' % (fn, ln)
        if status != 'TT':
            continue
        start = yearify(start)
        last = yearify(last)
        delta[start].append('+' + name)
        delta[last].append('-' + name)
        onleave = map(yearify,leave.split())
        year_min = min(start, year_min)
        for year in range(start, (last or year_max)+1):
            if prog == 'C':
                cs_tt[year] += 1
            elif prog == 'E':
                ece_tt[year] += 1
            else:
                print 'Bad program value', line

def yearify(s):
    """converts string into an integer representing a year by striping
    and ? off, convert to an int, return"""
    return int(s.strip().strip('?')) if s else ''

def main():
    load_data()
    years = range(year_min, year_max+1)
    out = open(outfile, 'w')
    out.write( "\t".join(['year']+ [str(y) for y in years]) + "\n")
    out.write( "\t".join(['CS']+[str(cs_tt[y]) for y in years]) + "\n")
    out.write( "\t".join(['ECE']+[str(ece_tt[y]) for y in years]) + "\n")
    out.close()
    out = open(deltafile, 'w')
    for y in years:
        out.write("%s: %s\n" % (y, ', '.join(sorted(delta[y]))))
    out.close()    

if __name__ == '__main__':
    main()

    
    
