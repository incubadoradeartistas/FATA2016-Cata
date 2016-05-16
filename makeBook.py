#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir, system
from os.path import join
from time import sleep

if __name__ == "__main__":
    DATA_DIR = "."
    HTML_TEMPLATE = "template.html"
    BOOK_NAME = "xbook"
    TOC_TAG = "<!-- !!! TOCTOCTOC !!! -->"
    BODY_TAG = "<!-- !!! BODYBODY !!! -->"

    
    TOC = ""
    BODY = ""

    for idx,filename in enumerate([f for f in listdir(DATA_DIR) if f.endswith(".txt")]):
        fullPath = join(DATA_DIR, filename)
        print "PROCESSING: %s"%fullPath
        
        cHtml = ""
        cTitle = ""

        # expand the html and add to TOC list
        with open(fullPath) as txt:
            for line in txt.read().splitlines():
                if cTitle is "":
                    cTitle = line
                    TOC += "				<li><a href=\"#ch%s\">%s</a></li>\n"%(str(idx), cTitle)
                elif "images/" in line:
                    if cHtml is "":
                        cHtml += "        <div class=\"projcover\">\n"
                        cHtml += "            <img src=%s />\n"%line
                        cHtml += "            <h2>%s</h2>\n"%cTitle.replace(": ","<br />")
                        cHtml += "        </div>\n"
                        cHtml += "        <h1 id=\"ch%s\" class=\"chapter\">%s</h1>\n"%(str(idx), cTitle)
                    else:
                        cHtml += "        <div class=\"projcover\">\n"
                        cHtml += "            <img src=%s />\n"%line
                        cHtml += "        </div>\n"
                else:
                    cHtml += "        %s\n"%line
            txt.close()

        if cHtml is not "":
            BODY += cHtml

    # write output file
    with open(join(DATA_DIR, BOOK_NAME+".html"), 'w') as out, open(join(DATA_DIR, HTML_TEMPLATE)) as temp:
        for line in temp.readlines():
            if TOC_TAG in line:
                line = TOC
            if BODY_TAG in line:
                line = BODY
            out.write(line)
        out.close()
        temp.close()

    # make pdf
    system("prince -s style.css %s.html -o %s.pdf"%(BOOK_NAME,BOOK_NAME))
    system("pdf2ps %s.pdf %s.ps"%(BOOK_NAME,BOOK_NAME))
    system("rm -rf %s.pdf"%(BOOK_NAME))
    system("ps2pdf %s.ps %s.pdf"%(BOOK_NAME,BOOK_NAME))
    system("rm -rf %s.ps"%(BOOK_NAME))

