#!/home/dino/anaconda3/bin/python

import json
import re

imagePersonGenderByDateLocation = {
    "Retail Store": 0,
    "Information Technology": 0,
    "Design": 1,
    "E-Commerce": 0,
    "Retail Corporate": 1
}
juniorOrSeniorMap = {
    "junior" : 1,
    "jr.": 2,
    "jr" : 3,
    "senior" : 4,
    "sr." : 5,
    "sr" : 6,
}
teamHeadMap = {
    "teamhead" :0 ,
    "team head" : 1
}
eCommerceMap = {
    "ecommerce" : 0, 
    "e-commerce" : 1
}
internshipMap = {
    "internship" : 0,
    "intern" : 1
}
globalMap = {
    "international" : 0,
    "global" : 1
}

def executeRegExWithMapping(regex, jobTitle, valuemap):
    searchResult = re.search(regex, jobTitle, re.IGNORECASE)    
    if searchResult:
        returnValue = searchResult.group(1).lower()
        # Map the found string to its numerical value and return this one    
        returnValue = valuemap[returnValue]
    else:
        returnValue = 99
    return returnValue

def executeRegExForOccuranceChecks(regex, jobTitle):
    # Returns 1 if something was found, else 0
    searchValue = re.search(regex, jobTitle, re.IGNORECASE)    
    if searchValue:
        return 1    
    return 0

def processLayoutInformation(rawJsonFile):
    # {0, 1, 2} => {oben, mitte, unten}
    imagePosition = 0

    # {0, 1} => {nicht ganz, ganz}
    imageSize = 1

    # {0, 1} => {nicht neben Text, neben Text}
    imageTextRatio = 1

    imagePersonCount = 1
    imagePersonGender = imagePersonGenderByDateLocation.get(rawJsonFile['date_location'], None)

    return {
        'image_position': imagePosition,
        'image_size': imageSize,
        'image_text_ratio': imageTextRatio,
        'image_person_count': imagePersonCount,
        'image_person_gender': imagePersonGender,
    }

def processJobTitle(jobTitle):    
    # {0, 1, 2} => {links, mittig, rechts} ueber Text
    jobTitlePosition = 1
    jobTitleLength = len(jobTitle)
    
    # Check whether Junior/Jr./Jr or Senior/Sr./Sr is within the job title
    juniorOrSenior = executeRegExWithMapping(r"\b(junior\b|jr\.|jr\b|senior\b|sr\.|sr\b)", jobTitle, juniorOrSeniorMap)    
    
    # Check whether Teamhead or Team Head is within the job title    
    teamHead = executeRegExWithMapping(r"\b(Teamhead|Team Head)\b", jobTitle, teamHeadMap)
        
    # Check whether eCommerce or e-Commerce is within the job title                          
    ecom = executeRegExWithMapping(r"\b(eCommerce|e-commerce)\b", jobTitle, eCommerceMap)
    
    # Check whether Internship or Intern is within the job title
    internship = executeRegExWithMapping(r"\b(internship|intern)\b", jobTitle, internshipMap)    
    
    # Check whether International or Global is within the job title   
    globOrInternational = executeRegExWithMapping(r"\b(international|global)\b", jobTitle, globalMap)
    
    # Check whether a "&" or "und" or "and" or "y" or "et" or "e" or "en" or "i" or "ve" within the job title
    # If one of the mentiones options is available it is necessary to distinguish between the "&" and all other options. 
    # If a "&" occured then insert that a sign was used, else insert that the words were written                  
    regex = re.search(r"[\s^](&|und|and|y|et|e|en|i|ve)[\s$]", jobTitle, re.IGNORECASE)    
    if regex:
        andValue = 0 if regex.group(1) == "&" else 1
    else:
        andValue = 99

    # Check whether m/w or w/m is within the job title
    # Check whether m/f or f/m is within the job title
    # Check whether h/f or f/h is within the job title
    # Check whether h/m or m/h is within the job title
    # If one of the four above matched something --> Enter it appeared, else it didn't appear
    genderValue = executeRegExForOccuranceChecks(r"m\/w|w\/m|m\/f|f\/m|h\/f|f\/h|h\/m|m\/h", jobTitle)

    # Check whether a comma is within the job title or not
    commaValue = executeRegExForOccuranceChecks(r"\,", jobTitle)            

    # Check whether a dash is within the job title or not
    dashValue = executeRegExForOccuranceChecks(r"\-", jobTitle)

    #  Check whether "BU" is within the job title or not
    buValue = executeRegExForOccuranceChecks(r"\b(BU)\b", jobTitle)

    #  Is WANTED within the job title or not
    wantedValue = executeRegExForOccuranceChecks(r"\b(WANTED)\b", jobTitle)
    
    #  Is PUMA within the job title or not    
    pumaValue = executeRegExForOccuranceChecks(r"\b(PUMA)\b", jobTitle)
    
    #  Is "(" within the job title or not
    bracketValue = executeRegExForOccuranceChecks(r"\(", jobTitle)

    return {
        'job_title_position': jobTitlePosition,
        'job_title_length': jobTitleLength,
        'job_title_jr_sr': juniorOrSenior,
        'job_title_team_head': teamHead,
        'job_title_ecommerce': ecom,
        'job_title_intern': internship,
        'job_title_comma': commaValue,
        'job_title_dash': dashValue,
        'job_title_global': globOrInternational,
        'job_title_abbreviation': buValue,
        'job_title_gender': genderValue,
        'job_title_wanted': wantedValue,
        'job_title_puma': pumaValue,
        'job_title_paren': bracketValue,
        'job_title_and': andValue,
    }


