# -*- coding: utf-8 -*-
"""
Description: Very basic test of htmltree under Cpython and Transcrypt.
Runs doctests first. Proceeds only if all pass.

Then creates a rudimentary html file that loads a JS file which replaces the
body element with new content. Opens the html file in the default browser.

Requires Transcrypt.

Author: Mike Ellis
Copyright 2017 Ellis & Grant, Inc.
"""
import doctest

if __name__ == '__main__':
    doctest.testmod()
import subprocess
import webbrowser
import os
import doctest
import htmltree
print("Running doctests ...")
doctest_result = doctest.testmod(htmltree)
if doctest_result.failed > 0:
    print("Failed {} doctests! Aborting.",format(doctest_result.failed))
    import sys
    sys.exit()
else:
    print("Passed all of {} doctests.".format(doctest_result.attempted))

from htmltree import *

head = Head(Script(src="../__javascript__/client.js", charset="UTF-8"))
body = Body(H1("Sanity check FAIL if this remains visible"))
doc = Html(head, body)

print("Writing sanitycheck.html ...")
if not os.path.exists("__html__"):
    os.makedirs("__html__")
with open('__html__/sanitycheck.html', 'w') as f:
    print(doc.render(0), file=f)

print("Building client.js")
proc = subprocess.Popen('transcrypt -b -n -m client.py', shell=True)
if proc.wait() != 0:
    raise Exception("Failed trying to build client.js")

print("Build complete. Opening sanitycheck.html in browser ...")
path = os.path.abspath("__html__/sanitycheck.html")
webbrowser.open("file://" + path)
