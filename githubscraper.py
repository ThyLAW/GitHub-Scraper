# GitHub Scraper
# Modify url to desired repository

# import items
import csv
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime

# url to scrape
url = "https://github.com/ThyLAW?tab=repositories"

# get raw data
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "html.parser")

# create arrays to store data
repoNamesStore = []
repositoryTypeStore = []
programLanguageStore = []
updatedStore = []

# iterate through and extract information into arrays

for item in soup.findAll("li", attrs={"class":"col-12 d-flex width-full py-4 border-bottom color-border-muted public source", "itemprop":"owns"}):
    repoNames = item.findAll("a", attrs={"itemprop":"name codeRepository"})
    for repoName in repoNames:
        repoNamesStore.append(repoName.text.strip())
    repositoryType = item.findAll("span", attrs={"class":"Label Label--secondary v-align-middle ml-1 mb-1"})
    for repository in repositoryType:
        repositoryTypeStore.append(repository.text.strip())
    primaryLanguagesDivs = item.findAll("div", attrs={"class":"f6 color-fg-muted mt-2"})
    for language in primaryLanguagesDivs:
        foundLanguage = item.find("span", attrs={"itemprop":"programmingLanguage"})
        if foundLanguage is not None:
            programLanguageStore.append(foundLanguage.text.strip())
        else:
            programLanguageStore.append("None Found")
    lastUpdatedTimes = item.findAll("relative-time", attrs={"class": "no-wrap"})
    for time in lastUpdatedTimes:
        updatedStore.append(time.text.strip())


# Generate ID for each entry

counter = 0

# Initiate DateTime for TimeStamp

timeDate = datetime.isoformat(datetime.now())

# write to githubrepos.csv file

with open('githubrepos.csv', 'w', newline= '') as file:
    writer = csv.writer(file)
    writer.writerow(["key", "repoName", "repoType", "repoLanguage", "lastUpdated", "timeStamp"])
    for i in range(len(repoNamesStore)):
        writer.writerow([counter, repoNamesStore[i], repositoryTypeStore[i].format(datetime.now()), programLanguageStore[i], updatedStore[i], timeDate])
        counter += 1

