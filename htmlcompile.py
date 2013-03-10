#!/usr/bin/env python
#coding: utf-8
import sys, re, os, string, webbrowser, cgi


try:
	chapter = string.join(sys.argv[1].split(".")[0:-1])
	data = open(sys.argv[1]).read()
	outfile = chapter + ".html"
	

except Exception as e:	print (""" Usage: htmlcompile <file> """, e);	sys.exit(1)

imgfolder = 'images'
pats = { 'img'	: r"(\[image:([^\]]+)\])", 
			'p'	: r"(\n)(.+?)(\n{2}|$)", 
			'h'	: r"^([^\n]*)\n",
		'config': re.compile(r"(\[config\])(.+?)(\[/config\])", flags=re.DOTALL),
		'list'	: r"^\s*\*\s*([^\n]*)\n"
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
		'config': lambda m: """<pre style="background:#f0f0f0; color:#000000; padding:13px;" class=""> %s </pre>""" % cgi.escape(m.group(2).decode('utf-8')).encode('ascii', 'xmlcharrefreplace'),
		'list' : r"""<li>\1</li>\n"""
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
# Isolating config snippets
data2   = re.findall(pats['config'], data)
data, n = re.subn(pats['config'], "1238placeholder1293", data)

# the real paragraphs
data, n = re.subn(pats['p'], html['p'], data)

# Putting config snipets back in.
for triple in data2: 
	data = re.sub("1238placeholder1293", triple[0] + repr(triple[1])[1:-1] + triple[2], data, 1)

print ("found ", n, " items")


print ("Compiling code")
data, n = re.subn(pats['config'], html['config'], data)
print ("found ", n, " items")


print ("Compiling lists")
data, n = re.subn(pats['list'], html['list'], data)
print ("found ", n, " items")


print ("Adding style")
style = """
	<style>
	pre {
		 white-space: pre-wrap;       /* css-3 */
		 white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
		 white-space: -pre-wrap;      /* Opera 4-6 */
		 white-space: -o-pre-wrap;    /* Opera 7 */
		 word-wrap: break-word;       /* Internet Explorer 5.5+ */
	}
	</style>
"""

print ("Adding utf-8 encoding declaration")
meta = """<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>"""
data = meta + style + data

print ("Creating outfile %s " % outfile)
print ("success"	 if not open(outfile, 'w+').write(data) else "Failure")

print ("opening webbrowser: %s" % webbrowser.get())
webbrowser.open_new(os.path.abspath(outfile))
