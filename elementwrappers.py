# -*- coding: utf-8 -*-
"""
Description: Wrappers for html element tags.

Functions are grouped in the categories given at
https://developer.mozilla.org/en-US/docs/Web/HTML/Element and
are alphabetical within groups.

Conventions:
    Functions are named by tag with initial caps, e.g. Html()

    The signature for non-empty tags is Tagname(*content, **attrs)
    The signature for empty tags is Tagname(**attrs)

    Empty refers to elements that enclose no content and need no closing tag.

    <style> is the only exception. It's signature is Style(**content). More
    details and explanation in the doc string.


Author: Mike Ellis
Copyright 2017 Ellis & Grant, Inc.
License: MIT
"""
import doctest
from htmltree import Element, KWElement

#######################################################################
## Obsolete and Deprecated Elements.
## No pull requests will be accepted for:
## acronym, applet, basefont, big, blink, center, command, content,
## dir, element, font, frame, frameset, isindex, keygen, listing,
## marquee, multicol, nextid, noembed, plaintext, shadow, spacer,
## strike, tt, xmp .
#######################################################################


#######################################################################
## Main Root
#######################################################################

def Html(*content, **attrs):
    """
    Wrapper for html tag
    >>> Html().render()
    '<html></html>'
    """
    return KWElement('html', *content, **attrs)

#######################################################################
## Document Metadata
#######################################################################

def Head(*content, **attrs):
    """
    Wrapper for head tag
    >>> Head().render()
    '<head></head>'
    """
    return KWElement('head', *content, **attrs)

def Body(*content, **attrs):
    """
    Wrapper for body tag
    >>> Body().render()
    '<body></body>'
    """
    return KWElement('body', *content, **attrs)

def Link(**attrs):
    """
    Wrapper for link tag
    >>> Link().render()
    '<link>'
    """
    return KWElement('link', None, **attrs)

def Meta(**attrs):
    """
    Wrapper for meta tag
    >>> Meta().render()
    '<meta>'
    """
    return KWElement('meta', None, **attrs)

def Title(*content, **attrs):
    """
    Wrapper for title tag
    >>> Title("The Title").render()
    '<title>The Title</title>'
    """
    return KWElement('title', *content, **attrs)

def Style(**content):
    """
    Wrapper for style tag. Notice that this breaks the pattern of most other
    wrappers by omitting the attrs arg and making content a keyword arg set.
    This is done to reduce (but alas not completely eliminate) the need for
    quoting the selectors in CSS rulesets.

    If you need to set attrs on a style element, do it in a secondary call as
    shown in the doctest below.

    >>> style = Style(body=dict(margin='4px'), p={'color':'blue'})
    >>> style.A.update({'type':'text/css'})
    >>> style.render()
    '<style type="text/css">body { margin:4px; } p { color:blue; }</style>'
    """
    return Element('style', {}, content)

#######################################################################
## Content Sectioning
## TODO address, article, aside, footer, header, hgroup, nav, section
#######################################################################

def H1(*content, **attrs):
    """
    Wrapper for h1 tag
    >>> H1().render()
    '<h1></h1>'
    """
    return KWElement('h1', *content, **attrs)

def H2(*content, **attrs):
    """
    Wrapper for h2 tag
    >>> H2().render()
    '<h2></h2>'
    """
    return KWElement('h2', *content, **attrs)

def H3(*content, **attrs):
    """
    Wrapper for h3 tag
    >>> H3().render()
    '<h3></h3>'
    """
    return KWElement('h3', *content, **attrs)

def H4(*content, **attrs):
    """
    Wrapper for h4 tag
    >>> H4().render()
    '<h4></h4>'
    """
    return KWElement('h4', *content, **attrs)

def H5(*content, **attrs):
    """
    Wrapper for h5 tag
    >>> H5().render()
    '<h5></h5>'
    """
    return KWElement('h5', *content, **attrs)

def H6(*content, **attrs):
    """
    Wrapper for h6 tag
    >>> H6().render()
    '<h6></h6>'
    """
    return KWElement('h6', *content, **attrs)

#######################################################################
## Text Content
## TODO dd, dl, dt, figcaption, figure, main
#######################################################################

def Blockquote(*content, **attrs):
    """
    Wrapper for blockquote tag
    >>> Blockquote().render()
    '<blockquote></blockquote>'
    """
    return KWElement('blockquote', *content, **attrs)

def Div(*content, **attrs):
    """
    Wrapper for div tag
    >>> Div().render()
    '<div></div>'
    """
    return KWElement('div', *content, **attrs)

def Hr(**attrs):
    """
    Wrapper for hr tag
    >>> Hr().render()
    '<hr>'
    """
    return KWElement('hr', None, **attrs)

def Li(*content, **attrs):
    """
    Wrapper for li tag
    >>> Li().render()
    '<li></li>'
    """
    return KWElement('li', *content, **attrs)

def Ol(*content, **attrs):
    """
    Wrapper for ol tag
    >>> Ol().render()
    '<ol></ol>'
    """
    return KWElement('ol', *content, **attrs)

def P(*content, **attrs):
    """
    Wrapper for p tag
    >>> P().render()
    '<p></p>'
    """
    return KWElement('p', *content, **attrs)

def Pre(*content, **attrs):
    """
    Wrapper for pre tag
    >>> Pre().render()
    '<pre></pre>'
    """
    return KWElement('pre', *content, **attrs)

def Ul(*content, **attrs):
    """
    Wrapper for ul tag
    >>> Ul().render()
    '<ul></ul>'
    """
    return KWElement('ul', *content, **attrs)

#######################################################################
## Inline Text Semantics
## TODO abbr, bdi, bdo, data, dfn, kbd, mark, q, rp, rt, rtc, ruby,
##      time, var, wbr
#######################################################################

def A(*content, **attrs):
    """
    Wrapper for a tag
    >>> A("Example", href="https://example.com").render()
    '<a href="https://example.com">Example</a>'
    """
    return KWElement('a', *content, **attrs)

def B(*content, **attrs):
    """
    Wrapper for b tag
    >>> B().render()
    '<b></b>'
    """
    return KWElement('b', *content, **attrs)

def Br(**attrs):
    """
    Wrapper for br tag
    >>> Br().render()
    '<br>'
    """
    return KWElement('br', None, **attrs)

def Cite(*content, **attrs):
    """
    Wrapper for cite tag
    >>> Cite().render()
    '<cite></cite>'
    """
    return KWElement('cite', *content, **attrs)

def Code(*content, **attrs):
    """
    Wrapper for code tag
    >>> Code().render()
    '<code></code>'
    """
    return KWElement('code', *content, **attrs)

def Em(*content, **attrs):
    """
    Wrapper for em tag
    >>> Em().render()
    '<em></em>'
    """
    return KWElement('em', *content, **attrs)

def I(*content, **attrs):
    """
    Wrapper for i tag
    >>> I().render()
    '<i></i>'
    """
    return KWElement('i', *content, **attrs)

def S(*content, **attrs):
    """
    Wrapper for s tag
    >>> S().render()
    '<s></s>'
    """
    return KWElement('s', *content, **attrs)

def Samp(*content, **attrs):
    """
    Wrapper for samp tag
    >>> Samp().render()
    '<samp></samp>'
    """
    return KWElement('samp', *content, **attrs)

def Small(*content, **attrs):
    """
    Wrapper for small tag
    >>> Small().render()
    '<small></small>'
    """
    return KWElement('small', *content, **attrs)

def Span(*content, **attrs):
    """
    Wrapper for span tag
    >>> Span().render()
    '<span></span>'
    """
    return KWElement('span', *content, **attrs)

def Strong(*content, **attrs):
    """
    Wrapper for strong tag
    >>> Strong().render()
    '<strong></strong>'
    """
    return KWElement('strong', *content, **attrs)

def Sub(*content, **attrs):
    """
    Wrapper for sub tag
    >>> Sub().render()
    '<sub></sub>'
    """
    return KWElement('sub', *content, **attrs)

def Sup(*content, **attrs):
    """
    Wrapper for sup tag
    >>> Sup().render()
    '<sup></sup>'
    """
    return KWElement('sup', *content, **attrs)

def U(*content, **attrs):
    """
    Wrapper for u tag
    >>> U().render()
    '<u></u>'
    """
    return KWElement('u', *content, **attrs)

#######################################################################
## Image and Multimedia
#######################################################################

def Area(**attrs):
    """
    Wrapper for area tag
    >>> Area().render()
    '<area>'
    """
    return KWElement('area', None, **attrs)

def Audio(*content, **attrs):
    """
    Wrapper for audio tag
    >>> Audio().render()
    '<audio></audio>'
    """
    return KWElement('audio', *content, **attrs)

def Img(**attrs):
    """
    Wrapper for img tag
    >>> Img().render()
    '<img>'
    """
    return KWElement('img', None, **attrs)

def Map(*content, **attrs):
    """
    Wrapper for map tag
    >>> Map().render()
    '<map></map>'
    """
    return KWElement('map', *content, **attrs)

def Track(**attrs):
    """
    Wrapper for track tag
    >>> Track().render()
    '<track>'
    """
    return KWElement('track', None, **attrs)

def Video(*content, **attrs):
    """
    Wrapper for video tag
    >>> Video().render()
    '<video></video>'
    """
    return KWElement('video', *content, **attrs)

#######################################################################
## Embedded Content
#######################################################################

def Embed(**attrs):
    """
    Wrapper for embed tag
    >>> Embed().render()
    '<embed>'
    """
    return KWElement('embed', None, **attrs)

def Object(*content, **attrs):
    """
    Wrapper for object tag
    >>> Object().render()
    '<object></object>'
    """
    return KWElement('object', *content, **attrs)

def Param(**attrs):
    """
    Wrapper for param tag
    >>> Param().render()
    '<param>'
    """
    return KWElement('param', None, **attrs)

def Source(**attrs):
    """
    Wrapper for source tag
    >>> Source().render()
    '<source>'
    """
    return KWElement('source', None, **attrs)

#######################################################################
## Scripting
#######################################################################

