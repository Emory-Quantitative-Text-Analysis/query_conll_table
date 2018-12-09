#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import sys
from subprocess import call
import os
import datetime
import re
from sys import platform
from tkinter import filedialog
import os
import tkinter.messagebox as mb
import tkinter as tk
import ntpath

#%%
set_POSTAG = {'IN', "''", 'LS', ',', ':', 'WDT', 'VBP', 'PRP$', '.', 'VBD', '#', 'JJR', 'PRP', ')',\
        'EX', 'MD', 'FW', 'VBZ', 'NNPS', 'TO', '(', 'NNS', 'RP', 'SYM', 'NNP', 'WP$', 'DT', 'RBS',\
        'UH', 'CD', 'NN', 'JJS', 'VBG', 'WRB', 'WP', 'VBN', 'VB', 'PDT', '$', '``', 'RBR', 'CC',\
        'RB', 'JJ'}
set_DEPREL = {'nsubj', 'det', 'compound:prt', 'case', 'auxpass',\
              'parataxis', 'csubj', 'nummod', 'det:predet', 'mark',\
              'neg', 'nmod:poss', 'expl', 'dep', 'cop', 'cc:preconj',\
              'csubjpass', 'advmod', 'compound', 'ccomp', 'nmod:npmod',\
              'acl:relcl', 'aux', 'nsubjpass', 'nmod', 'appos', 'dobj', \
              'iobj', 'xcomp', 'discourse', 'cc', 'mwe', 'amod', 'ROOT', \
              'conj', 'nmod:tmod', 'punct', 'acl', 'advcl'}
dict_DEPREL = {'acomp': 'adjectival complement',\
               'advcl': 'adverbial clause modifier',\
               'advmod': 'adverb modifier',\
               'agent': 'agent',\
               'amod': 'adjectival modifier',\
               'appos': 'appositional modifier',\
               'aux': 'auxiliary',\
               'auxpass': 'passive auxiliary',\
               'cc': 'coordination',\
               'ccomp': 'clausal complement',\
               'conj': 'conjunct',\
               'cop': 'copula',\
               'csubj': 'clausal subject',\
               'csubjpass': 'clausal passive subject',\
               'dep': 'dependent',\
               'det': 'determiner',\
               'discourse': 'discourse element',\
               'dobj': 'direct object',\
               'expl': 'expletive',\
               'goeswith': 'goes with',\
               'iobj': 'indirect object',\
               'mark': 'marker',\
               'mwe': 'multi-word expression',\
               'neg': 'negation modifier',\
               'nn': 'noun compound modifier',\
               'npadvmod': 'noun phrase as adverbial modifier',\
               'nsubj': 'nominal subject',\
               'nsubjpass': 'passive nominal subject',\
               'num': 'numeric modifier',\
               'number': 'element of compound number',\
               'parataxis': 'parataxis',\
               'pcomp': 'prepositional complement',\
               'pobj': 'object of a preposition',\
               'poss': 'possession modifier',\
               'possessive': 'possessive modifier',\
               'preconj': 'preconjunct',\
               'predet': 'predeterminer',\
               'prep': 'prepositional modifier',\
               'prepc': 'prepositional clausal modifier',\
               'prt': 'phrasal verb particle',\
               'punct': 'punctuation',\
               'quantmod': 'quantifier phrase modifier',\
               'rcmod': 'relative clause modifier',\
               'ref': 'referent',\
               'root': 'root',\
               'tmod': 'temporal modifier',\
               'vmod': 'reduced non-finite verbal modifier',\
               'xcomp': 'open clausal complement',\
               'xsubj': 'controlling subject',\
               'nmod:tmod': 'temporal modifier',\
               'nummod': 'numeric modifier',\
               'acl': 'clausal modifier of noun (adjectival clause)',\
               'nmod:poss': 'possessive nominal modifier',\
               'cc:preconj': 'preconjunct',\
               'case': 'case marking',\
               'ROOT': 'root',\
               'nmod': 'nmod: nominal modifier',\
               'compound':'compound',\
               'acl:relcl': 'relative clause modifier',\
               'compound:prt': 'phrasal verb particle',\
               'nmod:npmod': 'noun phrase as adverbial modifier',\
               'det:predet': 'predeterminer',\
               '#':    '#'
               }
