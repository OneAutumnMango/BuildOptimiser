import os
import yaml

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

configFileName = "BOconfigSimplified.yaml"

rolls = read_yaml(configFileName)["rolls"]
character = read_yaml(configFileName)["character"]
weapon = read_yaml(configFileName)["weapon"]
artifactMainStatChoice = read_yaml(configFileName)["artifactMainStatChoice"]
artifactMainStats = read_yaml(configFileName)["artifactMainStats"]


def baseStatCombine(key):
    return character[key]+weapon[key]

baseATK = baseStatCombine("ATK")
baseHP = baseStatCombine("HP")
baseDEF = baseStatCombine("DEF")

baseATKPercent = baseStatCombine("ATKPercent")
baseHPPercent = baseStatCombine("HPPercent")
baseDEFPercent = baseStatCombine("DEFPercent")

baseCritRate = baseStatCombine("CritRate")
baseCritDMG = baseStatCombine("CritDMG")
baseEM = baseStatCombine("EM")
baseEnergyRecharge = baseStatCombine("EnergyRecharge")

for i in list(artifactMainStatChoice):
    print(artifactMainStatChoice[i]) #prints the artifact main stat choices
    print(artifactMainStats[artifactMainStatChoice[i]]) #prints the value of the choices
          
