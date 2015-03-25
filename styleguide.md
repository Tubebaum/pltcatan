# Skit Styleguide

## Python Style
### Spacing

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

* No trailing whitespaces anywhere.
* There should only be one extra newline separating any two blocks.

```
\#Correct:
    def add(first, second):
        return first + second

    def sub(first, second):
        return first - second
\#Wrong:
    def add(first, second):
        return first + second


    def sub(first, second):
        return first - second
```

* Every arithmetic token should be seperated by one space.
```
\#Correct:
    num = 1 + 2
\#Wrong:
    num = 1+2
    num = 1  +  2
