# Skit Styleguide

## Python Style
### 1) Indentation

* Python heavily inforces indentation and as such we should have consistent
indentation throughout the entire project.
* Only use soft tabs, with each tab being equivalent to 4 spaces.
* Do not use hard tabs ('\\t' characters). For example in vim this can be
achieved with the following settings in your ~/.vimrc file:

```
set tabstop=4
set shiftwidth=4
set expandtab
```
* Each line should only be 80 columns wide.

### 2) Whitespace

* No trailing whitespaces. Only exception is that each file should end with a
newline character for prettier 'cat' output.
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
```

* The only exception is for default arguments in a function's parameter list.

```
#Correct:
    def __str__(name='John Smith', id):
        return '%s has id %d' % (name, id)

#Wrong:
    def __str__(name = 'John Smith', id):
        return '%s has id %d' % (name, id)
```

* Comma-delimited tokens should have one space after every comma.

```
#Correct:
    goodTuple = (1, 2, 3)

Wrong:
    badTuple = (1,2,3,   4)
```

### 3) String literals

* Use single quotes for string literals.

```
    name = 'John Smith'
```

* Can make an exception and use double quotes if the string contains a single
quote character (of course you can escape the character but that makes it
harder to read).

```
    name = "John Smith's house is down the block"
```

### 4) Shebangs

* If a file is meant to be executable, the first line should be:

```
#!/usr/bin/env python
```
