# Skit Styleguide

## Python Style
### 1) Indentation

* Python heavily inforces indentation and as such we should have consistent
indentation throughout the entire project.\n
* Only use soft tabs, with each tab being equivalent to 4 spaces.\n
* Do not use hard tabs ('\\t' characters). For example in vim this can be
achieved with the following settings in your ~/.vimrc file:

```
set tabstop=4
set shiftwidth=4
set expandtab
```
* Each line should only be 80 columns wide.

### 2) Whitespace

* No trailing whitespaces.
* No unnecessary blank lines. There should be one blank line after each
function and after the end of a class definition.

```
#Correct:
class MathThing(object):
    def add(first, second):
        return first + second

    def sub(first, second):
        return first - second

if __name__ == '__main__':
    thing = MathThing()
    'One and one is %d' % thing.add(1, 1)
#Wrong:
class MathThing(object):
    def add(first, second):
        return first + second


    def sub(first, second):
        return first - second
if __name__ == '__main__':

    thing = MathThing()
    'One and one is %d' % thing.add(1, 1)
```

* Every token involved in an operation should be seperated by one space.
```
#Correct:
    num = 1 + 2
#Wrong:
    num = 1+2
    num = 1  +  2
* The only exception is for default arguments in a function's parameter list.
```
#Correct:
    def __str__(name='John Smith', id):
        return '%s has id %d' % (name, id)
#Wrong:
    def __str__(name = 'John Smith', id):
        return '%s has id %d' % (name, id)
```

### 3) Shebangs

* If a file is meant to be executable, the first line should be:
```
#!/usr/bin/env python
