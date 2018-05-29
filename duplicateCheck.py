
import io
from difflib import SequenceMatcher


lines_large = [line.rstrip('\n') for line in io.open('/Users/jiangying/Desktop/scrapy/texhr/texhr/output_large.txt')]
lines_small = [line.rstrip('\n') for line in io.open('/Users/jiangying/Desktop/scrapy/texhr/texhr/spiders/output.txt')]

largelist = []
for line in lines_large:
    # print line.split(',')[2]
    largelist.append(line.split(',')[2].replace(" ", ""))

small_list = []
for line in lines_small:
    # print line.split(',')[0][1:]
    small_list.append(line.split(',')[0][1:])

new_compy=[]
for compy in small_list:
    if compy not in largelist:
        new_compy.append(compy)

        # if (SequenceMatcher(None, compy, compy1).ratio() > 0.8):
        #     print SequenceMatcher(None, compy, compy1).ratio()
        #     print compy
        #     print compy1
for compy in new_compy:
    for compy1 in largelist:
        if (SequenceMatcher(None, compy, compy1).ratio() > 0.95):
            print SequenceMatcher(None, compy, compy1).ratio()
            print compy
            print compy1
print new_compy.__len__()