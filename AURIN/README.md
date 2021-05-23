# About Twitter Data Fields

### Useful fields in twitter document:

> **text**: text/full_text
>
> **location**: place.full_name
>
> **language**: lang

### Twitter analysis:

> 1. Average sentiment score. Need Python package`affin`
>
>    > a. Distribution of sentiment score in different time slots of a day
>    >
>    > b. Distribution of sentiment score in different suburbs
>    
>    2. \# of Tweets in different suburbs
>
> 3. Langauge Distribution
>
> 4. Key word search:
>   > a. Covid related.
>    > 
>    > b. Vaccine related
>    > 
>    > c. Vulgar words related
>    > 
>    > d. Alcohol related
>    > 
>    > e. Crime related

# 关于AURIN数据

Study Area: Australia (country/au)

Aggregation Level: Greater Capital City Statistical Areas, Working Zone，Statistical Area 4 (SA4)

> **1. Greater Capital City Statistical Areas (GCCSA)**：
>
>  > **Sydney**：Greater Sydney
>  >
>  > **Melbourne**：Greater Melbourne
>  >
>  > **Adelaide**：Greater Adelaide
>  >
>  > **Perth**：Greater Perth
>  >
>  > **Canberra**：Australian Capital Territory 
>  >
>  > **Brisbane**：Greater Brisbane
>
> **2. Working Zone**：
>
> > **Sydney**：Sydney & Surrounds
> >
> > **Melbourne**：Melbourne & Surrounds
> >
> > **Adelaide**：Adelaide & Surrounds
> >
> > **Perth**：Perth & Surrounds
> >
> > **Canberra**：Canberra & Surrounds
> >
> > **Brisbane**：Brisbane & Surrounds
>
>   **3. Statistical Area 4 (SA4)**：
>
> > **Sydney**：Sydney + Points of the compass
> >
> > **Melbourne**：Melbourne + Points of the compass
> >
> > **Adelaide**：Adelaide + Points of the compass
> >
> > **Perth**：Perth + Points of the compass
> >
> > **Canberra**：Australian Capital Territory
> >
> > **Brisbane**：Brisbane + Points of the compass

For geo-tagged tweets，use Statistical Area 2 (SA2) for anslysis。

# Candidate AURIN Data:

Refer to folder`GCCSA`，`Melb_SA2` and`SA4`。Folder name is the data-set name and`meta.json`provides detailer description of the data-set and each field.