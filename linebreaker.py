import re
import sys
import lxml.etree as le

# first argument should be good TEI xml, second argument is pdftotext output
# pdftotext needs to be run with -layout or -raw to get faithful linebreaks
# the latter mode is deprecated but necessary for two-column documents
with open(sys.argv[1], "r", encoding="utf8") as tei_file:
	tei = tei_file.read()

with open(sys.argv[2], "r") as pdftotext_out:
	pdftotext = pdftotext_out.read()

linebreak_context = re.findall("[^\n]{20}\n[^\n]{20}", pdftotext)

for x in linebreak_context:
	x_lb = x.replace("\n", r"\g<1><lb/>\g<2>")
	x = x.replace("(", "\(")
	x = x.replace(")", "\)")
	x = x.replace("[", "\[")
	x = x.replace("]", "\]")
	x = x.replace("*", "\*")
	x = x.replace(".", "\.")
	x = x.replace("?", "\?")
	x = x.replace("+", "\+")
	x = re.sub("\n", "(<.+?>)?\s+?(<.+?>)?", x)
	x = re.sub("\s+", "\s+", x)
	tei = re.sub(x, x_lb, tei)

tei = re.sub("</head>", "<lb/></head>", tei)
tei = re.sub("</item>", "<lb/></item>", tei)
tei = re.sub("</row>", "<lb/></row>", tei)
tei = re.sub("<lb/><lb/>", "<lb/>", tei)

output_filename = re.sub("\.xml", ".training.fulltext.tei.xml", sys.argv[1])
with open(output_filename, "w", encoding="utf8") as output:
	output.write(tei)

tree = le.parse(output_filename)
for elem in tree.findall('//{http://www.tei-c.org/ns/1.0}teiHeader'):
	parent = elem.getparent()
	parent.remove(elem)
for elem in tree.findall('//{http://www.tei-c.org/ns/1.0}back'):
	parent = elem.getparent()
	parent.remove(elem)
with open(output_filename, "w", encoding="utf8") as output:
	output.write(le.tostring(tree).decode("utf8"))