dict_POSTAG = { 'CC':'Coordinating conjunction',\
                'CD': 'Cardinal number',\
                'DT': 'Determiner',\
                'EX': 'Existential there',\
                'FW': 'Foreign word',\
                'IN': 'Preposition or subordinating conjunction',\
                'JJ': 'Adjective',\
                'JJR':  'Adjective, comparative',\
                'JJS':  'Adjective, superlative',\
                'LS': 'List item marker',\
                'MD': 'Modal',\
                'NN': 'Noun, singular or mass',\
                'NNS':  'Noun, plural',\
                'NNP':  'Proper noun, singular',\
                'NNPS': 'Proper noun, plural',\
                'PDT':  'Predeterminer',\
                'POS':  'Possessive ending',\
                'PRP':  'Personal pronoun',\
                'PRP$': 'Possessive pronoun',\
                'RB': 'Adverb',\
                'RBR':  'Adverb, comparative',\
                'RBS':  'Adverb, superlative',\
                'RP': 'Particle',\
                'SYM':  'Symbol',\
                'TO': 'to',\
                'UH': 'Interjection',\
                'VB': 'Verb, base form',\
                'VBD':  'Verb, past tense',\
                'VBG':  'Verb, gerund or present participle',\
                'VBN':  'Verb, past participle',\
                'VBP':  'Verb, non-3rd person singular present',\
                'VBZ':  'Verb, 3rd person singular present',\
                'WDT':  'Wh-determiner',\
                'WP': 'Wh-pronoun',\
                'WP$':  'Possessive wh-pronoun',\
                'WRB':  'Wh-adverb',\
                '(':    '(',\
                ')':    ')',\
                '.':    '.',\
                ',':    '.',\
                ':':    ':',\
                '\'':   '\'',\
                '\"':   '\"',\
                '#':    '#'
                }

#to avoid key value error 
def find_full_postag(__form__,__postag__):
    
    if __postag__ in dict_POSTAG:
        
        return dict_POSTAG[__postag__] 
    else:
        return __form__

#to avoid key value error
def find_full_deprel(__form__,__deprel__):
    
    if __deprel__ in dict_DEPREL:
        return dict_DEPREL[__deprel__]
    else:
        return __form__

#%%
"""
This function divides the conll table into sentences
input: all rows
output: list of sentences, each sentence is a list of multiple rows
        each row represent a token in the file
"""
def sentence_division(list_csv_rows):
    list_sentences = []
    sentence_id_prev = 1 #sentence id of previous row
    current_sentence = []
    for _index_, item in enumerate(list_csv_rows):
        sentence_id = int(item[9])
        #This includes the last sentence
        if _index_ + 1 == len(list_csv_rows):
            list_sentences.append(current_sentence)
            current_sentence.append(item)
            return list_sentences
        if sentence_id == sentence_id_prev:
            current_sentence.append(item)
            continue
        else:
            sentence_id_prev = sentence_id
            list_sentences.append(current_sentence)
           # print(current_sentence)
            current_sentence = []
            current_sentence.append(item)
    return list_sentences
#%%%
"implement: any token that has a direct relation with this word"
"The dependency tree seem to not work well for our purposes?"
def find_children(sentence_children,ind_keyword):
    list_children = []
    list_children_index = []
    for ind, tok in enumerate(sentence_children):
        head_num = int(tok[5])
        if head_num == ind_keyword:
            token_index = int(tok[0])
            token_form = tok[1]
            token_postag = tok[3]
            token_deprel = tok[6]
            list_children.append((token_form,token_postag,token_deprel))
            list_children_index.append(token_index)
    return list_children, list_children_index
#%%
def search_head(token_id_in_sentence,sentence):
    token = sentence[int(token_id_in_sentence)-1]
    head_num = int(token[5])
    if head_num != token[0] and head_num != 0:
        head_form = sentence[head_num-1][1]   #form
        head_postag = sentence[head_num-1][3] #postag
        head_deprel = sentence[head_num-1][6] #deprel
    elif head_num == 0:
        return "NO_HEAD","NO_HEAD"
    else:
        return "NO_HEAD","NO_HEAD"
    return (head_form,head_postag,head_deprel), head_num
#print (search_head(6,sentence_0))
#%%
"""
return all indices of the input word
"""
def search_token_form(desired_form,sentence):
    #return a list of indices in the sentence related to the desired word
    list_indices = []
    for item in sentence:
        token_form = item[1]
        token_index_in_sent = int(item[0])
        if token_form == desired_form:
            list_indices.append(token_index_in_sent)
    return list_indices
