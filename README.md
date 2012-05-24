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

Download the repository as a
[zip file](https://github.com/jpaugh64/braille-converter/zipball/master),
then unzip it and navigate the `bin/` sub directory. run `brl.py`.
Double-clicking it should work, but if not, follow the commandline
instructions below.

Having difficulty? Please let me know! Drop me a line on the [issue
tracker](https://github.com/jpaugh64/braille-converter/issues/): Enjoy!

# How to use from the command line

Just download and unzip the file as above, but instead open a terminal,
navigate to the unzipped folder, and into the `bin/` subdirectory. Then
run `brl.py` instead. Like so:

    $ cd Downloads/jpaugh64-braille-converter-xxxxxx/bin
    $ python brl.py

(`$` represents the command prompt, and is not required.)

Now, type in some text, and see how it handles it! Note that access to
braille-converter from the terminal solely (without a gui at all) is in
the works.

#How to open a terminal
- Mac: Search in your utilities for a program called 'Terminal'
- Windows: In the Start Menu, seach for a program called 'cmd'.
- Linux: Press `Ctrl+Alt+F1` and log in. :-p

#Installation requirements

- Python (2.7 has been tested)
- Any operating system
- Minimum specs: Runs fine on my little netbook.

You can get easily get a copy of Python for your operating system. visit
www.python.org, and navigate to the download page, which has versions
for Windows, Mac, and Linux. Download and install a "precompiled binary"
for the least hassle.

#Python Developers

This program is also a package, with some handy functions inside:

- `convert` - This is the workhorse. Input a line of text, and receive
  the Braille text in return
- `dots` - Convert a string of "dots" to Braille cells. (See below.)
- `dot` - Convert a dot string for a _single cell_ to Braille
- `opt` - Mungles options that affect the behavior of the whole package.

Planned developments include parsing files en-masse, rather than
line-at-a-type, and a class-based api.

So, `import braille` for `5 * 'fun'`.

##What are dots?

Dots is a notation often used to succinctly describe Braille cells
without having to print them. Braille cells consist 6 dots, arranged in
a 3x2 grid pattern, which allows them to be easily numbered. For
example, the dots pattern "1235" represents the Braille cell ⠗ which
stands for the letter *r*.

In the internals of my module, I used the dot notation to avoid
repeating Ctl+Shift+u28xx and the uncomfortable hexadecimal math of the
codepoints--which for Braille follows a nice, regular pattern that makes
said math possible. Whenever I need multiple dots at a time, I string
them together with intervening spaces, like this: `dots('123 123 1 134
1')` which outputs `'⠇⠇⠁⠍⠁'` (llama). If I need to output a string with
embedded spaces, I simply double the spaces, like so: `dots('6 13   24
234  1234 246 12456 235')`, which outputs `'⠠⠅ ⠊⠎ ⠏⠪⠻⠖'` (Knowledge is
power!)
