# Autogram This

```text
The output of this Python script is composed of two a's, three c's, 
three d's, thirty-one e's, nine f's, three g's, ten h's, twelve i's, 
two l's, two m's, fourteen n's, fourteen o's, five p's, eight r's, 
twenty-seven s's, twenty-five t's, five u's, eight v's, seven w's, 
one x, and five y's.
```

A Python script that turns a given phrase into an autogram. 

From [Wikipedia](https://en.wikipedia.org/wiki/Autogram):
> An autogram is a sentence that describes itself in the sense of providing an inventory of its own characters.

- [Usage](#usage)
  - [Command Line](#command-line)
  - [Python](#python)
- [Capabilities](#capabilities)
  - [Add a suffix to the autogram](#add-a-suffix-to-the-autogram)
  - [Find a reflexicon](#find-a-reflexicon)
  - [Find a pangram](#find-a-pangram)
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

### Command Line
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

### Python
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
```text
Spam, Spam, Spam, six a's, two d's, twenty e's, seven f's, four g's, 
five h's, ten i's, two l's, five m's, seven n's, six o's, five p's, 
six r's, thirty-one s's, twelve t's, three u's, eight v's, five w's, 
four x's, three y's, eggs, and Spam.
```

### Find a *reflexicon*
A *reflexicon* is a self-enumerating list of words.
Finding these can take a while!
The script starts iterating from a sentence in the form `, one {random.choice(string.ascii_lowercase)}`. 
```commandline
python3 -m autogramthis --make-singular --no-and
```
```text
twenty e, four f, one g, five h, three i, one l, ten n, seven o, 
seven r, three s, nine t, three u, four v, three w, one x, two y
```

### Find a *pangram*
A *pangram* is a sentence that uses every letter of the alphabet. 
Use the `-p` or `--pangram` flag in the command line. 
```commandline
python3 -m autogramthis "The quick brown fox jumped over alphabet soup containing" --pangram
```
```text
The quick brown fox jumped over alphabet soup containing five a's, three b's, 
three c's, three d's, thirty-two e's, six f's, two g's, ten h's, twelve i's, 
two j's, two k's, three l's, two m's, sixteen n's, sixteen o's, four p's, 
two q's, thirteen r's, thirty-four s's, twenty-seven t's, seven u's, seven v's, 
ten w's, six x's, four y's, and one z.
```

## Options
### CLI
```commandline
$ python3 -m autogramthis --help          
usage: autogramthis [-h] [-s SUFFIX] [-p] [--make-singular] [--no-and]
                    [prefix]

Searches for an autogram from an optional starting string.

positional arguments:
  prefix                The text to begin the autogram sentence

options:
  -h, --help            show this help message and exit
  -s SUFFIX, --suffix SUFFIX
                        The text to end the autogram sentence
  -p, --pangram         Search for a pangram - i.e. where every letter occurs
                        at least once
  --make-singular       Exclude the 's from letters with count greater than
                        one
  --no-and              Exclude the word 'and' from before the last
                        character's count
```

### `Autogram` class
__Parameters__
- `prefix`: str, optional. The string to start the autogram.
- `suffix`: str, optional. The string that ends the autogram.

__Properties__
- `sentence`: str. A sentence generated using the current `counts` mapping.
- `is_autogram`: bool. True if `sentence` is an autogram.

__Methods__
- `init_counts()`: Initiates the `count` attribute with the letter counts in `prefix + suffix`.
- `counts_as_phrases(counts: dict) -> list`: 
Takes a mapping between letters to counts and outputs these counts as a comma 
delimited list with cardinal number names.
- `count_occurrences(s: str) -> dict`: Take a string and returns a mapping from lowercase chars 
to their count in the sentence.
- `update_counts()`:
Updates the `counts` dictionary by alternatively updating all letters or one random letter
as determined by the `update_all_counts` attribute.
- `search() -> str`:
Repeatedly applies `update_counts()` until an autogram is found.
Prints to stdout the initial sentence, the number of epochs (updated every 10,000),
the time taken, the dictionary of letter to counts in the final solution, and the autogram.
Returns the autogram. 

## Fun Resources
- [Lee Sallows](https://www.leesallows.com/index.php) invented autograms
<<<<<<< HEAD
- Lee Sallows paper on [reflexicons](https://www.leesallows.com/files/Reflexicons%20NEW(4c).pdf). 
=======
- Lee Sallows paper on [reflexicons]("https://www.leesallows.com/files/Reflexicons%20NEW(4c).pdf"). 
>>>>>>> a453447512f8a5f4eb4180a60180b0bdf9189638
Includes lots of fun variants and tips on searching for autograms. 
- [Autogram](https://en.wikipedia.org/wiki/Autogram) on Wikipedia
- [autograms.net](https://autograms.net/) has lots of autograms.
