<html>
<center>

<!-- Headings -->
<p align="center"> 
  
# Natural Language Processing: Grammatical Error Correction Implementation
</p>

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/luowensheng/Natural-Language-Processing-Grammatical-Error-Correction-/pulse)
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/luowensheng)

[Introduction](#Introduction) • [Tasks](#Tasks) • [Credits](#Credits) • [Questions](#Questions)

</center>

# Introduction
Several datasets are used: 
1. Linggle ngram frequency
2. GEC model

For this assignment, we had to build an error corrector model based on the spell check code by **Peter Norvig**.

What got from it is that to correct a word, you can first modify that word, check to see which one of those modifications is a known word then we apply some modifications to those known words to get a set a candidate word and we pick the one that has the highest probability.

I have used the same concept for my adaptation to correct strings of 2 to 5 words.

# Tasks
### **1. Accept the input string *INPUT* of 2 to 5 words**
The code accepts a string of two to five words. I have used the input.txt file for this purpose. It contains five sentences:
```
1. discuss about the issue
2. listen the music
3. study in university
4. stay home
5. search more information
```

### **2. Identify some problem word (PW, e.g., discuss) in *INPUT* and use a model that describe the likely error (e.g., unnecessary “about”) condition on PW and edits (ED) "discuss": [["D", "about", 1]]**
The next step is to identify some problem word. First, the sentence is split into a
list of words. Then, using the dictionary file model.text, I search to find which of
those words are contained in the dictionary file and those are the problem words.

### **3. Apply one edit in ED to PW to derive a set of candidate *CAND1***
After identifying the problem word, the next step is to apply some modifications to
come up with a set of candidates. Three types of modifications will be applied.

Each problem word has a set of modifications that can be applied to it denoted by
**‘R’** for *replacement*, **‘D’** for *deletion* and **‘I’** for *insertion*. When a problem word is
searched, the dictionary returns all those arrays for the given problem word.

*Deletion:*
>All the arrays containing **‘D’** is collected. For each of the arrays, we search to see if the word to be deleted is present in the location provided, if so, a new array
containing the modification is returned.

*Insertion:*
>All the arrays containing **‘I’** is collected. A word is inserted in the location
provided and a new array is returned.

*Replacement:*
>All the arrays containing **‘R’** is collected. For each of the arrays, we search to see if
the word to be replaced is present in the location provided, if so, a new array
containing the modification is returned.

Because sometimes the wrong answer is not the one the algorithm returns, I added a
new function find_verb which takes a sentence and finds which word is the most
likely to be a verb. To accomplish that function, first I have removed all of the
words that are also contained in the list of prepositions that I have provided, then I
combine each of the remaining words with these subjects ['i','you','he', 'she', 'we',
'they'] and use linggle to find a set of probabilities that are some up and the verb
would be the word with the highest probability. The final step is not to save or
replace that word in the edits1 function.

### **4. Apply another edit in ED to each ngram NGRAM in CAND1 to derive *CAND2***
After using preforming the modifications, we repeat the same of all of the
sentences that were provided by the algorithm.

### **5. Combine CAND1 and CAND2 to form a possible candidates set *CAND***
All of the candidates are combines but some that have length longer then 7 and
those that are 1 single word are all removed.

### **6. Use *Linggle API* to rank ngrams in CAND**
In the candidates function, I have ranked all of the results by probability by
constantly looking for the argmax of the probabilities, save the results, replace the
old results by –1000 to make it the minimal, then search for the argmax again and
repeat every single step until every candidate have a probability assigned to them.

### **7. Return highest ranked ngrams**
The algorithm will pick the winner and it will print the results as such:

```
0
The sentence to be corrected is:
discuss about the issue
discuss the issue

1
The sentence to be corrected is:
listen the music
listen to the music

2
The sentence to be corrected is:
study in university
study at university

3
The sentence to be corrected is:
stay home
stay at home

4
The sentence to be corrected is:
search more information
search for more information
```

# Credits
Please refer to Peter Norvig's [website](https://norvig.com/spell-correct.html).

# Questions
Submit your questions and bug reports [here](https://github.com/luowensheng/Natural-Language-Processing-Grammatical-Error-Correction-/issues).

