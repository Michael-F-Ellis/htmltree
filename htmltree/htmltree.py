# -*- coding: utf-8 -*-
"""
Description: Provides a general html tree class, HtmlElement and wrapper
functions for most standard non-obsolete HTML tags.

This file is part of htmltree
https://github.com/Michael-F-Ellis/htmltree

Compatibilty with Transcrypt Python to JS transpiler:
    By design, this module is intended for use with both CPython and
    Transcrypt.  The latter implies certain constraints on the Python
    constructs that may be used.  Compatibility with Transcrypt also requires
    the use of two __pragma__ calls to achieve compilation. These are contained
    in line comments and hence have no effect when running under CPython.

    The benefit of Transcrypt compatibility is complete freedom to use Python
    to define HTML/CSS at run time on the client side, i.e. in transpiled JS
    running in a browser.


Author: Michael Ellis
Copyright 2017 Ellis & Grant, Inc.
License: MIT License
"""
# __pragma__('kwargs')

def KWElement(tag, *content, **attrs):
    """
    It's recommended to import this function rather than the HtmlElement class it wraps.
    This function's signature reduces the need to quote attribute names.
    """
    if len(content) == 1 and content[0] is None:
        content = None
    else:
        content = list(content)
    return HtmlElement(tag, convertAttrKeys(attrs), content)

def convertAttrKeys(attrdict):
    """
    Convert underscores to minus signs ('-').  Remove one trailing minus sign if present.
    If no trailing minus signs, remove one leading minus sign.
    >>> convertAttrKeys({'_class':'foo'})
    {'class': 'foo'}
    >>> convertAttrKeys({'class_':'foo'})
    {'class': 'foo'}
    >>> convertAttrKeys({'data_role':'foo'})
    {'data-role': 'foo'}
    >>> convertAttrKeys({'_moz_style_':'foo'})
    {'-moz-style': 'foo'}
    """
    newdict = {}
    for k, v in attrdict.items():
        ## Replace all underscores with '-'
        k = k.replace('_', '-')
        if k.endswith('-'):
            ## Drop trailing '-'
            k = k[:-1].replace('_','-')
        elif k.startswith('-'):
            ## Drop leading '-'
            k = k[1:]
        newdict[k] = v
    return newdict

