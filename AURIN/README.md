# 关于Tweet数据

有用的Field:

> **推文**: text/full_text
>
> **地点**: place.full_name
>
> **语言**: lang

可以进行的分析:

> 1. Average sentiment score. 需要用Python和`affin`包
>
>    > a. 不同时间段的Sentiment分布
>    >
>    > b. 不同地点的Sentiment的分布(最后大概会有5000个推文有坐标)
>    >
>    > > 需要先标注出所在SA2的Code
>
> 2. Tweet 地区数量: 就是目前每个城市获取的推文的数量。
>
> 3. Langauge Distribution
>
> 4. Key word 搜索:
>    > a. Covid related.
>    > 
>    > b. Vaccine related
>    > 
>    > c. Vulgar words related
>    > 
>    > d. Alcohol related
>    > 
>    > e. Crime related

# 关于AURIN数据

Study Area需要选择: Australia (country/au)

Aggregation Level优先选择: Greater Capital City Statistical Areas, Working Zone，Statistical Area 4 (SA4)

> **1. Greater Capital City Statistical Areas (GCCSA)**：
>
>  > **悉尼**：Greater Sydney
>  >
>  > **墨尔本**：Greater Melbourne
>  >
>  > **阿德莱德**：Greater Alelaide
>  >
>  > **珀斯**：Greater Perth
>  >
>  > **堪培拉**：Australian Capital Territory 
>  >
>  > **布里斯班**：Greater Brisbane
>
> **2. Working Zone**：
>
> > **悉尼**：Sydney & Surrounds
> >
> > **墨尔本**：Melbourne & Surrounds
> >
> > **阿德莱德**：Alelaide & Surrounds
> >
> > **珀斯**：Perth & Surrounds
> >
> > **堪培拉**：Canberra & Surrounds
> >
> > **布里斯班**：Brisbane & Surrounds
>
>   **3. Statistical Area 4 (SA4)**：
>
> > **悉尼**：Sydney + 方位
> >
> > **墨尔本**：Melbourne + 方位
> >
> > **阿德莱德**：Alelaide + 方位
> >
> > **珀斯**：Perth + 方位
> >
> > **堪培拉**：Australian Capital Territory
> >
> > **布里斯班**：Brisbane + 方位

对于有坐标的数据的分析，使用Statistical Area 2 (SA2) 进行分析。

# 可用的AURIN数据:

TODO