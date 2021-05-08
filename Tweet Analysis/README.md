# 数据库的说明:

* `twitter/current/all`: 最近一个月的6大首府的推文数据。

* `twitter/hist/sydney/geo`: 2019-2020悉尼地区所有含有坐标信息的推文数据。(少部分推文可能也会没有SA2信息，因为不在大悉尼范围之内)

* `twitter/hist/sydney/relative`: 2019-2020悉尼地区至少含有一个关键字的推文数据。（不一定有坐标）

* `twitter/hist/melbourne/geo`: 2014-2020墨尔本地区所有含有坐标信息的推文数据。（貌似2019年以后的老师的数据库里没有）

* `twitter/hist/melbourne/relative`: 2014-2020墨尔本地区至少含有一个关键字的推文数据。（先爬下来，不一定用得到）


# 目前版本:

* `extractor.py`: 用于把所有已经爬取的文档的信息进行精炼提取。所有的数据库都合并在一起，并且只保存了关键的信息。

* `hist-update.py`: 用于保存Richard数据库里面的文档。只保存需要含有关键信息的文档。

* `sydney-update.sh`: 爬取悉尼的历史数据。通过循环语句把每一天的数据临时保存在`temp\twitter.json`里面，然后`hist-update.py`会处理这个文档。

* `melb-update.sh`: 爬取墨尔本的历史数据。和`sydney-update.sh`类似。

# Scenarios:

## a. 初步想法：

每一个Scenario就会跳转到一个网页。网页为静态，不需要和用户交互。该网页含有标题，数据来源（城市+时间），总推文数量，简单的Scenario的描述，最后就是该Scenario的图标（下面会说到）。

## b. 情景1:

**Topic:** How Chinese-Australia relationship and Australian people's views on China is influenced by the breakout of COVID-19?

**Abstraction:** Since the outbreak of the epidemic, discrimination against China and even Asians has become increasingly serious around the world, including Australia. So many news have been reported during the last year that a Chinese or Asian man is abused or discriminated against by locals. This scenario aims to discovering how Chinese-Australia relationship and Australian people's views on China is influenced by the breakout of COVID-19, where the sentiment score for the tweets is used as the indicator. This scenario will also explore how the sentiment score differs by the location of different SA2 area of Sydney and how this differene is correlated with demographic characteristics and macro-economic indicator.

**Data:** All tweets made during 2019-2020 in Greater Sydney. 

**图表A**：Line Chart

> **关键词：**`china_words`，`covid_words`，`vulgar_words`
>
> **数据库：**`twitter/hist/sydney/relative`
>
> **情景解释**：The time sereis of sentiment scores for tweets containing keywords related to China from 2019 to 2020.
>
> **横坐标**：2019年到2020年的月份（共24个月），或者2019年10月到2020年9月的月份（12个月），根据排版需要来决定。
>
> **纵坐标**: 
>
> > **1.** 涉及`china_words`的Average (或者Total) Sentiment Score。(**View:** `scenario_1/china_stats`)
> >
> > **2.** 涉及`china_words`和`covid_words`的Average (或者Total) Sentiment Score。(**View:** `scenario_1/china_covid_stats`)
> >
> > **3.** 涉及`china_words`和`vulgar_words`的Average (或者Total) Sentiment Score。(**View:** `scenario_1/chian_vulgar_stats`)
> >
> > **4.** 月新增确诊人数 **(这个可以弄成柱状图)**。

**图表B**：Line Chart

> **关键词：**`china_words`，`covid_words`，`vulgar_words`
>
> **数据库：**`twitter/hist/sydney/relative`
>
> **情景解释**：The time sereis of the number of tweets containing keywords related to China from 2019 to 2020.
>
> **横坐标**：2019年到2020年的月份（共24个月），或者2019年10月到2020年9月的月份（12个月），根据排版需要来决定。
>
> **纵坐标**: 
>
> > **1.** 涉及`china_words`的数量。(**View:** `scenario_1/china_stats`)
> >
> > **2.** 涉及`china_words`和`covid_words`的数量。(**View:** `scenario_1/china_covid_stats`)
> >
> > **3.** 涉及`china_words`和`vulgar_words`的数量。(**View:** `scenario_1/chian_vulgar_stats`)
> >
> > **4.** 月新增确诊人数 **(这个可以弄成柱状图)**。

