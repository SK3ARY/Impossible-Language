# Impossible Language 1.0.0

Impossible language (_IMPL for short_) is an _esoteric programming language_. The whole idea of Impossible language is that every time a program is run, the syntax changes to a random set of symbols making it very hard to write a program using this. Not to mention it only has two functionalities, set a cell to a value and print a value from a cell. I might add things like `if`, `for` and `while` but the more _"keywords"_ I add the harder it will be to actually run programs.

# What is "Base"

Using _base_ is just like not having the randomly generating tokens. It allows you to write a script using the following tokens and run every time.

__Set__: %<br>
__Out__: ><br>
__Strings__: "<br>
__Comments__: ;<br>

Programs written using base look like this:

```
; Set index (0) to "Hello world!"
% 0 "Hello world!"

; Print value of index (0)
> 0
```

# How it functions

IMPL works by creating a group of _"tokens"_ that the programmer is unaware of until compile time. The program will then use these instead of the base commands.

## Example

`Tokens = ["$", "}", "/", "."]`

Base:
```
; Prints "Hello world!"
% 0 "Hello world!"
> 0
```

Valid (with tokens):
```
$ Prints "Hello world!"
} 0 .Hello world!.
/ 0
```