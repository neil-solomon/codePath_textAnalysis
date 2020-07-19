"""
HashMap of Words
    word: {
        frequency: # sum of frequencyByChapter
        frequencyByChapter: [0,15,6] # a list of the word's frequency in each chapter of the book
        followedBy: [[word, chapter], [anotherWord,chapter]] # a list of all the words that follow this word and their chapters
    }

total number of words
    return sum of frequency for all words

number of unique words
    return len(words.keys())

20 most frequent words
    Make a maxHeap with max size of 20. Iterate through words and add each to the maxHeap.

20 most frequent words ingnoring x most common english words
    Make a maxHeap with max size of 20. Iterate through words and add each to the maxHeap if (word not in mostCommon).

20 least frequent words
    Make a minHeap with max size of 20. Iterate through words and add each to the minHeap.

return an array of the word frequency per chapter
    return words[word].frequencyByChapter

return the chapter(s) where a quote appears
    Take a string as input and turn it into a word array
    look for that quote[0] in the hashMap
    if that word is followed by quote[1] go to quote[1] in the hashMap
    repeat until quote[-1] is reached, return this chapter
    (track the chapter throughout the process)

generate a sentence 
    start with "The"
    Pick words["The"].followedBy[random]
    repeat until you have a 20 word sentence.


OPTIONAL
return the chapter(s) where a mis-quote appears
    Take a string as input and turn it into a word array
    Search the book for any permutation of this word array

make a trie out of the sentences of the book and create a sentence completion function

"""

import os
import re
import pprint
import random
import matplotlib.pyplot as plt
import heapq


