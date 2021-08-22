import os
import yaml
import math

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
buffs = read_yaml(configFileName)["buffs"]


def baseStatCombine(key):
    artifactBonus = 0
    for type in ["sands","goblet","circlet"]:
        if artifactMainStatChoice[type] == key:
            artifactBonus = artifactMainStats[artifactMainStatChoice[type]]
    
    return character[key]+weapon[key]+artifactBonus

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



maxATKRoll = artifactSubStatRolls["ATKPercent"]
maxCRRoll = artifactSubStatRolls["CritRate"]
maxCDRoll = artifactSubStatRolls["CritDMG"]
maxERRoll = artifactSubStatRolls["EnergyRecharge"]
maxEMRoll = artifactSubStatRolls["EM"]

reactionMultiplier = config["EMReactionMultiplier"]
reactionRatio = config["ReactionRatio"]
reactionBonus = config["ReactionBonus"]

rolls = config["rolls"]

if config["ERThreshold?"] == True and config["ERThreshold"] >= baseEnergyRecharge:
    rolls -= math.ceil((config["ERThreshold"]-baseEnergyRecharge)/maxERRoll)

    ERRolls = math.ceil((config["ERThreshold"]-baseEnergyRecharge)/maxERRoll)
    ER = round(math.ceil(ERRolls)*maxERRoll+baseEnergyRecharge,4)

else: 
    ERRolls = 0
    ER = baseEnergyRecharge



def optimiseRolls(rolls):
    ATKRolls = 0
    CRRolls = 0
    CDRolls = 0
    EMRolls = 0

    DMGValues = {}

    for i in range(rolls +1):
        ATKRolls = i

        for j in range(rolls-i +1):
            CRRolls = j

            for k in range(rolls - i - j +1):
                CDRolls = k

                EMRolls = rolls - i - j - k
                
                #DMGValues[(baseAtk*(1+baseATKPercent+ATKRolls*maxATKRoll)] = [ATKRolls, CRRolls, CDRolls, EMRolls]
                
                ATK = baseATK * (1 + baseATKPercent + ATKRolls * maxATKRoll) + artifactMainStats["ATK"] + buffs["FlatATK"]
                CR = baseCritRate + CRRolls * maxCRRoll
                if CR > 1: CR = 1
                CritMult = 1 + CR * (baseCritDMG + CDRolls * maxCDRoll)
                
                EM = baseEM + EMRolls * maxEMRoll
                V = reactionMultiplier * (1 + 2.78 * EM/(1400 + EM) + reactionBonus)
                EMMult = reactionRatio * (V - 1) + 1
                DMGValues[ATK * CritMult * EMMult] = [ATKRolls, CRRolls, CDRolls, EMRolls]

    maxDMG = max(DMGValues, key=int)
    return maxDMG, DMGValues[maxDMG]


optimisedRolls = optimiseRolls(rolls)

ATKRolls = optimisedRolls[1][0]
ATKPercent = round(baseATKPercent + ATKRolls * maxATKRoll,4)
ATK = round(baseATK * (1 + baseATKPercent + ATKRolls * maxATKRoll) + artifactMainStats["ATK"] + buffs["FlatATK"],2)

CRRolls = optimisedRolls[1][1]
CR = int((baseCritRate + CRRolls * maxCRRoll)*10000)/10000

CDRolls = optimisedRolls[1][2]
CD = int((baseCritDMG + CDRolls * maxCDRoll)*10000)/10000

EMRolls = optimisedRolls[1][3]
EM = round(baseEM + EMRolls * maxEMRoll,2)


resultantDMGValue = round(optimisedRolls[0],2)



print("""
ATK = %s, %s ATK%%, %d ATK rolls,
CR = %s%%, %d CR rolls,
CD = %s%%, %d CD rolls,
EM = %s, %d EM rolls,
ER = %s%%, %d ER rolls,

Resultant DMG Value = %s
""" % (ATK,ATKPercent*100,ATKRolls,CR*100,CRRolls,CD*100,CDRolls,EM,EMRolls,ER*100,ERRolls,resultantDMGValue))

input("Press Enter to Exit.")