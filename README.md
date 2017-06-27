# Python htmltree project

## Create and manipulate HTML and CSS from the comfort of Python
  * Easy to learn. Consistent, simple syntax.
  * 85 predefined tag functions.
  * Create HTML on the fly or save as static files.
  * Flexible usage and easy extension. 
  * Run locally with CPython or as Javascript in the browser using Jacques De Hooge's [*Transcrypt™*](https://transcrypt.org/) Python to JS transpiler
  * Dependencies: Python 3.x

### Quick Start
### Installation
`pip install htmltree`

#### Open a Python interpreter and type or paste the following
```
from htmltree import *
head = Head()
body = Body()
doc = Html(head, body)
```
#### Render and print the HTML
```
>>> print(doc.render(0))
<html>
  <head>
  </head>
  <body>
  </body>
</html>
```
#### Now add some metadata, styling and text ...
```
who = Meta(name="author",content="Your Name Here")
head.C.append(who)
body.A.update(dict(style={'background-color':'black'}))
banner = H1("Hello, htmltree!", _class='banner', style={'color':'green'})
body.C.append(banner)
```
#### and print the result.
```
>>> print(doc.render(0))
<html>
  <head>
    <meta content="Your Name Here" name="author">
  </head>
  <body style="background-color:black;">
    <h1 class="banner" style="color:green;">
      Hello, htmltree!
    </h1>
  </body>
</html>
```
In the examples above, we created elements and assigned them to variables so we could alter their content later. However, we could also have written  it out all at once.

```
doc = Html(
        Head(
          Meta(name="author",content="Your Name Here")),
        Body(
          H1("Hello, htmltree!", _class='banner', style={'color':'green'}),
          style={'background-color':'black'}))
```

That's short and clean and renders exactly the same html.  It also mimics the page structure but sacrifices ease of alteration later in the execution. Your choices should come down to whether you're creating static html or dynamic content based on information that's not available until run time.

### Reserved words and hyphenated attributes
Did you notice the underscore in `H1("Hello, htmltree!", _class='banner', ...)`? It's written that way because `class` is a Python keyword. Trying to use it as an identifier will raise a syntax error. 

As a convenience, all the wrapper functions strip off leading and trailing underscores in attribute names, so `class_` would also work. Normal HTML doesn't use underscores in attribute names so this fix is safe to use. I think `for` as a `<label>` attribute is the only other conflict in standard HTML.

The wrapper functions also replace internal underscores in attribute names with dashes. That avoids the problem of Python trying to interpret `data-role="magic"` as a subtraction expression. Use `data_role="magic"` instead. If you need to style with vendor-specific attributes that begin with a '-', add a trailing underscore, e.g. `_moz_style_` is converted to `-moz-style`.

*The conversion happens when the element is created, not when it is rendered.* If you add, update or replace an element attribute after it is created, use the attribute's true name, e.g. `mybutton.A.update({'class': 'super-button'})` rather than `mybutton.A.update(dict(_class='super-button'))`.



### Viewing your work
Use htmltree's `renderToFile` method and Python's standard `webbrowser` module.
```
import webbrowser
fileurl = doc.renderToFile('path/to/somefile.html')
webbrowser.open(fileurl)
```

The Quick Start example should look like this:

![Figure 1.](htmltree/doc/img/quickstart.png)

## Discussion
Importing * from htmltree.py provides 85 wrapper functions (as of this writing) that cover the most of the common non-obsolete HTML5 tags.  To see the most up-to-date list you can do `help(htmltree)` from the command line of a Python interactive session or look futher down on this page for a listing. The function names and arguments follow simple and consistent conventions that make use of Python's `*args, **kwargs`features.

- Functions are named by tag with initial caps, e.g. `Html()`
- The signature for non-empty tags is `Tagname(*content, **attrs)`
- The signature for empty tags is `Tagname(**attrs)` (Empty refers to elements that enclose no content and need no closing tag -- like `<meta>`, `<br>`, etc.)