class TextAnalyzer:
    def __init__(self, folder=None):
        self.words = {}
        self.totalNumberOfWords = 0
        self.totalUniqueWords = 0
        self.numChapters = 0
        self.mostFrequentWords = []
        self.leastFrequentWords = []
        self.filepath = ""

        if folder is not None:
            self.buildWordMap(folder)
            self.buildMinMaxWordHeaps()

        
    def buildWordMap(self, filepath):
        """
        'filepath' is a string which specifies the filepath to a folder. This folder
        contains a txt file for each chapter of the book.
        """
        self.filepath = filepath

        for root, directories, files in os.walk(filepath):
            self.numChapters = len(files)

            for filename in files:
                chapterNumber = int(re.findall(r'\d+', filename)[0])

                with open(filepath + "/" + filename) as chapterFile:
                    chapterWords = chapterFile.read().replace('\n', ' ') \
                        .replace('"', '').replace('.','').replace('!','') \
                        .replace('?','').replace(',','').replace(':','') \
                        .replace('--'," ").replace('_'," ").split(" ")

                    for i in range(len(chapterWords)):
                        if chapterWords[i] != " " and chapterWords[i] != "":
                            if chapterWords[i] not in self.words:
                                self.totalUniqueWords += 1
                                self.words[chapterWords[i]] = {
                                    "frequency" : 0,
                                    "frequencyByChapter" : [0] * self.numChapters,
                                    "followedBy" : []
                                }

                            self.words[chapterWords[i]]["frequencyByChapter"][chapterNumber] += 1
                            self.words[chapterWords[i]]["frequency"] += 1
                            self.totalNumberOfWords += 1
                            
                            if i != len(chapterWords) - 1 and chapterWords[i+1] != " " and chapterWords[i+1] != "":
                                self.words[chapterWords[i]]["followedBy"].append([chapterWords[i+1], chapterNumber])
    
    
    def buildMinMaxWordHeaps(self):
        for word in self.words:
            heapq.heappush(self.mostFrequentWords, [-1 * self.words[word]["frequency"], word])
            heapq.heappush(self.leastFrequentWords, [self.words[word]["frequency"], word])


    def getTotalNumberOfWords(self):
        return self.totalNumberOfWords


    def getTotalUniqueWords(self):
        return self.totalUniqueWords

    
    def get20MostFrequentWords(self):
        maxHeapCopy = []
        for word in self.mostFrequentWords:
            maxHeapCopy.append([ word[0], word[1] ])

        mostFrequentWords = []

        for i in range(20):
            mostFrequentWords.append(heapq.heappop(maxHeapCopy))

        for word in mostFrequentWords:
            word[0] *= -1

        return mostFrequentWords


    def get20MostInterestingFrequentWords(self, numWords=100):
        """
        Returns a list of 2-element-lists of the 20 most frequently used words, 
        along with the word's frequency. Ignores the 'numWords' most frequently used English words.
        """

        mostFrequentEnglishWords = self.getMostFrequentEnglishWords(numWords)

        maxHeapCopy = []
        for word in self.mostFrequentWords:
            maxHeapCopy.append([ word[0], word[1] ])

        mostFrequentWords = []
        while len(mostFrequentWords) < 20:
            word = heapq.heappop(maxHeapCopy)
            if word[1].lower() not in mostFrequentEnglishWords and word[1] not in mostFrequentEnglishWords:
                word[0] *= -1
                mostFrequentWords.append(word)

        return mostFrequentWords

    
    def get20LeastFrequentWords(self):
        """
        Returns a list of 2-element-lists of the 20 words with the lowest frequency,
        along with the word's frequency.
        If more than 20 words have a frequency of 1, 20 words of frequency 1 are randomly chosen.
        """

        minHeapCopy = []
        for word in self.leastFrequentWords:
            minHeapCopy.append([ word[0], word[1] ])

        count = 0
        leastFrequentWords = []
        while minHeapCopy[0][0] == 1 or count < 20:
            leastFrequentWords.append(heapq.heappop(minHeapCopy))
            count += 1

        if len(leastFrequentWords) == 20:
            return leastFrequentWords

        leastFrequentWordsEdited = []
        while len(leastFrequentWordsEdited) < 20:
            index = random.randrange(0, len(leastFrequentWords))
            leastFrequentWordsEdited.append(leastFrequentWords[index])
            leastFrequentWords.pop(index)

        return leastFrequentWordsEdited

    
    def getFrequencyOfWord(self, word):
        if word not in self.words:
            return [0]*len(self.numChapters)
        
        return self.words[word]["frequencyByChapter"]


    def getChapterQuoteAppears(self, quote):
        """
        Returns a list of chapters that contain the quote.
        """

        for root, directories, files in os.walk(self.filepath):
            self.numChapters = len(files)

            for filename in files:
                chapterNumber = int(re.findall(r'\d+', filename)[0])

                with open(self.filepath + "/" + filename) as chapterFile:
                    chapter = chapterFile.read().replace('\n', ' ')

                    if quote in chapter:
                        chapters.append(chapterNumber)
        
        return chapters
            

    def generateSentence(self):
        sentence = ["The"]
        
        for i in range(19):
            if len(self.words[sentence[-1]]["followedBy"]) == 0:
                break
            ix = random.randrange(0, len(self.words[sentence[-1]]["followedBy"]))
            sentence.append(self.words[sentence[-1]]["followedBy"][ix][0])

        sentence = " ".join(sentence) + "."
        return sentence

    
    def findClosestMatchingQuote(self, quote):
        """
        Returns the closet quote along with its chapter.

        1. Go through each chapter of the book.
        2. Scan chunks of words of size 2*len(quote).
        3. Give the chunk a score based on how similar it is to the quote.
        4. Return the chunk with the highest score along with its chapter.
        """

        quoteList = quote.lower().replace('"', '').replace('.','') \
            .replace('!','').replace('?','').replace(',','').replace(':','') \
            .replace('--'," ").replace('_'," ").split(" ")

        bestMatchingQuote = [-1, -1, "fooBar"] # bestMatchingQuote is [score, chapter, quote]

        for root, directories, files in os.walk(self.filepath):
            self.numChapters = len(files)

            for filename in files:
                chapterNumber = int(re.findall(r'\d+', filename)[0])

                with open(self.filepath + "/" + filename) as chapterFile:
                    chapterWords = chapterFile.read().replace('\n', ' ')

                    start = 0
                    end = 2*len(quote) - 1
                    count = 0
                    while end < len(chapterWords):
                        wordChunk = chapterWords[start : end]
                        wordChunkList = wordChunk.lower().replace('"', '').replace('.','') \
                            .replace('!','').replace('?','').replace(',','').replace(':','') \
                            .replace('--'," ").replace('_'," ").split(" ")
                        
                        wordChunkScore = 0

                        for i in range(len(quoteList)):
                            if quoteList[i] in wordChunkList:
                                wordChunkScore += 1
                            if i < len(wordChunkList) and quoteList[i] == wordChunkList[i]:
                                wordChunkScore += 2

                        if wordChunkScore > bestMatchingQuote[0]:
                            bestMatchingQuote = [wordChunkScore, wordChunk, chapterNumber]

                        start += 1
                        end += 1
                        count += 1

        return [bestMatchingQuote[1], bestMatchingQuote[2]]


    def printWordMap(self):            
        pprint.PrettyPrinter(indent=2).pprint(self.words)


    def plotFrequencyOfWords(self, words):
        x_axis = [x for x in range(self.numChapters)]
        y_axes = []
        
        for word in words:
            y_axes.append(self.words[word]["frequencyByChapter"])

        for y in y_axes:
            plt.plot(x_axis, y)

        plt.xlabel("Chapter")
        plt.ylabel("Frequency")
        plt.title("Frequency of Words",
          fontdict={'fontweight': 'bold'})
        plt.legend(words)

        plt.show()


    def getMostFrequentEnglishWords(self, numWords):
        """
        Returns a list of length 'numWords' of the most frequently used English words.
        List of words courtesy of https://gist.github.com/deekayen/4148741
        """

        mostFrequentWords = []

        with open("mostCommonWords.txt") as file:
            while len(mostFrequentWords) < numWords:
                mostFrequentWords.append(file.readline().replace("\n", ""))

        return mostFrequentWords



