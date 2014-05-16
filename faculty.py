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

def print_header(out, start, end):
    out.write('year')
    for y in range(start, end+1):
        out.write('\t%s' % y)
    out.write('\n')

def print_years(out, start, end, data, label):
    out.write(label)
    for y in range(start, end+1):
        out.write('\t%s' % (data[y],))
    out.write('\n')

def main():
    load_data()
    out = open(outfile, 'w')
    print_header(out, year_min, year_max)
    print_years(out, year_min, year_max, cs_lines, 'cs')
    print_years(out, year_min, year_max, ece_lines, 'ece')
    out.close()

if __name__ == '__main__':
    main()

    
    