To create, say, a div with two empty paragraphs separated by a horizontal rule element, you'd write

```mydiv = Div(P(), Hr(), P(), id=42, name='puddintane')```

Because the first three args are unnamed Python knows they belong, in order, `to *content`. The last two arguments are named and therefore belong to `**attrs`, the attributes of the div. Python's rules about not mixing list and keyword arguments apply. In every element, put all the *content args first, followed by all the **attrs arguments. 

The <style> tag is the only exception to the pattern. Its signature is `Style(**content)`.  This is done to reduce (but alas not completely eliminate) the need for quoting the selectors in CSS rulesets.
- If you need to set attributes on a style element, do it in a secondary call as shown in the doctest below.
```
          style = Style(body=dict(margin='4px'), p=dict(color='blue'))
          style.A.update({'type':'text/css'})
          style.render()
          '<style type="text/css">body { margin:4px; } p { color:blue; }</style>' 
```
The design pattern for `htmltree` is "as simple as possible but not simpler." Using built-in Python objects, dicts and lists, means that all the familiar methods of those objects are available when manipulating trees of Elements. Notice, for instance, the use of `update` and `append` in the Quick start examples. 
```
body.A.update(dict(style={'background-color':'black'}))
body.C.append(H1("Hello, htmltree!", _class='myclass', id='myid'))
```
But wait a minute! What are 'body.A' and 'body.C'? Read on ...

### Public members
You can access and modify the attributes and content of an element `el` as `el.A` and `el.C` respectively. The tagname is also available as `el.T` though this is generally not so useful as the other two. 

The attribute member, `el.A` is an ordinary Python dictionary containing whatever keyword arguments were passed when the element was created. You can modify it with `update()` as shown in the Quick Start example or use any of the other dictionary methods on it. You can also replace it entirely with any dict-like object that has an `items()` method that behaves like dict.items()

The content member, `el.C` is normally a Python list. It contains all the stuff that gets rendered between the closing and ending tags of an element. The list may hold an arbitrary mix of strings, ints, float, and objects. In normal usage, the objects are of type `htmltree.Element`. This is the element type returned by all the functions in htmltree.py. You can use all the normal Python list methods (append, insert, etc) to manipulate the list.

(If you insert objects (other than those listed above), they should have a `render(indent=-1)` method that returns valid HTML with the same indentation conventions as the htmltree.Element.render method described in the next section.)

### Rendering
The render method emits HTML. In the examples above, we've called it as doc.render(0) to display the entire document tree in indented form. Calling it with no arguments emits the HTML as a single line with no breaks or spaces. Values > 0 increase the indentations by 2 spaces * the value.
```
>>> print(head.render())
<head><meta name="author" content="Your Name Here"/></head>

>>> print(head.render(0))

<head>
  <meta name="author" content="Your Name Here"/>
</head>

>>> print(head.render(1))

  <head>
    <meta name="author" content="Your Name Here"/>
  </head>
```

The `renderToFile()` method also accepts an `indent` argument.

## Usage tips

### Rolling your own
The simplest possible extension is wrapping a frequently used tag to save a little typing. This is already done for you for all the wrapper functions in htmltree.py. But if you need something that's not defined it only takes two lines of code (not counting the import).
```
from htmltree import KWElement
def Foo(*content, **attrs):
    return KWElement('foo', *content, **wrappers)
```
For an empty tag element, omit the content arg and pass None to KWElement().
```
def Bar(**attrs):
    return KWElement('bar', None, **attrs)
```

### Bundling
Wrapping commonly used fragments in a function is easy and useful, e.g. 
```
def docheadbody():
    head = Head()
    body = Body()
    doc = Html(head, body)
    return doc, head, body
    
>>> doc, head, body = docheadbody()
```

