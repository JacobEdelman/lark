# Lark
A programming language with mutable syntax.
______
0.3.4: The prototyped version.

__Name: Note that Lark does share a name with another, obscure
[Lark](https://github.com/munificent/lark) that was last updated when I was 11.
This Lark has no relationship whatsoever with the other Lark except, by chance,
sharing a name. __

## Vision
Lark aims to be a language where syntax is fully mutable and all functions are defined simply as syntax mutations. This is similar to macros, but more powerful as a set of transformations (functions except with arbitrary syntax) is seen as a form of context-free grammar, and an algorithm similar to CYK parsing is used to parse the program. This is augmented by automatically handling interdependencies regardless of the order transformations are given in.

## Status
Lark is in very heavy development. As of now Lark can function fully and may be
usable for small tasks. The initial goal of making a proof-of-concept is
complete.

## Use
Lark is used in the following manner: `python lark [space separated file names
to execute]`. It works in both Python 2 and Python 3 as of now but Python 3 appears
to be significantly faster.

## Examples

### Hello world
The main value of any program will be printed out so the hello world program is as follows:
```
main = "hello world"
```
This may be executed by calling `./lark [file name]`

### Boolean Logic
The entire system of logic as it exists in lark is written in pure Lark and is defined as follows:
```
True = True
False = False
not $a = not $a
not True = False
not False = True
$a and $b = False
True and True = True
```
### If Statements
If statements may then be added in the following manner:
```
if True then $x else $y = $x
if False then $x else $y = $y
if $z then $x else $y = if $z then $x else $y
```
Notably, Lark's laziness is put to use here as the portions of the if statement that it does not evaluate to will not be executed.

### String and Tuple Manipulations
String and tuple manipulations are similar to those in python:
```
"abc"[1:] is "bc"
"de"[-1] is "e"
(1,2)[0] is 1
```

### Fibonacci
A simple but inefficient fibonacci function that is exponential time:
```
fib($x)=fib($x-1)+fib($x-2)
fib(1)=1
fib(2)=1
main = fib(10)
```

### Better Fibonacci
A more efficient fibonacci function that is linear time:
```
nextfib(()) = (1,1)
nextfib($a)=nextfib($a)
nextfib(cons($a,cons($b,$c))) = cons($a+$b,cons($a,cons($b,$c)))
fibs(0) = ()
fibs($x)=nextfib(fibs($x-1))
fib($x) = fibs($x)[0]
main = fib(10)
```

### Infinite List Lazy Fibonacci
A demonstrations of laziness using an infinite list fibonacci numbers:
```
fibs_after_nth($x) = cons(fib($x), fibs_after_nth($x+1))
infini_fibs = fibs_after_nth(1)
main = infini_fibs[3:5]
```

## Contributors
Jacob Edelman is the leader and, as of now, the sole creator of Lark. Pull requests are welcome.


## History:
- Version 0.0.0: Pre-Usable, mostly a rough draft of core code.
- Version 0.0.1: Core code for certain sections is done.
- Version 0.0.2: Core code is finished. It should be possible to write programs.
- Version 0.0.3: Basic programs can be created. Multiplication was created in
lark.
- Version 0.3.0: Old version of lark was completely trashed and rewritten three
times. I think. I lost count. The newest version is in python.
- Version 0.3.1: Lark is made fully usable and functioning.
- Version 0.3.2: Strings are added to Lark. All major features have now been
added to Lark.
- Version 0.3.3: Lark can be demoed and tests all work. Socket addition has
begun and a standard library has been initialized. To string methods were added.
- Version 0.3.3: Lark now runs with Python 3 as well as Python 2. Python 3 is
significantly faster.
