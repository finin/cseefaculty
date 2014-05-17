from collections import defaultdict
from sys import stdout

infile =  'faculty.csv'
outfile = 'by_year.tsv'

cs_lines =  defaultdict(int)
ece_lines =  defaultdict(int)

leave =  defaultdict(int)
cs_leave =  defaultdict(int)
ece_leave =  defaultdict(int)

year_min = 2525
year_max = 2014

def load_data():
    global year_max, year_min
    for line in open(infile):
        (fn,ln,status,prog,start,end,leave) = line.split(',')
        if status != 'TT':
            continue
        start = yearify(start)
        end = yearify(end) if end.strip() else year_max
        onleave = map(yearify,leave.split())
        if start < year_min:
            year_min = start
        if end > year_max:
            year_max = year
        for year in range(start, end+1):
            if prog == 'C':
                cs_lines[year] += 1
            elif prog == 'E':
                ece_lines[year] += 1
            else:
                print 'Bad program value', line

def yearify(s):
    """converts string into an integer representing a year by striping
    and ? off, convert to an int, return"""
    return int(s.strip().strip('?'))

def main():
    load_data()
    years = range(year_min, year_max+1)
    out = open(outfile, 'w')
    out.write( "\t".join(['year']+ [str(y) for y in years]) + "\n")
    out.write( "\t".join(['CS']+[str(cs_lines[y]) for y in years]) + "\n")
    out.write( "\t".join(['ECE']+[str(ece_lines[y]) for y in years]) + "\n")
    out.close()

if __name__ == '__main__':
    main()

    
    