### Looping
Use loops to simplify the creation of many similar elements.
```
for id in ('one', 'two', 'three'):
     content = "Help! I'm trapped in div {}.".format(id)
     body.C.append(Div(content, id=id))
    
>>> print(body.render(0))
<body>
  <div id="one">
    Help! I'm trapped in div one.
  </div>
  <div id="two">
    Help! I'm trapped in div two.
  </div>
  <div id="three">
    Help! I'm trapped in div three.
  </div>
</body>
```
### Using *htmltree* with [*Transcrypt™*](https://transcrypt.org/)
This project was designed from the ground up to be compatible with Transcrypt to create a pure Python development environment  for HTML/CSS/JS on both sides of the client/server divide.

If you've installed *htmltree* with `pip`, Transcrypt will find it when transpiling your Python files to JavaScript if you import it as `htmltree`. If you have a need to install and access *htmltree* by other means,  see 
  * http://www.transcrypt.org/docs/html/special_facilities.html for information about Transcrypt's module mechanism and 
  * https://github.com/Michael-F-Ellis/htmltree/issues/3 for a discussion of some specific ways to locate htmltree at compile time.

Also, look at the modules `sanitycheck.py` and `client.py` in the `tests/` directory as a template for developing and testing with htmltree and Transcrypt. For a more elaborate template with a built-in server, AJAX/JSON data updates and automatic rebuild/reload when source files change, see [NearlyPurePythonWebAppDemo](https://github.com/Michael-F-Ellis/NearlyPurePythonWebAppDemo)

All the functions should work the same as under CPython. If not, please submit an issue on GitHub so I can fix it!


## List of wrapper functions
```
Html(*content, **attrs):
Head(*content, **attrs):
Body(*content, **attrs):
Link(**attrs):
Meta(**attrs):
Title(*content, **attrs):
Style(**content):
Address(*content, **attrs):
Article(*content, **attrs):
Aside(*content, **attrs):
Footer(*content, **attrs):
Header(*content, **attrs):
H1(*content, **attrs):
H2(*content, **attrs):
H3(*content, **attrs):
H4(*content, **attrs):
H5(*content, **attrs):
H6(*content, **attrs):
Nav(*content, **attrs):
Section(*content, **attrs):
Blockquote(*content, **attrs):
Dd(*content, **attrs):
Div(*content, **attrs):
Dl(*content, **attrs):
Dt(*content, **attrs):
Figcaption(*content, **attrs):
Figure(*content, **attrs):
Hr(**attrs):
Li(*content, **attrs):
Main(*content, **attrs):
Ol(*content, **attrs):
P(*content, **attrs):
Pre(*content, **attrs):
Ul(*content, **attrs):
A(*content, **attrs):
B(*content, **attrs):
Br(**attrs):
Cite(*content, **attrs):
Code(*content, **attrs):
Em(*content, **attrs):
I(*content, **attrs):
S(*content, **attrs):
Samp(*content, **attrs):
Small(*content, **attrs):
Span(*content, **attrs):
Strong(*content, **attrs):
Sub(*content, **attrs):
Sup(*content, **attrs):
U(*content, **attrs):
Area(**attrs):
Audio(*content, **attrs):
Img(**attrs):
Map(*content, **attrs):
Track(**attrs):
Video(*content, **attrs):
Embed(**attrs):
Object(*content, **attrs):
Param(**attrs):
Source(**attrs):
Canvas(*content, **attrs):
Noscript(*content, **attrs):
Script(*content, **attrs):
Caption(*content, **attrs):
Col(**attrs):
Table(*content, **attrs):
Tbody(*content, **attrs):
Td(*content, **attrs):
Tfoot(*content, **attrs):
Th(*content, **attrs):
Thead(*content, **attrs):
Tr(*content, **attrs):
Button(*content, **attrs):
Datalist(*content, **attrs):
Fieldset(*content, **attrs):
Form(*content, **attrs):
Input(**attrs):
Label(*content, **attrs):
Legend(*content, **attrs):
Meter(*content, **attrs):
Optgroup(*content, **attrs):
Option(*content, **attrs):
Output(*content, **attrs):
Progress(*content, **attrs):
Select(*content, **attrs):
Textarea(*content, **attrs):
```


