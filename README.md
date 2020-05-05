# Personalized Local Resources Search Engine

## Motivation:
Throughout the COVID-19 pandemic, local resources have shifted in scope and availability. Consumers’ needs have also changed. Grocery stores are operating at reduced hours, businesses are offering increased delivery services, and shoppers’ habits have evolved due to newly established stay-at-home orders. All of this new and dynamic information is difficult to keep track of and not always straightforward to find.


## Goal:
- Our goal is to crawl, aggregate, and index information and updates from local resources/businesses in Baltimore and report on what is available.
  - To achieve this, we will build a search engine to retrieve information that is relevant to queries in this domain and is personalized to the user needs.
  - If time allows, we will use user-embeddings to capture the specific needs of a user.


## Datasets:
- Our retrieval engine will focus on scraping data from unstructured sources such as:
  - News articles (Baltimore Sun, CBS Baltimore, etc.)
  - Business/Company websites (CVS, Giant Foods, etc.)
  - FAQs (JHU HUB, JHU Newsletter, etc.)
- Compiled list of webpages for initial proof of concept, which can be found [here](https://docs.google.com/spreadsheets/d/1lw6fKY5JoMut-U1w-uCL6YN6VV_qd6RsKVaMCLCd0v8/edit?usp=sharing).

## Approach:
- **Web crawling and scraping**
  - Scrape a set of websites to create a corpus of documents
- **Preprocessing**
  - **Structured:** Stemming and Stop Words Removal
  - **Unstructured:** Acronyms, Emoticons, Spell Check, Contractions, Hashtags
- **Vectorization and Scoring**
  - TF-IDF, Word/Sentence embeddings (Word2Vec, GloVe, BERT, ELMo)
  - Cosine, Dice, Jaccard or anything from scipy.spatial.distance.
- **Query Optimization**
  - Personalize user queries based on usr2vec and rocchio relevance feedback

## Outcomes:
- Personalized search engine for the resources local to Baltimore.
- Web scraper for popular Baltimore news/business websites.
- Find the best
  - Word/sentence embedding
  - Way to personalize any query
  - Way to handle unstructured text

## Running instructions:

To run the basic search engine, use the following command, and type your query once the search engine is initialized.
```
$ python deploy.py
```

### Command line arguments
- `--user_profile`: Runs the search engine with mimicked user personalization (biased query results). _Example:_
```
$ python deploy.py --user_profile "<enter terms here>"
OR
$ python deploy.py --user_profile "cvs"
```
  - **Note:** the `user_profile` basically describes the current user's profile, search history and what type of content the user is biased towards.
- `--embedding`: Chooses the word embedding method to use. Choose from: `["one-hot", "word2vec-google-news-300", "glove-twitter-100", "glove-wiki-gigaword-100", "glove-wiki-gigaword-200", "fasttext-wiki-news-subwords-300"]`. _Example:_
```
$ python deploy.py --embedding "one-hot"
```
- `--weighting_scheme`: Chooses the weighting scheme to use for computing document vectors from word vectors. Choose from: `["mean", "tf-idf", "sif", "usif"]`. _Example:_
```
$ python deploy.py --weighting_scheme "tf-idf"
```
- `--top_k`: Number of results to return for each query. _Example:_
```
$ python deploy.py --top_k 25
```
