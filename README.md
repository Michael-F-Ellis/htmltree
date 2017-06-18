# Python htmltree module

## Create and manipulate HTML and CSS from the comfort of Python
  * Easy to learn. One module, one class, two methods.
  * Easy to extend. 
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


