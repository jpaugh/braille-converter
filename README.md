# What is it?

braille-converter is a program that converts English text to Fully
Contracted (Grade 2) Braille. Aims to account for every rule that does
not rely on semantic analysis, and even a few that do, but can be
roughly approximated.  Does not use BRF or any exotic format. It simply
uses the Braille code-points of Unicode. We're targeting the 2002
revision of *English Braille:Amerian Edition*, released by the Braille
Authority of North America. Right now, we have support for Rule I of
this document, and plan to support the other rules in future releases.

### What's it for?

This program is designed to aid Braille transcribers, by freeing them
from manually transcribing a document. It's output must still be edited
(as no computer can replace a transcriber, who must be able to interpret
the document's meaning and style). For this reason, usability is a major
aim of the project. braille-converter already has a graphical interface,
appropriate for transcribing shorter documents or notes. (Support for
large documents and batch processing of files is in the works).

### What's the difference between this program and online Braille converter X?

Many of the Braille converters online use what is called Grade 1
Braille, which consists of the alphabetical characters, and maybe some
punctuation.  However, there is a much more powerful version, called
Grade 2, or Contracted Braille, which empowers blind readers by allowing
them to read more quiclky. This is important, because reading by touch
is much slower than reading by sight.

braille-converter supports Grade 2 Braille, in a limited form which will
improve as the project progresses. It is already very usable, and aims
to support tricky features, including proper quote and apostrophe
handling for most cases.

## How to use

Download the latest version from the
[downloads](https://github.com/jpaugh64/braille-converter/downloads)
page, then unzip it and navigate the `bin/` sub directory. run `brl.py`.
Double-clicking it should work, but if not, follow the commandline
instructions below.

Having difficulty? Please let me know! Drop me a line on the [issue
tracker](https://github.com/jpaugh64/braille-converter/issues/). Enjoy!

### How to use from the command line

Just download and unzip the file as above, but instead open a terminal,
navigate to the unzipped folder, and into the `bin/` subdirectory. Then
run `brl.py` instead. Like so:

    $ cd Downloads/braille_converter-x.x.YYYY/bin
    $ ./brl

If you'd like to run brl without the gui, then pass in the `--cmdline` option

    $ ./brl --cmdline

On Windows, the commands are slightly different:

    > cd Downloads\braille_converter-x.x.YYYY\bin
    > brl

or perhaps

    > brl --cmdline

Now, type in some text, and see how it handles it! If you have any
problems or suggestions, don't hesitate to open an issue in the
[issue tracker](https://github.com/jpaugh64/braille-converter/issues/).
Please make sure to tell me which version you were using.

###How to open a terminal
- Mac: Search in your utilities for a program called 'Terminal'
- Windows: In the Start Menu, seach for a program called 'cmd'.
- Gnome: Press <kbd>Alt</kbd>+<kbd>F2</kbd> and type `gnome-terminal`, then
  press <kbd>Enter</kbd>
- Other Linux: Open xterm, or press <kbd>Ctrl</kbd><kbd>Alt</kbd>+<kbd>F1</kbd>
  and log in.

##Installation requirements

- Python (2.7 has been tested; 3.x is unfortunately unsupported)
- Any operating system
- Minimum specs: Runs fine on my little netbook.

To get a copy of Python, visit www.python.org and click on the
"Downloads" tab at the side. Under that, choose your operating system,
or if you wish, compile it from source. 

###For Mac
Macs have Python pre-installed, but usually that version is quite
outdated. For now, this module does not support any Python older than
2.7 (the current release), so you may need to get that version. To do
so, follow the generic instructions above.

###For Linux/BSD
Most likely, your package manager supplies a pre-compiled package for
python. On Ubuntu, the command to install it is

    $ sudo apt-get install python2.7

###For Windows
The installers at www.python.org are the best way to go. Follow the
generic instructions above.

##Python Developers

This program is also a package, with some handy functions inside:

- `convert` - This is the workhorse. Input a line of text, and receive
  the Braille text in return
- `dots` - Convert a string of "dots" to Braille cells. (See below.)
- `opt` - Mungles options that affect the behavior of the whole package.

Planned developments include parsing files en-masse, rather than
line-at-a-time, and a class-based api.

So, `import braille` for `5 * 'fun'`.

###What are dots?

Dots is a notation often used to succinctly describe Braille cells in
normal ASCII. Braille cells consist 6 dots, arranged in a 3x2 grid
pattern, which allows them to be easily numbered. For example, the dots
pattern "1235" represents the Braille cell ⠗ which stands for the letter
*r*.

In the internals of the module, you'll see the dot notation used to
avoid repeating Ctl+Shift+u28xx and the uncomfortable hexadecimal math
of the codepoints--which for Braille follows a nice, regular pattern
that makes said math possible. The digits describing each Braille cell
(character) must be separated by a single space, like this:

    dots('123 123 1 134 1')

whose return value is `'⠇⠇⠁⠍⠁'` (llama). To include spaces in the
returned string (for example, to Braille several words together), use an
an extra space between the dots fooutputs r each space you wish to return.

    dots('6 13   24 234  1234 246 12456 235')

Which becomes `'⠠⠅ ⠊⠎ ⠏⠪⠻⠖'` (Knowledge is power!)

## License

Copyright 2012 Jonathan Paugh. MIT style license. See [COPYING][1] for
details.
[1]: https://github.com/jpaugh64/braille-converter/blob/master/COPYING
