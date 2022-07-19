# FSE22_BuiltOntheRock
This is a replication package for `Are We Building on the Rock? On the Importance of Data Preprocessing for Code Summarizations`. Our project is public at: <https://github.com/BuiltOntheRock/FSE22_BuiltOntheRock>

## Content
1. [Get Started](#1-Get-Started)<br>
&ensp;&ensp;1.1 [Cleaned Datasets](#11-Cleaned-Datasets)<br>
&ensp;&ensp;1.2 [The Code-Comment Cleaning Tool](#12-The-Code-Comment-Cleaning-Tool)<br>
&ensp;&ensp;1.3 [Usage](#13-Usage)<br>
2. [Project Summary](#2-Project-Summary)<br>
3. [Benchmark Datasets](#3-Benchmark-Datasets)<br>
4. [Research Methodology](#4-Research-Methodology)<br>
5. [Taxonomy of Noisy Data](#5-Taxonomy-of-Noisy-Data)<br>
&ensp;&ensp;5.1 [Comment-related Noisy Data](#51-Comment-related-Noisy-Data)<br>
&ensp;&ensp;5.2 [Code-related Noisy Data](#52-Code-related-Noisy-Data)<br>

## 1 Get Started
### 1.1 Cleaned Datasets
Our cleaned datasets can be found at [cleaned datasets](https://drive.google.com/file/d/1m4uZi0hoInYxkgrSlF23EjVasSgaXOXy/view)

### 1.2 The Code-Comment Cleaning Tool
Run the following command to install our cleaning tool:
```
pip install FSE22-CAT==0.01
```
### 1.3 Usage

#### Get the first sentence of comment
```python
>>> from noise_detection import *
>>> raw_comment = "\t/**\n\t * Returns the high-value (as a double primitive) \n\t * for an item within a series.\n\t * \n\t * @param series\n\t * @param item \n\t * @return The high-value.\n\t */\n "
>>> getFirstSentence(raw_comment)
'Returns the high-value (as a double primitive) for an item within a series.'
```

#### Noise Detection
```python
>>> raw_comment = "/**\n     * relayTbList\u3068\u306e\u5916\u90e8\u7d50\u5408\u3092\u30c6\u30b9\u30c8\u3057\u307e\u3059\u3002\n     * \n     * @throws Exception\n     */\n "
>>> comment = getFirstSentence(raw_comment)
'relayTbListとの外部結合をテストします。'
>>> if_NonLiteral(comment)
True
```

#### Clean Code-Comment Data
```python
from rule_cleaner import RuleCleaner
import json
# prepare the raw data that may contain noise
with open('./test.data', 'r') as f:
    data_lines = f.readlines()
raw_code_list, raw_comment_list = [], []
for line in data_lines:
    json_line = json.loads(line.strip())
    raw_code_list.append(json_line['raw_code'])
    raw_comment_list.append(json_line['raw_comment'])
# get the cleaned code-comment data
cleaner = RuleCleaner(raw_code_list, raw_comment_list)
cleaned_code, cleaned_comment = cleaner.get_clean_data()
# get the noisy code-comment data
noisy_data = cleaner.get_noisy_data()
```
For more detailed usage and examples, please refer to the `CAT/Usage.ipynb`.

## 2 Project Summary
In this work, we conduct a systematic research to assess and improve the quality of four benchmark datasets widely used for code summarization tasks. First, we propose an automated code-comment cleaning tool that can accurately detect noisy data caused by inappropriate data preprocessing operations from existing benchmark datasets. Then, we apply the tool to further assess the data quality of the four benchmark datasets, based on the detected noises. Finally, we conduct comparative experiments to investigate the impact of noisy data on the performance of code summarization models. The results show that these data preprocessing noises widely exist in all four benchmark datasets, and removing these noisy data leads to a significant improvement on the performance of code summarization.

## 3 Benchmark Datasets
This study conducts various experiments on four widely-used code summarization datasets, including [FunCom](http://leclair.tech/data/funcom/), [TLC](https://github.com/xing-hu/TL-CodeSum), [CSN](https://github.com/github/codesearchnet), and [PCSD](https://github.com/EdinburghNLP/code-docstring-corpus).

More specifically, **FunCom** is a collection of 2.1M code-comment pairs from 29K projects. For each method, it extracted its Javadoc comment and treated the first sentence in the Javadoc of each method as its summary. **TLC** has 87K code-comment pairs collected from more than 9K open-source Java projects created from 2015 to 2016 with at least 20 stars. It extracted the Java methods and their corresponding Javadoc comments. These comments are considered as code summaries. **CSN** contains about 2M method and comment pairs mined from publicly available open-source non-fork GitHub repositories spanning six programming languages, i.e., Go, Java, JavaScript, PHP, Python, and Ruby. **PCSD** contains 105K pairs of Python functions and their comments from open source repositories in GitHub. Specifically, it uses docstrings (i.e., the string literals that appear right after the definition of functions) as summaries for Python functions.

## 4 Research Methodology
The research methodology overview consists of four main steps:  
**I. Taxonomy of Noisy Data :** First, we propose a taxonomy of 12 different types of data noises due to inappropriate or insufficient data preprocessing in code summarization, derived from observations on the selected four benchmark datasets.  
**II. The Code-Comment Cleaning Tool :** Second, we build a rule-based cleaning tool, named CAT (Code-comment cleAning Tool), for automatically scanning and detecting the occurrences and distribution of data noises for a given dataset, based on the proposed taxonomy.  
**III. Quality Assessment of Benchmarks :** Third, we conduct an evaluation study to assess the data quality of the four widely-used benchmark datasets. The results show that noisy data extensively exist in the four benchmark datasets (ranging from 31% to 66%).  
**IV. Impacts on the Performance of Code Summarization :** Finally, we investigate the impacts of noises on three typical code summarization models (i.e. NNGen, NCS, and Rencos) by comparing their performance trained on the same datasets before and after data cleaning.  

## 5 Taxonomy of Noisy Data
We propose a taxonomy of 12 different types of data noises due to inappropriate or insufficient data preprocessing in code summarization.

### 5.1 Comment-related Noisy Data
#### Partial Sentence
Since it is a common practice to place a method's summary at the first sentence of its comment, most researchers use the first sentences of the code comments as the target summaries. While, we have observed that some inappropriate processing can lead to partial first sentences collected. For example:
```
/* Returns the high-value
 * for an item within a series. */
 ----------------------------------
 Comment(FunCom): returns the high value
 ```
#### Verbose Sentence
When collecting the first sentence as the target comment, some inappropriate processing will lead to verbose first sentences collected. For example:
```
 """
 Generate a CSV file containing a summary of the xBlock usage
 Arguments:course_data
 """
 ----------------------------------
 Comment(PCSD): generate a csv file containing a summary of the xblock usage arguments course data
 ```
#### Content Tampering
Developers may use HTML tags for documentation auto-generation or URLs for external references in comments. We observe that some inappropriate processing will keep the tags or URL contents together with the comments, thus contaminating the benchmark data with meaningless text. For example:
```
/* <p> Builds the JASPIC application context.</p> */
 ----------------------------------
 Comment(CSN): builds the jaspic application context
 ```
#### Over-Splitting of Variable Identifiers
Code comments are likely to contain variable identifiers or API terms when describing code functionalities. Splitting code by camelCase or snake_case is a common operation for code understanding. However, we observe that some studies perform this operation on {every matched token in the} comments including the predefined variable identifiers or API terms. For example:
```
/* This method initializes jTextField. */ 
 ----------------------------------
 Comment(FunCom): this method initializes j text field
 ```
#### Non-Literal
Developers from different countries may write comments in their first languages, mixing with the English language in the comments sometimes. We observe that existing benchmark datasets occasionally discard the Non-English text but remain the English text as code comments. For example:
```
/* 将JSONArray转换为Bean的List，默认为ArrayList  */ 
 ----------------------------------
 Comment(CSN): jsonarray bean list arraylist
```
#### Interrogation
Based on our observation, some of the comments in the benchmark dataset are interrogations. For example:
```
/* Do we need to show the upgrade wizard prompt? */
public boolean isDue() {
  if (isUpToDate)
     return false; ...
 ----------------------------------
 Comment(CSN): : do we need to show the upgrade wizard prompt ?
```
#### Under-Development Comments
Based on our observation, some of the comments are related to ongoing and future development, including temporary tips, notes, etc. For example:
```
/* Description of the Method */
protected void openFile(File f) {
  if (f == null) { ...
 ----------------------------------
 Comment(TLC): description of the method
```
### 5.2 Code-related Noisy Data
#### Empty Function
Developers often take on technical debt to speed up software development. It has been widely observed that empty function is a common type of technical debt. However, the code-comment pairs extracted from these empty functions can introduce non-trivial noises, this is because an unimplemented empty function and its comment do not match either syntactically or semantically. For example:
```
/*Specifies the behaviour of the automaton in its end state*/
protected void end(){}
 ----------------------------------
 Comment(FunCom): protected void end
 ```
#### Commented-Out Method
Developers often comment out a whole method for deprecating a specific functionality. We observe that, in the studied benchmark datasets, some commented-out methods are collected as the comments for the sequential methods. For example:
```
/* for now try mappig full type URI  */
// public String transformTypeID(URI typeuri){
// return typeuri.toString();}
 ----------------------------------
 Comment(FunCom): public string transform type id ...
```
#### Block-Comment Code
We have observed that some code in the benchmark datasets contains block comments inside their bodies. The blocked comments could be natural-language comments or commented-out code. For example:
```
/* Get GPS Quality Data  */
public int getFixQuality(){
  checkRefresh();
  // TODO: Why is he using Math.round?
  Return Math.round(quality);}
 ----------------------------------
 Comment(FunCom): public int get fix quality check refresh todo why is he using math round return math round quality
```
#### Auto Code
Developers often use modern IDEs like Eclipse or Visual Studio to generate auxiliary functions such as getter, setter, toString, or tester for some predefined variables. The comments for these auto generated methods are often similar to or the same as the method names, which makes the code-comment pairs less informative. For example:
```
/* Test the constructor */
public void testConstructor() {
  System TestResult str;
  System TestID testID1; ...
 ----------------------------------
 Comment(FunCom): public void test constructor ...
```
#### Duplicated Code
Developers often reuse code by copying, pasting and modifying to speed up software development. These code snippets often have similar or the same comments. Sharing identical code and summarization pairs in the training and test sets is inappropriate and would make the model learn these cases easily.
