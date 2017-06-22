# -*- coding: utf-8 -*-
"""
Description: Client side of sanity check
Author: Mike Ellis
Copyright 2017 Owner
"""
from htmltree import *
def start():
    console.log("Starting")
    newcontent = H1("Sanity check PASS", style=dict(color='green'))
    console.log(newcontent.render(0))
    document.body.innerHTML = newcontent.render()
    console.log("Finished")
document.addEventListener('DOMContentLoaded', start)

