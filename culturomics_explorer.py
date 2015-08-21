INFO='''
    plots nGrams against contentful background timespans (e.g. US presidential terms) to provide context for visual 
    inspection of the trends in word frequency
    
    AE Jurgensen, UC Berkeley Linguistics --- jurgensen.anna@gmail.com

    This program plots nGrams against background timespans 1900-2008 (2008 is the last available year for
    available nGram data).  The plots produced are automatically formatted for legend, title, scale, and 
    axes labels.  The default corpus if none specified for a query in eng_us_2012.  Text input is formatted based
    on the limits of the algorithm .  If enclosed in parentheses, queries can be scaled, such as (petrichor*100), or
    can be the sum or difference of ngrams, such as (women-men) or (Chagall+Marc Chagall).  The program will allow
    the special characters used for these operations only if the query is (enclosed), and will otherwise remove special
    characters.  One caveat of the culturomics explorer is that it will not return data for 'wildcard' searches available
    on the Google ngrams webpage.

    Background timespans are read in from a .tsv file containing the labels and dates - see example file 'timespan_data.tsv' for 
    the acceptable format.  The default filename is 'timespan_data.tsv', but a different file can be selected from the  GUI 
    'files' menu, and the list of available background plots will be immediately updated.  If there is no recognizable file 
    for the background plots, the program will still function, but will only create plots with no background timespan.
    
    The program also writes to a log of the ngrams searched, recording the search term, the corpus searched, the label used for 
    plotting, and all of the ngram data returned from Google.  The default file is 'ngrams_data.tsv', but this can be changed 
    within the program from the menu (Files > nGrams).  If there is no file to write to, the program will create plots but 
    won't write to a log. 
    
    The program utilizes AE Jurgensen amateur py3 version of getNgrams.py, based on original py2 script from JB Michel.
    From original py2 version:
      -updated print functions
      -update urllib calls
      -utilized a different algorithm for collecting data from url call
      -modified the return to only return the data points, as getNgrams here searches for a single term at a time
    
    --------------some of original py2 script info--------------
    JB Michel for the Harvard Cultural Observatory, Oct 19 2012 www.culturomics.org, @culturomics, @jb_michel.
    License: None, please distribute, modify and improve as you see fit.
    
    This is a basic python code to retrieve data behind trajectories plotted on the Google
    Books Ngram Viewer: books.google.com/ngrams.
    
    Note to users -- known caveat: quotation marks are removed from the input query.
    '''

