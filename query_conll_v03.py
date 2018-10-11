#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jian
"""

#%%
"""
A column 1: the id of the token in the sentence *****token[0] id
B column 2: the form ********************************token[1] form
C column 3: the lemma *******************************token[2] lemma(stem) 
D column 4: part of speech tags**********************token[3] POS Tag
E column 5: Named Entity Recognition
F column 6: Head of the current word, either a value of ID or zero(0)**head
G column 7: Dependency Relation? ********************token[6] dep-relation
H column 8: id of the token in the whole table
I column 9: id of the article (file)
J column 10: id of the sentence in the article
K column 11: name of the file 
L column 12: date of the text (?)
----------------------------------------------------------------
"""
"""
1. processing within a sentence
1.1 to get the head and children of each word 
1.2 to get the POS tag of each word related

2. divide the data into sentences

3. query?


# in the table, "come out" are seperated into two tokens
# search the form or search the lemma
"""

"""
update @2018-08-11

1. Update the wording of the instruction of this python program.

2. Write a readme file to introduce the goal and mechanism of this program.

3. New function: map POS TAG and DEPREL to readable wording , refering to the stanford dependency relations manual.

"""

#%%
import csv
import sys
import random

#%%

set_POSTAG = {'IN', "''", 'LS', ',', ':', 'WDT', 'VBP', 'PRP$', '.', 'VBD', '#', 'JJR', 'PRP', ')', 'EX', 'MD', 'FW', 'VBZ', 'NNPS', 'TO', '(', 'NNS', 'RP', 'SYM', 'NNP', 'WP$', 'DT', 'RBS', 'UH', 'CD', 'NN', 'JJS', 'VBG', 'WRB', 'WP', 'VBN', 'VB', 'PDT', '$', '``', 'RBR', 'CC', 'RB', 'JJ'}

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
               'det:predet': 'predeterminer'\
               
               }


#%%




#%%
"""
This function divide the conll table into sentences

input: all rows

output: list of sentences, each sentence is a list of multiple rows
        each row represent a token in the file
"""

def sentence_division(list_csv_rows):
    
    list_sentences = []
    
    sentence_id_prev = 1 #sentence id of previous row
    
    current_sentence = []
    
    for item in list_csv_rows:
        
        sentence_id = int(item[9])
        
        if sentence_id == sentence_id_prev:
            
            current_sentence.append(item)
            
            continue
        
        else:
            
            sentence_id_prev = sentence_id
            
            list_sentences.append(current_sentence)
            
           # print(current_sentence)
            
            current_sentence = []
            
            current_sentence.append(item)
    
    #print ("A total of {} tokens has been grouped into {} sentences".format(len(list_csv_rows),len(list_sentences))) 
    return list_sentences

#%%%

"implement: any token that has a direct relation with this word"

"The dependency tree seem to not work well for our purposes?"

def find_children(sentence_children,ind_keyword):
    
    list_children = []
    
    list_children_index = []
    
    for ind, tok in enumerate(sentence_children):
        
        head_num = int(tok[5])
        
       # print (head_num, ind_keyword)
        
        if head_num == ind_keyword:
            
            token_index = int(tok[0])
            token_form = tok[1]
            token_postag = tok[3]
            token_deprel = tok[6]
            
            
            list_children.append((token_form,token_postag,token_deprel))
            
            list_children_index.append(token_index)
            
    return list_children, list_children_index

#print (find_children(sentence_0,6))


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
    
def search_token_form(desired_form,sentence):
    
    #return a list of indices in the sentence related to the desired word
    list_indices = []
    
    
    for item in sentence:
        
        token_form = item[1]
        
        #print(desired_form,token_form)
        
        token_index_in_sent = int(item[0])
        
        if token_form == desired_form:
            
            list_indices.append(token_index_in_sent)
    
    return list_indices
            

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
            
#################################################### 
#THIS SECTION OF CODE COULD BE MODIFIED...
            
            #if we want to restrict the postag of the key word
           # print (kw_desired_postag, kw_desired_deprel)
            
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
#####################################################
            
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
"""
def query_the_table(list_sentences, form_of_token, _field_ ='FORM', pos_tag = "*",dep_relation="*",sentence_id="*",_tok_postag_ ='*',_tok_deprel_ = '*'):
    
    #print("%%%%%%%%%",tok_postag,tok_deprel)
    
    list_queried = []
    
    for sent in list_sentences:
        
        list_word_indices = search_related_words(form_of_token,sent,_field_,_tok_postag_,_tok_deprel_)
        
        for node in list_word_indices:
            
            ind = node[0]
            
            is_head = node[1]
            
            row = sent[int(ind)-1]
            
            tok_form = row[1]
            
            tok_postag = row[3]
            
            tok_deprel = row[6]
            
            tok_sentence_id = row[9]
            
            tok_article_id = row[8]
            
            token_id = str(tok_article_id)[:-2]+str("-"+tok_sentence_id)
            
            list_queried.append((tok_form,tok_postag,tok_deprel,is_head,str(tok_article_id)[:-2],tok_sentence_id))

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

def print_result(list_queried):
    
    if len(list_queried) == 0:
        print ("There is no result matching the restriction given. Plase try with a different input.")
        exit()
        
    for item in list_queried:
        
        print (item[0],item[1],item[2],item[3],item[4],item[5])


