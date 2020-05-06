# Localized and Personalized Search Engine for COVID-19

## Motivation:
Throughout the COVID-19 pandemic, people’s needs have evolved due to a myriad of closures and stay-at-home orders. Local services have had to adapt themselves to this everyday and this information changes at a fast pace. All of this new and dynamic information is difficult to sift through and not always straightforward to find.


## Goal:
- Our goal is to crawl, aggregate, index and search/retrieve information from local news sources in Baltimore and report back relevant and personalized results to the user.
  - To achieve this, we built a search engine to retrieve relevant articles. We expanded our search engine to simulate user personalization based on the user’s profile, which can be mimicked through topics the user is biased towards, that are incorporated as a string of bias terms at run time. This allows us to retrieve results personalized to the user needs.


## Datasets - Evaluation:
To find an appropriate system for real-world data, we considered 4 labelled datasets ([CACM](http://ir.dcs.gla.ac.uk/resources/test_collections/cacm/), [CISI](https://www.kaggle.com/dmaso01dsta/cisi-a-dataset-for-information-retrieval/version/1), [Medline](http://www.trec-cds.org/2017.html), [Cranfield](http://ir.dcs.gla.ac.uk/resources/test_collections/cran/)) and conducted experiments on this data:
- **CACM:** abstracts and queries from Communications of ACM journal
- **CISI:** documents and queries from Centre for Inventions and Scientific Information
- **Medline:** collection of articles and queries from Medline journals
- **Cranfield:** commonly used IR dataset with aerodynamics journals articles, queries, and relevance judgements

## Datasets - Deployment:
- Then, we selected the best performing permutations from evaluation on development data to deploy on our COVID-19 news data.
- We crawled COVID-19 related articles from CBS Baltimore and WBALTV since they provide access to focused local information relevant to Baltimore.
- Note: for now the web scrappers for WBALTV and CBS Baltimore are in the `crawler` branch.

## Approach:
- **Web crawling and scraping**
  - Scrape a set of websites to create a corpus of documents
- **Preprocessing**
  - **Structured:** Stemming and Stop Words Removal
  - **Unstructured:** Acronyms, Emoticons, Spell Check, Contractions
- **Vectorization and Scoring**
  - **Word embeddings:** (Word2Vec, GloVe, FastText, Doc2Vec, OneHot)
  - **Word embeddings to Sentence embeddings Weighting Schemes:** Mean, TF-IDF, Smooth Inverse Frequency, Unsupervised Smooth Inverse Frequency.
  - **Similarity:** Cosine, Dice, Jaccard or anything from scipy.spatial.distance.
- **Query Optimization**
  - Personalize user queries using a modified Rocchio relevance feedback mechanism

## Outcomes:
- Personalized search engine for local Baltimore news.
- Web scraper for popular Baltimore news/business websites.
- Find the best
  - Word/Sentence embedding
  - Ways to personalize any query
  - Ways to handle unstructured text

## Running instructions:

Install all the packages this search engine requires to run using:
```
pip install -r requirements.txt
```

Then, to run the basic search engine, use the following command, and type your query once the search engine is initialized.
```
$ python deploy.py
```

**Command line arguments**

1. `--user_profile`: Runs the search engine with mimicked user personalization (biased query results). _Example:_
  ```
  $ python deploy.py --user_profile "<enter terms here>"
  OR
  $ python deploy.py --user_profile "cvs"
  ```
  **Note:** the `user_profile` basically describes the current user's profile, search history and what type of content the user is biased towards.

2. `--embedding`: Chooses the word embedding method to use. Choose from: `["one-hot", "word2vec-google-news-300", "glove-twitter-100", "glove-wiki-gigaword-100", "glove-wiki-gigaword-200", "fasttext-wiki-news-subwords-300"]`. _Example:_
  ```
  $ python deploy.py --embedding "one-hot"
  ```
3. `--weighting_scheme`: Chooses the weighting scheme to use for computing document vectors from word vectors. Choose from: `["mean", "tf-idf", "sif", "usif"]`. _Example:_
  ```
  $ python deploy.py --weighting_scheme "tf-idf"
  ```
4. `--top_k`: Number of results to return for each query. _Example:_
  ```
  $ python deploy.py --top_k 5
  ```
5. `--expand_query`: Enables query expansion based on GloVe (glove-wiki-gigaword-100). _Example:_
  ```
  $ python deploy.py --expand_query
  ```
