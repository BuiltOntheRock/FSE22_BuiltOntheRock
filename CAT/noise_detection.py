import re


def cleanCommentTag(comment):
    """
    :param comment: raw comment
    :return: list of comment lines
    """
    clean_p1 = re.compile('([\s/*=-]+)$|^([\s/*=-]+)')
    clean_p2 = re.compile('^([\s*]+)')

    def func(t):
        t = t.strip().replace('&nbsp;', ' ')
        return re.sub(clean_p2, '', t).strip()

    comment_list = []
    for line in re.sub(clean_p1, '', comment).split('\n'):
        cur_line = func(line)
        if cur_line != '':
            comment_list.append(cur_line)

    return comment_list


def getFirstSentence(comment):
    """
    :param comment: raw comment
    :return: the first sentence of the comment
    """
    pattern1 = re.compile(r'([^\n]+?)(((?<!i\.e)(?<!e\.g)(?<!\beg)(?<!\bie))\.\s|\.$)')
    pattern2 = re.compile(r'^[A-Z@]|(\(?i\.e\.)|(\(?e\.g\.)|(\(?eg\.)|(\(?ie\.)[\s\S]+')

    comment_list = cleanCommentTag(comment)
    if not comment_list:
        print(comment)
        raise Exception("null comment")

    first_sentence = ''
    for line in comment_list:
        if first_sentence == '':
            obj = re.match(pattern1, line)
            if obj:
                return obj[0]
            else:
                first_sentence += line
        else:
            if line == '' or re.match(pattern2, line) is not None:
                return first_sentence
            else:
                obj = re.match(pattern1, line)
                if obj:
                    return first_sentence + ' ' + obj[0]
                else:
                    first_sentence = first_sentence + ' ' + line

    return first_sentence.strip()


def if_ContentTamper(comment):
    javadoc_p = re.compile(r'@[a-zA-Z\d]+')
    url_p = re.compile('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])')
    html_p = re.compile(r'</?[^>]+>')

    if javadoc_p.search(comment) or url_p.search(comment) or html_p.search(comment):
        return True
    else:
        return False


def if_NonLiteral(comment):
    p = re.compile('[a-zA-Z]')
    if not comment.isascii():
        return True
    elif not p.search(comment):
        return True
    else:
        return False


def if_Interrogation(comment):
    pattern = re.compile(r'(?i)^(why\b|how\b|what\'?s?\b|where\b|is\b|are\b)')

    if comment[-1] == '?' or pattern.search(comment):
        return True
    else:
        return False


def if_UnderDevelop(comment):
    p1 = re.compile('(?i)^((Description of the Method)|(NOT YET DOCUMENTED)|(Missing[\s\S]+Description)|(not in use)|'
                    '(Insert the method\'s description here)|(No implementation provided)|(\(non\-Javadoc\)))')
    p2 = re.compile('(?i)^(todo|deprecate|copyright)')
    p3 = re.compile('^[A-Za-z]+(\([A-Za-z_]+\))?:')
    p4 = re.compile('[A-Z ]+')
    p5 = re.compile('\(.+\)|\[.+\]|\{.+\}')

    if p1.search(comment) or p2.search(comment) or p3.search(comment):
        return True
    elif re.fullmatch(p4, comment) or re.fullmatch(p5, comment):
        return True
    else:

        return False


def if_Partial(raw_comment, benchmark_comment):
    correct_comment = getFirstSentence(raw_comment)
    if len(benchmark_comment.split()) < len(correct_comment.split()):
        return True
    else:
        return False


def if_Verbose(raw_comment, benchmark_comment):
    correct_comment = getFirstSentence(raw_comment)
    if len(benchmark_comment.split()) > len(correct_comment.split()):
        return True
    else:
        return False


def if_OverSplit(raw_comment, benchmark_comment):
    def tokenize_with_camel_case(token):
        matches = re.finditer(r'.+?(?:(?<=[a-z\d])(?=[A-Z])|$)', token)
        return [m.group(0) for m in matches]

    def tokenize_with_snake_case(token):
        return token.split('_')

    correct_comment = getFirstSentence(raw_comment)
    for token in correct_comment.split():
        if len(tokenize_with_camel_case(token)) > 1 or len(tokenize_with_snake_case(token)) > 1:
            if token not in benchmark_comment:
                return True

    return False


