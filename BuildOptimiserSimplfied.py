import os
import yaml

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

configFileName = "BOconfigSimplified.yaml"

config = read_yaml(configFileName)["config"]
character = read_yaml(configFileName)["character"]
weapon = read_yaml(configFileName)["weapon"]
artifactMainStatChoice = read_yaml(configFileName)["artifactMainStatChoice"]
artifactMainStats = read_yaml(configFileName)["artifactMainStats"]
artifactSubStatRolls = read_yaml(configFileName)["artifactSubStatRolls"]


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
baseEnergyRecharge = baseStatCombine("EnergyRecharge")
baseEM = baseStatCombine("EM")


for i in list(artifactMainStatChoice):
    print(artifactMainStatChoice[i]) #prints the artifact main stat choices
    print(artifactMainStats[artifactMainStatChoice[i]]) #prints the value of the choices
          
print(artifactSubStatRolls)
maxATKRoll = artifactSubStatRolls["ATKPercent"]
maxCRRoll = artifactSubStatRolls["CritRate"]
maxCDRoll = artifactSubStatRolls["CritDMG"]
maxERRoll = artifactSubStatRolls["EnergyRecharge"]
maxEMRoll = artifactSubStatRolls["EM"]

rolls = config["rolls"]