def processJobLocation(jobLocation):
    #Extracts information about:
    #   - the city
    #   - the province (Information is not available within the JSON-file)
    #   - the country
    # and returns a list.
    address = jobLocation["address"]
    city = address["addressLocality"]
    country = address["addressCountry"]

    # returns the following list: (city, province, country) 
    # Province is not located within the JSON-file and must therefore be obtained in a different way.
    return {
        'city': city,
        'country': country,
    }


def getNumberOfListElements(qualifications):
    listElements = re.findall(r"<li>", qualifications, re.MULTILINE)
    return len(listElements)


def isListWithBulletPoints(qualifications):
    listElements = re.search(r"<li>", qualifications, re.MULTILINE)    
    if listElements:
        return 1
    return 0


def isSomethingBoldWithinBulletPoint(qualifications):
    isBold = re.search(r"<span>", qualifications, re.MULTILINE)
    if isBold:
        return 1
    return 0


def getNumberOfWordsForBulletPoint(qualifications):    
    # We check whether there is a <ul>-element within the JSON-file or not. 
    # If there is no <ul>-element that means there is no list at all and we return
    # a list with 20 zero values
    try:
        returnList = []
        listWithoutUlElement = re.split(r"<ul>", qualifications, re.MULTILINE|re.DOTALL)
        listWithoutUlEndElement = re.split(r"<\/ul>", listWithoutUlElement[1], re.MULTILINE|re.DOTALL)
        listWithoutLiElements = re.split(r"<li>", listWithoutUlEndElement[0], re.MULTILINE|re.DOTALL)          
        for listElement in listWithoutLiElements:
            wordCount = 0
            if listElement != "":            
                wordList = re.findall(r"[A-Za-z0-9]+|[^A-Za-z0-9 ]", listElement, re.MULTILINE)
                for word in wordList:
                    if re.match(r"[A-Za-z0-9]+", word) and word != "li" and word != "span":
                        wordCount += 1                    
                returnList.append(wordCount)    
    except:
        returnList = []
    
    if(len(returnList) < 20):
        emptyCells = 20 - len(returnList)
        for _ in range(0, emptyCells, 1):
            returnList.append(0)
    return returnList


def processQualifications(qualifications):
    isBold = isSomethingBoldWithinBulletPoint(qualifications)
    numberOfListElements = getNumberOfListElements(qualifications)
    isBulletPointOccuring = isListWithBulletPoints(qualifications)
    wordList = getNumberOfWordsForBulletPoint(qualifications)

    return {
        'talent_bold_text': isBold,
        'talent_bullet_point_count': numberOfListElements,
        'talent_bullet_point_layout': isBulletPointOccuring,
        'talent_bullet_point_word_count': wordList,
    }


def processResponsibilities(responsibilities):
    isBold = isSomethingBoldWithinBulletPoint(responsibilities)
    numberOfListElements = getNumberOfListElements(responsibilities)
    isBulletPointOccuring = isListWithBulletPoints(responsibilities)
    wordList = getNumberOfWordsForBulletPoint(responsibilities)

    return {
        'mission_bold_text': isBold,
        'mission_bullet_point_count': numberOfListElements,
        'mission_bullet_point_layout': isBulletPointOccuring,
        'mission_bullet_point_word_count': wordList,
    }



def openJSON(pathToJSON):    
    with open(pathToJSON) as file:        
        rawJsonFile = json.load(file)
        return rawJsonFile


def processJSON(rawJsonFile):
    jobtitle = rawJsonFile["title"]
    layoutInformation = processLayoutInformation(rawJsonFile)
    jobTitleInformation = processJobTitle(rawJsonFile["title"])      
    jobLocationInformation = processJobLocation(rawJsonFile["jobLocation"])

    responsibilities = processResponsibilities(rawJsonFile["responsibilities"])
    qualifications = processQualifications(rawJsonFile["qualifications"])    

    dayPosted = rawJsonFile["datePosted"]  # Day posted is currently not within the list
    dateLocation = rawJsonFile["date_location"]
    returnDict = {
        'job_title': jobtitle,
        'functional_area': dateLocation,
        **jobLocationInformation, **layoutInformation, **jobTitleInformation,
        **responsibilities, **qualifications}

    # There is only one column which needs to be filled. That is why I am checking if one of the two variables contains a 1 or 0
    returnDict['mission_talent_bold_text'] = 1 if (returnDict['talent_bold_text'] or returnDict['mission_bold_text']) else 0
    del returnDict['talent_bold_text']
    del returnDict['mission_bold_text']

    # Number of bulletpoints for responsibilities / number of bulletpoints for qualifications
    returnDict['talent_bullet_point_count_ratio'] = str(returnDict['mission_bullet_point_count']) + "/" + str(returnDict['talent_bullet_point_count'])

    print(returnDict)
    return returnDict
    

if __name__ == "__main__":
    rawJsonFile = openJSON("/home/dino/Desktop/puma/jobs/out/JSON files/r874.json")
    outputJsonFile = processJSON(rawJsonFile)

