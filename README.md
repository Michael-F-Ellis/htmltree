# Python htmltree module

## Create and manipulate HTML and CSS from the comfort of Python
  * Easy to learn. One module, one class, two methods.
  * Flexible usage and easy extension. 
  * Fully compatible with Jacques De Hooge's [*Transcrypt™*](https://transcrypt.org/) Python to JS transpiler

### Quick Start
#### Open a Python interpreter and type or paste the following
```
>>> from elementwrappers import *
>>> head = Head()
>>> body = Body()
>>> doc = Html(head, body)
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
>>> who = Meta(name="author",content="Your Name Here")
>>> head.C.append(who)
>>> body.A.update(dict(style={'background-color':'black'}))
>>> body.C.append(H1("Hello, htmltree!", _class='myclass', id='myid'))
```
#### and print the result.
```
>>> print(doc.render(0))
<html>
  <head>
    <meta content="Your Name Here" name="author">
  </head>
  <body style="background-color:black;">
    <h1 id="myid" class="myclass">
      Hello, htmltree!
    </h1>
  </body>
</html>
```
## Discussion
Importing * from elementwrappers.py provides 72 wrapper functions (as of this writing) that cover the most of the common non-obsolete HTML5 tags.  To see the most up-to-date list you can do `help(elementwrappers)` from the command line of a Python interactive session or look futher down on this page for listing. The function's names and arguments follow simple and consistent conventions.

- Functions are named by tag with initial caps, e.g. `Html()`
- The signature for non-empty tags is `Tagname(*content, **attrs)`
- The signature for empty tags is `Tagname(**attrs)` (Empty refers to elements that enclose no content and need no closing tag.)
- The <style> tag is the only exception. It's signature is `Style(**content)`.  This is done to reduce (but alas not completely eliminate) the need for quoting the selectors in CSS rulesets.
- If you need to set attrs on a style element, do it in a secondary call as shown in the doctest below.
```
          >>> style = Style(body=dict(margin='4px'), p={'color':'blue'})
          >>> style.A.update({'type':'text/css'})
          >>> style.render()
          '<style type="text/css">body { margin:4px; } p { color:blue; }</style>' 
```
The design pattern for `htmltree` is "as simple as possible but not simpler." Using built-in Python objects, dicts and lists, means that all the familiar methods of those objects are available when manipulating trees of Elements. Notice, for instance, the use of `update` and `append` in the Quick start examples. 
```
>>> body.A.update(dict(style={'background-color':'black'}))
>>> body.C.append(H1("Hello, htmltree!", _class='myclass', id='myid'))
```
But wait a minute! What are 'body.A' and 'body.C'? Read on ...

### Public members
You can access and modify the attributes and content of an Element `el` as `el.A` and `el.C` respectively. The tagname is also available as `el.T` though this is generally not so useful as the other two. 

The attribute member, `el.A` is an ordinary Python dictionary containing whatever keyword arguments were passed when the element was created. You can modify it with `update()` as shown in the Quick Start example or use any of the other dictionary methods on it. You can also replace it entirely with any dict-like object that has an `items()` method that behaves like dict.items()

The content member, `el.C` is normally a Python list. It contains all the stuff that gets rendered between the closing and ending tags of an element. The list may hold an arbitrary mix of strings, ints, float, and objects. In normal usage, the objects are of type `htmltree.Element`. This is the element type returned by all the functions in elementwrappers.py. You can use all the normal Python list methods (append, insert, etc) to manipulate the list.

(If you insert objects (other than those listed above), they should have a `render(indent=-1)` method that returns valid HTML with the same indentation conventions as the htmltree.Element.render method described in the next section.)

### Rendering
The render method emits HMTL. In the examples above, we've called it as doc.render(0) to display the entire document tree in indented form. Calling it with no arguments emits the HTML as a single line with no breaks or spaces. Values > 0 increase the indentations by 2 spaces * the value.
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


## Using and extending

In the Quick Start example, we created elements and assigned them to variables so we could alter their content later. However, we could also have created the example by writing it out all at once.

```
doc = Html(
        Head(
          Meta(name="author",content="Your Name Here")),
         Body(
           H1("Hello, htmltree!",
               id="myid", _class="myclass")))
```
That's short and clean and renders exactly the same html, but sacrifices ease of alteration later in the execution. Your choices should come down to whether you're creating static html or dynamic content based on information that's not available until run time.

The simplest possible extension is wrapping a frequently used tag to save a little typing. This is already done for you for all the wrapper functions in elementwrappers.py. But if you need something that's not defined it only takes two lines of code (not counting the import).
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

Wrapping common used fragments in a function can be useful, e.g. 
```
def docheadbody():
    head = Head()
    body = Body()
    doc = Html(head, body)
    return doc, head, body
    
>>> doc, head, body = docheadbody()
```

Python loops simplify the creation of many similar elements.
```
for id in ('one', 'two', 'three'):
     attrs = dict(id=id)
     content = "Help! I'm trapped in div {}.".format(id)
     body.C.append(Div(attrs, content))
    
>>> print(body.render(0))
<body>
  <div>
    {'id': 'one'}
    Help! I'm trapped in div one.
  </div>
  <div>
    {'id': 'two'}
    Help! I'm trapped in div two.
  </div>
  <div>
    {'id': 'three'}
    Help! I'm trapped in div three.
  </div>
</body>

```
#### A small gotcha
Did you notice the underscore in `H1("Hello, htmltree!", _class='myclass', id='myid')`? That's because `class` is a Python reserved word.  Prefixing it with an underscore avoids a syntax error. Class is the most common problem but you might also run into it with `for` as a label attribute. 

To help deal with this, the render() function strips off leading and trailing underscores in attribute names. It also replaces internal underscores in attribute names with dashes. That avoids the problem of Python trying to interpret ` ... data-role="magic"` as a subtraction expression. Use ```data_role="magic"``` instead.






