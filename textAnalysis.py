import os
import re
import pprint
import random
import matplotlib.pyplot as plt
import heapq


class TextAnalyzer:
    def __init__(self, filepath=None):
        self.words = {}     # word -> frequency
        self.sentences = SentenceTrie()
        self.totalNumberOfWords = 0
        self.totalUniqueWords = 0
        self.numChapters = 0
        self.mostFrequentWords = []     # max-heap of all words
        self.leastFrequentWords = []    # min-heap of all words
        self.filepath = filepath        # filepath to folder containing all chapters of the book
        self.fullText = []              # list of chapters of the book's full text

        if filepath is not None:
            self.readBook(filepath)


    def readBook(self, filepath):
        """
        Initializes the word map, sentence trie, mostFrequentWords heap, and leastFrequentWords heap.
        Filepath points to a folder which contains a txt file for each chapter in the book.
        Warning: There must be a chapter0
        """
        if filepath is None:
            return

        self.filepath = filepath
        
        for root, directories, files in os.walk(filepath):
            self.numChapters = len(files)
            self.fullText = [""] * self.numChapters

            for filename in files:
                chapterNumber = int(re.findall(r'\d+', filename)[0])

                with open(filepath + "/" + filename) as chapterFile:
                    chapterText = chapterFile.read().replace('\n', ' ')
                    self.fullText[chapterNumber] = chapterText
                    self.buildWordMap(chapterNumber, chapterText)
                    self.buildSentenceTrie(chapterNumber, chapterText)

        self.buildMinMaxWordHeaps()


    def buildWordMap(self, chapterNumber, chapterText):
        """
        Strips all punctuation from the text and adds every word to self.words
        """

        chapterWords = chapterText.replace('"', '').replace('.','').replace('!','') \
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
    

    def buildSentenceTrie(self, chapterNumber, chapterText):
        sentences = re.split('\? |\! |\. |\... |\?! |\?!', chapterText)

        for sentence in sentences:
            self.sentences.add(sentence.strip(), chapterNumber)

    
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

        i = 0 
        while i < len(maxHeapCopy) and i < 20:
            mostFrequentWords.append(heapq.heappop(maxHeapCopy))
            i += 1

        for word in mostFrequentWords:
            word[0] *= -1

        return mostFrequentWords


    def get20MostInterestingFrequentWords(self, numWords=100):
        """
        Returns a list of 2-element-lists of the 20 most frequently used words, 
        along with the word's frequency. Ignores the 'numWords' most frequently used English words.
        """

        if numWords > 1000:
            numWords = 100

        mostFrequentEnglishWords = self.getMostFrequentEnglishWords(numWords)

        maxHeapCopy = []
        for word in self.mostFrequentWords:
            maxHeapCopy.append([ word[0], word[1] ])

        mostFrequentWords = []
        while len(mostFrequentWords) < len(maxHeapCopy) and len(mostFrequentWords) < 20:
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
        while len(minHeapCopy) > 0 and (minHeapCopy[0][0] == 1 or count < 20):
            leastFrequentWords.append(heapq.heappop(minHeapCopy))
            count += 1

        if len(leastFrequentWords) <= 20:
            return leastFrequentWords

        leastFrequentWordsEdited = []
        while len(leastFrequentWordsEdited) < len(minHeapCopy) and len(leastFrequentWordsEdited) < 20:
            index = random.randrange(0, len(leastFrequentWords))
            leastFrequentWordsEdited.append(leastFrequentWords[index])
            leastFrequentWords.pop(index)

        return leastFrequentWordsEdited

    
    def getFrequencyOfWord(self, word):
        if word not in self.words:
            return [0] * self.numChapters
        
        return self.words[word]["frequencyByChapter"]


    def getChapterQuoteAppears(self, quote):
        """
        Returns a list of chapters that contain the quote.
        """

        chapters = []
        
        for i in range(len(self.fullText)):
            if quote in self.fullText[i]:
                chapters.append(i)
        
        return chapters
            

    def generateSentence(self):
        sentence = ["The"]
        
        for i in range(19):
            if sentence[i] not in self.words:
                break 

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

        bestMatchingQuote = [-1, -1, None] # bestMatchingQuote is [score, chapter, quote]

        for i in range(len(self.fullText)):
            start = 0
            end = 2*len(quote) - 1

            while end < len(self.fullText[i]):
                wordChunk = self.fullText[i][start : end]
                wordChunkList = wordChunk.lower().replace('"', '').replace('.','') \
                    .replace('!','').replace('?','').replace(',','').replace(':','') \
                    .replace('--'," ").replace('_'," ").split(" ")
                
                wordChunkScore = 0

                for j in range(len(quoteList)):
                    if quoteList[j] in wordChunkList:
                        wordChunkScore += 1
                    if j < len(wordChunkList) and quoteList[j] == wordChunkList[j]:
                        wordChunkScore += 2

                if wordChunkScore > bestMatchingQuote[0]:
                    bestMatchingQuote = [wordChunkScore, wordChunk, i]

                start += 1
                end += 1

        return [bestMatchingQuote[1], bestMatchingQuote[2]]


    def printWordMap(self):            
        pprint.PrettyPrinter(indent=2).pprint(self.words)


    def plotFrequencyOfWords(self, words):
        x_axis = [x for x in range(self.numChapters)]
        y_axes = []
        
        for word in words:
            if word in self.words:
                y_axes.append(self.words[word]["frequencyByChapter"])
            else:
                y_axes.append([0]*len(x_axis))

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


    def finishSentence(self, sentence):
        """
        Returns a list of all the sentences that start with 'sentence' along with their chapters.
        Returns None if no sentences start with 'sentence'.
        """
        sentenceList = sentence.replace("\n"," ").split(" ")
        currentNode = self.sentences.head

        for word in sentenceList:
            childIx = currentNode.indexOfChild(word)

            if(childIx == -1):
                return None
            
            currentNode = currentNode.children[childIx]
        
        if len(currentNode.children) == 0:
            return [sentence, -1]
        
        sentenceFinishers = []

        for child in currentNode.children:
            self.finishSentence_helper(child, sentence + " ", sentenceFinishers)

        return sentenceFinishers


    def finishSentence_helper(self, currentNode, sentence, sentenceFinishers):
        sentence += currentNode.word + " "

        if len(currentNode.children) == 0:
            sentenceFinishers.append([sentence, currentNode.chapterNumber])
        
        else:
            if currentNode.endsSentence:
                sentenceFinishers.append([sentence, currentNode.chapterNumber])
            
            for child in currentNode.children:
                self.finishSentence_helper(child, sentence, sentenceFinishers)



class SentenceTrieNode:
    def __init__(self, word="", chapterNumber=None):
        self.word = word
        self.endsSentence = False
        self.chapterNumber = chapterNumber
        self.children = []


    def indexOfChild(self, word):
        for i in range(len(self.children)):
            if self.children[i].word == word:
                return i

        return -1


    def addChild(self, word, chapterNumber=None):
        self.children.append(SentenceTrieNode(word, chapterNumber))



class SentenceTrie:
    def __init__(self):
        self.head = SentenceTrieNode()
        self.numWords = 0
        self.numSentences = 0


    def printSentences(self, node=None):
        if node is None:
            node = self.head

        for child in node.children:
            self.printSentences_helper(child, "")
        print()

    
    def printSentences_helper(self, currentNode, sentence):
        sentence += currentNode.word + " "

        if len(currentNode.children) == 0:
            print(sentence, currentNode.chapterNumber)
        
        else:
            if currentNode.endsSentence:
                print(sentence, currentNode.chapterNumber)
            
            for child in currentNode.children:
                self.printSentences_helper(child, sentence)

    
    def add(self, sentence, chapterNumber=None):
        sentence = sentence.split(" ")
        currentNode = self.head
        self.numSentences += 1

        for i in range(len(sentence)):
            childIx = currentNode.indexOfChild(sentence[i])

            if childIx == -1:
                currentNode.addChild(sentence[i], chapterNumber)
                currentNode = currentNode.children[len(currentNode.children)-1]
                
                if i == len(sentence)-1:
                    currentNode.endsSentence = True
                
                self.numWords += 1

            else:
                currentNode = currentNode.children[childIx]
                
                if i == len(sentence)-1:
                    currentNode.endsSentence = True
        


if __name__ == "__main__":
    myBook = TextAnalyzer("ThePictureOfDorianGray")

    print("Number of words:" , myBook.getTotalNumberOfWords())
    print("Number of unique words:" , myBook.getTotalUniqueWords())
    print("Most Frequent words:" , myBook.get20MostFrequentWords())
    print("Most Frequent words(100):" , myBook.get20MostInterestingFrequentWords())
    print("Most Frequent words(300):" , myBook.get20MostInterestingFrequentWords(300))
    print("Least frequent words:" , myBook.get20LeastFrequentWords())
    print("Chapter frequency of 'Dorian':" , myBook.getFrequencyOfWord("Dorian"))
    print("Chapter of quote 'Dorian Gray'", myBook.getChapterQuoteAppears("Dorian Gray"))
    print("Chapter of quote 'Dorian Gray is'", myBook.getChapterQuoteAppears("Dorian Gray is"))
    print("Chapter of quote 'Dorian Gray is to me simply a motive in art.'",
        myBook.getChapterQuoteAppears("Dorian Gray is to me simply a motive in art.")
    )
    print("Generated sentence:" , myBook.generateSentence())
    print(myBook.findClosestMatchingQuote("eternal pathos human tragedy"))
    print(myBook.finishSentence("Basil"))
    print(myBook.finishSentence("Basil had"))
    print(myBook.finishSentence("Basil had painted"))

    myBook.plotFrequencyOfWords(["love", "beautiful"])