from pyresparser import ResumeParser
from flask import Flask,render_template,redirect,request
from PyPDF2 import PdfReader,PdfWriter
import numpy as np
import pandas as pd
import re
from ftfy import fix_text
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from os.path import relpath
import spacy 
nlp = spacy.load('en_core_web_sm')
from json import loads, dumps


stopw  = set(stopwords.words('english'))

df1 =pd.read_csv('dice_com-job_us_sample.csv')
df1['test'] =df1['skills'].apply(lambda x: ' '.join([word for word in str(x).split() if len(word)>2 and word not in (stopw)]))
def submit_data(files):
        try:
            reader  = PdfReader(files)
            page = reader.pages[0]
            text = page.extract_text()
            lines = [text]

            with open('textresume.txt','w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line)
                    f.write('\n')
                    
            
        except Exception as e:
            print(e)

        try:
            data = ResumeParser(files).get_extracted_data()
            # data = ResumeParser.read_file('textresume.txt')
            print("Data Extracted : ", data)
        except Exception as e:
            print(str(e))
        # print(data)
        if data['skills']:
          resume=data['skills'] 
          print(type(resume))  
          skills=[]
          skills.append(' '.join(word for word in resume))
          org_name_clean = skills
        
        def ngrams(string, n=3):
            string = fix_text(string) # fix text
            string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
            string = string.lower()
            chars_to_remove = [")","(",".","|","[","]","{","}","'"]
            rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
            string = re.sub(rx, '', string)
            string = string.replace('&', 'and')
            string = string.replace(',', ' ')
            string = string.replace('-', ' ')
            string = string.title() # normalise case - capital at start of each word
            string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
            string = ' '+ string +' ' # pad names for ngrams...
            string = re.sub(r'[,-./]|\sBD',r'', string)
            ngrams = zip(*[string[i:] for i in range(n)])
            return [''.join(ngram) for ngram in ngrams]
        vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase=False)
        tfidf = vectorizer.fit_transform(org_name_clean)
        print('Vecorizing completed...')
        

        nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)
        test = (df1['test'].values.astype('U'))
        
        def getNearestN(query):
          queryTFIDF_ = vectorizer.transform(query)
          distances, indices = nbrs.kneighbors(queryTFIDF_)
          return distances, indices
        
        distances, indices = getNearestN(test)
        test = list(test)
        matches = []

        for i,j in enumerate(indices):
          dist=round(distances[i][0],2)
  
          temp = [dist]
          matches.append(temp)
    
        matches = pd.DataFrame(matches, columns=['Match confidence'])
        df1['match']=matches['Match confidence']
        df=df1.sort_values('match',ascending=False)
        df2 = df[['company','employmenttype_jobstatus','jobtitle','skills','jobdescription','joblocation_address','advertiserurl']].head(30)
        
        res  = df2.to_json(orient="split")
        parsed = loads(res)
        res = dumps(parsed, indent=4)
        return res