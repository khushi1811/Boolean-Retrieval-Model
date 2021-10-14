#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize


# In[22]:


nltk.download_shell()


# In[2]:


import nltk
nltk.download('wordnet')


# In[3]:


import os

file_location = os.path.join('InformationRetrieval', '*.txt')
print(file_location)


# In[4]:


import glob
filenames = glob.glob(file_location)
print(filenames)


# In[5]:


corpusfin=[]
for f in filenames:
    file = open(f,"r",encoding='utf-8' ,errors='ignore')
    line = file.read().replace("\n", " ")
    corpusfin.append(line)
    file.close()


# In[6]:


print(len(corpusfin))
#prints the length of corpusfin


# In[7]:


from nltk.tokenize import RegexpTokenizer
corpus_words = []
tokenizer = RegexpTokenizer(r'\w+')
# Tokenize a paragraph into sentences and each sentence in to
# words
for c in corpusfin:
    word_tokens = tokenizer.tokenize(c)
    corpus_words += word_tokens

len(corpus_words)
#prints the length of corpus words


# In[8]:


print(corpus_words)

#prints the list of corpus words


# In[9]:


corpus_words.index('Professor'), corpus_words.index('Professor')
#gives the index of the word Professor


# In[10]:


lower_corpus_words = set([ x.lower() for x in corpus_words ])
len(lower_corpus_words)
#converts corpus wods into lower case


# In[11]:


# Remove the stopwords
from nltk.corpus import stopwords

stwords = set(stopwords.words('english'))

# Using set difference to eliminate stopwords from our words
stopfree_words = lower_corpus_words - stwords
len(stopfree_words)
# gives length of stopwords
    
    


# In[12]:


#Stemming
from nltk.stem import snowball

stemmer = snowball.SnowballStemmer('english')
stemmed_words = set([stemmer.stem(x) for x in stopfree_words])
#stems the stopfree_words and makes a list called stemmed_words
len(stemmed_words)
#gives length of stemmed list


# In[13]:


list(stemmed_words)[-100:]
#prints the stemmed list


# In[14]:


#imports WordNetLemmatizer package to lemmatize stopfree_words and save it in list lemm_words
from nltk.stem import WordNetLemmatizer
  
lemmatizer = WordNetLemmatizer()
lemm_words = set([lemmatizer.lemmatize(x) for x in stopfree_words])

len(lemm_words)
#gives length of lemm_words


# In[15]:


list(lemm_words)[-100:]
#prints list of lemm_words


# In[16]:


#Inverted Index Function
inverted_index = defaultdict(set)

for docid, c in enumerate(corpusfin):
    for sent in sent_tokenize(c):
        for word in word_tokenize(sent):
            word_lower = word.lower()
            if word_lower not in stwords:
                word_lemm =lemmatizer.lemmatize(word_lower)
                # We add the document to the set againt the word in our
                # index
                inverted_index[word_lemm].add(docid)

len(inverted_index.keys())
#prints length of keys of inverted_index dictionary


# In[17]:


#function to find inverted index of a particular token
def process_and_search(query):
    matched_documents = set() 
    for word in word_tokenize(query):
        word_lower = word.lower()
        if word_lower not in stwords:
            word_stem = stemmer.stem(word_lower)
            matches = inverted_index.get(word_stem)
            if matches:
                # The operator |= is a short hand for set union
                matched_documents |= matches
    return matched_documents


# In[18]:


process_and_search("professor")


# In[19]:


#AND function
def AND(posting1, posting2):
    p1 = 0
    p2 = 0
    result = list() #result is saved in the form of an empty list
    while p1 < len(posting1) and p2 < len(posting2):
        if posting1[p1] == posting2[p2]:
            result.append(posting1[p1])
            p1 += 1
            p2 += 1
        elif posting1[p1] > posting2[p2]:
            p2 += 1
        else:
            p1 += 1
    return result


# In[20]:


