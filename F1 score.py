#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install bert_score')


# In[2]:


import bert_score
bert_score.__version__


# In[3]:


import logging
import transformers
transformers.tokenization_utils.logger.setLevel(logging.ERROR)
transformers.configuration_utils.logger.setLevel(logging.ERROR)
transformers.modeling_utils.logger.setLevel(logging.ERROR)


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["xtick.major.size"] = 0
rcParams["xtick.minor.size"] = 0
rcParams["ytick.major.size"] = 0
rcParams["ytick.minor.size"] = 0

rcParams["axes.labelsize"] = "large"
rcParams["axes.axisbelow"] = True
rcParams["axes.grid"] = True


# In[5]:


from bert_score import score


# In[6]:


with open("C:/Users/zhuwe/Desktop/CV/learning materials/SQL/CRA/Azure/generated.txt") as f:
    cands = [line.strip() for line in f]

with open("C:/Users/zhuwe/Desktop/CV/learning materials/SQL/CRA/Azure/groundtruth.txt") as f:
    refs = [line.strip() for line in f]


# In[7]:


cands[0]


# In[8]:


P, R, F1 = score(cands, refs, lang='en', verbose=True)


# In[9]:


F1


# In[10]:


print(f"System level F1 score: {F1.mean():.3f}")


# In[11]:


P


# In[12]:


print(f"System level Precision score: {P.mean():.3f}")


# In[13]:


R


# In[14]:


print(f"System level Recall score: {R.mean():.3f}")


# In[ ]:




