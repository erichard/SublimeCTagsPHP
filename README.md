Sublime CTags PHP
=================

This Sublime Text 2 Package provides cool stuff for PHP 5.3+ coding session.


Dependency
==========

Obviously, you NEED the CTags plugin for Sublime Text 2.

  - https://github.com/SublimeText/CTags
  - Via package control (search for ctag)


Installation
===========

Search `ctagphp` in package control and you have done !

Or clone this repo in your Sublime Text 2 Package dir.

```
$ git clone https://github.com/erichard/SublimeCTagsPHP
```


Features
========

Two AWESOME features for the moment !


import_use
----------

The first one is 'import use statement'. Just bring your cursor hover
a class name, hit the F5 key (default but customizable) and that's it.

Based on the current file content, the use statement could be added in :

  - Below the last use statement
  - Below the namespace statement (with an empty line between both)
  - Below the php opening tag (with an empty line between both)


import_namespace
----------------

Just hit the F4 key, it will add the namespace definition based on the absolute
filename of the current file. I use a simple trick to determine where the
namespace begun, actually the namespace will start at the first CamelCased
folder.

If a namespace is already declared, the command will shout how crazy you are in
the status bar.

**Warning:** This feature require a filename so the command won't work in an unsaved buffer.