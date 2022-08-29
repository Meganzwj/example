#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spacy
nlp = spacy.load("en_core_web_sm")


# In[3]:


with open ("C:/Users/zhuwe/Desktop/CV/learning materials/SQL/CRA/Azure/groundtruth.txt","r") as f:
    text=f.read()
    print (text)


# In[4]:


with open ("C:/Users/zhuwe/Desktop/CV/learning materials/SQL/CRA/Azure/generated.txt","r") as g:
    text1=g.read()
    print (text1)


# In[5]:


doc =nlp(text)
doc1 =nlp(text1)


# In[6]:


doc.similarity(doc1)


# In[7]:


doc1.similarity(doc)


# In[ ]:


##output [6] and output [7]: 0.9707215035869386

