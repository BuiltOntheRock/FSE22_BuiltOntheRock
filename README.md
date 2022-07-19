# FSE22_BuiltOntheRock
This is a replication package for `Are We Building on the Rock? On the Importance of Data Preprocessing for Code Summarizations`. Our project is public at: <https://github.com/BuiltOntheRock/FSE22_BuiltOntheRock>

## Content
1. [Project Summary](#1-Project-Summary)<br>
2. [Benchmark Datasets](#2-Benchmark-Datasets)<br>
3. [Research Methodology](#3-Research-Methodology)<br>
4. [Taxonomy of Noisy Data](#4-Taxonomy-of-Noisy-Data)<br>
&ensp;&ensp;4.1 [Comment-related Noisy Data](#41-Comment-related-Noisy-Data)<br>
&ensp;&ensp;4.2 [Code-related Noisy Data](#42-Code-related-Noisy-Data)<br>
5. [The Code-Comment Cleaning Tool](#5-The-Code-Comment-Cleaning-Tool)<br>
6. [Quality Assessment of Benchmarks](#6-Quality-Assessment-of-Benchmarks)<br>
7. [Impacts on the Performance of Code Summarization](#7-Impacts-on-the-Performance-of-Code-Summarization)<br>
8. [Download](#8-Download)<br>
&ensp;&ensp;8.1 [Cleaned Datasets](#81-Cleaned-Datasets)<br>
&ensp;&ensp;8.2 [The Code-Comment Cleaning Tool](#82-The-Code-Comment-Cleaning-Tool)<br>

## 1 Project Summary
In this work, we conduct a systematic research to assess and improve the quality of four benchmark datasets widely used for code summarization tasks. First, we propose an automated code-comment cleaning tool that can accurately detect noisy data caused by inappropriate data preprocessing operations from existing benchmark datasets. Then, we apply the tool to further assess the data quality of the four benchmark datasets, based on the detected noises. Finally, we conduct comparative experiments to investigate the impact of noisy data on the performance of code summarization models. The results show that these data preprocessing noises widely exist in all four benchmark datasets, and removing these noisy data leads to a significant improvement on the performance of code summarization.

## 2 Benchmark Datasets
This study conducts various experiments on four widely-used code summarization datasets, including [FunCom](http://leclair.tech/data/funcom/), [TLC](https://github.com/xing-hu/TL-CodeSum), [CSN](https://github.com/github/codesearchnet), and [PCSD](https://github.com/EdinburghNLP/code-docstring-corpus).

More specifically, **FunCom** is a collection of 2.1M code-comment pairs from 29K projects. For each method, it extracted its Javadoc comment and treated the first sentence in the Javadoc of each method as its summary. **TLC** has 87K code-comment pairs collected from more than 9K open-source Java projects created from 2015 to 2016 with at least 20 stars. It extracted the Java methods and their corresponding Javadoc comments. These comments are considered as code summaries. **CSN** contains about 2M method and comment pairs mined from publicly available open-source non-fork GitHub repositories spanning six programming languages, i.e., Go, Java, JavaScript, PHP, Python, and Ruby. **PCSD** contains 105K pairs of Python functions and their comments from open source repositories in GitHub. Specifically, it uses docstrings (i.e., the string literals that appear right after the definition of functions) as summaries for Python functions.

## 3 Research Methodology
The research methodology overview consists of four main steps:  
**I. Taxonomy of Noisy Data :** First, we propose a taxonomy of 12 different types of data noises due to inappropriate or insufficient data preprocessing in code summarization, derived from observations on the selected four benchmark datasets.  
**II. The Code-Comment Cleaning Tool :** Second, we build a rule-based cleaning tool, named CAT (Code-comment cleAning Tool), for automatically scanning and detecting the occurrences and distribution of data noises for a given dataset, based on the proposed taxonomy.  
**III. Quality Assessment of Benchmarks :** Third, we conduct an evaluation study to assess the data quality of the four widely-used benchmark datasets. The results show that noisy data extensively exist in the four benchmark datasets (ranging from 31% to 66%).  
**IV. Impacts on the Performance of Code Summarization :** Finally, we investigate the impacts of noises on three typical code summarization models (i.e. NNGen, NCS, and Rencos) by comparing their performance trained on the same datasets before and after data cleaning.  

## 4 Taxonomy of Noisy Data
We propose a taxonomy of 12 different types of data noises due to inappropriate or insufficient data preprocessing in code summarization.

### 4.1 Comment-related Noisy Data
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
### 4.2 Code-related Noisy Data
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

## 5 The Code-Comment Cleaning Tool
This table demonstrates the syntax feature of heuristic rules and our actions to resolve noises detected



We use three commonly-used metrics to evaluate the performance of CAT, i.e., Precision, Recall, and F1. We can see that, it can accurately detect noises on the four benchmark datasets. The F1 scores of detecting comment-related noises are ranging from 93.0% to 100.0%, and 95.5% on average. The average F1 scores of detecting code-related noises are ranging from 95.6% to 100.0%, and 98.3% on average. The results show that, CAT can achieve highly satisfactory performance on filtering noisy data from code-comment datasets. In summary, our code-comment cleaning tool can accurately filter noisy data, with all the F1 scores of over 90.0%, which can help build a high-quality dataset for the follow-up code summarization tasks.



## 6 Quality Assessment of Benchmarks
This table illustrates the distribution of each noise category on the four benchmark datasets.



Noisy data extensively exist in the four widely-used benchmark datasets, ranging from 31.2% to 65.8%. 29.8% of the code in Funcom is auto-generated; 22.8% comments in TLC are verbose first sentences; 24.4% comments in CSN are contaminated by the meaningless text; and 15.9% comments in PCSD are the partial first sentences.
## 7 Impacts on the Performance of Code Summarization
Existing code summarization models can be divided into three categories: Information Retrieval (IR) based approaches, Neural Machine Translation (NMT) based approaches, and hybrid approaches that combine IR and NMT techniques. We select one state-of-the-art method from each category to explore the impact of noisy data on model performance. They are NNGen, NCS and Rencos. We evaluated the performance of the three models using four metrics including BLEU, METEOR, ROUGE-L, and CIDEr.
This table shows the performance of the three models trained over different experimental datasets.



Removing noisy data from the training set in the four benchmark datasets has a positive influence on the performance of the models. Training three existing models with the filtered benchmark datasets improves the BLEU-4 by 26.9%, 20.7%, and 24.1%, respectively.
## 8 Download
### 8.1 Cleaned Datasets
Our cleaned datasets can be found at [cleaned datasets](https://drive.google.com/file/d/1m4uZi0hoInYxkgrSlF23EjVasSgaXOXy/view)

### 8.2 The Code-Comment Cleaning Tool
Run the following command to install our cleaning tool:
```
pip install FSE22-CAT==0.01
```