#%%
def usage():
    
    print("Please type the following command\n"
          "python3 [path of query_conll.py] [filepath_of_conill_table]\n"\
          "EXAMPLE:\n\n"
          "python3 query_conll.py mergedConllTables_GAYMEN.conll \n\n"
          )
#%%

def output_file(list_queried,path_output):
    
    if path_output is None:
        print ("ERROR: empty output path.")
        exit()
    
    list_output = [['FORM','POSTAG','DEPREL','Dependency_Relation','is_HEAD','ARTICLE-ID','SENTENCE-ID']]
    
    for item in list_queried:
        
        list_output.append([item[0],item[1],item[2],dict_DEPREL[item[2]],item[3],item[4],item[5]])
    
    with open(path_output, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(list_output)
    
    csvFile.close()
#%%

"""
make a summary of the data
"""

#%%

introduction_of_program =  "\nThis python routing will search all the tokens, \
which are related to a user-selected keyword (found in Form or Lemma in the conll table).\n\n\
In output it will create a tab-seperated csv file with a user-supplied name.\n\nIt will also display the same infomation in the command line.\n"

instruction_enter_token = "Please, enter the token (i.e., word) to be searched: "

empty_input_warning = "ERROR. There is no search word.\n"

instruction_enter_field = "Please, enter the CoNLL field where to search. (FORM or LEMMA).\n \
(RETURN for default FORM):"

instruction_token = "You will be asked next to enter POSTAG and DEPREL values. \
If you want to filter the searched token for specific POSTAG and DEPREL values for both search and co-occurring tokens.\n \
(e.g., POSTAG NN for nowns, DEPREL nsubjpass for passive nowns that are subjects.)"

instruction_POSTAG_token = "Please, enter POSTAG value for searched token (e.g., NN for noun; RETURN for ANY POSTAG value): "

instruction_DEPREL_token = "Please, enter DEPREL value for searched token (e.g., DEPREL nsubjpass for passive nouns that are subjects; RETURN for ANY DEPREL value):"
    
instruction_POSTAG_co =  "Please, enter POSTAG value for co-occurring token (e.g., NN for noun; RETURN for ANY POSTAG value):"

instruction_DEPREL_co = "Please, enter DEPREL value for co-occurring token (e.g., DEPREL nsubjpass for passive nouns that are subjects; RETURN for ANY DEPREL value): "


#%%
"""

Main program

"""    
if len(sys.argv)<2:
    usage()
else:
    file_path = sys.argv[1]


file_name = file_path

print(introduction_of_program+"\n")

key_word = input(instruction_enter_token)

while len(key_word)==0:
    print ('\n')
    print(empty_input_warning)
    print ('\n')
    key_word = input(instruction_enter_token)

print ('\n')
field = input(instruction_enter_field)

if len(field) == 0:  
    field = "FORM"
    print ('Default search field: FORM')
elif field == 'form':
    field = 'FORM'
    print ('search field: FORM')
elif field == 'lemma':
    field = 'LEMMA'
    print ('search field: LEMMA')
elif field == 'LEMMA':
    print ('search field: LEMMA')
else:
    filed = "FORM"
    print ('The program cannot recognize this input. use default search field: FORM')

print ('\n')
print (instruction_token+'\n')

kw_postag_restriction = input(instruction_POSTAG_token)


if len(kw_postag_restriction)==0:
    kw_postag_restriction = '*'

if kw_postag_restriction != '*' and kw_postag_restriction not in set_POSTAG:
    print ("The program cannot recognize this input. Will use default value\'*\'(i.e. ANY VALUE).")
    kw_postag_restriction = '*'

print ('\n')
kw_deprel_restriction = input(instruction_DEPREL_token)

if len(kw_deprel_restriction)==0:
    kw_deprel_restriction = '*'

if kw_deprel_restriction != '*' and kw_deprel_restriction not in set_DEPREL:
    print ("The program cannot recognize this input. Will use default value\'*\'(i.e. ANY VALUE).")
    kw_deprel_restriction = '*'

print ('\n')
pos_tag = input (instruction_POSTAG_co)


if len(pos_tag)==0:
    pos_tag = '*'

if pos_tag != '*' and pos_tag not in set_POSTAG:
    print ("The program cannot recognize this input. Will use default value\'*\'(i.e. ANY VALUE).")
    pos_tag = '*'
    
print ('\n')
deprel = input (instruction_DEPREL_co)
 
if len(deprel) ==0:
    deprel = '*'

if deprel!='*' and deprel not in set_DEPREL:
    print ("The program cannot recognize this input. Will use default value\'*\'(i.e. ANY VALUE).")
    deprel = '*'

print ('\n')    
output_file_name = input("Plase enter the file path of the output file. \nIf only given a name, the output file will be put in the current working directory.\nOUTPUT NAME:")

if output_file_name == '':
    
    output_file_name = key_word+'_search'+str(random.random()*1000000)[:6]+'.csv'
    print ("The program did not detect any output name. A name is randomly generated :"+output_file_name)
    
elif output_file_name[-4:] != '.csv':
    
    output_file_name += '.csv'

f = open(file_name,encoding='ISO-8859-1')

reader = csv.reader(f,delimiter='\t')

data = [r for r in reader]

all_sents = sentence_division(data)

queried_list=query_the_table(all_sents,key_word,field, pos_tag,deprel, _tok_postag_=kw_postag_restriction,_tok_deprel_=kw_deprel_restriction)       

print_result(queried_list)

output_file(queried_list,output_file_name)
#%%

