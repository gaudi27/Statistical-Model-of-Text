#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
"""
Created on Sun Dec  4 18:40:08 2022

@author: gaudi
"""


def clean_text(txt):
    '''cleans the given text by removing puncuation'''
    words = txt.split()
    for i in range(len(words)):
        for symbol in """.,?"'!;:""":
            if symbol in words[i]:
                words[i]= words[i].replace(symbol, '')
            words[i]= words[i].lower()
    return words


def stem(s):
    '''root part of the word, which excludes any 
    prefixes and suffixes.'''
    if s[-1] == 's':
        s = s[:-1]
    if len(s) > 3:
        if s[-3:] == 'ate':
            s = s[:-3]
        elif s[-3:] == 'ies':
            s = s[:-3]
        elif s[-1] == 'y':
            s = s[:-1] + 'i'
        elif s[-4:] == 'ship':
            s = s[:-4]
        elif s[-2:] == 'er':
            if len(s)>3:
                if s[-3] == s[-4]:
                    s = s[:-3]
                else:
                    s = s[:-2]
        elif s[-1] == 'e':
            s = s[:-1]
    return s
        


def compare_dictionaries(d1, d2):
    '''compares the d1 and d1 dictionarys'''
    if d1 == {}:
        return -50
    score = 0
    total = 0
    for i in d1:
        total += d1[i]
    for i in d2:
        if i not in d1:
            score += math.log(.5 / total) * d2[i]
        else:
            score += math.log(d1[i] / total) * d2[i]
    return score

class TextModel:
    
    
    
    
    def __init__(self, model_name):
        '''constructs a new TextModel object by 
        accepting a string model_name as a parameter'''
        
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.questions = {}
        

    

    def __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of questions: ' + str(len(self.questions))
        return s



    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """
        
        y = 0
        z = 0
        word_list = clean_text(s)
        s_length = s.split()
        for w in word_list:
            i = len(w)
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
            if i in self.word_lengths:
                self.word_lengths[i] += 1
            else:
                self.word_lengths[i] = 1
            if w[-1] not in '?':
                self.questions[w[-1]] = 1
            else:
                self.questions[w[-1]] += 1
            if w in self.stems:
                self.stems[stem(w)] += 1
            else:
                self.stems[stem(w)] = 1
                
        for x in range(len(s_length)):
            if s_length[x][-1] =='.' or s_length[x][-1] =='!' or s_length[x][-1] =='?':
                z = x+1 - y
                y=x+1
                if z in self.sentence_lengths:
                    self.sentence_lengths[z] += 1
                else:
                    self.sentence_lengths[z] = 1
                
            
    def add_file(self, filename):
        '''adds all of the text in the file identified 
        by filename to the model'''
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()
    
        words = text.split()
    
        for word in words: 
            self.add_string(word)
                



    def save_model(self):
        """saves the TextModel object self by writing
        its various feature dictionaries to files
        """
        
        f = open(self.name + '_' + 'words', 'w')    
        f.write(str(self.words))              
        f.close()                
        
        g = open(self.name + '_' + 'word_lengths', 'w')     
        g.write(str(self.word_lengths))              
        g.close() 
        
        h = open(self.name + '_' + 'stems', 'w')     
        h.write(str(self.stems))              
        h.close() 
        
        i = open(self.name + '_' + 'sentence_lengths', 'w')     
        i.write(str(self.sentence_lengths))              
        i.close() 
        
        j = open(self.name + '_' + 'questions', 'w')     
        j.write(str(self.questions))              
        j.close() 


    def read_model(self):
        '''reads the stored dictionaries for the 
        called TextModel object from their files
        and assigns them to the attributes of the 
        called TextModel'''
        
        f = open(self.name + '_' + 'words', 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()

        self.words = dict(eval(d_str))      # Convert the string to a dictionary.

        g = open(self.name + '_' + 'word_lengths', 'r')    # Open for reading.
        d_str = g.read()           # Read in a string that represents a dict.
        g.close()

        self.word_lengths = dict(eval(d_str))      # Convert the string to a dictionary.
        
        h = open(self.name + '_' + 'stems', 'r')    # Open for reading.
        d_str = h.read()           # Read in a string that represents a dict.
        h.close()

        self.stems = dict(eval(d_str))      # Convert the string to a dictionary.
        
        i = open(self.name + '_' + 'sentence_lengths', 'r')    # Open for reading.
        d_str = i.read()           # Read in a string that represents a dict.
        i.close()

        self.sentence_lengths = dict(eval(d_str))      # Convert the string to a dictionary.
        
        j = open(self.name + '_' + 'questions', 'r')    # Open for reading.
        d_str = j.read()           # Read in a string that represents a dict.
        j.close()

        self.questions = dict(eval(d_str))      # Convert the string to a dictionary.
        
        
    def similarity_scores(self, other):
       '''gets the similarity scores for each feature'''
       word_score = compare_dictionaries(other.words, self.words)
       word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
       stems_score = compare_dictionaries(other.stems, self.stems)
       sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
       questions_score = compare_dictionaries(other.questions, self.questions)
       return [word_score, word_lengths_score, stems_score, sentence_lengths_score, questions_score]
        
    def classify(self, source1, source2):
        '''compares scores and says which source is more likley to be the correct one'''
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print(scores1)
        print(scores2)
        weighted_sum1 = 10*scores1[0] + 5*scores1[1] + 7*scores1[2] + 5*scores1[3] + 3*scores1[4]
        weighted_sum2 = 10*scores2[0] + 5*scores2[1] + 7*scores2[2] + 5*scores2[3] + 3*scores2[4]
        if weighted_sum1 > weighted_sum2:
            print(self.name + ' is more likely to have come from ' + source1.name)
        else:
            print(self.name + ' is more likely to have come from ' + source2.name)
        




def test():
    """ tester """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)    






def run_tests():
    """ your docstring goes here """
    source1 = TextModel('rowling')
    source1.add_file('JKRowling.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare.txt')

    new1 = TextModel('wr100')
    new1.add_file('wr100.txt')
    new1.classify(source1, source2)

    new2 = TextModel('inside_science')
    new2.add_file('inside_science.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('charles_Q_Chi')
    new3.add_file('CHARLES_Q_CHOI.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('WIRED')
    new4.add_file('WIRED.txt')
    new4.classify(source1, source2)





