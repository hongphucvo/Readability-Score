# write your code here
import re
import math
import argparse



class Counting:
    def __init__(self, text,norm_list):
        sentences=len(text)
        words=0
        characters=sentences-1
        syllables=0
        polysyllables=0
        diff_words= 0
        if(text[sentences-1]==""):
            sentences-=1
        vowel=['a','e','i','u','o','y']
        for line in text:
            sent_of_word=line.split()
            words+=len(sent_of_word)
            for w in sent_of_word:
                characters+=len(w)
                w=w.replace(',','').replace(')','').replace('(','')
                if(w.lower() not in norm_list):
                    diff_words+=1
                #syllables
                vol_in_word=0
                if(w[0] in vowel): vol_in_word+=1
                if(w[-1]=='e'):
                    if(w[-2] not in vowel or w[-2]):
                        vol_in_word-=1

                for index in range (1,len(w)):
                    if(w[index] in vowel and w[index-1] not in vowel):
                        vol_in_word+=1
                if(vol_in_word==0):vol_in_word+=1
                elif(vol_in_word>2):polysyllables+=1
                syllables+=vol_in_word
        #return
        self.sentences=sentences
        self.words=words
        self.characters=characters
        self.syllables=round(syllables+5,-1)
        self.polysyllables=polysyllables
        self.diff_words=diff_words

#SCORING
def ARI(data):
    val= 4.71*data.characters/data.words+0.5*data.words/data.sentences-21.43
    age=ari_age(val)
    print("Automated Readability Index:",round(val-0.005,2), "(about",str(age)+"-year-olds)")
    return age
def FKRT(data):
    val = 0.39*data.words/data.sentences+11.8*data.syllables/data.words-15.59
    age=ari_age(val)
    print("Flesch–Kincaid readability tests:",round(val-0.005,2), "(about",str(age)+"-year-olds)")
    return age
def SMOG(data):
    val = 1.043 * math.sqrt(data.polysyllables*30/data.sentences)+3.1291
    age=ari_age(val)
    print("Simple Measure of Gobbledygook:",round(val-0.005,2), "(about",str(age)+"-year-olds)")
    return age
def CLI(data):
    val= 0.0588*data.characters/data.words*100-0.298*100*data.sentences/data.words-15.8
    age=ari_age(val)
    print("Coleman–Liau index:",round(val-0.005,2), "(about",str(age)+"-year-olds)")
    return age
def PB(data):
    val=0.1579*data.diff_words/data.words*100+0.0496*data.words/data.sentences
    if(data.diff_words/data.words>0.05): val+=3.6365
    age=dif_age(round(val,1))
    print("Probability-based score:",round(val-0.005,2), "(about",str(age)+"-year-olds)")
    return age

#OUTPUT
def overall(stat):
    print("Words:",stat.words)
    print("Difficult words:",stat.diff_words)
    print("Sentences:",stat.sentences)
    print("Characters:",stat.characters)
    print("Syllables:",stat.syllables)
    print("Polysyllables:",stat.polysyllables)

def ari_age(score):
    if(score<3): return int(score+5)
    elif(score<13): return int(score+6)
    elif(score==13): return 24
    else: return 25
def dif_age(score):
    if(score<=4.9): return 10
    elif(score<9): return int(2* score)
    elif(score<10):return 24
    else: return 25

def display(method,stat):
    if(method=="ARI"): ARI(stat)
    elif(method=="FK"): FKRT(stat)
    elif(method=="SMOG"): SMOG(stat)
    elif(method=="CL"): CLI(stat)
    elif(method=="PB"): PB(stat)
    else:
        sum=ARI(stat)+FKRT(stat)+SMOG(stat)+CLI(stat)+PB(stat)
        avg_age=sum/5
        print("\n This text should be understood in average by",str(avg_age)+"-year-olds.")

def main():

    parser = argparse.ArgumentParser()
    #READ THE INFILE
    parser.add_argument('--infile', type=argparse.FileType('r'), default=1.0)
    parser.add_argument('--words', type=argparse.FileType('r'), default=1.0)
    args = parser.parse_args()
    text=args.infile.read()
    word_list=args.words.read().split()
    args.infile.close()
    args.words.close()

    #Statistics
    stop_punc="\.|\!|\?|'\n'"
    sent=re.split(stop_punc,text)
    stat= Counting(sent,word_list)
    overall(stat)
    #method print
    print("Enter the score you want to calculate (ARI, FK, SMOG, CL, all):")
    method=str(input())
    display(method,stat)

if __name__ == "__main__":
    main()
