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

**1.** 分析2019-2020年每个月的含有关键词信息的推文数量以及其Sentiment的变化。（Time Series）

**2.** 使用2014-2021年墨尔本的推文数据，对墨尔本每个SA2地区的含有关键词的推文数量以及Sentiment进行比较。其结果和AURIN数据做Correlation。

**2.** 使用2021年近一个月六大首府的推文数据，对每个首府的含有关键词的推文数量以及Sentiment进行比较。其结果和AURIN数据做Correlation。