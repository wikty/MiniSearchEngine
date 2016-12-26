爬虫
将网页数据保存到本地，仅仅保存原始HTML数据以及url

文档信息熵跟文档信息量以及文档哪些单词表征文档信息（较少出现的单词，名词）

文档预处理
1. tokenization

2. stop words removed by a list of stop-words

3. normalization(lowercase) & spelling correct

4. group nouns

5. stemming

文档向量表示

单词在文档中的出现次数作为权重

用长度为词典大小的向量表示文档，向量第i个位置的值等于词典中第i个单词在该文档中的出现次数，在文档中出现频率越高的词则越重要，显然向量十分稀疏

TF-IDF作为Term权重

当TF=0时，权重等于0；当TF!=0时，权重=(1+log(TF))*IDF，即在文档中出现次数多且在语料库中出现次数少的单词具有高权重

预备知识

TF Term在整个语料库中出现次数
DF 在语料库中含有Term的文档数量
IDF=log(N/DF) Term的反向文档频率，词在越少的文档中出现则词越重要，抑制高频词噪音
Zipf's Law，如果将语料库中单词按照其出现频率排名，则出现次数跟排名成反比

度量查询和文档相似度

查询和文档都表示为向量，计算欧几里得距离


反转文档 inverted file

将文档由下面形式

文档1 -> w1, w2
文档2 -> w4, w1
文档3 -> w3, w5

转换为

w1 -> [{文档ID，w1的位置，w1的TF（要不要归一化），文档URL，文档点击次数，PageRank}]
w2 -> [{文档ID，w1的位置，w1的TF（要不要归一化），文档URL，文档点击次数，PageRank}]
w3 -> [{文档ID，w1的位置，w1的TF（要不要归一化），文档URL，文档点击次数，PageRank}]

为Term指定ID，通过Tire树实现

网页跟查询通过cosine或者欧式距离排名

pagerank 是rerank技术，主要利用网页中超链接重排网页


爬虫爬取html数据并记录url

raw将html数据转换为纯文本数据

将raw进行分词

统计文档中term频率，
统计Term在语料库中的频率，
构建文档到ID数据结构
构建Term到ID数据结构
构建语料库