def if_EmptyFunc(raw_code):
    pattern = re.compile('(?!\{\s+\})\{[\s\S]+\}')
    if pattern.search(raw_code):
        return False
    else:
        return True


def if_CommentedOut(raw_code):
    raw_code = raw_code.strip()
    p0 = re.compile('(^/\*)')
    p1 = re.compile('(\*/$)')
    if p0.search(raw_code) and p1.search(raw_code):
        return True
    p2 = re.compile('(^//)')
    for row in raw_code.split('\n'):
        row = row.strip()
        if row != '' and not p2.search(row):
            return False
    return True


def if_BlockComment(raw_code):
    raw_code = raw_code.strip()
    p0 = re.compile('^(//|/\*)')
    p1 = re.compile(';\n*(//|/\*)')
    for row in raw_code.split('\n'):
        row = row.strip()
        if row != '' and (p0.search(row) or p1.search(row)):
            return True
    return False


def if_AutoCode_by_comment(comment, raw_comment=None):
    p1 = re.compile(r'(?i)@[a-zA-Z]*generated\b')
    p2 = re.compile('(?i)^([aA]uto[-\s]generated)')
    p3 = re.compile('(?i)^(This method initializes)')
    p4 = re.compile('(?i)^(This method was generated by)')

    if raw_comment is not None:
        if p1.search(raw_comment):
            return True

    if p2.search(comment) or p3.search(comment) or p4.search(comment):
        return True
    else:
        return False


def if_AutoCode_by_code(raw_code, language='java'):
    code_list = [t.strip() for t in raw_code.strip().split('\n')]
    first_code = code_list[0]
    p1 = re.compile(' toString\(')
    p2 = re.compile('([ _]test[A-Z_(])|([a-z_ ]Test[A-Z_(])')
    p3 = re.compile(' [a-zA-Z_]*Constructor[s]?\(')
    p4 = re.compile(' (set|get)[A-Z][a-zA-Z_]+\(')

    p5 = re.compile('__str__')
    if language == 'java':
        if p1.search(first_code) or p2.search(first_code) or p3.search(first_code):
            return True
        elif p4.search(first_code) and len(code_list) <= 3:
            return True
        else:
            return False
    elif language == 'python':
        if p2.search(first_code) or p5.search(first_code):
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    # test
    raw_comment = "\t/**\n\t * Returns the high-value (as a double primitive) \n\t * for an item within a series.\n\t " \
                  "* \n\t * @param series\n\t * @param item \n\t * @return The high-value.\n\t */\n "
    print(raw_comment)
    print(getFirstSentence(raw_comment))

    raw_comment = "\t/**\n\t * Creates a new adapter for an object of class '{@link " \
                  "org.jsenna.eclipse.schema.dictionary.AbstractDataGroup <em>Abstract Data Group</em>}'.\n\t * <!-- " \
                  "begin-user-doc -->\n\t * This default implementation returns null so that we can easily ignore " \
                  "cases;\n\t * it's useful to ignore a case when inheritance will catch all the cases anyway.\n\t * " \
                  "<!-- end-user-doc -->\n\t * @return the new adapter.\n\t * @see " \
                  "org.jsenna.eclipse.schema.dictionary.AbstractDataGroup\n\t * @generated\n\t */\n "
    comment = getFirstSentence(raw_comment)
    print(comment)
    print(if_ContentTamper(comment))

    raw_comment = "/**\n     * relayTbList\u3068\u306e\u5916\u90e8\u7d50\u5408\u3092\u30c6\u30b9\u30c8\u3057\u307e" \
                  "\u3059\u3002\n     * \n     * @throws Exception\n     */\n "
    comment = getFirstSentence(raw_comment)
    print(comment)
    print(if_NonLiteral(comment))


    raw_code = "\tpublic void\n\tpreinitPage() { }\n"
    print(raw_code)
    print(if_EmptyFunc(raw_code))

    raw_code = "    //    public String transformTypeID(URI typeuri) {\n    //\treturn typeuri.toString();\n    //    }\n"
    print(raw_code)
    print(if_CommentedOut(raw_code))

    raw_code = "\tpublic int compareTo(Inparalog inpara) {\n\t\t// sort by 2 digits after .\n\t\treturn (int) (inpara.confidence * 100 - confidence * 100);\n\t}\n"
    print(raw_code)
    print(if_CommentedOut(raw_code))
    print(if_BlockComment(raw_code))

