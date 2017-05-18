# ====================================================================
# PDF Scrapper
# Found here: http://davidhuynh.net/spaces/nicar2011/tutorial.pdf
# ====================================================================

import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

pdfurl = "http://www.lillyfacultyregistry.com/documents/
EliLillyFacultyRegistryQ22010.pdf"
pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
for page in root:
   assert page.tag == 'page'
   pagelines = { }
   for v in page:
       if v.tag == 'text':
           text = re.match('(?s)<text.*?>(.*?)</text>',
                    lxml.etree.tostring(v)).group(1)
           top = int(v.attrib.get('top'))
           if (top - 1) in pagelines:
               top = top - 1
           elif (top + 1) in pagelines:
               top = top + 1
           elif top not in pagelines:
               pagelines[top] = [ ]
           pagelines[top].append((int(v.attrib.get('left')), text))
   lpagelines = pagelines.items()
   lpagelines.sort()
   for top, line in lpagelines:
      line.sort()
      key = page.attrib.get('number') + ':' + str(top)
      scraperwiki.datastore.save(unique_keys=[ 'key' ],
               data={ 'key' : key, 'line' : line })
               
# ==========================================================================
