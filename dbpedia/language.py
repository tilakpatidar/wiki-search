#! /usr/bin/python
# coding: utf-8

__author__="Tilak"

"""
Language related regex.
"""
from refo import Question, Plus
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dbpedia.dsl import IsLanguage, SpeakersOf, SpokenIn, LabelOf, \
LanguageFamilyOf, OfficialLanguageOf, NameOf, CommonNameOf

class Language(Particle):
    
    regex = Plus(Pos("JJ") | Pos("NN") | Pos("NNP") | Pos("NNS"))
   
    def interpret(self, match):
        name = match.words.tokens
        return IsLanguage() + HasKeyword(name)
   
    
class ListAllLanguagesQuestion(QuestionTemplate):
    """
    Regex for questions about listing all languages in dbpedia
    Ex: "list all languages?"
        "list all languages in dbpedia?"
    """
    
    regex = (Question(Lemma("list")) + Lemma("all") + Lemma("language") + Question(Pos("."))) | \
        (Question(Lemma("list")) + Lemma("all") + Lemma("language") + Pos("IN") + Lemma("dbpedia") + Question(Pos("."))) 
    
    def interpret(self, match):
        LanguageNames = IsLanguage()
        return LabelOf(LanguageNames), "enum"
    

class SpeakersOfQuestion(QuestionTemplate):
    """
    Regex for questions about the number of people that speaks a language
    Ex: "How many people speaks English language?"
        "How many people speak Canadian French?"
        "How many people in the world can speak Arabic language?"
    """
    
    regex = (Lemmas("how many") + Lemma("people") + (Lemma("speaks") | Lemma("speak")) + Language() + Question(Pos("."))) | \
        (Lemmas("how many") + Lemma("people") + Pos("IN") + Pos("DT") + Lemma("world") + Lemma("can") + (Lemma("speak") | Lemma("speaks")) + Language() + Question(Pos(".")))
     
    def interpret(self, match):
        NumberOfSpeakers = SpeakersOf(match.language)
        return NumberOfSpeakers, "literal"
    

class SpokenInQuestion(QuestionTemplate):
    """
    Regex for questions about where is a language spoken
    Ex: "Where is Thai language spoken?"
        "list of countries speaks Arabic language?"
        "Countries that speaks Japanese language?"
    """
    
    regex = (Lemmas("where be")  + Language() + Lemma("spoken") + Question(Pos("."))) | \
        (Question(Lemma("list")) + Pos("IN") + Lemma("country") +  (Lemma("speaks") | Lemma("speak")) + Language() + Question(Pos("."))) | \
        (Lemma("countries") + Question(Lemma("that")) + (Lemma("speaks") | Lemma("speak")) + Language() + Question(Pos(".")))    
     
    def interpret(self, match):
        SpokenInLocations = SpokenIn(match.language)
        return NameOf(SpokenInLocations), "enum"
    
    
class LanguageFamilyOfQuestion(QuestionTemplate):
    """
    Regex for questions about the language family for a language
    Ex: "What language family does Thai language belong to?"
        "What language family does Arabic language part of?"
        "What is the language family of English language?"
    """
    
    regex = (Lemma("what")  + Lemma("language") + Lemma("family") + Pos("VBZ") + Language() + ((Lemma("belong") | Lemma("belongs")) + Pos("TO") | Lemma("part") + Pos("IN")) + Question(Pos("."))) | \
        (Lemma("what")  + Lemma("be") + Pos("DT") + Lemma("language") + Lemma("family")  + Pos("IN") + Language() + Question(Pos(".")))
    
    def interpret(self, match):
        FamilyLanguage = LanguageFamilyOf(match.language)
        return LabelOf(FamilyLanguage), "enum"
    

class OfficialLanguageQuestion(QuestionTemplate):
    """
    Regex for questions about which countries speaks a language as official language
    Ex: "where is Thai language spoken as an official language?"
        "list of countries that speaks Arabic language as an official language?"
        "Countries speaks English language as official language?"
    """
    
    regex = (Lemmas("where be")  + Language() + Lemma("spoken") + Pos("IN") + Question(Pos("DT")) + Lemma("official") +  Lemma("language") + Question(Pos("."))) | \
        (Question(Lemma("list") + Pos("IN")) + (Lemma("country")|Lemma("countries")) +  Question(Lemma("that")) + (Lemma("speaks") | Lemma("speak")) + Language() + Pos("IN") + Question(Pos("DT")) + Lemma("official") +  Lemma("language") + Question(Pos(".")))

              
    def interpret(self, match):
        OfficialLanguage = OfficialLanguageOf(match.language)
        return CommonNameOf(OfficialLanguage), "enum"