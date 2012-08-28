#!/usr/bin/env python
# This code was taken from:
#   http://docs.python.org/library/csv.html
#
import sys,re
import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding, errors='ignore'):
        self.reader = codecs.getreader(encoding)(f,errors)
                    
    def __iter__(self):
        return self

    def next(self):
        line = self.reader.next().encode("utf-8")
        line = line.strip()
        line = re.sub('""',"'",line)
        return line

class UnicodeCSVReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding. If a header is detected
    in "f", it will be stored in the class variable "header".
    """

    def __init__(self, f, encoding="utf-8", errors='ignore',
                 forceHeader=False, **kwds):

        self.header = None
        self.isCSV = True
        recoder = UTF8Recoder(f, encoding, errors)
        inlines = []
        for i in range(10):
            inline = recoder.next()
            if not inline:
                break
            inline = inline.strip()
            if len(inline) == 0:
                continue
            inlines.append(inline)

        recoder.reader.seek(0)
        
        # Check out the file to see if it looks like
        # a csv file. It could just be a plain
        # text file...
        try:
            # try to determine the dialect...
            d = csv.Sniffer().sniff('\n'.join(inlines))
        except csv.Error:
            d = None

        if d is not None and d.delimiter == ',':
            self.CSV = True
            self.reader = csv.reader(recoder, dialect=d, **kwds)
            
            # See if we can auto-detect a header
            hasHeader = csv.Sniffer().has_header('\n'.join(inlines))
            if hasHeader:
                # double-check the guess about the header
                firstLine = self.reader.next()
                if len(firstLine[0]) > 100:
                    hasHeader = False
                recoder.reader.seek(0)

            if forceHeader or hasHeader:
                self.header = self.reader.next()

        else:
            self.isCSV = False
            self.reader = recoder.reader
            
    def next(self):
        row = self.reader.next()
        if self.isCSV:
            return [unicode(s, "utf-8") for s in row]
        else:
            return [row.strip()]

    def __iter__(self):
        return self

class UnicodeCSVWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
        
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

if __name__ == "__main__":

    #csvfile = open("unicodeExamps.txt", "rb")
    #csvfile = open("ChaseCalls_meta.txt", "rb")
    #csvfile = open("CA_FirstPosts.txt", "rb")
    #csvfile = open("ATT_feb_7-10_grading_period.csv","rb")
    csvfile = open("testline.csv","rb")
    #csvfile = open("ChaseCalls.txt", "rb")
    #csvfile = open("ATT-Bad-Chats-1.csv", "rb")
    myReader = UnicodeCSVReader(csvfile)
    if myReader.header is not None:
        print "Header:",myReader.header
    myWriter = UnicodeCSVWriter(sys.stdout,delimiter=",")
    for row in myReader:
        length = len(row)
        print "%d: "%length,
        for item in row:
            print "%s::"%item.encode('ascii','ignore'),
        print
        #myWriter.writerow(row)
        
    sys.exit(0)
    