class HtmlElement:
    """
    General nested html element tree with recursive rendering

    Note: Directly importing this class is deprecated (or at least not
    recommended) because the arguments to this classes constructor are not in
    the most convenient order. Import KWElement defined above instead.

    Constructor arguments:
        tagname : valid html tag name (string)

        attrs   : attributes (dict | dict-like object | None)
                    keys must be valid attribute names (string)
                    values must be (string | list of strings | dict of styles)

        content : (None | string | int | float | list of (strings/ints/floats and/or elements)
                  elements must have a 'render' method that returns valid html.

                  None has a special meaning. It denotes a singleton tag, e.g. <meta> or <br>

                  The <style> tag gets special handling. You may pass the css as a dict of
                  the form {'selector': {'property':'value', ...}, ...}

    Public Members:
        T : tagname
        A : attribute dict
        C : content

    Instance methods:
        render(indent=-1) -- defaults to no indentation, no newlines
                             indent >= 0 behaves according to the indented()
                             function in this module.

    Helper functions (defined at module level):

        indented(contentstring, indent) -- applies indentation to rendered content

        renderstyle(d) -- Special handline for inline style attributes.
                          d is a dictionary of style definitions

        renderCss(d, indent=-1) -- Special handling for <style> tag
                                   d is a dict of CSS rulesets

    Doctests:
    >>> E = HtmlElement
    >>> doc = E('html', None, [])
    >>> doc.render()
    '<html></html>'
    >>> doc.C.append(E('head', None, []))
    >>> doc.render()
    '<html><head></head></html>'
    >>> body = E('body', {'style':{'background-color':'black'}}, [E('h1', None, "Title")])
    >>> body.C.append(E('br', None, None))
    >>> body.render()
    '<body style="background-color:black;"><h1>Title</h1><br></body>'
    >>> doc.C.append(body)
    >>> doc.render()
    '<html><head></head><body style="background-color:black;"><h1>Title</h1><br></body></html>'

    >>> style = E('style', None, {'p.myclass': {'margin': '4px'}})
    >>> style.render()
    '<style>p.myclass { margin:4px; }</style>'

    >>> comment = E('!--', None, "This is out!")
    >>> comment.render()
    '<!-- This is out! -->'

    >>> comment.C = [body]
    >>> comment.render()
    '<!-- <body style="background-color:black;"><h1>Title</h1><br></body> -->'

    """
    def __init__(self, tagname, attrs, content):
        ## Validate arguments
        assert isinstance(tagname, str)
        self.T = tagname.lower()
        if self.T == '!--': ## HTML comment
            attrs = None
            self.endtag = " -->"
        else:
            self.endtag = "</{}>".format(self.T)

        if attrs is not None:
            ## hasattr isn't quite right in Transcrypt,
            ## hence we need to test with a try clause.
            try:
                _ = attrs.items()
            except AttributeError:
                msg = "attrs must be a dict-like object or None"
                raise ValueError(msg)

        self.A = attrs
        self.C = content

    def render(self, indent=-1):
        """ Recursively generate html """
        rlist = []
        ## Render the tag with attributes
        opentag = "<{}".format(self.T)
        rlist.append(indented(opentag, indent))

        ## Render the attributes
        if self.A is not None:
            for a, v in self.A.items():
                if isinstance(v, str):
                    rlist.append(' {}="{}"'.format(a,v))
                elif v is None:
                    rlist.append(' {}'.format(a)) # bare attribute, e.g. 'disabled'
                elif isinstance(v,list):
                    _ = ' '.join(v)     ## must be list of strings
                    rlist.append(' {}="{}"'.format(a, _))
                elif a == 'style':
                    rlist.append(' {}="{}"'.format(a,renderInlineStyle(v)))
                else:
                    msg="Don't know what to with attribute {}={}".format(a,v)
                    raise ValueError(msg)

        if self.C is None and self.T != "!--":
            ## It's a singleton tag. Close it accordingly.
            closing = ">"
        else:
            ## Close the tag
            if self.T == "!--":
                rlist.append(" ")
            else:
                rlist.append('>')

            ## Render the content
            if isinstance(self.C, str):
                rlist.append(indented(self.C, indent))
            elif self.T == "style":
                rlist.append(renderCss(self.C, indent))
            else:
                cindent = indent + 1 if indent >= 0 else indent
                for c in self.C:
                    if isinstance(c, (str,int,float)):
                        rlist.append(indented(str(c), cindent))
                    else:
                        rlist.append(c.render(cindent)) ## here's the recursion!

            closing = indented(self.endtag, indent)
        rlist.append(closing)

        return ''.join(rlist)

    #__pragma__('skip')
    def renderToFile(self, filepath, indent=-1):
        """
        Render to a local file and return a "file://" url for convenient display.
        Note: This method has no meaning under Transcrypt and is not compiled.
        """
        import os
        with open(filepath, 'w') as f:
            print(self.render(indent=indent), file=f)
        return "file://" + os.path.abspath(filepath)
    #__pragma__('noskip')

def indented(contentstring, indent=-1):
    """
    Return indented content.
    indent >= 0 prefixes content with newline + 2 * indent spaces.
    indent < 0 returns content unchanged

    Docstrings:
    >>> indented("foo bar", -1)
    'foo bar'

    >>> indented("foo bar", 0)
    '\\nfoo bar'

    >>> indented("foo bar", 1)
    '\\n  foo bar'

    """
    if not indent >= 0:
        return contentstring
    else:
        return "\n{}{}".format("  " * indent, contentstring)


def renderInlineStyle(d):
    """If d is a dict of styles, return a proper style string """
    if isinstance(d, (str, int, float)):
        result = str(d)
    else:
        style=[]
        for k,v in d.items():
            ## See note in HtmlElement.render() about underscore replacement.
            kh = k.replace('_', '-')
            kh = kh.strip('-')
            # Ugly hack until Transcrypt implemnts strip() correctly
            while kh.startswith('-'):
                kh = kh[1:]
            while kh.endswith('-'):
                kh = kh[:-1]
            style.append("{}:{};".format(kh, v))
        separator = ' '
        result = separator.join(style)
    return result

def renderCss(d, indent=-1):
    """
    Render a string of CSS rulesets from d, a dict (or dict-like object) of
    rulesets,.
    """
    rulesetlist = []
    for selector, declaration in d.items():
        ruleset = " ".join([selector,
                            '{',
                            renderInlineStyle(declaration),
                            '}'
                            ])
        rulesetlist.append(indented(ruleset, indent))
    return ' '.join(rulesetlist)



#######################################################################
## Wrappers for html element tags.
##
## Functions are grouped in the categories given at
## https://developer.mozilla.org/en-US/docs/Web/HTML/Element and
## are alphabetical within groups.
##
## Conventions:
##     Functions are named by tag with initial caps, e.g. Html()
##
##     The signature for non-empty tags is Tagname(*content, **attrs)
##     The signature for empty tags is Tagname(**attrs)
##
##     Empty refers to elements that enclose no content and need no closing tag.
##
##     <style> is the only exception. It's signature is Style(**content). More
##     details and explanation in the doc string.
##
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
## TODO: base
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
    >>> html = style.render()
    >>> a = '<style type="text/css">body { margin:4px; } p { color:blue; }</style>'
    >>> b = '<style type="text/css">p { color:blue; } body { margin:4px; }</style>'
    >>> html in (a,b) # order is indeterminate, so test both ways
    True
    """
    return HtmlElement('style', {}, content)

#######################################################################
## Content Sectioning
## TODO hgroup
#######################################################################

def Address(*content, **attrs):
    """
    Wrapper for address tag
    >>> Address().render()
    '<address></address>'
    """
    return KWElement('address', *content, **attrs)

def Article(*content, **attrs):
    """
    Wrapper for article tag
    >>> Article().render()
    '<article></article>'
    """
    return KWElement('article', *content, **attrs)

def Aside(*content, **attrs):
    """
    Wrapper for aside tag
    >>> Aside().render()
    '<aside></aside>'
    """
    return KWElement('aside', *content, **attrs)

def Footer(*content, **attrs):
    """
    Wrapper for footer tag
    >>> Footer().render()
    '<footer></footer>'
    """
    return KWElement('footer', *content, **attrs)

def Header(*content, **attrs):
    """
    Wrapper for header tag
    >>> Header().render()
    '<header></header>'
    """
    return KWElement('header', *content, **attrs)


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

def Nav(*content, **attrs):
    """
    Wrapper for nav tag
    >>> Nav().render()
    '<nav></nav>'
    """
    return KWElement('nav', *content, **attrs)

def Section(*content, **attrs):
    """
    Wrapper for section tag
    >>> Section().render()
    '<section></section>'
    """
    return KWElement('section', *content, **attrs)

#######################################################################
## Text Content
#######################################################################

def Blockquote(*content, **attrs):
    """
    Wrapper for blockquote tag
    >>> Blockquote().render()
    '<blockquote></blockquote>'
    """
    return KWElement('blockquote', *content, **attrs)

def Dd(*content, **attrs):
    """
    Wrapper for dd tag
    >>> Dd().render()
    '<dd></dd>'
    """
    return KWElement('dd', *content, **attrs)

def Div(*content, **attrs):
    """
    Wrapper for div tag
    >>> Div().render()
    '<div></div>'
    """
    return KWElement('div', *content, **attrs)

def Dl(*content, **attrs):
    """
    Wrapper for dl tag
    >>> Dl().render()
    '<dl></dl>'
    """
    return KWElement('dl', *content, **attrs)

def Dt(*content, **attrs):
    """
    Wrapper for dt tag
    >>> Dt().render()
    '<dt></dt>'
    """
    return KWElement('dt', *content, **attrs)

def Figcaption(*content, **attrs):
    """
    Wrapper for figcaption tag
    >>> Figcaption().render()
    '<figcaption></figcaption>'
    """
    return KWElement('figcaption', *content, **attrs)

def Figure(*content, **attrs):
    """
    Wrapper for figure tag
    >>> Figure().render()
    '<figure></figure>'
    """
    return KWElement('figure', *content, **attrs)

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

def Main(*content, **attrs):
    """
    Wrapper for main tag
    >>> Main().render()
    '<main></main>'
    """
    return KWElement('main', *content, **attrs)

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

# __pragma__('nokwargs')

## The 'skip' pragma tells the Transcrypt Python to JS transpiler to
## ignore a section of code. It's needed here because the 'run as script'
## idiom causes an error in Transcrypt and has no meaning in that context.
## Putting the pragmas in comments means they'll be ignored and cause no
## problems in a real python interpreter.

# __pragma__ ('skip')
if __name__ == '__main__':
    import doctest
    doctest.testmod()
# __pragma__ ('noskip')