class SentenceTrieNode:
    def __init__(self, word=""):
        self.word = word
        self.endsSentence = False
        self.children = []


    def indexOfChild(self, word):
        if word in self.children:
            return self.children.index(word)

        return -1


    def addChild(self, word):
        self.children.append(SentenceTrieNode(word))



class SentenceTrie:
    def __init__(self):
        self.head = SentenceTrieNode()
        self.numWords = 0
        self.numSentences = 0


    def print(self):
        for child in self.head.children:
            self.print_helper(child, "")
        print()

    
    def print_helper(self, currentNode, sentence):
        sentence += currentNode.word + " "

        if len(currentNode.children) == 0:
            print(sentence)
        
        else:
            if currentNode.endsSentence:
                print(sentence)
            
            for child in currentNode.children:
                self.print_helper(child, sentence)

    
    def add(self, sentence):
        sentence = sentence.replace("\n"," ").split(" ")
        currentNode = self.head

        for i in range(len(sentence)):
            childIx = currentNode.indexOfChild(sentence[i])
            
            if childIx == -1:
                currentNode.addChild(sentence[i])
                currentNode = currentNode.children[len(currentNode.children)-1]
                
                if i == len(sentence)-1:
                    currentNode.endsSentence = True
                
                self.numWords += 1

            else:
                currentNode = currentNode.children[childIx]
                
                if i == len(sentence)-1:
                    currentNode.endsSentence = True


    def finishSentence(self, sentence):
        """
        Returns a list of all the sentences that start with 'sentence'.
        Returns None if no sentences start with 'sentence'.
        """
        sentenceList = sentence.replace("\n"," ").split(" ")
        currentNode = self.head

        for word in sentenceList:
            childIx = currentNode.indexOfChild(word)

            if(childIx == -1):
                return None
            
            currentNode = currentNode.children[childIx]
        
        if len(currentNode.children) == 0:
            return [sentence]
        
        childSentences = self.getChildSentences(currentNode)

        


if __name__ == "__main__":
    # myBook = TextAnalyzer("./ThePictureOfDorianGray")

    # print("Number of words:" , myBook.getTotalNumberOfWords())
    # print("Number of unique words:" , myBook.getTotalUniqueWords())
    # print("Most Frequent words:" , myBook.get20MostFrequentWords())
    # print("Most Frequent words(100):" , myBook.get20MostInterestingFrequentWords())
    # print("Most Frequent words(300):" , myBook.get20MostInterestingFrequentWords(300))
    # print("Least frequent words:" , myBook.get20LeastFrequentWords())
    # print("Chapter frequency of 'Dorian':" , myBook.getFrequencyOfWord("Dorian"))
    # print("Chapter of quote 'Dorian Gray'", myBook.getChapterQuoteAppears("Dorian Gray"))
    # print("Chapter of quote 'Dorian Gray is'", myBook.getChapterQuoteAppears("Dorian Gray is"))
    # print("Chapter of quote 'Dorian Gray is to me simply a motive in art.'",
    #     myBook.getChapterQuoteAppears("Dorian Gray is to me simply a motive in art.")
    # )
    # print("Generated sentence:" , myBook.generateSentence())
    # print(myBook.findClosestMatchingQuote("eternal pathos of the human tragedy"))

    sentences = SentenceTrie()
    sentences.add("hello world!")
    sentences.add("hello everyone in the world?")
    sentences.add("hello world everywhere...")
    sentences.add("hello, world")
    sentences.print()

    # myBook.plotFrequencyOfWords(["young", "old", "life", "death"])