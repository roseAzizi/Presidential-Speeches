import pandas as pd 
import json  
import re 

def main(): 
    # creating the speeches df and cleaning it up a little bit (removing urls panel and stuff)
    df = pd.read_json("/Users/rose/Desktop/speech_project/allSpeech.json") 
    df = df.drop("url", axis = 'columns')  
    df.insert(4, "Flesch–Kincaid Score", '')  
    df.insert(5, "cleaned speech", '') 
    # new smaller df for testing purposes when writing script. Subset of larger df 
    bbDf = df.loc[986:988]   
    FleschScore(bbDf).to_csv('test.csv', index=False) 
  

    
def FleschScore(speechDF):   
    # score is given by: 206.835-1.015(total_words/total_sentences)-84.6(total_syllables/total_words) 

    for index, row in speechDF.iterrows(): 
        #cleanup
        cleaned_speech = SpeechCleanup(row['transcript'])
        speechDF.at[index,"cleaned speech"] = cleaned_speech
        #count the words in a given speech 
        word_count = len(cleaned_speech.split())
        #then, count the sentences in a given speech  
        punctuation = re.compile(r"\.\.\.|\.|\!|\?") 
        sentence_count = len(punctuation.findall(cleaned_speech))
        #then the total syllables 

        #apply the formula and return the flesch score

    return speechDF
def SpeechCleanup(speech):  
    # it should be noted that many live speeches are interjected audience reactions, or different speakers. 
    # as such, any words/phrases in paraenthesis (usually just applause or laughter) or in all caps
    # followed by a ":" will be cleaned up

    speech = re.sub(r'\(.*?\)', '', speech)
    #this pattern identifies string bits of ALL CAP phrases followed by a ":" 
    pattern = r'([A-Z][A-Z\s\.]*:)'  
    matches = list(re.finditer(pattern, speech)) 
    if matches:  
        #find numeric index of each match in the text
        speech_split = [match.start() for match in matches]  
        # get a list of of chat length in between each split
        split_char = [0] + speech_split + [len(speech)] 
        #generates segmented speech by speaker by slicing the text according to split_char characters 
        segments = [speech[split_char[i]:split_char[i + 1]] for i in range(len(split_char) - 1)] 
        for i, segment in enumerate(segments[:]): 
            if not segment.startswith('THE PRESIDENT'): 
                segments.remove(segment) 
        segments = [segment[14:] for segment in segments]
        speech = ' '.join([str(segment) for segment in segments])
    return speech

def SyllableCount(speech): 
    #will do later, in seperate project






    


if __name__ == "__main__":
    main()

