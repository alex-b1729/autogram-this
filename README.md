# Autogram This

A program that searches for and validates [autograms](https://en.wikipedia.org/wiki/Autogram), for example:

> This example autogram has nine o's, two f's, seventeen t's, three m's, thirty-one s's, three y's, seven h's, seven i's, seven w's, two p's, six a's, two d's, seven v's, two l's, three u's, seven r's, two g's, twenty-nine e's, sixteen n's, and four x's.




From [Wikipedia](https://en.wikipedia.org/wiki/Autogram):
> An autogram is a sentence that describes itself in the sense of providing an inventory of its own characters.

- [Usage](#usage)
  - [Python CLI](#python-cli)
  - [Rust CLI](#rust-cli)
  - [Python module](#python-module)
- [Capabilities](#capabilities)
  - [Add a suffix to the autogram](#add-a-suffix-to-the-autogram)
  - [Include punctuation](#include-punctuation)
  - [Find a reflexicon](#find-a-reflexicon)
  - [Find a pangram](#find-a-pangram)
  - [Validation](#validation)
- [Options](#options)
  - [Command line interface](#cli)
  - [`Autogram` class](#autogram-class)
- [Fun resources](#fun-resources)

## Usage
Clone this repository. 
```commandline
git clone git@github.com:alex-b1729/autogram-this.git
cd ~/autogram-this
```

### Python CLI

```commandline
$ python3 -m autogramthis "This sentence contains"
```
```comandline
Iterating sentences to find an autogram
Starting sentence: This sentence contains one a, two c's, three e's, one h, two i's, four n's, one o, three s's, and three t's.
Epoch: 122,420
Found an autogram!
Total time: 0 minutes 6 seconds
Raw count dictionary: {'a': 3, 'c': 3, 'd': 2, 'e': 27, 'f': 4, 'g': 1, 'h': 5, 'i': 11, 'l': 2, 'n': 16, 'o': 7, 'r': 5, 's': 29, 't': 16, 'u': 2, 'v': 6, 'w': 6, 'x': 6, 'y': 3}

This sentence contains three a's, three c's, two d's, twenty-seven e's, four f's, one g, five h's, eleven i's, two l's, sixteen n's, seven o's, five r's, twenty-nine s's, sixteen t's, two u's, six v's, six w's, six x's, and three y's.
```

### Rust CLI

A *vastly* faster multi-threaded Rust version is also available. You need to have a Rust compiler [installed](https://www.rust-lang.org/tools/install).

```commandline
# build
cd rust
cargo build --release

# run
$ target/release/autogramthis "This test of the Rust version has"
Starting parallel search with 48 threads
Iterating sentences to find an autogram
Starting sentence: This test of the Rust version has one n, one a, five t's, one f, three e's, two i's, two o's, two r's, three h's, one u, one v, and five s's.

T1: 1,168 | T2: 2,245 | T3: 2,267 | T4: 25,109 | T5: 2,230 | T6: 26,498 | T7: 1,147 | T8: 26,185 | T9: 21,880 | T10: 2,238 | T11: 25,999 | T12: 2,220 | T13: 16,620 | T14: 22,015 | T15: 30,056 | T16: 26,057 | T17: 2,224 | T18: 23,504 | T19: 2,202 | T20: 2,197 | T21: 2,173 | T22: 28,605 | T23: 23,451 | T24: 2,228 | T25: 2,234 | T26: 21,650 | T27: 2,254 | T28: 2,221 | T29: 2,198 | T30: 23,908 | T31: 25,116 | T32: 18,105 | T33: 26,475 | T34: 28,068 | T35: 23,638 | T36: 2,195 | T37: 20,529 | T38: 2,202 | T39: 2,249 | T40: 15,781 | T41: 2,227 | T42:T1: 2,463 | T2: 4,749 | T3: 4,784 | T4: 54,964 | T5: 4,754 | T6: 56,272 | T7: 2,439 | T8: 55,006 | T9: 51,658 | T10: 4,746 | T11: 55,447 | T12: 4,701 | T13: 46,082 | T14: 50,878 | T15: 59,773 | T16: 55,124 | T17: 4,715 | T18: 52,156 | T19: 4,716 | T20: 4,690 | T21: 4,658 | T22: 57,340 | T23: 52,676 | T24: 4,753 | T25: 4,785 | T26: 50,702 | T27: 4,783 | T28: 4,751 | T29: 4,666 | T30: 52,868 | T31: 54,566 | T32: 46,790 | T33: 55,691 | T34: 57,398 | T35: 52,869 | T36: 4,681 | T37: 50,447 | T38: 4,712 | T39: 4,811 | T40: 45,304 | T41: 4,746 | T42: 4,687 | T43: 4,654 | T44: 4,648 | T45: 2,399 | T46: 50,053 | T47: 4,752 | T48: 46,091 |
🎉 Thread 9 found the solution!
Found an autogram!
Raw count dictionary: {'x': 1, 'y': 3, 'w': 5, 'd': 2, 'l': 2, 't': 18, 'i': 11, 'h': 9, 'g': 4, 'a': 3, 'n': 15, 'f': 8, 'r': 7, 's': 25, 'e': 29, 'v': 7, 'u': 4, 'o': 8}

This test of the Rust version has one x, three y's, five w's, two d's, two l's, eighteen t's, eleven i's, nine h's, four g's, three a's, fifteen n's, eight f's, seven r's, twenty-five s's, twenty-nine e's, seven v's, four u's, and eight o's.

Total iterations across all threads: 1,641,373
Total time: 1.231 seconds (0 minutes 1 seconds)
Total iterations per second: 1,333,905
```

### Python module
```python
from autogramthis import Autogram

ag = Autogram("This sentence contains")
autogram = ag.search()
print(autogram)
```

## Capabilities
### Add a suffix to the autogram
The `-s` option sets the `suffix` and the `--no-and` flag removes the 'and' from before the last letter count.
```commandline
python3 -m autogramthis "Spam, Spam, Spam" -s "eggs, and Spam." --no-and
```
> `Spam, Spam, Spam, six a's, two d's, twenty e's, seven f's, four g's, five h's, ten i's, two l's, five m's, seven n's, six o's, five p's, six r's, thirty-one s's, twelve t's, three u's, eight v's, five w's, four x's, three y's, eggs, and Spam.`

### Include punctuation
The script can search for and validate autograms that include the count of the characters `,-'.!`.
In the sentence their full names are written as 'comma', 'hyphen', 'apostrophe', 'period'.
The exception is the exclamation point (`!`) which is written as '!' since that's how it's used in
[Lee Sallow's autogram](https://web.archive.org/web/20130926213111/http://www.fatrazie.com/EWpangram.html) in 
Hofstadter's 1982 "Metamagical Themas" column in Scientific American. 

```commandline
python3 -m autogramthis 'An autogram with punctuation includes' --include-punctuation
```
> `An autogram with punctuation includes eight a's, four c's, four d's, thirty-three e's, ten f's, six g's, twelve h's, eighteen i's, four l's, four m's, nineteen n's, sixteen o's, six p's, fourteen r's, thirty-two s's, twenty-eight t's, twelve u's, six v's, eight w's, five x's, seven y's, twenty-four comma's, five hyphen's, twenty-four apostrophe's, and one period.`

```commandline
python3 -m autogramthis --include-punctuation --validate "Only the fool would take trouble to verify that his 
sentence was composed of ten a's, three b's, four c's, four d's, forty-six e's, sixteen f's, four g's, 
thirteen h's, fifteen i's, two k's, nine l's, four m's, twenty-five n's, twenty-four o's, five p's, 
sixteen r's, forty-one s's, thirty-seven t's, ten u's, eight v's, eight w's, four x's, eleven y's, 
twenty-seven commas, twenty-three apostrophes, seven hyphens and, last but not least, a single \!"
```
```commandline
Valid autogram!
```

### Find a *reflexicon*
A *reflexicon* is a self-enumerating list of words.
Simply calling the script without passing the `prefix` argument or assigning a `suffix` will cause it to search for a list of cardinal number names and characters.
The script starts iterating from a sentence in the form `, one {random.choice(string.ascii_lowercase)}`. 
Finding these can take a while!
```commandline
python3 -m autogramthis --make-singular --no-and
```
> `twenty e, four f, one g, five h, three i, one l, ten n, seven o, seven r, three s, nine t, three u, four v, three w, one x, two y`

### Find a *pangram*
A *pangram* is a sentence that uses every letter of the alphabet. 
Use the `-p` or `--pangram` flag in the command line. 
```commandline
python3 -m autogramthis "The quick brown fox jumped over alphabet soup containing" --pangram
```
> `The quick brown fox jumped over alphabet soup containing five a's, three b's, three c's, three d's, thirty-two e's, six f's, two g's, ten h's, twelve i's, two j's, two k's, three l's, two m's, sixteen n's, sixteen o's, four p's, two q's, thirteen r's, thirty-four s's, twenty-seven t's, seven u's, seven v's, ten w's, six x's, four y's, and one z.`

__Note__ that pangrams with punctuation included will not force include additional characters but will still count
the ones that occur. 


### Validation
Validate if a string is an autogram using `--validate "<sentence to validate>"` in the command line or 
using the `Autogram.validate(sentence: str)` function. 
The `-v` command line flag sets validation output to verbose.

```commandline
$ python3 -m autogramthis --validate "twenty e, four f, one g, five h, three i, one l, ten n, seven o, seven r, three s, nine t, three u, four v, three w, one x, three y"
e: INVALID. True count: 22, Sentence says: 20.
h: INVALID. True count: 6, Sentence says: 5.
o: INVALID. True count: 6, Sentence says: 7.
r: INVALID. True count: 8, Sentence says: 7.
w: INVALID. True count: 2, Sentence says: 3.
y: INVALID. True count: 2, Sentence says: 3.
Invalid!
```

## Options
### CLI
```commandline
usage: autogramthis [-h] [-s SUFFIX] [-p] [--make-singular] [--no-and] [--include-punctuation]
                    [--validate VALIDATE] [-v]
                    [prefix]

Search for autograms from an optional starting or ending string or validate an autogram.

positional arguments:
  prefix                The text to begin the autogram sentence

options:
  -h, --help            show this help message and exit
  -s SUFFIX, --suffix SUFFIX
                        The text to end the autogram sentence
  -p, --pangram         Search for a pangram - i.e. where every letter occurs at least once
  --make-singular       Exclude the 's from characters with count greater than one
  --no-and              Exclude the word 'and' from before the last character's count
  --include-punctuation
                        Include the punctuation characters ,-'.! in search and validation
  --validate VALIDATE   Validate whether the given string is an autogram. Other arguments are ignored
                        if --validate is specified.
  -v                    Verbose output when validating.
```

### `Autogram` class
__Parameters__
- `prefix : str` (optional) The string to start the autogram.
- `suffix : str` (optional) The string that ends the autogram.

__Properties__
- `sentence : str` A sentence generated using the current `counts` mapping.
- `is_autogram : bool` True if `sentence` is an autogram.

__Attributes__
- `counts : dict[str, int]` Maps lower case letters and chars to their count in the current sentence.
  Only includes characters with count > 0.
- `make_plural : bool` If True, appends a 's to the end of characters with count greater than 1. (default True)
- `include_final_and : bool` If True, add the word 'and' before the last character count. (default True)
- `is_pangram : bool`  If True, search for autograms where all letters of the alphabet are included. (default False)
- `epoch : int` The number of sentences tried during search.
- `update_all_counts : bool` If True, update all character counts on next epoch, 
  otherwise update one, random character's count.

__Methods__
- `init_counts()`: Sets the `count` attribute to the character counts in `prefix + suffix`.
- `counts_as_phrases(counts: dict) -> list`: 
  Takes a mapping between characters to counts and outputs these counts as a comma 
  delimited list with cardinal number names.
- `count_occurrences(s: str) -> dict`: Take a string and returns a mapping from lowercase chars 
  to their count in the sentence.
- `update_counts()`:
  Updates the `counts` dictionary by alternatively updating all characters or one random character
  as determined by the `update_all_counts` attribute.
- `search() -> str`:
  Repeatedly applies `update_counts()` until an autogram is found.
  Prints to stdout the initial sentence, the number of epochs (updated every 10,000),
  the time taken, the dictionary of character to counts in the final solution, and the autogram.
  Returns the autogram. 

__Static Methods__
- `validate(sentence: str) -> bool`: 
  Returns True if given sentence is an autogram.
  Only works for sentences with individual character counts < 100.
- `find_counts_and_chars(sentence: str) -> list[tuple[str, str]]`:
  Regex searches for number words followed by single character, potentially followed by 's. 
  Returns a list of tuples in the format ('number words', 'character'). 

## Fun Resources
- [Lee Sallows](https://www.leesallows.com/index.php) invented autograms
- Lee Sallows paper on [reflexicons](https://www.leesallows.com/files/Reflexicons%20NEW(4c).pdf). 
  Includes lots of fun variants and tips on searching for autograms. 
- [Autogram](https://en.wikipedia.org/wiki/Autogram) on Wikipedia
- [autograms.net](https://autograms.net/) has lots of autograms in english and other languages.
- [Searching for Autograms](https://curiosityarb.blog/2024/12/01/searching-for-autograms.html) describes the autogram search algorithm used by this program. 