"""
return all indices of the co-occuring word
"""
def search_related_words(desired_form, sentence, __field__ = 'FORM', kw_desired_postag = '*',kw_desired_deprel='*'):
    list_indices_related_word = []
    for token in sentence:
        token_form = token[1]
        token_lemma = token[2]
        token_id = token[0]
        token_postag = token[3]
        token_deprel = token[6]
        if __field__ == 'FORM':
            compare_term = token_form
        else:
            compare_term = token_lemma
        if compare_term == desired_form:
            if kw_desired_postag != '*':
               # print ("AAA")
                if '*' not in kw_desired_postag:
                    if token_postag != kw_desired_postag:
                        continue
                else:
                    if kw_desired_postag == "NN*":
                        if token_postag in ['NN','NNS','NNP','NNPS']:
                            continue
            if kw_desired_deprel != "*":
               # print ("#######",token_deprel,kw_desired_deprel)
                if token_deprel != kw_desired_deprel:
                    continue
            head, head_num = search_head(token_id,sentence)
            if head != "NO_HEAD":
               list_indices_related_word.append((head_num,1))
            #print (find_children(sentence,int(token_id)))
            for child in find_children(sentence,int(token_id))[1]:
                list_indices_related_word.append((child,0))
               # print ("children")
    return list_indices_related_word
#%%
"""
1. return the list of tokens related to the word
2. filter out all the co-occuring words with undesired postag, deprel
"""
def query_the_table(list_sentences, form_of_token, _field_ ='FORM', pos_tag = "*",dep_relation="*",sentence_id="*",_tok_postag_ ='*',_tok_deprel_ = '*'):
    list_queried = []
    for sent in list_sentences:
        list_word_indices = search_related_words(form_of_token,sent,_field_,_tok_postag_,_tok_deprel_)
        whole_sent = ""
        for token in sent:
            whole_sent+= token[1]+" "
        whole_sent = whole_sent.strip()
        for node in list_word_indices:
            ind = node[0]
            is_head = node[1]
            row = sent[int(ind)-1]
            tok_form = row[1]
            tok_postag = row[3]
            tok_deprel = row[6]
            tok_sentence_id = row[9]
            tok_article_id = row[8]
            #tok_document_id = row[9]
            tok_document_name = row[10]
            token_id = str(tok_article_id)[:-2]+str("-"+tok_sentence_id)
            list_queried.append((tok_form,tok_postag,tok_deprel,is_head,str(tok_article_id)[:-2],tok_sentence_id,tok_document_name,whole_sent))
    #filter the output list
    if pos_tag == "*" and dep_relation == "*" and sentence_id == "*":
        return list_queried
   # postag_list_queried = list_queried
    if "*" not in pos_tag:
        postag_list_queried = list(filter(lambda tok:tok[1]==pos_tag,list_queried))
    elif pos_tag == "NN*":
        postag_list_queried = list(filter(lambda tok:tok[1] in ['NN','NNS','NNP','NNPS'],list_queried))
    else:
        postag_list_queried = list_queried
    if "*" not in dep_relation:
        deprel_list_queried = list(filter(lambda tok:tok[2]==dep_relation,postag_list_queried))
    else:
        deprel_list_queried = postag_list_queried
    return deprel_list_queried
#%%
"""
Print all the output.
"""
def print_result(_list_queried_):
    if len(_list_queried_) == 0:
        print ("No results found matching your criteria. Please, try a different input.")
        exit()
    for _item_ in _list_queried_:
        print (_item_[0],_item_[1],find_full_postag(_item_[0],_item_[1]),_item_[2],find_full_deprel(_item_[0],_item_[2]),_item_[3],_item_[4],_item_[5],_item_[6],_item_[7])
#%%
"""
print the usage of this program.
"""
def usage():
    print("Please, type the following command:\n"
          "python query_conll.py [conll_table_path] [output path] keyword field postag deprel co-postag co-deprel [y/n](open output file or not)\n"\
          "EXAMPLE:\n\n"\
          "python3 query_conll.py mergedConllTables_GAYMEN.conll father_search.csv father form NN '*' '*' '*' y\n\n"\
          "All the arguments need to be accurate and in the right order. Otherwise, Graphical User Interface will be prompted."
          )