**图表C**：Bar Chart

> **关键词**：`china_words`
>
> **数据库：**`twitter/hist/sydney/geo`
>
> **情景解释**：The distribution the sentiment score for tweets made in 2019 and 2020 containing China-related keywords over different SA2 locations in Sydney. (At least 20 related tweets are requried for each SA2 location)
>
> **横坐标**：前五位与后五位地区名。
>
> **纵坐标**:  涉及`china_words`的Average (或者Total) Sentiment Score。(**View:** `scenario_1/china_stats`)
>
> **备注**：有条件的话可以改成区域HeatMap。

**图表D**：Bar Chart

> **关键词**：`china_words`
>
> **数据库：**`twitter/hist/sydney/geo`
>
> **情景解释**：The distirbution of the number of tweets made in 2019 and 2020 containing China-related keywords over different SA2 locations in Sydney. 
>
> **横坐标**：前十位地区名。
>
> **纵坐标**:  涉及`china_words`的数量。(**View:** `scenario_1/china_stats`)
>
> **备注**：有条件的话可以改成区域HeatMap。

**图表E,F**：Scatter Plot (两个)

> **关键词**：`china_words`
>
> **数据库：**`twitter/hist/sydney/geo`
>
> **情景解释**：The correlation between sentiment score distribution for tweets made in 2019 and 2020 containing China-related keywords over each SA2 location in Sydney and the demographic characteristics and macro-economic indicator. 
>
> **横坐标**：AURIN的某项数据。图E为经济指标。图F为人口特征。
>
> **纵坐标**: 涉及`china_words`的 (或者Total) Average Sentiment Score。(**View:** `scenario_1/china_stats`)

## c. 情景2:

**Topic:** Which suburb is considered as most unsafe place in Melbourne ?

**Abstraction:** There are hundreds of suburb in Melbourne and people always have a preference when choosing which suburb to live. Some suburbs are considered as comparably unsafe, which may be due to the frequency of criminal case or population distribution. This scenario aims to discovering which SA2 area is considered as the unsafest place in melbourne, where the proportion of tweets containing certain keywords is used as the indicator. This scenario will also explore how the result above  is correlated with demographic characteristics and economic indicator of each SA2 area.

**Data:** All tweets made between 2014-2021 in Greater Melbourne. 

**图表A**：Bar Chart

> **关键词**：`vulgar_words`，`crime_words`，`alcohol_words`
>
> **数据库：**`twitter/hist/melbourne/geo`
>
> **情景解释**：The distirbution of the proportion of tweets containing vulgar, crime or alcohol related words over different SA2 locations in Melbourne. (At least 50 total tweets are requried for each SA2 location)
>
> **横坐标**：前十位地区名。
>
> **纵坐标**: 涉及`vulgar_words`，`crime_words`和`alcohol_words`的推文的比例 (**View:** `scenario_2/bad_words_stats`)
>
> **备注**：有条件的话可以改成区域HeatMap。

**图表B**：Bar Chart

> **关键词**：`vulgar_words`，`crime_words`，`alcohol_words`
>
> **数据库：**`twitter/hist/melbourne/geo`
>
> **情景解释**：The distirbution the number of tweets containing vulgar, crime or alcohol related words over different SA2 locations in Melbourne.
>
> **横坐标**：前十位地区名。
>
> **纵坐标**: 涉及`vulgar_words`，`crime_words`和`alcohol_words`的推文的数量 (**View:** `scenario_2/bad_words_stats`)
>
> **备注**：有条件的话可以改成区域HeatMap。

**图表C**：Bar Chart

> **关键词**：无
>
> **数据库：**`twitter/hist/melbourne/geo`
>
> **情景解释**：The distribution the sentiment score for tweets over different SA2 locations in Melbourne. (At least 50 total tweets are requried for each SA2 location)
>
> **横坐标**：**后**十位地区名。
>
> **纵坐标**: 所有推文的Average (或者Total) Sentiment Score。 (**View:** `scenario_2/afinn_stats`)
>
> **备注**：有条件的话可以改成区域HeatMap。

**图表D**：Scatter Plot

> **关键词**：`vulgar_words`，`crime_words`，`alcohol_words`
>
> **数据库：**`twitter/hist/melbourne/geo`
>
> **情景解释**：The correlation between the distribution of the sentiment score and the distirbution of the vulgar, crime or alcohol related tweets proportion over different SA2 locations in Melbourne.
>
> **横坐标**：涉及`vulgar_words`，`crime_words`和`alcohol_words`的推文的比例 (**View:** `scenario_2/bad_words_stats`)
>
> **纵坐标**: 所有推文的Average (或者Total) Sentiment Score。 (**View:** `scenario_2/afinn_stats`)

**图表E,F**：Scatter Plot (两个)

> **关键词**：`vulgar_words`，`crime_words`，`alcohol_words`
>
> **数据库：**`twitter/hist/melbourne/geo`
>
> **情景解释**：The correlation between the distirbution of the vulgar, crime or alcohol related tweets proportion over each SA2 location in Melbourne and the demographic characteristics and macro-economic indicator. (At least 20 tweets is requried for each SA2 location)
>
> **横坐标**：AURIN的某项数据。图E为经济指标。图F为人口特征。
>
> **纵坐标**: 涉及`vulgar_words`，`crime_words`和`alcohol_words`的推文的比例 (**View:** `scenario_2/bad_words_stats`)

## d. 情景3:

**Topic:** Which major city in Australia do non-English speaking immigrants favour most?

**Abstraction:** Australia is a country of immigrants and it is also the first choice of the destination country for many immigrants at the same time. Thousands of overseas travelers come to live in Australia every year in order to obtain Australian immigration qualifications, of whom a significant number comes from non-English speaking contries.  This scenario aims to discovering which major city in Australia has most non-English speaker living there by calculating the proportion of non-English tweets made during the last month. This scenario will also explore how the result above is correlated with demographic characteristics and economic indicator of each city.

**Data:** All tweets made in the latest month in Sydney, Melbourne, Brisbane, Adelaide, Perth and Canberra.

**图表A**：Bar Chart

> **关键词**：无
>
> **数据库：**`twitter/current/all`
>
> **情景解释**：The distirbution of the proportion of non-English tweets over the 6 major cities in Australia. 
>
> **横坐标**：城市名字（根据纵坐标从高到低）。
>
> **纵坐标**: 非英文的推文的比例 (**View:** `scenario_3/nonenglish_stats`)

**图表B**：Scatter Plot

> **关键词**：无
>
> **数据库：**`twitter/current/all`
>
> **情景解释**：The correlation between distirbution of the proportion of non-English tweets and the distribution of the average sentiment score for all tweets over the 6 major cities in Australia. 
>
> **横坐标**：所有推文的Average (或者Total) Sentiment Score。 (**View:** `scenario_3/afinn_stats`)。
>
> **纵坐标**: 非英文的推文的比例 (**View:** `scenario_3/nonenglish_stats`)

**图表C,D**：Scatter Plot (两个)

> **关键词**：无
>
> **数据库：**`twitter/current/all`
>
> **情景解释**：The correlation between the distirbution of the proportion of non-English tweets and the demographic characteristics and macro-economic indicator. 
>
> **横坐标**：AURIN的某项数据。图C为经济指标。图D为人口特征。
>
> **纵坐标**: 非英文的推文的比例 (**View:** `scenario_3/nonenglish_stats`)