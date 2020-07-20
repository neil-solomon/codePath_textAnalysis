import textAnalysis

if __name__ == "__main__":
    testBook = textAnalysis.TextAnalyzer("testBook")

    print("getTotalNumberOfWords()",
        testBook.getTotalNumberOfWords() == 109
    )

    print("getTotalUniqueWords()",
        testBook.getTotalUniqueWords() == 57
    )

    print("get20MostFrequentWords()",
        testBook.get20MostFrequentWords() == [[10, 'chapter'], [8, 'is'], [7, 'three'], [5, 'for'], [4, 'Three'], [4, 'the'], [3, 'I'], [3, 'Some'], [3, 'hope'], [3, 'one'], [3, 'text'], [3, 'this'], [2, 'And'], [2, 'Chapter'], [2, 'Hello'], [2, 'This'], [2, 'a'], [2, 'test'], [2, 'to'], [2, 'you']]
    )

    print("get20MostInterestingFrequentWords()",
        testBook.get20MostInterestingFrequentWords() == [[10, 'chapter'], [7, 'three'], [4, 'Three'], [3, 'hope'], [3, 'text'], [2, 'Chapter'], [2, 'Hello'], [2, 'test'], [1, 'Welcome'], [1, 'best'], [1, 'crowd'], [1, "e's"], [1, 'enjoyed'], [1, 'fantastic'], [1, 'favorite'], [1, 'finish'], [1, 'four'], [1, 'going'], [1, 'here'], [1, "it's"]]
    )

    print("get20LeastFrequentWords()",
        len(testBook.get20LeastFrequentWords()) == 20
    )

    print("getFrequencyOfWord('chapter')",
        testBook.getFrequencyOfWord("chapter") == [0, 4, 3, 2, 1]
    )

    print("getChapterQuoteAppears('my favorite chapter')",
        testBook.getChapterQuoteAppears("my favorite chapter") == [2]
    )

    print("generateSentence()", end = " ")
    try:
        testBook.generateSentence()
        print("True")
    except:
        print("False")
    

    print("findClosestMatchingQuote('favorite chapter is')",
        testBook.findClosestMatchingQuote("favorite chapter is") == ['favorite chapter. This is the best ch', 2]
    )

    print("finishSentence('Three is')", 
        testBook.finishSentence("Three is") == [['Three is a crowd ', 3], ['Three is a nice chapter ', 3]]
    )