#OR function
def OR(posting1, posting2):
    p1 = 0
    p2 = 0
    result = list()
    while p1 < len(posting1) and p2 < len(posting2):
        if posting1[p1] == posting2[p2]:
            result.append(posting1[p1])
            p1 += 1
            p2 += 1
        elif posting1[p1] > posting2[p2]:
            result.append(posting2[p2])
            p2 += 1
        else:
            result.append(posting1[p1])
            p1 += 1
    while p1 < len(posting1):
        result.append(posting1[p1])
        p1 += 1
    while p2 < len(posting2):
        result.append(posting2[p2])
        p2 += 1
    return result


# In[21]:


#NOT function
def NOT(posting):
    result = list()
    i = 0
    for item in posting:
        while i < item:
            result.append(i)
            i += 1
        else:
            i += 1
    else:
        while i < len(corpusfin):
            result.append(i)
            i += 1
    return result


# In[22]:


p1_1= list(process_and_search("professor"))
p1_2= list(process_and_search("hagrid"))
#searches and saves inverted index list of tokens professor and hagrid in p1_1 and p1_2 respectively


# In[23]:


result= NOT(p1_1)


# In[24]:


print(result)


# In[25]:


print(stemmed_words)


# In[26]:


p1_1= list(process_and_search("faint"))
p1_2= list(process_and_search("midnight"))
#searches and saves inverted index list of tokens faint and midnight in p1_1 and p1_2 respectively
result= OR(p1_1,p1_2)
#OR function call
print(result)


# In[27]:


print(lemm_words)


# In[28]:


def _parse_query(infix_tokens):#parsing the query 
        precedence = {}#setting the precedence
        precedence['NOT'] = 3
        precedence['AND'] = 2
        precedence['OR'] = 1
        precedence['('] = 0
        precedence[')'] = 0    

        output = []
        operator_stack = []

        for token in infix_tokens:
            if (token == '('):
                operator_stack.append(token)
            
            elif (token == ')'):
                operator = operator_stack.pop()
                while operator != '(':
                    output.append(operator)
                    operator = operator_stack.pop()
            
            elif (token in precedence):
                # if operator stack is not empty
                if (operator_stack):
                    current_operator = operator_stack[-1]
                    while (operator_stack and precedence[current_operator] > precedence[token]):
                        output.append(operator_stack.pop())
                        if (operator_stack):
                            current_operator = operator_stack[-1]
                operator_stack.append(token) # add token to stack
            else:
                output.append(token.lower())

        while (operator_stack):
            output.append(operator_stack.pop())

        return output


# In[29]:


import collections

def process_query( query):
        # prepare query list and break it into words
        query = query.replace('(', '( ')
        query = query.replace(')', ' )')
        query = query.split(' ')

        indexed_docIDs = list(range(1, len(corpusfin) + 1))

        results_stack = []
        postfix_queue = collections.deque(_parse_query(query)) # get query in postfix notation 

        while postfix_queue:
            token = postfix_queue.popleft()
            result = [] 
            if (token != 'AND' and token != 'OR' and token != 'NOT'):
                token = stemmer.stem(token) # stem the token
                # default empty list if not in dictionary
                if (token in inverted_index):
                    result = list(process_and_search(token))
            
            elif (token == 'AND'):
                right_operand = results_stack.pop()
                left_operand = results_stack.pop()
                result = AND(left_operand, right_operand)  

            elif (token == 'OR'):
                right_operand = results_stack.pop()
                left_operand = results_stack.pop()
                result = OR(left_operand, right_operand)    

            elif (token == 'NOT'):
                right_operand = results_stack.pop()
                result = NOT(right_operand) 
            results_stack.append(result)                        

        if len(results_stack) != 1: 
            print("ERROR: Invalid Query. Please check query syntax.") 
            return None
        
        return results_stack.pop()


# In[30]:


p1_1= list(process_and_search("came"))
p1_2= list(process_and_search("wanted"))
p1_3= list(process_and_search("anthing"))
p1_4= list(process_and_search("think"))
result= (OR(AND(p1_1,p1_2),p1_4))
print(result)


# In[31]:


query= input("Enter your query:")
print("Your query is:", query)


# In[32]:


res= process_query(query)


# In[33]:


print(res)


# In[ ]:




