#!/usr/bin/python3
import urllib.request
import json
import csv


def pageCollect(drawId):
    page = urllib.request.urlopen(f'https://api.opap.gr/draws/v3.0/5104/{drawId}')
    content = json.loads(page.read())

    # empty dictionary
    ret = {}

    # drawId
    ret["drawId"] = content["drawId"]

    # Winning numbers
    ret["winningNumbers"] = content["winningNumbers"]["list"]

    # Joker
    ret["joker"] = content["winningNumbers"]["bonus"][0]

    # 5+1 winners
    ret["winners"] = content["prizeCategories"][0]["winners"]

    # jackpot winning money
    ret["jackpot"] = content["prizeCategories"][0]["jackpot"]

    # normal winning money
    ret["distributed"] = content["prizeCategories"][0]["distributed"]

    # columns played
    ret["columns"] = content["wagerStatistics"]["columns"]

    return ret

if __name__ == "__main__":
    # Get latest drawId
    page = urllib.request.urlopen(f'https://api.opap.gr/draws/v3.0/5104/last-result-and-active')
    latestId = json.loads(page.read())["last"]["drawId"]

    print("Latest drawId: ", latestId)

    fieldNames = ["drawId", "winningNumbers", "joker", "winners", "jackpot", "distributed", "columns"]

    with open(f'data{latestId}.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldNames)

        writer.writeheader()

        for drawId in range(1, latestId+1):
            rowData = pageCollect(drawId)
            writer.writerow(rowData)
