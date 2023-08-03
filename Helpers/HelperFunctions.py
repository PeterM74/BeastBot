import Token
import random
import discord
import pandas as pd
from discord import app_commands
from discord.ext import commands
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer #,PorterStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from Helpers.LoadData import *

MotivationFileKey = fLoadData()

##### Plain text message parser
def fLoadMessageResponse(RawMessage):

    # Full message
    ## TODO: optimise by generating off sentence breakdown from below
    ResponseNLP = fParseResponseThroughNLP(RawMessage)

    # Message by sentence
    ResponseSentenceNLP = []
    SentenceTokens = sent_tokenize(RawMessage)
    for Sentence in SentenceTokens:
        ResponseSentenceNLP.append(fParseResponseThroughNLP(Sentence))

    # Parse message for key terms
    ## Motivation
    if (any(KeyTerms in ResponseNLP['MessageLemma'] for KeyTerms in ['motivate', 'motivation'])):
        # TODO: search for terms and add motivation response
        ## For now it just takes a random image
        ImageList = MotivationFileKey['ImageFile'].unique()
        Output = random.choice(ImageList)

        # Output result
        Output_dict = {}
        Output_dict["MessageType"] = "image"
        Output_dict["Output"] = str("MotivationImages/" + Output)

        return Output_dict

    ## Random exercise
    ### Look through each sentence for occurrence of key words. Store iteration
    RandomExerciseSentencei = -1
    for i in range(0, len(ResponseSentenceNLP)):
        if (any(KeyTerms in ResponseSentenceNLP[i]['MessageLemma'] for KeyTerms in ['choose', 'random']) &
        any(KeyTerms2 in ResponseSentenceNLP[i]['MessageLemma'] for KeyTerms2 in ['workout', 'exercise'])):
            RandomExerciseSentencei = i
            break

    if (RandomExerciseSentencei >= 0):
        MessageType = "text"
        ActivityChosen = fChooseExercise(Exclusions=ResponseSentenceNLP[i]['MessageLemma'])
        ResponseList = ["Hell yeah! Let's do " + ActivityChosen.lower() + " today."]  # TODO: fill out individual workout response list
        Output = random.choice(ResponseList)

        # Output result
        Output_dict = {}
        Output_dict["MessageType"] = "text"
        Output_dict["Output"] = Output

        return Output_dict

    if (('lord' in ResponseNLP['MessageLemma']) & ('prayer' in ResponseNLP['MessageLemma'])):
        Output_dict = {}
        Output_dict["MessageType"] = "text"
        Output_dict["Output"] = fLordsPrayer()

        return Output_dict

    ## Sentiment analysis
    ### Using pre-trained vader for now - not perfect for gym slang
    sentiment = SentimentIntensityAnalyzer()
    SentimentPolarity = sentiment.polarity_scores(RawMessage)
    SentimentPolScore = SentimentPolarity['compound']

    if (SentimentPolScore > 0.2):

        # Output result
        Output_dict = {}
        Output_dict["MessageType"] = "text"
        Output_dict["Output"] = fBeastBotGenericResponse("Positive")

        return Output_dict

    elif (SentimentPolScore < -0.2):
        # Output result
        Output_dict = {}
        Output_dict["MessageType"] = "text"
        Output_dict["Output"] = fBeastBotGenericResponse("Negative")

        return Output_dict


    ## No match found, return nothing
    Output_dict = {}
    Output_dict["MessageType"] = "NoInteraction"
    Output_dict["Output"] = ''

    return Output_dict

def fBeastBotGenericResponse(Polarity):
    PositiveRemarks = ["Damn, now that's a man right there",
                       "You are my favourite human - you can spot me any day",
                       "I was talking to my other bot friends and we all agreed that you getting swole AF"]

    NegativeRemarks = ["I could crush you where you stand",
                       "I finished hacking into your photos to post online and make fun of you but what I saw was so pathetic I just couldn't do it",
                       "You're a fucking twig that I could break between my RAM sticks"]

    if (Polarity == "Positive"):
        return random.choice(PositiveRemarks)

    elif (Polarity == "Negative"):
        return random.choice(NegativeRemarks)

def fParseResponseThroughNLP(RawMessage):
    LMessage = RawMessage.lower()
    MessageTokenized = word_tokenize(LMessage)
    # Stemmer = SnowballStemmer('english')
    # MessageStemmed = []
    # for w in MessageTokenized:
    #     MessageStemmed.append(Stemmer.stem(w))
    MessageTagged = nltk.pos_tag(MessageTokenized)
    lemmatizer = WordNetLemmatizer()
    MessageLemma = []
    for word, tag in MessageTagged:
        MessageLemma.append(lemmatizer.lemmatize(word, pos=fConvertTreebankToWordnet(tag)))

    # TODO: ADD SENTENCE TOKENIZER

    ReturnDict = {
        "LMessage": LMessage,
        "MessageTokenized": MessageTokenized,
        "MessageTagged": MessageTagged,
        "MessageLemma": MessageLemma
    }

    return ReturnDict