#%%
"""
put all the output in a csv file.
"""
def output_file(list_queried,path_output):
    list_output = [['FORM','POSTAG','POSTAG-DESCRIPTION','DEPREL','DEPREL-DESCRIPTION','is_HEAD','DOCUMENT-ID','SENTENCE-ID','DOCUMENT-NAME','FULL_SENTENCE']]
    for item in list_queried:
        list_output.append([item[0],item[1],find_full_postag(item[0],item[1]),item[2],find_full_deprel(item[0],item[2]),item[3],item[4],item[5],item[6],item[7]])
    with open(path_output, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(list_output)
    print("An output file",path_output,"is generated.")
    csvFile.close()
#%%
introduction_of_program =  "This python3 routine will search all the tokens (i.e., words) related to a user-supplied keyword\nfound in either FORM or LEMMA of a user-supplied conll table.\n\nYou can filter results by specific POSTAG and DEPREL values for both searched and co-occurring tokens\n(e.g., POSTAG NN for nouns, DEPREL nsubjpass for passive nouns that are subjects.)\n\nIn INPUT the routine expects a conll table generated by the python routine StanfordCoreNLP.py.\nIn OUTPUT the routine creates a tab-separated csv file with a user-supplied filename and path;\nit also displays the same infomation in the command line."
instruction_enter_path = "Please, enter the INPUT filename and path of the document to be analyzed: "
empty_input_path_warning = "No filename+path entered."
instruction_enter_token = "Please, enter the token (i.e., word) to be searched: "
empty_input_token_warning = "ERROR. No search token entered."
instruction_enter_field = "Please, enter the CoNLL field to be used for the search (FORM or LEMMA; RETURN for default FORM): "
instruction_token = "For this section, Enter POSTAG and DEPREL values for both searched and co-occurring tokens if you want to filter results (e.g., POSTAG NN for nouns, DEPREL nsubjpass for passive nouns that are subjects.)"
instruction_POSTAG_token = "Please, enter POSTAG value for searched token (e.g., NN for noun; RETURN for ANY POSTAG value): "
instruction_DEPREL_token = "Please, enter DEPREL value for searched token (e.g., nsubjpass for passive nouns that are subjects; RETURN for ANY DEPREL value): "
instruction_POSTAG_co =  "Please, enter POSTAG value for co-occurring token (e.g., NN for noun; RETURN for ANY POSTAG value): "
instruction_DEPREL_co = "Please, enter DEPREL value for co-occurring token (e.g., DEPREL nsubjpass for passive nouns that are subjects; RETURN for ANY DEPREL value): "
#%%

"""
Main Program
"""
window = tk.Tk()
window.title('Query the CONLL')
window.geometry('800x600')

intro = tk.Label(window, 
                 anchor = 'w',
                 text='All fields with \'*\' need to be filled',font=('red'))
intro.pack()
tk.Label(window, text='Field *').place(x=50, y= 70)
tk.Label(window, text='Keyword *').place(x=50, y= 110)
tk.Label(window, text='Postag of keyword').place(x=50, y= 150)
tk.Label(window, text='Deprel of keyword').place(x=50, y= 190)
tk.Label(window, text='Postag of co-occuring words').place(x=50, y= 230)
tk.Label(window, text='Deprel of co-occuring words').place(x=50, y= 270)

var_field = tk.StringVar()
var_field.set('FORM')

var_kw = tk.StringVar()
var_kw.set('e.g.: father')

var_postag = tk.StringVar()
var_postag.set('*')

var_deprel = tk.StringVar()
var_deprel.set('*')

var_co_postag = tk.StringVar()
var_co_postag.set('*')

var_co_deprel = tk.StringVar()
var_co_deprel.set('*')

entry_var_field = tk.Entry(window, textvariable=var_field)
entry_var_field.place(x=250, y=70)

entry_var_kw = tk.Entry(window, textvariable=var_kw)
entry_var_kw.place(x=250, y=110)

entry_var_postag = tk.Entry(window, textvariable=var_postag)
entry_var_postag.place(x=250, y=150)

entry_var_deprel = tk.Entry(window, textvariable=var_deprel)
entry_var_deprel.place(x=250, y=190)

entry_var_co_postag = tk.Entry(window, textvariable=var_co_postag)
entry_var_co_postag.place(x=250, y=230)

entry_var_co_deprel = tk.Entry(window, textvariable=var_co_deprel)
entry_var_co_deprel.place(x=250, y=270)


on_hit = False
def hit_me():
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('Saved file will be opened for inspection')
    else:
        on_hit = False
        var.set('')

"""
massage boxes
"""
def main_msgbox():
    mb.showinfo(title='Introduction', message=introduction_of_program)
    
def field_msgbox():
    mb.showinfo(title='Field',
                           message='Please, enter the CoNLL field to be used for the search (FORM or LEMMA)')

def keyword_msgbox():
    mb.showinfo(title='Keyword',
                           message='Please, enter the token (i.e., word) to be searched')    

def kw_postag_msgbox():
        mb.showinfo(title='postag of token',
                           message=instruction_token+'\n\n'+instruction_POSTAG_token)  
        
def kw_deprel_msgbox():
        mb.showinfo(title='deprel of msgbox',
                           message=instruction_token+'\n\n'+instruction_DEPREL_token)  
        
def postag_msgbox():
        mb.showinfo(title='postag of keyword',
                           message=instruction_token+'\n\n'+instruction_POSTAG_co)
        
def deprel_msgbox():
        mb.showinfo(title='postag of keyword',
                           message=instruction_token+'\n\n'+instruction_DEPREL_co)


def exit_window():
    print('hey')
    global window
    window.destroy()
    #print(var_field.get(),var_kw.get())
    exit()
    
openfilename=tk.StringVar()
openfilename.set('')
def ask_openfilename():
    global openfilename
    openfilename.set(filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("conll tables","*.conll"),("all files","*.*"))))
    
    #print (openfilename)

