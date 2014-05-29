from collections import defaultdict
from sys import stdout
import numpy as np
import matplotlib.pyplot as plt

infile =  'faculty.csv'
outfile = 'by_year.tsv'
deltafile = 'changes.txt'

cs_tt =  defaultdict(int)
ece_tt =  defaultdict(int)

cs_who = defaultdict(list)
ece_who = defaultdict(list)

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
                cs_who[year].append('%s_%s' % (ln,fn))
            elif prog == 'E':
                ece_tt[year] += 1
                ece_who[year].append('%s_%s' % (ln,fn))
            else:
                print 'Bad program value', line

def yearify(s):
    """converts string into an integer representing a year by striping
    and ? off, convert to an int, return"""
    return int(s.strip().strip('?')) if s else ''

def graph_tt():
    years = range(year_min, year_max+1)    
    N = len(years)
    width = 0.5
    ind = np.arange(0, 4*N, 4)    # the x locations for the groups
    cs = [cs_tt[y] for y in years]
    ece = [ece_tt[y] for y in years]
    top = max(max(cs),max(ece))
    p1 = plt.bar(ind, cs, width, color='r')
    p2 = plt.bar(ind, ece, width, color='y', bottom=cs)
    # p2 = plt.bar(ind+width, ece, width, color='y')
    plt.ylabel('TT lines')
    plt.title('CSEE Tenure Track lines by year')
    plt.xticks(ind+width/2.0, years)
    plt.yticks(np.arange(0,top+5,10))
    plt.legend( (p1[0], p2[0]), ('CS', 'ECE') )
    plt.show()

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
    print sorted(cs_who[2013])
    # graph_tt()

if __name__ == '__main__':
    main()

    
    
