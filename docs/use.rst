.. py:currentmodule:: manipulate

Using manipulate
================


Installation
~~~~~~~~~~~~

manipulate is available on the `Python Package Index`__ and can be installed
with any tools for managing Python environments.

__ https://pypi.org

mpl modify *.csv eval:x=int(y)+1 drop:z

mpl modify *.py parse:pretty add:x,default=1

mpl read *.csv pick:a,b,c render:pretty write:suffix=.txt

mpl read *.csv pick:1,2,3
