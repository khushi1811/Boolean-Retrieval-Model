#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize


# In[2]:


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


from nltk.tokenize import RegexpTokenizer
corpus_words = []
tokenizer = RegexpTokenizer(r'\w+')
# Tokenize a paragraph into sentences and each sentence in to
# words
for c in corpusfin:
    word_tokens = tokenizer.tokenize(c)
    corpus_words.append(word_tokens)

len(corpus_words)


# In[7]:


print(corpus_words)


# In[8]:


corpuslower_words = []
tokenizer = RegexpTokenizer(r'\w+')
# Tokenize a paragraph into sentences and each sentence in to
# words

for corpus_word in corpus_words:
    word_tokens1 = set([ x.lower() for x in corpus_word])
    corpuslower_words.append(word_tokens1)

len(corpuslower_words)


# In[9]:


print(corpus_words)


# In[10]:


#Positional Index code
def positional_index(tokens):
    d = defaultdict(lambda:[])
    for docID, sub_l in enumerate(tokens):
        for t in set(sub_l):
            d[t].append([docID] + [ind for ind, ele in enumerate(sub_l) if ele == t])
    return d


# In[11]:


index=  positional_index(corpus_words)
print(index)
#prints positional index dict


# In[12]:


index["The"]
#gives positional index of After


# In[14]:


index["Lived"]
#gives positional index of all


# In[17]:


#runs two pointers to check within positional index of both terms to find the document in which the two terms
#are present at certain difference
def positional_index_query(index1, index2, diff):
    i=1
    j = 1
    
    if(len(index1) <= len(index2)):
        for term in index1:
            for term1 in index2:
                if(term[0] == term1[0]):
                    if(len(term) <= len(term1)):
                        while i < len(term):
                            while j < len(term1):
                                if(term[i] == term1[j] - diff):
                                    print("HELLO1")
                                    print("The phrase is found at DocID:",term[0], "and at positions:", term[i]," and " ,term1[j])
                                    break
                                else:
                                    j+=1
                            i+=1     
                                
                        
                    elif(len(term) > len(term1)):
                        while i < len(term1):
                            while j < len(term):
                                if(term[j] == term1[i] - diff):
                                    print("HELLO2")
                                    print("The phrase is found at DocID:",term[0], "and at positions:", term[j]," and " ,term1[i])
                                    break
                                else:
                                    j+=1
        
                        
            
    elif(len(index1) > len(index2)):
        
        for term1 in index2:
            
            for term in index1:
                
                if(term1[0] == term[0]):
                    
                    if(len(term1) <= len(term)):
                        
                        while i < len(term1):
                            
                            while j < len(term):
                                
                                if(term[j] == term1[i] - diff):
                                   
                                    print("HELLO3")
                                    print("The phrase is found at DocID:",term1[0], "and at positions:", term[j]," and " ,term1[i])
                                    break
                                else:
                                    j+=1
                            i+=1        
                                   
                            
                    elif(len(term1) > len(term)):
                        while i < len(term):
                            while j < len(term1):
                                if(term[j] == term1[i] - diff):
                                    print("HELLO4")
                                    print("The phrase is found at DocID:",term1[0], "and at positions:", term[j]," and " ,term1[i])
                                    break
                                else:
                                    j+=1
                            i+=1
                                
           


# In[19]:


index1= index["The"]
index2 = index["Lived"]
positional_index_query(index1, index2,3)


# In[20]:


#Soundex function
# finds out soundex code for a particular token using mapping and soundex rules
def soundex(name):

    soundexcoding = [' ', ' ', ' ', ' ']
    soundexcodingindex = 1

    #           ABCDEFGHIJKLMNOPQRSTUVWXYZ
    mappings = "01230120022455012623010202"

    soundexcoding[0] = name[0].upper()

    for i in range(1, len(name)):

        c = ord(name[i].upper()) - 65

        if c >= 0 and c <= 25:

             if mappings[c] != '0':

                if mappings[c] != soundexcoding[soundexcodingindex-1]:

                    soundexcoding[soundexcodingindex] = mappings[c]
                    soundexcodingindex += 1

                if soundexcodingindex > 3:

                     break

    if soundexcodingindex <= 3:
        while(soundexcodingindex <= 3):
            soundexcoding[soundexcodingindex] = '0'
            soundexcodingindex += 1

    return ''.join(soundexcoding)


# In[21]:


#saves soundex transformed list of lists of all tokens in corpus word and prints the list of lists i.e. soundex_words1
soundex_words = []
soundex_words1 = []
i=0

for corpus_word in corpus_words:
    var = len(corpus_word)
    while(i<var):
        soundex_tokens = soundex(corpus_word[i]) 
        soundex_words.append(soundex_tokens)   
        i+=1
    soundex_words1.append(soundex_words)   
       

print(soundex_words1)        


# In[23]:


#stores similar var as soundex(name)
name = 'Bye'
similar = soundex(name)

count =0
i=0
#iterated the list of list using a nested loop to find out the word with equivalent soundex code and prints count and the word
for soundex_word1 in soundex_words1:
    for soundex_word in soundex_word1:
        if(soundex_word == similar):
            count+=1
            i = soundex_words1.index(soundex_word1)
            j = soundex_words.index(soundex_word)
            soundexlist = corpus_words[i][j]
            
    
print("Your word",name, "resembles the word",soundexlist, "in the documents and has appeared", count, "times")       


# In[319]:





# In[ ]:




