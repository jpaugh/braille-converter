# What is it?

braille-converter is a program that converts English text to Fully
Contracted (Grade 2) Braille. Aims to account for every rule that does
not rely on semantic analysis, and even a few that do, but can be
roughly approximated.  Does not use BRF or any exotic format. It simply
uses the Braille code-points of Unicode.

# What's it for?

This program is designed to aid Braille transcribers, by freeing them
from manually transcribing a document. It's output must still be edited
(as no computer can replace a transcriber, who must be able to interpret
the document's meaning and style). For this reason, usability is a major
aim of the project. braille-converter already has a graphical interface,
appropriate for transcribing shorter documents or notes. (Support for
large documents and file processing of files is in the works).

# What's the difference between this program and online Braille converter X?

Many of the Braille converters online use what is called Grade 1
Braille, which consists of the alphabetical characters, and maybe some
punctuation.  However, there is a much more powerful version, called
Grade 2, or Contracted Braille, which empowers blind readers by allowing
them to read more quiclky. This is important, because reading by touch
is much slower than reading by sight.

braille-converter supports Grade 2 Braille, in a limited form which will
improve as the project progresses. It is already very usable, and aims
to support advanced features--I bet you won't find better handling of
single quotes and apostrophes! By the way, it uses American English
Braille, and is coded according to the 2002 *English Braille: American
Edition* released by the *Braille Authority of North America*.

# How to use

Using it is as easy as pie, but it does require that you have
[Python](www.python.org) installed--at least for the time being. Just
download the project as a
[zip file](https://github.com/jpaugh64/braille-converter/zipball/master),
then unzip it, and run the 'gui.py' file in Python. (This should work by
double-clicking on it. If not, follow the command line instructions
below, but type  `python gui.py` instead of `python braille.py`.)

# How to use from the command line

Just download and unzip the file as above, but instead open a terminal,
navigate to the unzipped folder, and run `braille.py` instead. Like so:

```shell
$ cd Downloads/jpaugh64-braille-converter-xxxxxx
$ python braille.py
```

Now, type in some text, and see how it handles it!


Press Ctrl+C (or Ctrl+Break) to quit, and please send me any suggestions
or bugs, via the [issue
tracker](https://github.com/jpaugh64/braille-converter/issues/): Enjoy!

#How to open a terminal
- Mac: Search in your utilities for a program called 'Terminal'
- Windows: In the Start Menu, seach for a program called 'cmd'.
- Linux: Press `Ctrl+Alt+F1` and log in. :-p

#Installation requirements

- Python (2.7 has been tested) 
- Any operating system
- Minimum specs: Runs fine on my little netbook.

#Python Developers

This program is also a module, with some handy functions defined:

- `convert` - This is the workhorse. Input a line of text, and receive
  the Braille text in return
- `dots` - Convert a string of "dots" to Braille cells. (See below.)
- `dot` - Convert a dot string for a _single cell_ to Braille

So, `import braille` for `5 * 'fun'`.

##What are dots?

Dots is a notation often used to succinctly describe Braille cells
without having to print them. Braille cells consist 6 dots, arranged in
a 3x2 grid pattern, which allows them to be easily numbered. For
example, the dots pattern "123" represents the Braille cell ⠇ which
stands for the letter *l*.

In the internals of my module, I used the dot notation to avoid
repeating Ctl+Shift+u28xx and the uncomfortable hexadecimal math of the
codepoints--which follow a nice, regular pattern that makes said math
possible. Whenever I need multiple dots at a time, I string them
together with intervening spaces, like this: `dots('123 123 1 134 1')`
which outputs `'⠇⠇⠁⠍⠁'` (llama). IfI need to output a string with
embedded spaces, I si mply double the spaces, like so: `dots('6 13   24
234  246 12456 235')`, which outputs `'⠠⠅ ⠊⠎ ⠏⠪⠻⠖'` (Knowledge is
power!)
