#!/usr/bin/env python
#coding: utf-8
import sys, re, os, string
sys.argv.append('View.txt')
try:
	chapter = string.join(sys.argv[1].split(".")[0:-1])
	data = open(sys.argv[1]).read()
	outfile = chapter + ".html"
except Exception as e:	print (""" Usage: htmlcompile <file> """, e);	sys.exit(1)

imgfolder = 'images'
pats = { 'img'	: r"(\[image:([^\]]+)\])", 
			'p'	: r"(\n)(\s*[^<].*)(\n{2}|$)", 
			'h'	: r"^([^\n]*)\n",
		'config0': r"(\[config\])",
		'config1': r"(\[/config\])"
}
imgtypes = ['png', 'jpg', 'jpeg', 'bmp']

html = {
		'img': 
"""<div class="img">
	<b>%s</b>
	<img src='""" + imgfolder + """/%s' style="text-align: center;" alt="%s" />
</div> """, 
		'p': r"\1<p>\2</p>\3", 
		'h': r"<h1>\1</h1>\n\n", 
		'code0': r"""<pre style="background:#2a2a2a; color:#f1d325; padding:13px;" class="">""",
		'code1': r"""</pre>"""
	}

# Listing all images that are on disk
images = [f for f in os.listdir(imgfolder) if os.path.isfile("%s/%s" % (imgfolder, f)) and f.lower().split('.')[-1] in imgtypes]
imgids = [string.join(f.split('.')[0:-1]) for f in images]
imgdict = dict(zip(imgids, images))
print ("Found images: ", images)

################################
#	COMPILING
################################
print ("Compiling headers")
data = re.sub(pats['h'], html['h'], data)

print ("Compiling images")
for i, match in enumerate(re.findall(pats['img'], data)):
	m=match[1]
	if not m in imgids:
		print ("Missing image: %s" % m)
	else:
		print ("Inserting image: %s (%s)" % (m, imgdict[m]))
		caption = "Fig. %s.%d - %s" % (chapter, i+1, m)
		data = data.replace(match[0], html['img'] % ( caption, imgdict[m], caption))

print ("Compiling paragraphs")
data,n  = re.subn(pats['p'], html['p'], data)
print ("found ", n, " items")

print ("Compiling code")
data, n = re.subn(pats['config0'], html['code0'], data)
data, n = re.subn(pats['config1'], html['code1'], data)

print ("found ", n, " items")

print ("Creating outfile %s " % outfile)
print ("success"	 if open(outfile, 'w+').write(data) else "Failure")


