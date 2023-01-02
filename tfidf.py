import jieba
import jieba.analyse
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from sklearn.naive_bayes import MultinomialNB

# documents=["Im an apple",
#            "today is saturaday",
#            "im from china"]
documents=[
    "import React from 'react'",
    "",
    "import { contextHoc4FC } from 'ROOT_SOURCE/base/BaseContainer'",
    "import combineContainer from 'ROOT_SOURCE/base/CompConjunction'",
    "",
    "import F from './form'",
    "import T from './table'",
    "",
    "import actions from './actions'",
    "import reducers from './reducers'",
    "import BaseBreadcrumb from 'ROOT_SOURCE/components/BaseBreadcrumb'",
    "",
    "let ListTable = combineContainer(T).withReducers(reducers).withActions(actions).val()",
    "let ListForm = combineContainer(F).withReducers(reducers).withActions(actions).val()",
    "",
    "",
    "export default contextHoc4FC((props, context) => (",
    "    <section>",
    "        <BaseBreadcrumb",
    "            routes={[",
    "                { name: '车险订单管理' },",
    "                { name: '售车订单管理' }",
    "            ]}",
    "        />",
    "        <ListForm />",
    "        <ListTable />",
    "    </section>",
    "))",
    ""
  ]

documents = [" ".join(jieba.cut(item)) for item in documents]

print("文本分词结果： \n", documents)

with open("stop_words_tf", "r", encoding='utf-8') as fn:
    stpwrdlist = fn.read().splitlines()
fn.close()
vectorizer = TfidfVectorizer(stop_wods=stpwrdlist, max_features=10)

X = vectorizer.fit_transform(documents)

words = vectorizer.get_feature_names()

print("特征词表：",words) #idf

X = X.toarray()
print(X)  #tf-idf矩阵

for i in range(len(X)):
    for j in range(len(words)):
        print(words[j], X[i][j])

modelNB = MultinomialNB()
modelNB.fit(X)
// 朴素贝叶斯训练误差
