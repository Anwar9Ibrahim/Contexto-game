import streamlit as st
import pandas as pd
import numpy as np

from Game import Analyzer

import torch
import torch.nn.functional as f

from transformers import BertModel, BertTokenizer

from time import sleep

import os



#forms functions

def formCreation():
    

    st.header('Contexto')

    languages= ( 'English', 'русский', 'العربية')
   
    chooseform(languages)

    return




def chooseform(languages):
    languageOption = st.selectbox(
        'please select your language',
        languages)
    
    if (languageOption== 'العربية'):
        directory = os.getcwd()
        guessesPath= directory + "\\guesses.txt"
        ArabicContexto = createArabicEnviroment()
        ArabicForm(guessesPath,ArabicContexto)
        return 
    
    
    elif (languageOption== 'English'):
        directory = os.getcwd()
        guessesPath= directory + "\\guesses.txt"
        englishContexto= createEnglishEnvironment()
        EnglishForm(guessesPath, englishContexto)
        return
    else:

        directory = os.getcwd()
        guessesPath= directory + "\\guesses.txt"
        RussianContexto = createRussianEnviroment()
        RussianForm(guessesPath,RussianContexto)
        return

#Forms
def ArabicForm(guessesPath,ArabicContexto):
    Arabiccontainer = st.container()
    guess= Arabiccontainer.text_input("رجاء: أدخل كلمة للتخمين", "type a word")
    guess= guess.strip()
    
    if guess == "type a word":
        Arabiccontainer.info(""" **كيفية اللعب:**
        لديك عدد غير محدود من التخمينات لتتمكن من العثور على الكلمة السرية:
        تم ترتيب الكلمات عن طريق خوارزمية ذكاء صنعي وفقاً لمدى التقارب بين الكلمة السرية والتخمينات.
        بعد اختيارك للتخمين سترى مدى قرب التخمين من الكلمة السرية، حيث تمتلك الكلمة السرية القيمة 1 وتقل هذه القيمة كلما كان التخمين بعيد عن الكلمة السرية.""")

        f = open(guessesPath, "w")
        f.write("Words , Similarities \n")
        f.close() 
    
    else:
        
        arabicContextoDone=False
        _ ,arabicContextoSim, arabicContextoDone, new_target_arabic= checkSimilarity(guess, ArabicContexto)         
        guessWrite= guess+  " , " + str(arabicContextoSim*1)      

    
        if not arabicContextoDone:
            if arabicContextoSim== (-1000):
                st.write(" الكلمة "+ guess+" غير موجودة")
                show( guessesPath, guessWrite=None)
            else:
                show( guessesPath, guessWrite)
            if st.button('Give Up'):
                st.write(ArabicContexto.giveup())            
        else:
            st.write("**مبارك: لقد استطعت تخمين الكلمة الصحيحة**")
            st.balloons()
            setNewTarget("Arabic", new_target_arabic)
            show( guessesPath, guessWrite)
            f = open(guessesPath, "w")
            f.write("Words , Similarities \n")
            f.close() 
    
    return 

def RussianForm(guessesPath,RussianContexto):
    
    Russiancontainer = st.container()
    guess= Russiancontainer.text_input("Пожалуйста, введите свое предположение:", "type a word")
    guess= guess.strip()

    if guess == "type a word":
        Russiancontainer.info(""" **как играть:**  
        Найди секретное слово. У вас есть неограниченное количество догадок.  
        Слова были отсортированы с помощью алгоритма искусственного интеллекта в соответствии с тем, насколько они были похожи на секретное слово.  
        После отправки слова вы увидите его позицию. Секретное слово - это цифра 1.  
        Алгоритм проанализировал тысячи текстов. Он использует контекст, в котором используются слова, для вычисления сходства между ними.""")

        f = open(guessesPath, "w")
        f.write("Words , Similarities \n")
        f.close() 
        f = open(guessesPath, "w")
        f.write("Words , Similarities \n")
        f.close() 
    
    else:

        russianContextoDone=False
        _ ,russianContextoSim, russianContextoDone, new_target_Russian= checkSimilarity(guess, RussianContexto) 
        guessWrite= guess+  " , " + str(russianContextoSim*1)
    
        if not russianContextoDone:
            if russianContextoSim== (-1000):
                st.write("Это слово "+ guess+" не существует")
                show( guessesPath, guessWrite=None)
            else:
                show( guessesPath, guessWrite)
            if st.button('Give Up'):
                st.write(RussianContexto.giveup())            
        else:
            st.write("**Поздравляем, вы угадали секретное слово**")
            st.balloons()
            setNewTarget("Russian", new_target_Russian)
            show( guessesPath, guessWrite)
            f = open(guessesPath, "w")
            f.write("Words , Similarities \n")
            f.close() 
    
    return


