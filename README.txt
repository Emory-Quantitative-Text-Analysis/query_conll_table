@by Jian Chen
@version: beta 1.0 
@date: 2018-10-11

@remark: INCOMPLETE

This python routing will search all the tokens, which are related to a user-selected keyword (found in Form or Lemma in the conll table).In output it will create a tab-seperated csv file with a user-supplied name.It will also display the same infomation in the command line.

It takes one command line argument: file_path.

The argument 'file_path' is the path of the conll table that the user wish to look at.

####################################################

The program takes seven command line input:

@key_word: the token to be searched. e.g., 'father'

@field: 'FORM' or 'LEMMA', DEFAULT: 'FORM'.
		 In the case of 'FORM', the program will search the column 'FORM' of the table to find matchings. For example, if you search 'come', the program will look for all words with the form 'come' and find the co-occuring words of them. 

		 In the case of 'LEMMA', the program will search the column 'LEMMA' of the table to find matchings. In this case, if you search 'come', the program will be able to find words whose lemma is 'come'. As a result, the tokens with the form 'came' and 'coming' as well as 'come' would be found. The program will then search the co-occuring words of them. If you put 'friend', result from the tokens with form 'friends' will show up.  

@kw_postag_restriction: some part of speech tag (IN CAPITAL), DEFALT '*' (ANYTHING)

		 The program contains a list of all postags(which may be incomplete). If the program did not find a match of the input(i.e., input not in the right form, wrong input, etc.), it will use the default value '*'.

		 This input is a filter on the input word. If you put 'NN', with 
		 @key_word = 'gay' and @field='FORM' then the program will only look at the word 'gay' as a singular nown. 

		 Then, the program will find the co-occuring words of these tokens. 

@kw_deprel_restriction: some dependency relation (deprel) from 'Universal Dependency Relations'

		The program contains a list of incomplete deprel tags.If the program did not find a match of the input(i.e., input not in the right form, wrong input, etc.), it will use the default value '*'.

		This input is a filter on the input word.


@pos_tag: some part of speech tag (IN CAPITAL), DEFALT '*' (ANYTHING)

		 The program contains a list of all postags(which may be incomplete). If the program did not find a match of the input(i.e., input not in the right form, wrong input, etc.), it will use the default value '*'.

		 This input is a filter on the output tokens (i.e., co-occuring words). If you put 'NN', with @key_word = 'gay', @kw_postag_restriction = '*', the program will find all tokens with the keyword 'gay', regardless of its part of speech tag. Then, the program will only find the co-occuring words with POSTAG 'NN'.

@deprel:

@output_file_name:

#######################################################

The output file contains seven column:

@FORM:

@POSTAG:

@DEPREL:

@Dependency Relation

@is_HEAD: value '1' or '0'

		In case of 1, the token is the head of the input @key_word.
		
		For example, if @key_word = 'come', there is a result entry as following.

		Choosing	VBG	csubj	clausal subject	1	9	10

		This means that in the dependency tree of article 9 sentence 10, 'Choosing' is the head of 'come'.

		In case of 0, the input keyword is the head of this token.

		For example, if @key_word = 'come', there is a result entry as following.

		out	RP	compound:prt	phrasal verb particle	0	9	10

		This means that in the dependency tree of article 9 sentence 10, 'come' is the head of 'out'.


@ARTICLE-ID

@SENTENCE-ID