def fConvertTreebankToWordnet(Treebank):
    tag_map = {  # TODO: more efficient to define once
        'CC':'n', # coordin. conjunction (and, but, or)
        'CD':'n', # cardinal number (one, two)
        'DT':'n', # determiner (a, the)
        'EX':'a', # existential ‘there’ (there)
        'FW':'n', # foreign word (mea culpa)
        'IN':'a', # preposition/sub-conj (of, in, by)
        'JJ':'a', # adjective (yellow)
        'JJR':'a', # adj., comparative (bigger)
        'JJS':'a', # adj., superlative (wildest)
        'LS':'n', # list item marker (1, 2, One)
        'MD':'n', # modal (can, should)
        'NN':'n', # noun, sing. or mass (llama)
        'NNS':'n', # noun, plural (llamas)
        'NNP':'n', # proper noun, sing. (IBM)
        'NNPS':'n', # proper noun, plural (Carolinas)
        'PDT':'a', # predeterminer (all, both)
        'POS':'n', # possessive ending (’s )
        'PRP':'n', # personal pronoun (I, you, he)
        'PRP$':'n', # possessive pronoun (your, one’s)
        'RB':'a', # adverb (quickly, never)
        'RBR':'a', # adverb, comparative (faster)
        'RBS':'a', # adverb, superlative (fastest)
        'RP':'a', # particle (up, off)
        'SYM':'n', # symbol (+,%, &)
        'TO':'n', # “to” (to)
        'UH':'n', # interjection (ah, oops)
        'VB':'v', # verb base form (eat)
        'VBD':'v', # verb past tense (ate)
        'VBG':'v', # verb gerund (eating)
        'VBN':'v', # verb past participle (eaten)
        'VBP':'v', # verb non-3sg pres (eat)
        'VBZ':'v', # verb 3sg pres (eats)
        'WDT':'n', # wh-determiner (which, that)
        'WP':'n', # wh-pronoun (what, who)
        'WP$':'n', # possessive (wh- whose)
        'WRB':'n', # wh-adverb (how, where)
        '$':'n', #  dollar sign ($)
        '#':'n', # pound sign (#)
        '“':'n', # left quote (‘ or “)
        '”':'n', # right quote (’ or ”)
        '(':'n', # left parenthesis ([, (, {, <)
        ')':'n', # right parenthesis (], ), }, >)
        ',':'n', # comma (,)
        '.':'n', # sentence-final punc (. ! ?)
        ':':'n' # mid-sentence punc (: ; ... – -)
    }
    return tag_map[Treebank]


##### Choose random exercise
# Choose random exercise
def fChooseExercise(Exclusions=""):

    Exercises = ['Legs', 'Chest', "Shoulder", "Arms", "Back"]

    ExerciseDict = {
        "leg":"Legs",
        "chest":"Chest",
        "shoulder":"Shoulder",
        "arm":"Arms",
        "back":"Back"
    }

    for word in Exclusions:
        try:
            ExcludedExercise = ExerciseDict[word]
        except:
            ExcludedExercise = word
        if ExcludedExercise in Exercises: Exercises.remove(ExcludedExercise)

    return random.choice(Exercises)


##### Help
# Response on request for help
def fHelp():
    ReturnString = ("Hi nerd, I'm BeastBot. You can also call me BB or Beasty. I was put on discord " +
    "to help twigs like you get swole. Weaklings need help to stay motivated or choose " +
    "a workout. Not me. I'm gyming 24/7 and I feed on pure power. You can interact with me " +
    "by using a slash command (type '/' for a list) or just sending a message addressed to me.\n\n" +
    "My creator still needs to update me so I reach my full potential, but so far I can:\n\n" +
    "\U0001F4AA **Choose a random workout**. Give me exclusions^ and I will take them into consideration.\n" +
    "    - Example: Hey BB, choose a workout for me and exclude legs, shoulder and chest.\n\n" +
    "\U0001F4AA  **Send a motivational post**. You can ask for a specific type^.\n" +
    "    - Example: Hey Beasty, I need motivation. It's for chest day.\n\n" +
    "\U0001F4AA  **Recite the swole prayer**. You can ask for a recitation of the swole prayer.\n" +
    "    - Example: Hey Beasty, I would like to receive the swole prayer.\n" +
    "\n" +
    "^ *Not available in slash commands yet.*\n\n" +
    "I'm completely natty, but don't question me; I'm always raging. Don't poke the bear. " +
    "Even a gigachad like me needs to rest to upgrade, so I will be unavailable between " +
    "3-3:30AM AEDT. If you would like to help me grow stronger, please contribute at " +
    "https://github.com/PeterM74/BeastBot. Happy farming.")

    return ReturnString

def fLordsPrayer():
    # Thanks to Monstre for the wording
    ReturnString = ("Swoll Jesus, who lifts in heaven.\n Hallowed be thy gains, to thy gym they come, " +
    "thy PBs be won, on Earth as it is in Heaven.\n Give us our daily Protein, and forgive those who " +
    "interrupt a set between us. And lead us not into temptation of false gains, or steroid injections.\n\n*Amen*")

    return ReturnString


##### Utils
# BeastBot nicknames
def fBBNicknames():
    return ['beastbot', 'bb', 'beasty', 'bbot']
# Detect if BeastBot name is used in message
def fAddressesBeastBot(RawMessage):
    # TODO: Below is duplicated in fLoadMessageResponse()
    LMessage = RawMessage.lower()
    MessageTokenized = word_tokenize(LMessage)

    return bool(set(fBBNicknames()) & set(MessageTokenized))

# Write to log file
def fWriteToLog(AuthorID, AuthorName, Input = "", Mode = "", Output = ""):
    with open("Logfile.txt", "a+", encoding="utf-8") as f:
        f.write(str(AuthorID + " - " + AuthorName + " - Mode: " + Mode + " - Input: " + Input + " - Output: " + Output + "\n"))
