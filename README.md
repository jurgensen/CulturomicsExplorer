# CulturomicsExplorer
A python 3 script for producing preformatted plots of Google Ngrams against backgrounds of labelled time spans to visually investigate possible patterns in word usage.  My final project for UC Berkeley's Info 155, 'Intro to High-Level Programming'.



What is Culturomics Explorer?

CE is a script designed to plot ngram timeseries from the corpora of Google books against a background of a user-selected timespan to allow the user to visually inspect the data for potential contextual factors that have influenced the trends in the use of words.


What is Culturomics?

Culturomics is the concept proposed by JB Michel, et. al. (2011) that utilizes the frequencies of words from a very large corpus of books as evidence of cultural and social trends.  The changes in the frequencies of words in a corpus can be telling, but only if the person interpreting the data can find contextual reasons for changes in word use.

For the original python 2 script,  information about the data of the Google N-gram viewer, or 
information about culturomics or the interpretation of ngram results, please visit <http://culturomics.org/> or review the original Michel, et. al. article in Science: Jean-Baptiste Michel, Yuan Kui Shen, Aviva Presser Aiden, Adrian Veres, Matthew K. Gray, The Google Books Team, Joseph P. Pickett, Dale Hoiberg, DanClancy, Peter Norvig, Jon Orwant, Steven 
Pinker, Martin A. Nowak, and Erez Lieberman Aiden. 'Quantitative Analysis of Culture Using 
Millions of Digitized Books'. Science(331). 2011, 176-182.


How do you use CE?

CE was developed using Python 3, and is designed to be run from the command line.  Call the script from the directory in which the script is located.   Depending on your platform and how you've installed Python 3, the call will look something like: 'C:Users\Anna\CulturomicsExplorer>python culturomics_explorer.py' or 'C:Users\Anna\CulturomicsExplorer>python3 culturomics_explorer.py'.

Running the culturomics_explorer.py script from the command line launches the CE GUI.  The program, by default, reads in the background plots available for use from the file named 'timespan_data.tsv' in the same folder as the python script.  If the file is not present or is unreadable, the GUI will load with only the option 'none' for background plots.  The program also writes all successfully retrieved ngram data to a file that, by default, is named 'ngrams_data.tsv' located in the same folder as the python script.  If this file is absent or is unreadable the program will create plots as normal, but will not log the ngram data.  Both the timespan .tsv file and the ngrams log .tsv file can be changed from the GUI once the program has been launched using the 'Files' options on the program's menu bar.  

Because the program retrieves the ngram data from the Google server, you must have a working internet connection for the program to produce plots.  Also, the program uses the python modules urllib, matplotlib, re, json, and tkinter, so it is necessary to have these modules installed for python 3.  

Once the program has been launched, simply enter the term(s) you'd like to search, select for each term the corpus you want to search in, and the background plot you want the ngrams displayed with.  If you do not select a corpus or background plot, the program will use the eng_us_2012 corpus (English language books published in the US), and will not plot with a background (option 'none').


What are some examples of ngrams I can plot?

Try plotting the names of censored scientists, writers, or artists in multiple languages against information about the political control of a country (such as 'Einstein' or 'Marc Chagall' across period of political control in Germany).  Try plotting different terms that have been used for the same thing, such as 'World War I' and 'Great War' across the timespans of wars that the US has participated in.  Try plotting the difference between popular political topics (or even ordinary words), as in '(women-men)' or '(privacy-security)', across spans of party control of a house of the US Congress.  If you want to compare the changes in frequency of two words, but one word has a much higher frequency than the other, you can scale one word by multiplying it by a numerical value and placing the whole query in parentheses, as in '(petrichor*100)'. 


Does CE have all of the same functionalities as the Google Ngram viewer?

No.  CE cannot search queries containing apostrophes or quotation marks (the program will remove them if they are entered), nor can it return data for wildcard searches (such as '*_ADJ books').  Searches of both kinds can be made in the Google ngram viewer at <https://books.google.com/ngrams>.

CE does have many of the same functionalities as the Google Ngram viewer, though.  Using CE you can search using part of speech tags (such as _DET/_DET_ or _NOUN/_NOUN_), scale searched ngrams (word*100), search for the difference between ngrams for two words(word-another word), or the sum of ngrams for two words (word+another word).

How do I use my own timespan data?


Simply prepare your timespan data in a .tsv file in the format shown below and select that file from the 'Files > Timespan' menu in the GUI.  Once a new file is selected, the program will automatically update the available background plots in the GUI listbox.  

Note that the program pulls the labels and title from the text of the .tsv, so format your text as you desire it to appear on the plot. The program will recognize timespans with two dates (start year, end year), and timespans with three dates (start year, midpoint year, end year).  In the case of the three-date spans, the labels in the first row for the start and midpoint years are added to the plot legend.  Note that all of the spans in a set must have the same number of years associated with each entry, so if any span in the set requires three dates, provide three dates for all spans in the set, but use the same year for the start and midpoint year for spans that would otherwise be recorded with two dates.

Importantly, use one (and only one) blank space between background plot data sets.  If you don't use a blank line between sets, the program cannot differentiate between the sets, and if you use more than one the program will read blank lines into the options list.  Should they come up, selecting these blank lines in the options list should they come up will prevent the program from producing a plot until a different background option is selected in the listbox.


What is recorded in the ngram log?

For each term that successfully returns ngram data from the Google server the program writes to a .tsv file, separated by tabs: the term searched for, the corpus in which it was searched for, the label used in the plot legend, and the ngram data for the years 1900-2008, inclusive.


Who do I complain to?

For information, help, suggestions, or bug reports contact author AE Jurgensen at 'jurgensen.anna@gmail.com'.