savefilename = tk.StringVar()
savefilename.set('')
def ask_savefilename():
    global savefilename
    savefilename.set(filedialog.asksaveasfilename(initialdir = os.getcwd(),
            title = "Save file",filetypes = (("csv files","*.csv"),("all files","*.*"))))
    #print (savefilename)
def print_open_file_or_not():
    if var1.get() == 1:
        l_checkbox.config(text="You will open the saved file for inspection")
    elif var1.get() == 0:
        l_checkbox.config(text="You will NOT open the saved file for inspection")
        
def execute_query_conll():
    pass

def test_input_and_run_query():
    """
    Test input
    """
    field=var_field.get()
    if field.lower() not in ['field','form']:
        field = 'FORM'
    
    keyword=var_kw.get() 
    if keyword == 'e.g.: father':
        mb.showwarning(title='keyword input error', message='Please check the \'Keyword\' field and try again')
        return
    
    postag = var_postag.get()
    if postag != '*' and postag not in set_POSTAG:
        postag = '*'
        
    deprel = var_deprel.get()
    if deprel!='*' and deprel not in set_DEPREL:
        print ("The routine cannot recognize your input. The default value\'*\'(i.e. ANY VALUE) will be used.")
        deprel = '*'
        
    co_postag=var_co_postag.get()
    if co_postag != '*' and co_postag not in set_POSTAG:
        co_postag = '*'
        
    co_deprel=var_co_deprel.get()
    if co_deprel!='*' and co_deprel not in set_DEPREL:
        print ("The routine cannot recognize your input. The default value\'*\'(i.e. ANY VALUE) will be used.")
        co_deprel = '*'
        
    #file path
    input_file_name = openfilename.get()
    
    if not os.path.isfile(input_file_name.strip()) or not input_file_name.strip()[-6:]=='.conll':
        mb.showwarning(title='input file path error', message='Please check INPUT FILE PATH and try again')
        return        
    
    output_file_name = savefilename.get()
    if not output_file_name[-4:] == '.csv':
        mb.showwarning(title='output file path error', message='Please check OUTPUT FILE PATH and try again')
        return
    
    open_file_or_not = var1.get()

    print (field,keyword,postag,deprel,co_postag,co_deprel,input_file_name,output_file_name,open_file_or_not)

    #todo: execute query
    f = open(input_file_name.strip(),encoding='ISO-8859-1')
    reader = csv.reader(f,delimiter='\t')
    data = [r for r in reader]
    all_sents = sentence_division(data)
    queried_list=query_the_table(all_sents,keyword,field, co_postag,co_deprel, _tok_postag_=postag,_tok_deprel_=deprel)       
    print_result(queried_list)
    output_file(queried_list,output_file_name)
    
    if open_file_or_not != 0:
        ##windows
        if platform in ['win32','cygwin']:
            os.system('start '+output_file_name)
        ##macOS and ubuntu
        else:        
            call(['open',output_file_name])
    #todo: exit program

"""
select file button
"""
tk.Label(window, textvariable=openfilename).place(x=250, y= 310)
tk.Label(window, textvariable=savefilename).place(x=250, y= 350)


select_file_button=tk.Button(window, text='select input conll table *',bg='blue',command=ask_openfilename)
select_file_button.place(x=50,y=310)