def culturomics_explorer():
    
    import matplotlib.pyplot as plt
    import tkinter as tk
    from tkinter import filedialog as fd
    from tkinter import ttk
    import re
    
    
    class PlotSettings (object):
        def __init__ (self, start, end, smooth):
            self.start_year = start
            self.end_year = end
            self.smoothing = smooth
            
        def __str__ (self):
            return ('start year: {}, end year: {}, smoothing: {}'.format(self.start_year, self.end_year, self.smoothing))
    
    
    class Corpus (object):
        def __init__ (self, named = 'American', corpus_name = 'eng_us_2012', corpus_number = 17, corpus_tag = '(US)'):
            self.name = named
            self.corpus = corpus_name
            self.number = corpus_number
            self.tag = corpus_tag
            
        def __str__ (self):
            return ('{}: {}, \'{}\', \'{}\''.format(self.corpus, self.number, self.name, self.tag))
        
        

    class Timespan (object):
        def __init__(self, named = 'timespan', data = [[0, 0, 0]], coloring = ['red', 'orange']):
            #Create attributes for intermittent periods vs. full coverage of timeperiod, staged or not, timespans
            #and names, and optionally colors.  If full coverage, 2 colors needed, else 1 color.  If staged, will use
            #solid shading and hatched shading to represent the different stages of timespan
            self.name = named
            self.dates = data
            self.colors = coloring

                
        def __str__(self):
            return ('{} {} {}'.format(self.name, self.dates, self.colors))
            #if has self.dates = 3 then not staged (just name and start and end), if self.dates = 4 then staged
            #for a single year date, start year and end year are same year (entered twice)
        
                        
        def alternate_color (self, set_color):
            if set_color == self.colors[0]:
                set_color = self.colors [1]
            else:
                set_color = self.colors[0]

            return set_color
            
        def plot_single_year (self, year, line_color):
            plt.axvline(year, color = line_color, alpha = .4, linewidth = 2)
            
            
        def plot_span (self, start_yr, end_yr, span_color, filled, hatched, labelled = None):
            if hatched:
                hatching = '..'
                alpha_val = .2
            else:
                hatching = None
                alpha_val = .2
            
            plt.axvspan(start_yr, end_yr, color = span_color, fill = filled, hatch = hatching, \
                        alpha = alpha_val, label = labelled)
            
            
        def plot_staged (self, start, stage_break, end, color):
            self.plot_span(start, end, color, True, False)    
            self.plot_span(stage_break, end, color, False, True)
        
        
        def staged_labels (self, color):
            #for labels, use the column titles for the 1st and 2nd date columns from .tsv
            self.plot_span(1900, 1900, color, True, False, self.dates[0][1])
            self.plot_span(2008, 2008, color, True, True, self.dates[0][2])
            
            
        def plot_full (self, staged_span):
            if type(self.colors) != list:
                self.colors = ['red', 'orange']
            
            color = self.colors[1] #will alternate colors (span, staged span)
               
            if staged_span:
                for era in self.dates[1:]:
                    color = self.alternate_color(color)
                    self.plot_staged(era[1], era[2], era[3], color)
                self.staged_labels(self.colors[0])
            else:
                for era in self.dates[1:]:
                    color = self.alternate_color(color)
                    self.plot_span(era[1], era[2], color, True, False)
         
        
        def plot_intermittent (self, staged_span):   
            if type(self.colors) == str:
                color = self.colors #will only use one color
            elif type(self.colors) == list:
                color = self.colors[0]
            else:
                color = 'red'
            
            if staged_span:
                for era in self.dates[1:]:
                    self.plot_staged(era[1], era[2], era[3], color)
                self.staged_labels(color)
            else:
                for era in self.dates[1:]:
                    if era[1] == era[2]:
                        self.plot_single_year(era[1], color)
                    else:
                        self.plot_span(era[1], era[2], color, True, False)
                            
                            
        def is_it_staged(self):
            has_staged_dates = False
            has_invalid_entries = False
                
            if len(self.dates[0]) == 4:
                has_staged_dates = True
            elif len(self.dates[0]) != 3:
                has_invalid_entries = True
                print('The format of the data of \'{}\' is incorrect.'.format(self.name))
                    
            return (has_staged_dates, has_invalid_entries)
        
        
        def plot (self): 
            #return from method is [staged(True)/not, invalid entries(True)/not]
            is_staged, has_invalid = self.is_it_staged()
                
            if not has_invalid:
                summed_years_covered = 0
                
                ending_year = 2
                if is_staged:
                    ending_year = 3
    
                for era in self.dates[1:]:#self.dates[0] is a list of column labels
                    summed_years_covered += (era[ending_year] - era[1])#era[0] is the str label for the timespan
            
                if summed_years_covered >= ((2008 - 1900) - 10):#the spans cover all or nearly all of the plot
                    self.plot_full(is_staged)
                else:
                    self.plot_intermittent(is_staged)
                        
                        
        def get_labels(self):
            #label names, and the year at which the label is to be placed
            #typically the average of their corresponding dates, but if 
            #two spans overlap, place both labels at year = 0 to avoid
            #label overlap
                
            labels = [[],[]] 
                
            if self.is_it_staged()[0] == True:
                end_year = 3
            else:
                end_year = 2
                   
            for era in self.dates[1:]:
                labels[0].append(era[0])
                labels[1].append((era[end_year] + era[1]) / 2)
                
            for index in range(1, len(labels[1])):
                if (labels[1][index] - labels[1][index - 1]) <= 1:
                    labels[1][index] += .5
                    labels[1][index - 1] -= .5
                    
            return labels

    
                    
    class NGram (object):
        def __init__ (self, named = '', corpus_chosen = '', smooth = 0, labelled = '', data_values = []):
            #Create object containing the ngram term(s), the corpus they were found in, and the
            #data from this specific term + corpus search on Google nGrams
            self.name = named
            self.corpus = corpus_chosen
            self.data = data_values
            self.label = labelled
            self.smoothing = smooth
            
            
        def __str__(self):
            return ('{}\t{}\t{}\t{}'.format(self.name, self.corpus, self.smoothing, self.label, self.data))
            
            
        def set_label(self):
         
            self.label = self.name
            
            if self.label[0] == '(':
                self.label = self.label.strip('()')
                
            for element in corpora:
                if element.corpus == self.corpus:
                    self.label = '\'' + self.label + '\'' + element.tag
                    break
                    
    class Application(object):
        def __init__(self, master, file_name = 'timespan_data.tsv', write_file = 'ngrams_data.tsv', \
                     timespans = [], plots = []):
            #variables
            self.master = master
            self.master.title("Culturomics Explorer")
            self.master.resizable(width = tk.FALSE, height = tk.FALSE)
            self.timespan_objects = timespans
            self.options_list = plots
            self.timespan_file = file_name
            self.write_file_name = write_file
            self.entry_lbl = tk.StringVar()
            self.success_lbl = tk.StringVar()
            
            self.default_plot_settings = PlotSettings(1900, 2008, 5)
            self.plot_settings = self.default_plot_settings
            
    
            #Frame and menu
            self.mainframe = ttk.Frame(master, padding='3 3 12 12')
            self.mainframe.grid(column= 0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
            self.mainframe.columnconfigure(0, weight=1)
            self.mainframe.rowconfigure(0, weight=1)           
            self.menu_bar = tk.Menu(master)
            self.master['menu'] = self.menu_bar
    
            self.file_menu = tk.Menu(self.menu_bar, tearoff = 0)
            self.file_menu.add_command(label = 'Timespan File', command = self.get_timespan_file)
            self.file_menu.add_command(label = 'Ngram log', command = self.get_ngrams_file)
            self.menu_bar.add_cascade(label = 'Files', menu = self.file_menu)
            
            self.plot_menu = tk.Menu(self.menu_bar, tearoff = 0)
            self.plot_menu.add_command(label = 'Reset', command = self.get_plot_settings)
            self.menu_bar.add_cascade(label = 'Plot Settings', menu = self.plot_menu)
                        
    
            #ngram text entry boxes
            ttk.Label(self.mainframe, text='Ngram').grid(column=1, row=1, sticky=(tk.N, tk.W))
            self.entry_1 = ttk.Entry(self.mainframe, width=15)
            self.entry_1.grid(column=2, row=1, sticky = (tk.W, tk.E))
            self.entry_2 = ttk.Entry(self.mainframe, width=15)
            self.entry_2.grid(column=3, row=1, sticky = (tk.W, tk.E))
            self.entry_3 = ttk.Entry(self.mainframe, width=15)
            self.entry_3.grid(column=4, row=1, sticky = (tk.W, tk.E))
            self.entry_4 = ttk.Entry(self.mainframe, width=15)
            self.entry_4.grid(column=5, row=1, sticky = (tk.W, tk.E))
            self.entry_5 = ttk.Entry(self.mainframe, width=15)
            self.entry_5.grid(column=6, row=1, sticky = (tk.W, tk.E))
            self.entries = [self.entry_1, self.entry_2, self.entry_3, self.entry_4, self.entry_5]
    
            #corpus selection
            ttk.Label(self.mainframe, text='corpus').grid(column=1, row=2, sticky=tk.W)
            self.corp_listbox_1 = tk.Listbox(self.mainframe, width = 15, height = 11, exportselection = 0)
            self.corp_listbox_1.grid(column = 2, row =2)
            self.corp_listbox_2 = tk.Listbox(self.mainframe, width = 15, height = 11, exportselection = 0)
            self.corp_listbox_2.grid(column = 3, row =2)
            self.corp_listbox_3 = tk.Listbox(self.mainframe, width = 15, height = 11, exportselection = 0)
            self.corp_listbox_3.grid(column = 4, row =2)
            self.corp_listbox_4 = tk.Listbox(self.mainframe, width = 15, height = 11, exportselection = 0)
            self.corp_listbox_4.grid(column = 5, row =2)
            self.corp_listbox_5 = tk.Listbox(self.mainframe, width = 15, height = 11, exportselection = 0)
            self.corp_listbox_5.grid(column = 6, row =2)
            self.listboxes = [self.corp_listbox_1, self.corp_listbox_2, self.corp_listbox_3, self.corp_listbox_4, self.corp_listbox_5]
    
            self.populate_corpora()
    
            #background plot selection
            ttk.Label(self.mainframe, text='background plot').grid(column = 1, row=3)
            self.background = tk.Listbox(self.mainframe, width = 35, height = 3, exportselection = 0)
            self.background.grid(column = 2, row = 3, columnspan = 2, sticky = (tk.W, tk.E))
    
            self.yscroll = tk.Scrollbar(self.mainframe, command=self.background.yview, orient=tk.VERTICAL)
            self.yscroll.grid(row=3, column=3, sticky=(tk.N, tk.E, tk.S))
            self.background.configure(yscrollcommand=self.yscroll.set)
            self.get_timespans()
        
            #Plot button, messages, instructions
            ttk.Button(self.mainframe, text='plot ngrams', command=self.plot_ngrams).grid(column=5, row=3)
    
            self.messages = tk.Frame(self.mainframe, padx = 5, pady = 5, relief = tk.SUNKEN, bd = 3)
            self.messages.grid(column = 2, row = 8, columnspan = 6, rowspan = 9, sticky=(tk.W, tk.E))
            ttk.Label(self.messages, textvariable = self.success_lbl).grid(column = 1, row = 0, sticky = (tk.W, tk.E))
            ttk.Label(self.messages, textvariable = self.entry_lbl).grid(column = 1, row = 1, sticky = (tk.W, tk.E))
    
            ttk.Label(self.mainframe, text='Default corpus is the 2012 corpus for English books published in the US (eng_us_2012). ' + \
                        '\nUse parentheses for scaled data, as in (petrichor*100), or for plotting the difference in frequencies, ' + \
                        'as in (past-future). \nApostrophes, commas, and other special characters aren\'t searchable.' + \
                        ' Searches are case sensitive.').grid(column = 2, row = 17, columnspan = 5, \
                                                              sticky = (tk.W, tk.E))
    
            for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
            self.master.bind('<Return>', self.plot_ngrams)
            
            
        def populate_corpora(self):
            for corpus_listbox in self.listboxes:
                for element in corpora:
                    corpus_listbox.insert(tk.END, element.name)


        def get_timespans(self):
            #read in data from tsv file, converting data into timespan objects for background plots
            
            mass_lst = []
            temp_lst = []
            line_count = 0
            try:
                with open(self.timespan_file) as timespan_data:
                    for line in timespan_data:
                        temp_lst = line.split('\t')
                        mass_lst.append(temp_lst)
                        line_count += 1
            except:
                pass
            
            #append '\n' to end of data so algorithm will process the last block of timespan data in the file
            mass_lst.append('\n')

            
            object_line = 0
            temp_lst = []
            object_data = []
            created_timespans = [Timespan('none', [])]
            self.options_list = [] #reset to nill in case previously populated
            
            
            if len(mass_lst) != 0: 
                for line in mass_lst:
                    if len(line) == 1:  
                        #line that is ['\n'] is break between timespan objects, so instantiate Timespan with collected info
                        #and reset the variables to collect info for next timespan
                        if len(temp_lst) != 1:
                            created_timespans.append(Timespan(give_name, object_data))
                            #created_timespans.append('new')
                            #created_timespans[created_timespans.index('new')] = Timespan(give_name, object_data)
                        give_name, object_data, object_line = '', [], 0
    
                    else:
                        #collect info for non-break lines; object_line = 0 is first line 
                        #with labels and contains no type int dates
                        for element in line:
                            if object_line is 0:
                                if line.index(element) == 0:
                                    give_name = element
                                temp_lst.append(element.rstrip('\n'))
                            else:
                                if line.index(element) == 0:
                                    temp_lst.append(element)
                                else:
                                    temp_lst.append(int(element.rstrip('\n')))
                        object_line += 1
                        object_data.append(temp_lst)
                        temp_lst = []
    
    
            self.timespan_objects = created_timespans    
            
            for timespan in self.timespan_objects:
                self.options_list.append(timespan.name)
                
            if self.background.size() > 0:  #reset the backgound options list if alreaday populated
                self.background.delete(0, self.background.size())
                
            for label in self.options_list:
                self.background.insert(tk.END, label)

                
                
        def get_timespan_file(self):
            try:
                self.timespan_file = fd.askopenfilename()
                self.get_timespans()
            except:
                pass
    
    
        def get_ngrams_file(self): 
            try:
                self.write_file_name = fd.askopenfilename()
            except:
                pass
            
            
        def get_plot_settings(self):
            #second window for changing plot settings
            self.reset_plot = tk.Toplevel(self.master)
            self.reset_plot.transient(self.master)
            self.reset_plot.resizable(width = tk.FALSE, height = tk.FALSE)
            self.reset_plot.geometry('200x230+200+200')

            
            self.resetframe = ttk.Frame(self.reset_plot, padding='6 6 24 24')
            self.resetframe.grid(column= 0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
            self.resetframe.columnconfigure(0, weight=1)
            self.resetframe.rowconfigure(0, weight=1)
            
    
            ttk.Label(self.resetframe, text = 'for a default value,\n leave entry blank').grid(column = 1, \
                                                                                               row = 1, rowspan = 2)
            ttk.Label(self.resetframe, text = 'start year\n(default 1900)', width = 15).grid(column = 1, row = 3, sticky=(tk.W))
            ttk.Label(self.resetframe, text = 'end year\n(default 2008)', width = 15).grid(column = 1, row = 5, sticky=(tk.W))
            ttk.Label(self.resetframe, text = 'smoothing\n(default 5)', width = 15).grid(column = 1, row = 7, sticky=(tk.W))
            
            self.st_year = ttk.Entry(self.resetframe, width = 4)
            self.fin_year = ttk.Entry(self.resetframe, width = 4)
            self.smooth = ttk.Entry(self.resetframe, width = 3)
            self.st_year.grid(column = 2, row = 3, sticky=(tk.W))
            self.fin_year.grid(column = 2, row = 5, sticky=(tk.W))
            self.smooth.grid(column = 2, row = 7, sticky=(tk.W))
            
            ttk.Button(self.resetframe, text='set values', command=self.set_values).grid(column = 1, row = 8, rowspan = 3)
                                                                                         
            
            for child in self.resetframe.winfo_children(): child.grid_configure(padx = 5, pady=5)
            self.reset_plot.bind('<Return>', self.set_values)
            
        
        def set_values(self, *args):    
            values = []
            entries = [self.st_year, self.fin_year, self.smooth]
            settings = [self.default_plot_settings.start_year, self.default_plot_settings.end_year, \
                        self.default_plot_settings.smoothing]
            for entry, setting in zip(entries, settings):
                value = entry.get()
                if len(value) == 0:
                    value = setting
                values.append(int(value))

            #make sure start year is before end year,  and that start year is
            #not before 1900 and end year is not after 2008
            if values[0] > values[1]:
                values[0], values[1] = values[1], values[0]
            
            if values[0] < 1900:
                values[0] = 1900
                
            if values[1] > 2008:
                values[1] = 2008
            
            self.plot_settings = PlotSettings(values[0], values[1], values[2])
            
            self.reset_plot.destroy()
                    
            
        def validate_input(self, term_to_check):
            #the url call to google ngrams will not search certain character
            #these chars (and leading and trailing whitespace) are removed
        
            not_searchable_parentheses = [',', '\'', '\"', ':', ';', '[', ']', '<', '>']
            not_searchable = not_searchable_parentheses + ['+', '*', '.']
            formatted_term = ''
            found = []
        
            if term_to_check[0] == '(':
                compare_set =  not_searchable_parentheses
            else:
                compare_set =  not_searchable
        
            for letter in term_to_check:     
                if letter in compare_set:
                    found.append(letter)
                else:
                    formatted_term = formatted_term + letter
    
            formatted_term = formatted_term.strip(' ')
    
            #replace any number of spaces >1 with a single space
            space = re.compile( '  +' ) 
            formatted_term = space.sub(' ', formatted_term)
    
            return formatted_term, found


        def plot_ngrams(self, *args):
    
            queries = []
            corpora_selected = []
            entry_messages = []
    
            self.entry_lbl.set('')
            self.success_lbl.set('')
    
            #get and validate entered ngrams
            for ngram in self.entries:
                if len(ngram.get()) > 0:
                    queries.append(ngram.get())
    
            for ngram in queries:
                validated_term, found = self.validate_input(ngram)
    
                if len(found) > 0:
                    for character in found:
                        entry_messages.append('The character \'{}\' is not searchable and was '.format(character) + \
                                              'removed from \'{}\''.format(ngram))
    
                queries[queries.index(ngram)] = validated_term
    
            if len(entry_messages) > 0:
                self.entry_lbl.set('{}'.format('\n'.join(entry_messages)))

        
            #only run ngram search and plotting if something is entered in at least one entry field
            if len(queries) > 0:
                for index in range(len(queries)):
                    if self.listboxes[index].curselection():
                        corpora_selected.append(corpora[self.listboxes[index].curselection()[0]].corpus)
                    else:
                        corpora_selected.append('eng_us_2012')
                
                if self.background.curselection():
                    bck_plot = self.options_list[self.background.curselection()[0]]
                else:
                    bck_plot = 'none'

                #retrieve background plot object selected
                bck_plot_object = self.timespan_objects[self.options_list.index(bck_plot)]
    
                ###CALL TO PLOT###
                plot_success = plot_ngrams_against(queries, corpora_selected, bck_plot_object, self.write_file_name, \
                                                  self.plot_settings)  
        
                if plot_success != 'none':
                    self.success_lbl.set('no data found for {}'.format(', '.join(plot_success)))
    
            else:
                self.success_lbl.set('nothing entered to search')


                
    #
    #data and plotting
    #               
    ngrams = []
    corpora = [Corpus(), Corpus('British', 'eng_gb_2012', 18, '(GB)'), Corpus('English', 'eng_2012', 15, '(Eng)'), \
        Corpus('Fiction', 'eng_fiction_2012', 16, '(Fiction)'), Corpus('German', 'ger_2012', 20, '(Ger)'), \
        Corpus('French', 'fre_2012', 19, '(Fre)'), Corpus('Spanish', 'spa_2012', 21, '(Spa)'), \
        Corpus('Italian', 'ita_2012', 22, '(Ita)'), Corpus('Hebrew', 'heb_2012', 24, '(Heb)'), \
        Corpus('Russian', 'rus_2012', 25, '(Rus)'), Corpus('Chinese', 'chi_2012', 23, '(Chi)')]
                    


    def plot_ngrams_against(terms, languages, bck_plot_object, write_file_name, plot_settings): 
        #using ngram terms, chosen corpora, and background plot from GUI, determined
        #if ngram data exists for the given entries, and if so plot it 
        #retrieved ngram data is for 1900-2008, smoothing 5
        #if return for a query is [0], no ngram found & don't append data; then 
        #delete term and corpus at the appropriate index in respective lists
        
        not_found = []
        successful_terms_corpora = [[], []]
        
        
        def find_in_master_set(term, corpus):
            #find a term, corpus pair in the master list of ngrams already searched in the session

            found = []

            if len(ngrams) > 0:
                for object_saved in ngrams:
                    if term == object_saved.name and corpus == object_saved.corpus and \
                    plot_settings.smoothing == object_saved.smoothing:
                        found = object_saved
                        break

            return found  
        

        def set_max_min(terms, languages, plot_settings):
            #set the y-axis max to be more than the greatest value in the data
            #if data minimum < 0, set y-axis min to be less than the minimum
            #value in the data by at least 10% of min value

            maximum = 0.0
            minimum = 0.0
            
            x_start = plot_settings.start_year - 1900
            x_end = plot_settings.end_year - 1900 + 1

            for term, corpus in zip(terms, languages):
                ngram_object = find_in_master_set(term, corpus)
                if max(ngram_object.data[x_start:x_end]) >= maximum: 
                    maximum = max(ngram_object.data[x_start:x_end])
                if min(ngram_object.data[x_start:x_end]) <= minimum:
                    minimum = min(ngram_object.data[x_start:x_end])

            if abs(minimum) > abs(maximum):
                margin = abs(minimum)/10
            else: 
                margin = maximum/10
            maximum += margin

            if minimum != 0:
                minimum -= margin

            return minimum, maximum



        def plotting(terms, languages, bck_plot_object, write_file_name, plot_settings): 
            #create plot if there is data to plot (i.e. at least one query returned ngram data)

            import matplotlib.axis as axis
            from mpl_toolkits.axes_grid1 import make_axes_locatable

            plt.clf()

            min_val, max_val = set_max_min(terms, languages, plot_settings)
            plt.axis([plot_settings.start_year, plot_settings.end_year, min_val, max_val])

            for ngram_object in ngrams:
                try:
                    with open(write_file_name, mode = 'a') as ngrams_file:
                        ngrams_file.write(('{}\t{}\t').format(ngram_object.name, ngram_object.corpus) + \
                                            '{}\t{}\t{}\n'.format(ngram_object.smoothing, ngram_object.label, ngram_object.data))
                except:
                    pass


            #plot the chosen background timespan info
            main_plot = plt.subplot(1, 1, 1)
            timespan_name = bck_plot_object.name    
            if timespan_name != 'none': 
                bck_plot_object.plot()
                plt.subplots_adjust(bottom=0.17, right=0.76, top=0.92, left = 0.09)
            else:
                plt.axvspan(1900, 2008, color = 'grey', alpha = .2)
                for year in range(1900, 2010, 5):
                    plt.axvline(year, color = 'white', alpha = .7)
                plt.subplots_adjust(bottom=0.09, right=0.76, top=0.92, left = 0.09)


            #if there is negative data, plot horizontal line at y = 0.0
            if min_val < 0.0:
                plt.axhline(0.0, color = 'black', alpha = .5, linewidth = 0.5)


            #plot the data for the years 1900-2008
            colors = ['black', 'blue', 'green', 'red', 'indigo']
            for queried_term, queried_corpus, plot_color in zip(terms, languages, colors):
                for object_saved in ngrams:
                    if queried_term == object_saved.name and queried_corpus == object_saved.corpus and \
                    plot_settings.smoothing == object_saved.smoothing:
                        plt.plot(range(1900, 2009), object_saved.data, label = object_saved.label, \
                                    color = plot_color, linewidth = 2.0)
                        break


            #create title and legend for main plot
            if timespan_name == 'none':
                plt.title('Ngrams {}-{}'.format(plot_settings.start_year, plot_settings.end_year))
            else:
                plt.title('Ngrams and {}'.format(timespan_name))
            plt.ylabel('% of ngrams')
            plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.2)


            #if background data plotted, create bar with timespan info beneath main plot
            if timespan_name is not 'none':
                divider = make_axes_locatable(main_plot)
                box = divider.append_axes('bottom', size = '5%', pad=0.25)  
                bck_plot_object.plot() 
                box.axes.get_yaxis().set_visible(False)
                tick_info = bck_plot_object.get_labels()
                box.set_xticks(tick_info[1])
                box.set_xticklabels(tick_info[0], rotation = 45, ha = 'right')
                plt.axis([plot_settings.start_year, plot_settings.end_year, 0, 1])
                box.tick_params(axis = u'both', which = u'both', length = 0) 

            plt.show()



        def getNgrams(query, corpus, startYear, endYear, smoothing):
            #getNgrams py3 update adapted for plot_ngram_against()
            #parse the query to format for url, convert the returned binary data to a 
            #string, and then find and return the ngram data as a list
            #NB: in py3 urllib request read() returns binary data that must be decoded to utf-8

            import urllib
            import json

            urlquery = urllib.parse.quote_plus(query, safe = '')
            for element in corpora:
                if element.corpus == corpus:
                    corpusNumber = element.number
                    break
            url = 'http://books.google.com/ngrams/graph?content={:s}&year_start={:d}'.format(urlquery, startYear) \
            + '&year_end={:d}&corpus={:d}&smoothing={:d}&share='.format(endYear, corpusNumber, smoothing)


            return_values = []
            try:
                response_str = urllib.request.urlopen( url ).read().decode('utf-8')
            except:
                return_values = [0]


            if not return_values:
                pattern = ('(?<=var data = \[).*?}(?=\])')
                var_data = re.findall(pattern, response_str)
                data = json.loads(var_data[0])
                return_values = data['timeseries']

            return return_values
    
    
    
        #search ngrams (list of ngrams created) for the term/corpus combinations queried
        #if any of these searches are already present in ngrams, there is  no 
        #need to make another url call to get that data
        for word, corpus in zip(terms, languages):
            if find_in_master_set(word, corpus): 
                get = False
                successful_terms_corpora[0].append(word)
                successful_terms_corpora[1].append(corpus)
            else:
                get = True
                
            if get == True:
                values = getNgrams(word, corpus, 1900, 2008, plot_settings.smoothing)
                if len(values) == 1:
                    not_found.append('\'' + word + '\' in ' + corpus)
                else:
                    ngrams.append(NGram(word, corpus, plot_settings.smoothing, '', values))
                    ngrams[-1].set_label()
                    successful_terms_corpora[0].append(word)
                    successful_terms_corpora[1].append(corpus)
    
    
        #if all ngrams have plottable data, plot & return 'none'
        #else remove the corresponding words and corpora from the 
        #lists so aren't produced in the plot figure, then plot ngram 
        #queries with data, and return those that didn't have data to plot
        
        if len(successful_terms_corpora[0]) == 0:
            success = not_found
        elif len(not_found) > 0:
            plotting(successful_terms_corpora[0], successful_terms_corpora[1], bck_plot_object, write_file_name, \
                    plot_settings)
            success = not_found
        else:
            plotting(successful_terms_corpora[0], successful_terms_corpora[1], bck_plot_object, write_file_name, \
                    plot_settings)
            success = 'none'
            
        return(success)
    
    
    
    root = tk.Tk()
    gui = Application(root)
    root.mainloop()
    
    
if __name__ == '__main__':
    culturomics_explorer()