def EnglishForm(guessesPath, englishContexto):
    Englishcontainer = st.container()

    guess= Englishcontainer.text_input("Please enter your guess:", "type a word")
    guess= guess.strip()
    #guess= "agricultural"
    

    if guess == "type a word":
        Englishcontainer.info("""**how to play:**  
        Find the secret word. You have unlimited guesses.  
        The words were sorted by an artificial intelligence algorithm according to how similar they were to the secret word.  
        After submitting a word, you will see its position. The secret word is number 1.  
        The algorithm analyzed thousands of texts. It uses the context in which words are used to calculate the similarity between them.""")

        f = open(guessesPath, "w")
        f.write("Words , Similarities \n")
        f.close() 

    else:
        englishContextoDone=False
        _ ,englishContextoSimilarity, englishContextoDone, new_target_English= checkSimilarity(guess, englishContexto)
        if type(englishContextoSimilarity) != int:
            guessWrite= guess+  " , " + str(englishContextoSimilarity*1)
    
        if not englishContextoDone:
            if englishContextoSimilarity== (-1000):
                st.write("The word "+ guess+" doesent exist")
                show( guessesPath, guessWrite=None)
            else:
                show( guessesPath, guessWrite)

            if st.button('Give Up'):
                st.write(englishContexto.giveup())            
        else:
            st.write("**Congratulations you guessed the secret word**")
            st.balloons()
            setNewTarget("English", new_target_English)
            show( guessesPath, guessWrite)
            f = open(guessesPath, "w")
            f.write("Words , Similarities \n")
            f.close() 
                
    return 


def color(x):
    cold= 0
    worm= 0.65
    hot= 0.8
    amount = x[1]

    if  amount >= cold and amount<= worm :
        return ['background-color : #e81e80']*len(x)
    elif amount> worm and amount<= hot:
        return ['background-color : #Ea7051']*len(x)
    elif amount > hot:
        return ['background-color : #73f181']*len(x)
 
    
def show( guessesPath, guessWrite):
    if guessWrite != None:

        f = open(guessesPath, "a",encoding="utf-8")
        f.write(guessWrite+ "\n")
        f.close() 

    pdguessed= pd.read_csv(guessesPath, sep=",", header=0)
    pdguessed = pdguessed.drop_duplicates()
    sortedGuesses=pdguessed.sort_values(by=[pdguessed.keys()[1]], ascending=False) 
    st.dataframe(sortedGuesses.style.apply(color, axis=1), use_container_width=True)
        

#environment functions

def setNewTarget(language, new_taregt):
    directory = os.getcwd()
    targetPath = directory +"\\"+language+"Target.txt"
    f = open(targetPath, "w",encoding="utf-8")
    f.write(new_taregt)
    f.close() 

def checkSimilarity(guess , contexto):
    contexto.act(guess)
    if torch.is_tensor(contexto.reward):
        contexto.reward = contexto.reward.item()
    return contexto.observations, contexto.reward, contexto.done, contexto.new_target

#####English########


def createEnglishEnvironment():
    bert_model_name= "bert-base-multilingual-cased"
    directory= os.getcwd()
    wordsPath= directory + "\\nouns_.txt"
    available_words=[line.strip() for line in open(wordsPath, 'r')]
    targetPath= directory + "\\EnglishTarget.txt"
    targetFile = open(targetPath, "r")
    target = targetFile.read()
    targetFile.close()
    print (target)    
    embed_calc = Analyzer(similarity_func=torch.nn.CosineSimilarity(),bert_version= bert_model_name,available_words = available_words,target= target)
    return embed_calc


####### arabic ######
def createArabicEnviroment():
    bert_model_name = 'asafaya/bert-base-arabic'
    directory = os.getcwd()
    wordsPath = directory + "\\arabic_nouns.txt"
    
    available_words=[line.strip() for line in open(wordsPath, 'r',encoding="utf8")]
    targetPath= directory + "\\ArabicTarget.txt"
    targetFile = open(targetPath, "r",encoding="utf8")
    target = targetFile.read()
    targetFile.close()
    print (target)   
    embed_calc = Analyzer(similarity_func=torch.nn.CosineSimilarity(),bert_version= bert_model_name,available_words = available_words,target= target)
    return embed_calc



####### Russian ########
def createRussianEnviroment():
    bert_model_name = 'DeepPavlov/rubert-base-cased'
    directory = os.getcwd()
    wordsPath = directory + "\\russian_nouns.txt"
    available_words=[line.strip() for line in open(wordsPath, 'r',encoding="utf8")]
    targetPath= directory + "\\RussianTarget.txt"
    targetFile = open(targetPath, "r",encoding="utf8")
    target = targetFile.read()
    targetFile.close()
    print (target)    
    embed_calc = Analyzer(similarity_func=torch.nn.CosineSimilarity(),bert_version= bert_model_name,available_words = available_words,target= target)
    return embed_calc


#main code

formCreation()




