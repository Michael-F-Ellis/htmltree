# -*- coding: utf-8 -*-
"""
Description: Client side of sanity check
Uses JS functions insertAdjacentHTML, innerHTML and addEventListener.
See https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML
    https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML
    https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener

Author: Mike Ellis
Copyright 2017 Owner
"""
from htmltree import *
def start():
    console.log("Starting")
    ## insert a style element at the end of the <head?
    cssrules = {'.test':{'color':'green', 'text-align':'center'}}
    style = Style(**cssrules)
    document.head.insertAdjacentHTML('beforeend', style.render())

    ## Replace the <body> content
    newcontent = Div(H1("Sanity check PASS", _class='test'))
    document.body.innerHTML = newcontent.render()
    console.log("Finished")

## JS is event driven.
## Wait for DOM load to complete before firing
## our start() function.
document.addEventListener('DOMContentLoaded', start)

