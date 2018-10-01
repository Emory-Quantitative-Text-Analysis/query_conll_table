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
#%%
import csv
import sys
import os

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
            

def search_related_words(desired_form, sentence):
    
    list_indices_related_word = []
    
    for token in sentence:
        
        token_form = token[1]
        
        token_id = token[0]
        
        if token_form == desired_form:
            
            head, head_num = search_head(token_id,sentence)
            
            if head != "NO_HEAD":
                
               list_indices_related_word.append(head_num)
               
               
            #print (find_children(sentence,int(token_id)))
            
            for child in find_children(sentence,int(token_id))[1]:
                
                list_indices_related_word.append(child)
               # print ("children")
    
    return list_indices_related_word

#print ()

#%%
"""
1. return the list of tokens related to the word
"""
def query_the_table(list_sentences, form_of_token, pos_tag = "*",dep_relation="*",sentence_id="*"):
    
    list_queried = []
    
    for sent in list_sentences:
        
        #search form-->search lemma? stem
        
        #first, search the form
        list_word_indices = search_related_words(form_of_token,sent)
        
        for ind in list_word_indices:
            
            row = sent[int(ind)-1]
            
            tok_form = row[1]
            
            tok_postag = row[3]
            
            tok_deprel = row[6]
            
            list_queried.append((tok_form,tok_postag,tok_deprel))

    if pos_tag == "*" and dep_relation == "*" and sentence_id == "*":
        
        return list_queried
    
    
   # postag_list_queried = list_queried
    
    if "*" not in pos_tag:
        
        postag_list_queried = list(filter(lambda tok:tok[1]==pos_tag,list_queried))
        
    elif pos_tag == "NN*":
        
        postag_list_queried = list(filter(lambda tok:tok[1] in ['NN','NNS','NNP','NNPS'],list_queried))
        
    else:
        
        postag_list_queried = list_queried
    
    #deprel_list_queried = postag_list_queried
    
    if "*" not in dep_relation:
        
        deprel_list_queried = list(filter(lambda tok:tok[2]==dep_relation,postag_list_queried))
    
    else:
        
        deprel_list_queried = postag_list_queried
    
    
    return deprel_list_queried

#%%

def print_result(list_queried):
    
    for item in list_queried:
        
        print (item[0],item[1],item[2])


#%%
def usage():
    
    print("Please put this file in the same directory as the conll table.\n"\
          "Type the following command\n"
          "python3 query_conll.py [filepath_of_conill_table] [keyword] [pos_tag] [deprel]\n"\
          "EXAMPLE:\n\n"
          "python3 query_conll.py come NN dobj\n\n"
          "This command will print all the token related to \"come\", with postag == \"NN\" and deprel=\"amod\""
          )

#%%
"""

Main program

"""    
if len(sys.argv)<3:
    usage()
else:
    file_path = sys.argv[1]
    key_word = sys.argv[2]

    if len(sys.argv)==3:
        pos_tag = "*"
        deprel = "*"
    elif len(sys.argv)==4: 
        pos_tag = sys.argv[3]
        deprel = "*"
    else:
        pos_tag = sys.argv[3]
        deprel = sys.argv[4]

file_name = file_path

f = open(file_name,encoding='ISO-8859-1')

reader = csv.reader(f,delimiter='\t')

data = [r for r in reader]
#sentence_0 = data[:25]
all_sents = sentence_division(data)

queried_list=query_the_table(all_sents, key_word, pos_tag,deprel)       

print_result(queried_list)
#%%
"""
1. if the noun is 
2. find a way to group "come out" together, search for a more general way
"""

    
