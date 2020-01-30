# Tweets Analyze
## Usage
### 1. Sentiment & Semantic Analysis
- #### For real time analysis:
	- Put tweets in `/tweets` dir
	- Load tweets
	- Use `load_lexicon(file)` to load semantic lexicon
	- Use `plot_sem_sent(tweets,lexicon)` to get the plot
	- `plot_sem_sent(tweets,lexicon)` will also output a json file `offline.json` which holds the results
- #### For offline analysis:
	- This will use the `offline.json` file from real time results
	- Use `plot_sem_sent_offline(offline_file, lexicon)`

### 2. Wordcloud
- #### Wordcloud based on tweets content:
	- Use generate_wordcloud(tweets, outputname)

- #### Wordcloud based on lexicon words:
	- Use load_lexicon_original(file) to load the original lexicon
	- Use tweets_match_keyword(tweets, lexicon) to find matched words
	- Use generate_wordcloud_text(tweets_match, outputname) to generate the wordcloud

### 3. Geographic vs Temporal vs Topics:
- Use reformat() to reformat the offline.json into offline_dict.json
- Use sem_geo_time() to get the csv output

### 4. Other analysis are mostly about statistics and are pretty straight forward to use.
