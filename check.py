# coding=utf-8
"""Grammar Checker in Python 3; see http://norvig.com/spell-correct.html

Copyright (c) 2019-2019 Jason S. Chang
MIT license: www.opensource.org/licenses/mit-license.php
"""

import re, json, operator, sys, urllib, requests, string
import numpy as np
from collections import Counter
from math import log10, log
import copy as cp


# model path


# linggle api url
#NGRAM_API_URI = "https://{0}.linggle.com/query/"
#EXP_API_URI = "https://{0}.linggle.com/example/"

NGRAM_API_URI = "https://www.linggle.com/query/"

# 設定最大可分析長度
max_len = 5

punc = [i for i in string.punctuation]
alf=['a','b','c','d','e','f','g','h','i','j','k','l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z']


###################
# Linggle api 
###################
class Linggle:
	def __init__(self, ver='www'):
		self.ver = ver
        
	def __getitem__(self, query):
		return self.search(query)
    
	def search(self, query):
		query = query.replace('/', '@')
		query = urllib.parse.quote(query, safe='')
		req = requests.get(NGRAM_API_URI.format(self.ver) + query)
		results = req.json()
		return  results.get("ngrams", [])
    
	def get_example(self, ngram_str):
		res = requests.post(EXP_API_URI.format(self.ver), json={'ngram': ngram_str})
		if res.status_code == 200:
			result = res.json()
			return result.get("examples", [])
		return []


# 開linggle api
ling = Linggle(NGRAM_API_URI)


#####################
# Ngram probability #
#####################
def P(ngram, logN=12., MINCOUNT=40.): 
	"Probability of ngram based Web 1T using Linggle API"
	ngram, leng = ' '.join(ngram), float(len(ngram))
	# 查詢次數
	linggle_ngram = ling.search(ngram)
	linggle_ngram = linggle_ngram[0][1] if len(linggle_ngram)>0 else 0
	return (log(linggle_ngram,10)-12)/pow(leng,1./2.5) if linggle_ngram>0 else (log10(MINCOUNT)-12)


##############################################
# 編輯(Insert, Delete, Replace)一步之後的結果
#Edit (Insert, Delete, Replace) results after one step
##############################################
def edits1(ngram, model):
    "TODO: handle possible Insert, Delete, Replace edits using data from model"
    words=[[ngram[x],x] for x in range(len(ngram)) if channel_model(ngram[x],model) ]
    sentences=[ngram]
    verb=find_verb(ngram)
    for i in range(len(words)):
        
        problem_word=cp.copy(words[i][0]) 
       # ngram.index(model[problem_word][x][1])   words[i][1]
        deletes=[ngram[:words[i][1]+model[problem_word][x][2]] +  ngram[words[i][1] +1+ model[problem_word][x][2]:] for x  in range(len(model[problem_word])) if model[problem_word][x][1] in ngram and model[problem_word][x][0]=='D']
        for i1 in range(len(deletes)):
            #if len(deletes[i])>0:
               if verb in deletes[i1]:# i=0
                  sentences.append(deletes[i1])
            
        inserts=[ngram[:words[i][1]+model[problem_word][x][2]] + [model[problem_word][x][1]]+ngram[words[i][1] + model[problem_word][x][2] :]   for x  in range(len(model[problem_word])) if model[problem_word][x][0]=='I' ]
        for i1 in range(len(inserts)):
          #  if len(sentences[i])>0:
            if problem_word in inserts[i1]:# i=0
               sentences.append(inserts[i1])
            
        replaces=[ngram[:ngram.index(model[problem_word][x][1])] + [model[problem_word][x][2]] + ngram[ngram.index(model[problem_word][x][1])+1:]  for x  in range(len(model[problem_word])) if model[problem_word][x][0]=='R' and model[problem_word][x][1] in ngram ] 
        for i1 in range(len(replaces)):
            if verb in replaces[i1]:
               sentences.append(replaces[i1])
          
    return sentences   

##########################
# 編輯兩步之後的結果 ngram =input_string
# Edit the results after two steps
##########################
def edits2(ngram, model): 
	#"All changes that are two edits away from ngram"
    return [edits1(ngram[x], model) for x in range(len(ngram))]        


def find_verb(ngram):
    subjects=['i','you','he', 'she', 'we', 'they'] 
    prepositions=['for','from','in','of', 'on', 'to', 'with','about','at','the','more','and','must','just','might','also','really','still',
                  'never', 'only','ever','always','not','now','first','already','the','even','or','all','finally','probably','so','then']
    ngram=[ngram[i] for i in range(len(ngram)) if ngram[i] not in prepositions ]
    return ngram[np.argmax([np.sum([ P([subjects[x]]+ [ngram[i]]) for x in range(len(subjects)) if ngram[1] not in prepositions ])  for i in range(len(ngram))])]

#############################
# edit 2次之後的 candidates
# edit 2 after the candidate
#############################
def candidates(ngram, model): 
	#"TODO: Generate possible correction"
    ranking=[]
    probabilities= [P(ngram[x]) for x in range(len(ngram))]
    prob=cp.copy(probabilities)
    for i in range(len(ngram)):
      x=np.argmax(probabilities)
      ranking.append(x)
      probabilities[x]=-10000
    top_candidates=[ngram[ranking[x]] for x in range(len(ranking))]
    return top_candidates, [ prob[ranking[x]] for x in range(len(ranking))]
     #return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])


###############################
# 找最好的編輯
# Find the best editor
###############################
def correction(ngram, model): 
	#"TODO: Return most probable grammatical error correction for ngram."
    assert len(ngram)<6
    
    sas=edits1(ngram, model)
    sa2=edits2(sas,model)
    
    for v in range(len(sa2)):
        [sas.append(sa2[v][x]) for x in range(len(sa2[v])) if len(sa2[v][x])<7 and len(sa2[v][x][0])+len(sa2[v][x][1])>2  ] # the last one removes 1 word answers 
      
    Results=candidates(sas, model)  # All the cadidate results are stored here
    winner=' '.join(Results[0][0])
    print('The best correction is:')
    print(winner)
    return winner#,Results 

################################
# 找出problem word有沒有在model裡
# Find the problem word is in the model
################################
def channel_model(problem_word, model):
	return model[problem_word] if(problem_word in model) else []



##############################
# 把model json檔獨進來
# Invent the model JSON party alone
##############################
problem_word_path ='model.txt'    
path=problem_word_path    
f=open(path, 'r')

def read_problem_word(path):
	with open(path, 'r') as f:
		model = json.load(f)
	return model

#################
# MAIN
#################
if __name__ == '__main__':
	# 讀進problem_word
   model = read_problem_word(problem_word_path)
   #model=json.load(open('model.txt')) 
   with open('input.txt') as f:
         text = (f.read()).split('\n')
   with  open("Results.txt","w")  as file1:    
         for i in range(len(text)):
             print('\n')
             print(i)
             print('\nThe sentence to be corrected is :')
             print(text[i])
             input_string=text[i].split(' ')
             
             sentence=correction(input_string, model) 


#TODO: Read testing data, write correction to output file"


             
           
             writes=' '.join(sentence.split(" ")+ ['\n'])
       #write mode 
             file1.write(writes) 
       
         


































