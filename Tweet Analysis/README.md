## 数据库的说明:

* `twitter/current/all`: 最近一个月的6大首府的推文数据。

* `twitter/hist/sydney/geo`: 2019-2020悉尼地区所有含有坐标信息的推文数据。(少部分推文可能也会没有SA2信息，因为不在大悉尼范围之内)

* `twitter/hist/sydney/relative`: 2019-2020悉尼地区至少含有一个关键字的推文数据。（不一定有坐标）

* `twitter/hist/melbourne/geo`: 2014-2020墨尔本地区所有含有坐标信息的推文数据。（貌似2019年以后的老师的数据库里没有）

* `twitter/hist/melbourne/relative`: 2014-2020墨尔本地区至少含有一个关键字的推文数据。（先爬下来，不一定用得到）


## 目前版本:

* `extractor.py`: 用于把所有已经爬取的文档的信息进行精炼提取。所有的数据库都合并在一起，并且只保存了关键的信息。

* `hist-update.py`: 用于保存Richard数据库里面的文档。只保存需要含有关键信息的文档。

* `sydney-update.sh`: 爬取悉尼的历史数据。通过循环语句把每一天的数据临时保存在`temp\twitter.json`里面，然后`hist-update.py`会处理这个文档。

* `melb-update.sh`: 爬取墨尔本的历史数据。和`sydney-update.sh`类似。

## Scenarios:

### 初步想法：

每一个Scenario就会跳转到一个网页。网页为静态，不需要和用户交互。该网页含有标题，数据来源（城市+时间），总推文数量，简单的Scenario的描述，最后就是该Scenario的图标（下面会说到）。

### 情景1:

分析2019-2020年悉尼地区每个月的含有关键词信息的推文数量以及其Sentiment的变化。

**图表A：**折线图

> **关键词：**`china_words`
>
> **数据库：**`twitter/hist/sydney/relative`
>
> **情景解释：**研究COVID爆发前后6个月（或者一年）时间内，悉尼地区英文母语者对中国的情绪态度。
>
> **横坐标**：2019年到2020年的月份（共24个月），或者2019年10月到2020年9月的月份（12个月），根据排版需要来决定。
>
> **纵坐标**: 纵坐标全部都Normalize到0-100。但是Annotation以实际数量标记。(**View:** `scenario_1/china_stats`)
>
> > **1.** 涉及关键词的Total Sentiment Score。
> >
> > **2.** 涉及关键词的Average Sentiment Score。
> >
> > **3.** 涉及关键词的推文数量。
> >
> > **4.** 月新增确诊人数

**图表B：**折线图

> **关键词：**`covid_words`
>
> **数据库：**`twitter/hist/sydney/relative`
>
> **情景解释：**研究COVID爆发前后6个月（或者一年）时间内，悉尼地区英文母语者对新冠疫情的情绪态度。
>
> **横坐标**：2019年到2020年的月份（共24个月），或者2019年10月到2020年9月的月份（12个月），根据排版需要来决定。
>
> **纵坐标**: 纵坐标全部都Normalize到0-100。但是Annotation以实际数量标记。(**View:** `scenario_1/china_stats`)
>
> > **1.** 涉及关键词的Total Sentiment Score。
> >
> > **2.** 涉及关键词的Average Sentiment Score。
> >
> > **3.** 涉及关键词的推文数量。
> >
> > **4.** 月新增确诊人数

**图表C：**柱状图

> **关键词：**无
>
> **数据库：**`twitter/hist/sydney/geo`
>
> **情景解释：**比较COVID爆发**后**9个月时间内（2020.3 - 2020.10），悉尼地区每一个SA2区域的英文母语者整体情绪态度（只使用含有坐标信息的推文）。
>
> **横坐标**：前五位与后五位地区名。
>
> **纵坐标**: (**View:** `scenario_1/all_stats`)
>
> > **1.** 整体的Average Sentiment Score。
>
> **备注：**有条件的话可以改成区域HeatMap。

**图表D：**点状图

> **关键词：**无
>
> **数据库：**`twitter/hist/sydney/geo`
>
> **情景解释：**比较COVID爆发**后**9个月时间内（2020.3 - 2020.10），悉尼地区每一个SA2区域的英文母语者整体情绪态度（只使用含有坐标信息的推文）和AURIN的某项数据的关系。
>
> **横坐标**：整体的Average Sentiment Score。(**View:** `scenario_1/all_stats`) 。
>
> **纵坐标**: AURIN的某项数据数据。

**2.** 使用2014-2021年墨尔本的推文数据，对墨尔本每个SA2地区的含有关键词的推文数量以及Sentiment进行比较。其结果和AURIN数据做Correlation。

**3.** 使用2021年近一个月六大首府的推文数据，对每个首府的含有关键词的推文数量以及Sentiment进行比较。其结果和AURIN数据做Correlation。

