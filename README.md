# Python htmltree module

## Create and manipulate HTML and CSS from the comfort of Python
  * Easy to learn. One module, one class, two methods.
  * Flexible usage and easy extension. 
  * Fully compatible with Jacques De Hooge's [*Transcrypt™*](https://transcrypt.org/) Python to JS transpiler

### Quick start -- open a Python interpreter and type or paste the following
```
>>> from htmltree import Element as E
>>> head = E('head', {}, [])
>>> body = E('body', {}, [])
>>> doc = E('html', {}, content=[head, body])
>>> print(doc.render(0))

<html>
  <head>
  </head>
  <body>
  </body>
</html>

>>> ## Add some attributes and content
>>> who = E('meta', dict(name="author", content="Your Name Here"), None)
>>> head.C.append(who)
>>> body.A.update({'style':{'background-color':'black'}})
>>> body.C.append(E('h1',{'class':'myclass', 'id':'myid'}, ["Hello htmltree!"]))
>>> print(doc.render(0))

<html>
  <head>
    <meta name="author" content="Your Name Here"/>
  </head>
  <body style="background-color:black;">
    <h1 id="myid" class="myclass">
      Hello htmltree!
    </h1>
  </body>
</html>

```
## Explanations
The Element class (which we've shortened to 'E') can represent and render any HTML element. The constructor signature is 

```
Element(tag, attrs, content)
```
* `tag` is any valid tag name, e.g. 'div', 'span', ...
* `attrs` should be a dictionary of valid attribute names and values, e.g. {'class':'myclass', 'id':'myid', ... } 
* `content` is what goes between the opening and closing tag. It should be either None or a list containing any mixture of Elements and strings. 
  * Passing None as the content argument has a special meaning. It tells the render() method that the tag is a singleton with no content or closing tag, e.g. `<meta>` or `<br>`.

### Special cases
The `style` attribute and `<style>` tag are both handled correctly if you pass them as a nested dictionary, e.g.
```
{'style':{'background-color':'black', ...}}
```
for an inline style attribute, and

```
>>> mystyle = E('style', None, {'p.myclass': {'margin': '4px', 'font-color': 'blue'}})
>>> print(mystyle.render(0))

<style>
p.myclass { margin:4px; font-color:blue; }
</style>

```
The nested dicts may have as many items as you desire, i.e. no need for separate CSS files! Just code it Python along with the HTML.

### Public members
You can access and modify the attributes and content of an Element `el` as `el.A` and `el.C` respectively. The tagname is also available as `el.T` though this is generally not so useful as the other two.

### Rendering
The render method emits HMTL. In the examples above, we've called it as doc.render(0) to display the entire document tree in indented form. Calling it with no arguments emits the HTML as a single line with no breaks or spaces. For example
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
Values > 0 increase the indentations by 2 spaces * the value.

## Using and extending
The design pattern for `htmltree` is "as simple as possible but not simpler." Using built-in Python objects, dicts and lists, means that all the familiar methods of those objects are available when manipulating trees of Elements. Notice the use of `update` and `append` in the Quick start examples. 
```
>>> body.A.update({'style':{'background-color':'black'}})
>>> body.C.append(E('h1',{'class':'myclass', 'id':'myid'}, ["Hello htmltree!"]))
```

The simplest possible extension is wrapping a frequently used tag to save a little typing.
```
def div(attrs, content):
    return E('div', attrs, content)

>>> el = div({},["Help! I'm trapped in a div."])
>>> print(el.render(0))
<div>
  Help! I'm trapped in a div.
</div>
```
Similarly, we could have written a reusable doc outline to create the first part of our example.
```
def docheadbody():
    head = E('head', {}, [])
    body = E('body', {}, [])
    doc = E('html', {}, [head, body])
    return doc, head, body
    
>>> doc, head, body = docheadbody()
>>> print(doc.render(0))
<html>
  <head>
  </head>
  <body>
  </body>
</html>
```

Python loops simplify the creation of many similar elements.
```
>>> for id in ('one', 'two', 'three'):
...     attrs = dict(id=id)
...     content = "Help! I'm trapped in div {}.".format(id)
...     body.C.append(div(attrs, content))
...     
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
>>> 
```

## Module help
```
>>> help(E)
class Element(builtins.object)
 |  Generalized nested html element tree with recursive rendering
 |  
 |  Constructor arguments:
 |      tagname : valid html tag name (string)
 |  
 |      attrs   : attributes (dict | None)
 |                  keys must be valid attribute names (string)
 |                  values must be (string | list of strings | dict of styles)
 |  
 |      content : (None | string | int | float | list of (strings/ints/floats and/or elements)
 |                elements must have a 'render' method that returns valid html.
 |                <style> tag gets special handling. You may pass the css as a dict of
 |                the form {'selector': {'property':'value', ...}, ...}
 |  
 |  Public Members:
 |      T : tagname
 |      A : attribute dict
 |      C : content
 |  
 |  Instance methods:
 |      render(indent=-1) -- defaults to no indentation, no newlines
 |                           indent >= 0 behaves according to the indented()
 |                            function in this module.
 |
 |  Helper functions (defined at module level):
 |  
 |      indented(contentstring, indent) -- applies indentation to rendered content
 |  
 |      renderstyle(d) -- Special handline for inline style attributes.
 |                        d is a dictionary of style definitions
 |  
 |      renderCss(d, indent=-1) -- Special handling for <style> tag
 |                                 d is a dict of CSS rulesets
 |  
 |  Doctests:
 |  >>> E = Element
 |  >>> doc = E('html', None, [])
 |  >>> doc.render()
 |  '<html></html>'
 |  >>> doc.C.append(E('head', None, []))
 |  >>> doc.render()
 |  '<html><head></head></html>'
 |  >>> body = E('body', {'style':{'background-color':'black'}}, [E('h1', None, "Title")])
 |  >>> body.C.append(E('br', None, None))
 |  >>> body.render()
 |  '<body style="background-color:black;"><h1>Title</h1><br/></body>'
 |  >>> doc.C.append(body)
 |  >>> doc.render()
 |  '<html><head></head><body style="background-color:black;"><h1>Title</h1><br/></body></html>'
 |  
 |  >>> style = E('style', None, {'p.myclass': {'margin': '4px', 'font-color': 'blue'}})
 |  >>> style.render()
 |  '<style>p.myclass { margin:4px; font-color:blue; }</style>'
 |  
 |  >>> comment = E('!--', None, "This is out!")
 |  >>> comment.render()
 |  '<!-- This is out! -->'
 |  
 |  >>> comment.C = [body]
 |  >>> comment.render()
 |  '<!-- <body style="background-color:black;"><h1>Title</h1><br/></body> -->'
 |  
 |  Methods defined here:
 |  
 |  __init__(self, tagname, attrs, content)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  render(self, indent=-1)
 |      Recursively generate html
 |  
 ```

