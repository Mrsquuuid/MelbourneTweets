### 目前版本:

* `extractor.py`: 用于把所有已经爬取的文档的信息进行精炼提取。所有的数据库都合并在一起，并且只保存了关键的信息。

* `sydney-update.py`: 用于保存Richard数据库里面的文档。只保存需要含有关键信息的文档。

* `sydney-update.sh`: 通过循环语句把每一天的数据临时保存在`temp\twitter.json`里面，然后`sydney-update.py`会处理这个文档。