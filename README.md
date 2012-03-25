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

Just clone this repo in your Sublime Text 2 Package dir.

```
$ git clone https://github.com/erichard/SublimeCTagsPHP
```


Features
========

One unique feature for the moment, but it's AWESOME !

I've called it the 'import use statement' feature. Just bring your cursor hover
a class name, hit the F5 key (default but customizable) and that's it.

Based on the current file content, the use statement could be added in :

  - Below the last use statement
  - Below the namespace statement (with an empty line between both)
  - Below the php opening tag (with an empty line between both)