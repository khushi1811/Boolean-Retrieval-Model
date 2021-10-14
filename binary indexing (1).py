#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize


# In[3]:


nltk.download_shell()


# In[2]:


import nltk
nltk.download('averaged_perceptron_tagger')


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


# In[7]:


from nltk.tokenize import RegexpTokenizer
corpus_words = []
tokenizer = RegexpTokenizer(r'\w+')
# Tokenize a paragraph into sentences and each sentence in to
# words
for c in corpusfin:
    word_tokens = tokenizer.tokenize(c)
    corpus_words.append(word_tokens)

len(corpus_words)


# In[8]:


print(corpus_words)


# In[9]:


corpuslower_words = []
tokenizer = RegexpTokenizer(r'\w+')
# Tokenize a paragraph into sentences and each sentence in to
# words

for corpus_word in corpus_words:
    word_tokens1 = set([ x.lower() for x in corpus_word])
    corpuslower_words.append(word_tokens1)

len(corpuslower_words)


# In[10]:


print(corpuslower_words)


# In[11]:


def positional_index(tokens):
    d = defaultdict(lambda:[])
    for docID, sub_l in enumerate(tokens):
        for t in set(sub_l):
            d[t].append([docID] + [ind for ind, ele in enumerate(sub_l) if ele == t])
    return d


# In[12]:


index=  positional_index(corpuslower_words)
index["pretend"]



# In[13]:


index["hagrid"]


# In[28]:


def biwords(corpus_words):
    bilist=[]
    types= nltk.pos_tag(corpus_words) #saving the positional tags of the list of strings passed
    x= len(types) 
    for ttuple in types:
        #print(ttuple[1])
        bilist.append(ttuple[1]) # adding only the tags to other list
    return bilist


# In[29]:


tip= biwords(corpus_words[1])
print(tip)


# In[30]:


print(len(corpusfin))


# In[34]:


def biwordindex(t,corpus_words): 
    bind=[]
    for val in t:
        if (val =='NN' or val == 'NNS' or val == 'NNPS' or val == 'NNP'):
            #print("ifnoun")
            index= t.index(val)
            temp= corpus_words[index]
            #bind.append(temp)
            val2= t[index+1]
            term2=corpus_words[index+1]
            if(val2 =='NN' or val2 == 'NNS' or val2 == 'NNPS' or val2 == 'NNP'):
                temp= temp+" "+term2
                bind.append(temp)
                continue
            elif (val2=='DT' or val2=='IN'):
                temp= temp+" "+term2
                val3=t[index+2]
                term3=corpus_words[index+2]
                if(val3 =='NN' or val3 == 'NNS' or val3 == 'NNPS' or val3 == 'NNP'):
                    temp= temp+" "+term3   
                    bind.append(temp)
                    continue
                else:    
                    while(val3=='DT' or val3=='IN'):
                        term4=corpus_words[index+2]
                        nextval=t[index+2]
                        temp= temp+" "+term3
                        index +=1
                        if(nextval =='NN' or nextval == 'NNS' or nextval == 'NNPS' or nextval == 'NNP'):
                            temp= temp+" "+term4
                            bind.append(temp)
                            break
    return bind


# In[54]:


bind = biwordindex(tip,corpus_words[10])
print(bind)


# In[51]:


bindex=[]
for corpus_word in corpus_words:
    t= biwords(corpus_word)
    bind = biwordindex(t,corpus_word)
    bindex.append(bind)
bindexfin=[]   
for bini in bindex:
    binif= list(set(bini))
    bindexfin.append(binif)


    


# In[52]:


print(bindexfin)


# In[72]:


query= input("Enter the phrase to be searched:")
print("Your query is:", query)


# In[73]:


flag= False
for ele in bindexfin:
    for i in ele:
        if i==query:
            print("Your phrase is in document number", bindexfin.index(ele))
            flag= True
            
if(flag==False):
    print("No match found")


# In[ ]:




