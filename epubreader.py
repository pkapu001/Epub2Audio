import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import sys
import codecs

# bookname = 'Slime_ln11.epub'
# outputname = "Slime_LN11"

class EpubReader:
    blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', ]
    getlist = ['chapter', 'prologue', 'epilogue']
    def __init__(self,bookname):
        self.bookname = bookname
        self.book = epub.read_epub(f'{bookname}.epub')
        self.parts = self.__getParts()
        self.getChapters()
        self.total_cost = self.cal_cost(self.total_char)

    cal_cost = lambda self,l: (l/1000)*0.02

    def chap2text(self,chap):
        output = ''
        soup = BeautifulSoup(chap, 'html.parser')
        text = soup.find_all(text=True)
        for t in text:
            if t.parent.name not in self.blacklist:
                output += '{} '.format(t)
        return output

    def __getParts(self):
        parts = []
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                parts.append(item)
        # parts = [part for part in parts if 'chapter' in part.get_name()]
        parts = [self.chap2text(part.get_content()) for part in parts if 'chapter' in part.get_name()]
        return [part.strip() for part in parts if part.strip() ]

    def getChapters(self):
        res = {}
        self.chapters_cost = {}
        self.total_char = 0
        self.chapters_len = {}
        temp = {}
        end = False
        i = 1
        i_s = str(i).zfill(2)
        self.chapters = {}

        for part in self.parts:
            if any(x for x in self.getlist if x in part.splitlines()[0].lower()):
                if temp:
                    self.chapters[i] = temp
                    i+=1
                    self.chapters_len[temp['name']]= len(temp['content'])
                    self.total_char += len(temp['content'])
                    self.chapters_cost[temp['name']] = self.cal_cost(self.chapters_len[temp['name']])
                    temp = {}
                temp['name'] = part.splitlines()[0].strip().replace(" ","_" )
                temp['content'] = temp.get('content','')+ part
            else:
                temp['content'] = temp.get('content', '') + part
        if temp:
            self.chapters[i] = temp
            i += 1
            self.chapters_len[temp['name']] = len(temp['content'])
            self.total_char += len(temp['content'])
            self.chapters_cost[temp['name']] = self.cal_cost(self.chapters_len[temp['name']])

    def write_to_files(self,foldername):
        for k, v in self.chapters.items():
            outputfile = codecs.open(f"{foldername}/{str(k).zfill(2)}_{self.bookname.split('.')[0]}_{v['name']}.txt", "w", encoding="utf-8")
            outputfile.write(v['content'])
            outputfile.close()



# book = EpubReader(bookname)
# book.write_to_files('Slime_LN11')



