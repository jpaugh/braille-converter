# What is it?

braille-converter is a program that converts English text to Fully
Contracted (Grade 2) Braille. Aims to account for every rule that does
not rely on semantic analysis, and even a few that do, but can be
roughly approximated.  Does not use BRF or any exotic format. It simply
uses the Braille code-points of Unicode.

# What's it for?

Eventually, I expect this program to be useable by Braille transcribers,
who can refine its output rather than doing it all by hand. Therefore,
usability is a major aim: if you can't figure out how to use it, hang
tight until I get a simpler-to-use version released. And, yes, I do
intend to add a *graphical* interface.

# How to use

Using it is as easy as pie, but it does require that you have Python
installed--at least for now. Just download
[`braille.py`](https://github.com/downloads/jpaugh64/braille-converter/braille.py)
and open a terminal, then navigate to the download folder, and type:

    $ python ./braille.py

Now, type in some text, and see how it handles it!

Press Ctrl+C (or Ctrl+Break) to quit, and please send me any suggestions
or bugs, via the [issue
tracker](https://github.com/jpaugh64/braille-converter/issues/): Enjoy!

#Installation requirements

- Python 2.7 (tested) 
- Any operating system

#Python Developers

This program is also a module, with some handy functions defined:

- `convert` - This is the workhorse. Input a line of text,
and receive the Braille text in return
- `dots` - Convert a string of "dots" to Braille cells. (See below.)
- `dot` - Convert a dot string for a _single cell_ to Braille

So, import for `5 * 'fun'`.

##What are dots? 

Dots is a notation often used to succinctly describe Braille cells
without having to print them. Braille cells consist 6 dots, arranged in
a 3x2 grid pattern, which allows them to be easily numbered. For
example, the dots pattern "123" represents the Braille cell ⠇ which
stands for the letter *l*.

In the internals of my module, I used the dot notation to avoid
repeating Ctl+Shift+u28xx and the uncomfortable hexadecimal math of
the codepoints--which follow a nice, regular pattern that makes said math 
possible. Whenever I need multiple dots at a time, I string them together 
with intervening spaces, like this: `dots('123 123 1 134 1')` which outputs 
`'⠇⠇⠁⠍⠁'` (llama). IfI need to output a string with embedded spaces, I si
mply double the spaces, like so: `dots('6 13   24 234  246 12456 235')`, which outputs
`'⠠⠅ ⠊⠎ ⠏⠪⠻⠖'` (Knowledge is power!)