def Canvas(*content, **attrs):
    """
    Wrapper for canvas tag
    >>> Canvas().render()
    '<canvas></canvas>'
    """
    return KWElement('canvas', *content, **attrs)

def Noscript(*content, **attrs):
    """
    Wrapper for noscript tag
    >>> Noscript().render()
    '<noscript></noscript>'
    """
    return KWElement('noscript', *content, **attrs)

def Script(*content, **attrs):
    """
    Wrapper for script tag
    >>> Script().render()
    '<script></script>'
    """
    return KWElement('script', *content, **attrs)

#######################################################################
## Demarcating Edits
## TODO del, ins
#######################################################################

#######################################################################
## Table Content
## TODO colgroup (maybe. It's poorly supported.)
#######################################################################

def Caption(*content, **attrs):
    """
    Wrapper for caption tag
    >>> Caption().render()
    '<caption></caption>'
    """
    return KWElement('caption', *content, **attrs)

def Col(**attrs):
    """
    Wrapper for col tag
    >>> Col().render()
    '<col>'
    """
    return KWElement('col', None, **attrs)

def Table(*content, **attrs):
    """
    Wrapper for table tag
    >>> Table().render()
    '<table></table>'
    """
    return KWElement('table', *content, **attrs)

def Tbody(*content, **attrs):
    """
    Wrapper for tbody tag
    >>> Tbody().render()
    '<tbody></tbody>'
    """
    return KWElement('tbody', *content, **attrs)

def Td(*content, **attrs):
    """
    Wrapper for td tag
    >>> Td().render()
    '<td></td>'
    """
    return KWElement('td', *content, **attrs)

def Tfoot(*content, **attrs):
    """
    Wrapper for tfoot tag
    >>> Tfoot().render()
    '<tfoot></tfoot>'
    """
    return KWElement('tfoot', *content, **attrs)

def Th(*content, **attrs):
    """
    Wrapper for th tag
    >>> Th().render()
    '<th></th>'
    """
    return KWElement('th', *content, **attrs)

def Thead(*content, **attrs):
    """
    Wrapper for thead tag
    >>> Thead().render()
    '<thead></thead>'
    """
    return KWElement('thead', *content, **attrs)

def Tr(*content, **attrs):
    """
    Wrapper for tr tag
    >>> Tr().render()
    '<tr></tr>'
    """
    return KWElement('tr', *content, **attrs)

#######################################################################
## Forms
#######################################################################

def Button(*content, **attrs):
    """
    Wrapper for button tag
    >>> Button().render()
    '<button></button>'
    """
    return KWElement('button', *content, **attrs)

def Datalist(*content, **attrs):
    """
    Wrapper for datalist tag
    >>> Datalist().render()
    '<datalist></datalist>'
    """
    return KWElement('datalist', *content, **attrs)

def Fieldset(*content, **attrs):
    """
    Wrapper for fieldset tag
    >>> Fieldset().render()
    '<fieldset></fieldset>'
    """
    return KWElement('fieldset', *content, **attrs)

def Form(*content, **attrs):
    """
    Wrapper for form tag
    >>> Form().render()
    '<form></form>'
    """
    return KWElement('form', *content, **attrs)

def Input(**attrs):
    """
    Wrapper for input tag
    >>> Input().render()
    '<input>'
    """
    return KWElement('input', None, **attrs)

def Label(*content, **attrs):
    """
    Wrapper for label tag
    >>> Label().render()
    '<label></label>'
    """
    return KWElement('label', *content, **attrs)

def Legend(*content, **attrs):
    """
    Wrapper for legend tag
    >>> Legend().render()
    '<legend></legend>'
    """
    return KWElement('legend', *content, **attrs)

def Meter(*content, **attrs):
    """
    Wrapper for meter tag
    >>> Meter().render()
    '<meter></meter>'
    """
    return KWElement('meter', *content, **attrs)

def Optgroup(*content, **attrs):
    """
    Wrapper for optgroup tag
    >>> Optgroup().render()
    '<optgroup></optgroup>'
    """
    return KWElement('optgroup', *content, **attrs)

def Option(*content, **attrs):
    """
    Wrapper for option tag
    >>> Option().render()
    '<option></option>'
    """
    return KWElement('option', *content, **attrs)

def Output(*content, **attrs):
    """
    Wrapper for output tag
    >>> Output().render()
    '<output></output>'
    """
    return KWElement('output', *content, **attrs)

def Progress(*content, **attrs):
    """
    Wrapper for progress tag
    >>> Progress().render()
    '<progress></progress>'
    """
    return KWElement('progress', *content, **attrs)

def Select(*content, **attrs):
    """
    Wrapper for select tag
    >>> Select().render()
    '<select></select>'
    """
    return KWElement('select', *content, **attrs)

def Textarea(*content, **attrs):
    """
    Wrapper for textarea tag
    >>> Textarea().render()
    '<textarea></textarea>'
    """
    return KWElement('textarea', *content, **attrs)

#######################################################################
## Interactive Elememts (Experimental. Omitted for now.)
#######################################################################

#######################################################################
## Web Components (Experimental. Omitted for now.)
#######################################################################



if __name__ == '__main__':
    doctest.testmod()