select_save_file_button=tk.Button(window, text='save output file name *', command=ask_savefilename)
select_save_file_button.place(x=50,y=350)

#checkbox
l_checkbox = tk.Label(window, width=50, text='You will NOT open the saved file for inspection')
l_checkbox.place(x=150,y=390)

var1 = tk.IntVar()
var1.set(0)
c1 = tk.Checkbutton(window, text='open saved file?', variable=var1, onvalue=1, offvalue=0,
                    command=print_open_file_or_not)
c1.place(x=50,y=390)

"""
Small Buttons
"""
button_field_help = tk.Button(window, text='Instruction', command=field_msgbox)
button_field_help.place(x=500,y=70)

button_kw_help = tk.Button(window, text='Instruction', command=keyword_msgbox)
button_kw_help.place(x=500,y=110)

button_kw_postag_help = tk.Button(window, text='Instruction', command=kw_postag_msgbox)
button_kw_postag_help.place(x=500,y=150)

button_kw_deprel_help = tk.Button(window, text='Instruction', command=kw_deprel_msgbox)
button_kw_deprel_help.place(x=500,y=190)

button_postag_help = tk.Button(window, text='Instruction', command=postag_msgbox)
button_postag_help.place(x=500,y=230)

button_deprel_help = tk.Button(window, text='Instruction', command=deprel_msgbox)
button_deprel_help.place(x=500,y=270)


"""
MAJOR BUTTONS
"""
quit_button = tk.Button(window, text='QUIT', width=15,height=2, command=exit_window)
quit_button.place(x=350,y=500)

execute_button = tk.Button(window, text='Run Query', width=15,height=2, command=test_input_and_run_query)
execute_button.place(x=200,y=500)

intro_button = tk.Button(window, text='Read Me',command=main_msgbox,width=15,height=2)
intro_button.place(x=50,y=500)


try:
    usage()
    input_file_name = sys.argv[1]
    if not os.path.isfile(input_file_name.strip()) or not input_file_name.strip()[-6:]=='.conll':
        raise FileNotFoundError
    openfilename.set(input_file_name)
    
    output_file_name = sys.argv[2]
    #default output name 
    keyword = sys.argv[3]
    var_kw.set(keyword)
    
    field = sys.argv[4]

    if field.lower() not in ['field','form']:
        field = 'FORM'
    var_field.set(field)
    
    postag = sys.argv[5]
    if postag != '*' and postag not in set_POSTAG:
        print ("The routine cannot recognize your input. The default value\'*\'(i.e. ANY VALUE) will be used.")
        postag = '*'
    var_postag.set(postag)
    
    deprel = sys.argv[6]
    if deprel!='*' and deprel not in set_DEPREL:
        print ("The routine cannot recognize your input. The default value\'*\'(i.e. ANY VALUE) will be used.")
        deprel = '*'   
    var_deprel.set(deprel)

    co_postag = sys.argv[7]
    if co_postag != '*' and co_postag not in set_POSTAG:
        print ("The routine cannot recognize your input. The default value\'*\'(i.e. ANY VALUE) will be used.")
        co_postag = '*'
    var_co_postag.set(co_postag)
    
    co_deprel = sys.argv[8] 
    if co_deprel!='*' and co_deprel not in set_DEPREL:
        print ("The routine cannot recognize your input. The default value\'*\'(i.e. ANY VALUE) will be used.")
        co_deprel = '*'    
    var_co_deprel.set(co_deprel)
    
    open_file_or_not = sys.argv[9]
    if open_file_or_not.lower() == 'n':
        open_file_or_not = 0
    else:
        open_file_or_not = 1
        
    f = open(input_file_name.strip(),encoding='ISO-8859-1')
    reader = csv.reader(f,delimiter='\t')
    data = [r for r in reader]
    all_sents = sentence_division(data)
    
    queried_list=query_the_table(all_sents,keyword,field, co_postag,co_deprel, _tok_postag_=postag,_tok_deprel_=deprel)       
    print_result(queried_list)
    output_file(queried_list,output_file_name)
    
    if open_file_or_not != 0:
        ##windows
        if platform in ['win32','cygwin']:
            os.system('start '+output_file_name)
        ##macOS and ubuntu
        else:        
            call(['open',output_file_name])
    exit()
except Exception as e:
    print ("\nCommand line arguments are empty or not correct: "+e.__doc__)
    print ("\nGraphical User Interface will be activated")
    window.mainloop()


