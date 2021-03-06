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
- We crawled COVID-19 related articles from Baltimore Sun, CBS Baltimore, and WBALTV since they provide access to focused local information relevant to Baltimore.
- Note: CBS and WBALTV local news source spiders based on [RISJbot](https://github.com/pmyteh/RISJbot)

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

### Scraping data

1. `$ scrapy crawl <news source>`: Runs the scrapy spider on news site. Choose from: `['cbs', 'wbaltv']`
2. Process the jsonl output into CSV and document-format required by data loader.
  ```
  $ cd data/local_news_data
  $ python process.py
  ```

### Search Engine

Then, to run the basic search engine, use the following command, and type your query once the search engine is initialized. (**Note:** It takes approximately 3-5 mins to initialize the search engine)
```
$ python deploy.py
```

**Command line arguments**

1. `--personalize`: Runs the search engine with mimicked user personalization (biased query results). **Note:** With this mode enabled we need search history, to be able to personalize towards the type of content the user is biased. So, search for terms that show the user's preferences first and then key in your normal queries to see the improved and personalized results. _Example:_
  ```
  $ python deploy.py --personalize
  ```
2. `--embedding`: Chooses the word embedding method to use. **Choose from:** `["one-hot", "word2vec-google-news-300", "glove-twitter-100", "glove-wiki-gigaword-100", "glove-wiki-gigaword-200", "fasttext-wiki-news-subwords-300"]`. _Example:_
  ```
  $ python deploy.py --embedding "one-hot"
  ```
3. `--weighting_scheme`: Chooses the weighting scheme to use for computing document vectors from word vectors. **Choose from:** `["mean", "tf-idf", "sif", "usif"]`. _Example:_
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

## Types of Search Queries to Try:

- **Default**
  - *Command:* `python deploy.py`
  - *Examples:*
    - *General:*
      - "masks"
      - "vaccine"
      - "ventilators"
    - *With mis-spellings*
      - "stayy at homew ordero"
      - "johnss hopoins universitio"
    - *With acronyms or contractions*
      - "JHU"
      - "VP"
      - "ICU"
      - "CDC"
      - "cases last wk"
- **Pretrained Word Embeddings**
  - *Command:* `python deploy.py --embedding "word2vec-google-news-300" --weighting_scheme "usif"`
  - *Effect:* Results capture the semantics of the query
  - *Examples:*
    - "employment"
    - "grocery"
    - "medicine"
- **User Personalization**
  - *Command:* `python deploy.py --personalize`
  - *Effect:* Results are personalized towards the user's biases
  - *Examples:*
    - search for "costco" then "social distancing" AND just "social distancing" in a fresh session
    - search for "sports" then "lakers" AND just "lakers" in a fresh session
- **Query Expansion**
  - *Command:* `python deploy.py --expand_query`
  - *Effect:* Gives more concentrated and meaningful results that talk about the query's topic
  - *Examples:*
    - "recession"
    - "economy"
    - "pizza"

**Note**: Try the *Pretrained Word Embeddings*, *User Personalization*, and *Query Expansion* query examples in the default mode (`python deploy.py`) also to notice how the search results are improved using these techniques.
