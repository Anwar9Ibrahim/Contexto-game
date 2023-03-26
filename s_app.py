import streamlit as st
from game import environment
import pandas as pd
import numpy as np

from PIL import Image


import datetime

englishContexto= environment()

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
        st.write('You selected:', languageOption)
        return 
    elif (languageOption== 'English'):
        guessesPath= "D:\\projectContexto\\contextoApp\\guesses.txt"
        
        EnglishForm(guessesPath)
        return
    else:
        st.write('You selected:', languageOption)
        return

def ArabicForm():
    return 

def RussianForm():
    return

def EnglishForm(guessesPath):
    Englishcontainer = st.container()

    
    guess= Englishcontainer.text_input("Please enter your guess:", "type a word")

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
        #check the simiarity
        englishContextoDone=False
        #                                                                                           for final
        englishContextoSimilarity, englishContextoDone= checkSimilarity(guess) #np.random.randint(10) , englishContextoDone #9 , False using the model

        guessWrite= guess+  " , " + str(englishContextoSimilarity*0.1)
        #remove for final
        #if englishContextoSimilarity ==9:
        #    englishContextoDone=True

        if not englishContextoDone:
            
            if type(guess)== str:
                st.write("the guessed word is: " ,guess)
            else:
                st.write("Please enter a valid word")
            if st.button('Give Up'):
                st.write(englishContexto.giveup())
            show(englishContextoDone, guessesPath, guessWrite)
            
        else:

            st.write("**Congratulations you guessed the secret word**  refresh this page to replay")
            st.balloons()
            show(englishContextoDone, guessesPath, guessWrite)
            f = open(guessesPath, "w")
            f.write("Words , Similarities \n")
            f.close() 
                  
    return 


def color(x):
    cold= 0
    worm= 0.4
    hot= 0.7
    print(x[1])
    if  x[1]>= cold and x[1]<= worm :
        return ['background-color : #e81e80']*len(x)
    elif x[1]> worm and x[1]<= hot:
        return ['background-color : #Ea7051']*len(x)
    elif x[1]> hot:
        return ['background-color : #73f181']*len(x)
 
    
def show(englishContextoDone, guessesPath, guessWrite):
    #show the guessed words so far

    f = open(guessesPath, "a")
    f.write(guessWrite+ "\n")
    f.close() 

    #read from the file
    pdguessed= pd.read_csv(guessesPath, sep=",", header=0)

    #drop duplicates 
    pdguessed = pdguessed.drop_duplicates()
    
    #sort by similarities
    sortedGuesses=pdguessed.sort_values(by=[pdguessed.keys()[1]], ascending=False) 
    #show 
    st.dataframe(sortedGuesses.style.apply(color, axis=1), use_container_width=True)
        

#environment functions

def checkSimilarity(guess):
    englishContexto.act(guess)  
    return englishContexto.reward, englishContexto.done



#main code



formCreation()


