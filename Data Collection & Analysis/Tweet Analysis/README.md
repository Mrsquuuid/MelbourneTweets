# How to dump couchDB database to a file:

Click [here](https://stackoverflow.com/questions/11639534/couchdb-dump-to-file-and-load-from-file).

# Databases:

* *sydney-relative*: All tweets containing at least one occurrence of any keyword collected between 2019 and 2020 in Sydney. This database incorporates in total 2887199 tweets and will be used in Scenario 1.
* *sydney-geo*: All geo-tagged tweets collected between 2019 and 2020 in Sydney. This database incorporates in total 104977 tweets and will be used in Scenario 1.
* *melbourne-geo*: All geo-tagged tweets collected since 2014 in Melbourne. This database incorporates in total 622872 tweets and will be used in Scenario 2.
* *all*: All tweets collected over the past 30 days (2021 Mid-April - 2021 Mid-May) in Sydney, Melbourne, Brisbane, Adelaide, Perth and Canberra. This database includes in total 288860 tweets and will be used in Scenario 3.


# Scripts:

* `hist-update.py`: Extract, pre-process and save twitter data from downloaded Richard's private database.
* `sydney-update.sh`: Download and save historical Sydney data。
* `melb-update.sh`: Download and save historical Melbourne data

# Scenarios:

## a. Scenario 1:

**Topic:** How Chinese-Australia relationship and Australian people's views on China is influenced by the breakout of COVID-19?

**Abstraction:** Since the outbreak of the epidemic, discrimination against China and even Asians has become increasingly serious around the world, including Australia. So many news have been reported during the last year that a Chinese or Asian man is abused or discriminated against by locals. This scenario aims to discovering how Chinese-Australia relationship and Australian people's views on China is influenced by the breakout of COVID-19, where the sentiment score for the tweets is used as the indicator. This scenario will also explore how the sentiment score differs by the location of different SA2 area of Sydney and how this difference is correlated with demographic characteristics and macro-economic indicator.

**Data:** In total 42425272 Tweets, of which 291408 tweets have relative keywords.

> All tweets made during 2019-2020 in Greater Sydney. 

**Figure A**：Line Chart

> **Keywords：**`china_words`，`covid_words`，`vulgar_words`
>
> **Database：**`twitter/hist/sydney/relative`
>
> **Data Info**：The time series of sentiment scores for tweets containing keywords related to China from 2019 to 2020.
>
> **X-axis**：Months from 2019 to 2020.
>
> **Y-axis**: 
>
> > **1.** `china_words` Average Sentiment Score。(**View:** `scenario_1/china_stats`)
> >
> > **2.** `china_words` and `covid_words` Average Sentiment Score。(**View:** `scenario_1/china_covid_stats`)
> >
> > **3.** `china_words` and`vulgar_words` Average Sentiment Score。(**View:** `scenario_1/chian_vulgar_stats`)
> >
> > **4.** Monthly COVID Newly diagnosed Number in AU.

**Figure B**：Line Chart

> **Keywords：**`china_words`，`covid_words`，`vulgar_words`
>
> **Database：**`twitter/hist/sydney/relative`
>
> **Data Info**：The time series of the number of tweets containing keywords related to China from 2019 to 2020.
>
> **X-axis**：Months from 2019 to 2020.
>
> **Y-axis**: 
>
> > **1.** `china_words` number。(**View:** `scenario_1/china_stats`)
> >
> > **2.** `china_words` and `covid_words` number。(**View:** `scenario_1/china_covid_stats`)
> >
> > **3.** `china_words` and `vulgar_words` number。(**View:** `scenario_1/chian_vulgar_stats`)
> >
> > **4.** Monthly COVID Newly diagnosed Number in AU.

**Figure C**：Bar Chart

> **Keywords**：`china_words`
>
> **Database：**`twitter/hist/sydney/geo`
>
> **Data Info**：The distribution the sentiment score for tweets made in 2019 and 2020 containing China-related keywords over different SA2 locations in Sydney. (At least 20 related tweets are required for each SA2 location)
>
> **X-axis**：Top 5 and Last 5 Suburbs.
>
> **Y-axis**:  `china_words` Average Sentiment Score。(**View:** `scenario_1/china_stats`)

**Figure D**：Bar Chart

> **Keywords**：`china_words`
>
> **Database：**`twitter/hist/sydney/geo`
>
> **Data Info**：The distribution of the number of tweets made in 2019 and 2020 containing China-related keywords over different SA2 locations in Sydney. 
>
> **X-axis**：Top 10 Suburbs.
>
> **Y-axis**:  # of `china_words`。(**View:** `scenario_1/china_stats`)

**Figure E,F**：Scatter Plot

> **Keywords**：`china_words`
>
> **Database：**`twitter/hist/sydney/geo`
>
> **Data Info**：The correlation between sentiment score distribution for tweets made in 2019 and 2020 containing China-related keywords over each SA2 location in Sydney and the demographic characteristics and macro-economic indicator. 
>
> **X-axis**：AURIN
>
> **Y-axis**: `china_words`Average Sentiment Score。(**View:** `scenario_1/china_stats`)

## b. Scenario 2:

**Topic:** Which suburb is considered as most unsafe place in Melbourne ?

**Abstraction:** There are hundreds of suburb in Melbourne and people always have a preference when choosing which suburb to live. Some suburbs are considered as comparably unsafe, which may be due to the frequency of criminal case or population distribution. This scenario aims to discovering which SA2 area is considered as the unsafest place in Melbourne, where the proportion of tweets containing certain keywords is used as the indicator. This scenario will also explore how the result above  is correlated with demographic characteristics and economic indicator of each SA2 area.

**Data:** In total 42033167 Tweets, of which 622872 tweets are geo tagged.

> All tweets made between 2014-2021 in Greater Melbourne. 

**Figure A**：Bar Chart

> **Keywords**：`vulgar_words`，`crime_words`，`alcohol_words`
>
> **Database：**`twitter/hist/melbourne/geo`
>
> **Data Info**：The distribution of the proportion of tweets containing vulgar, crime or alcohol related words over different SA2 locations in Melbourne. (At least 50 total tweets are required for each SA2 location)
>
> **X-axis**：Top 10 Suburbs.
>
> **Y-axis**: `vulgar_words`，`crime_words` and `alcohol_words` proportion (**View:** `scenario_2/bad_words_stats`)

**Figure B**：Bar Chart

> **Keywords**：`vulgar_words`，`crime_words`，`alcohol_words`
>
> **Database：**`twitter/hist/melbourne/geo`
>
> **Data Info**：The distribution the number of tweets containing vulgar, crime or alcohol related words over different SA2 locations in Melbourne.
>
> **X-axis**：Last 10 Suburbs.
>
> **Y-axis**: `vulgar_words`，`crime_words` and `alcohol_words` number (**View:** `scenario_2/bad_words_stats`)

**Figure C**：Bar Chart

> **Keywords**：None.
>
> **Database：**`twitter/hist/melbourne/geo`
>
> **Data Info**：The distribution the sentiment score for tweets over different SA2 locations in Melbourne. (At least 50 total tweets are required for each SA2 location)
>
> **X-axis**：Last 10 Suburbs.
>
> **Y-axis**: All Average Sentiment Score。 (**View:** `scenario_2/afinn_stats`)

**Figure D**：Scatter Plot

> **Keywords**：`vulgar_words`，`crime_words`，`alcohol_words`
>
> **Database：**`twitter/hist/melbourne/geo`
>
> **Data Info**：The correlation between the distribution of the sentiment score and the distribution of the vulgar, crime or alcohol related tweets proportion over different SA2 locations in Melbourne.
>
> **X-axis**：`vulgar_words`，`crime_words` and `alcohol_words` (**View:** `scenario_2/bad_words_stats`)
>
> **Y-axis**: All Average Sentiment Score。 (**View:** `scenario_2/afinn_stats`)

**Figure E,F**：Scatter Plot

> **Keywords**：`vulgar_words`，`crime_words`，`alcohol_words`
>
> **Database：**`twitter/hist/melbourne/geo`
>
> **Data Info**：The correlation between the distribution of the vulgar, crime or alcohol related tweets proportion over each SA2 location in Melbourne and the demographic characteristics and macro-economic indicator. (At least 20 tweets is required for each SA2 location)
>
> **X-axis**：AURIN
>
> **Y-axis**: `vulgar_words`，`crime_words` and `alcohol_words` proportion (**View:** `scenario_2/bad_words_stats`)

## c. Scenario 3:

**Topic:** Which major city in Australia do non-English speaking immigrants favour most?

**Abstraction:** Australia is a country of immigrants and it is also the first choice of the destination country for many immigrants at the same time. Thousands of overseas travellers come to live in Australia every year in order to obtain Australian immigration qualifications, of whom a significant number comes from non-English speaking countries.  This scenario aims to discovering which major city in Australia has most non-English speaker living there by calculating the proportion of non-English tweets made during the last month. This scenario will also explore how the result above is correlated with demographic characteristics and economic indicator of each city.

**Data:** In total 233689 Tweets, of which all are geo-tagged.

> All tweets made in the latest month in Sydney, Melbourne, Brisbane, Adelaide, Perth and Canberra.

**Figure A**：Bar Chart

> **Keywords**：None
>
> **Database：**`twitter/current/all`
>
> **Data Info**：The distribution of the proportion of non-English tweets over the 6 major cities in Australia. 
>
> **X-axis**：City names
>
> **Y-axis**: Non-english proportion (**View:** `scenario_3/nonenglish_stats`)

**Figure B**：Scatter Plot

> **Keywords**：None
>
> **Database：**`twitter/current/all`
>
> **Data Info**：The correlation between distribution of the proportion of non-English tweets and the distribution of the average sentiment score for all tweets over the 6 major cities in Australia. 
>
> **X-axis**：All Average Sentiment Score。 (**View:** `scenario_3/afinn_stats`)。
>
> **Y-axis**: Non-english proportion (**View:** `scenario_3/nonenglish_stats`)

**Figure C,D**：Scatter Plot

> **Keywords**：None
>
> **Database：**`twitter/current/all`
>
> **Data Info**：The correlation between the distribution of the proportion of non-English tweets and the demographic characteristics and macro-economic indicator. 
>
> **X-axis**：AURIN
>
> **Y-axis**: Non-english proportion (**View:** `scenario_3/nonenglish_stats`)
