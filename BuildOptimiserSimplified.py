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
            artifactBonus += artifactMainStats[artifactMainStatChoice[type]]
    
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

if config["ifRollCountFromConfig"] == True:
    rolls = config["rolls"]
else: 
    rolls = int(input("\nHow many rolls would you like to optimiser for? "))

if config["ERThreshold?"] == True and config["ERThreshold"] >= baseEnergyRecharge:
    rolls -= math.ceil((config["ERThreshold"]-baseEnergyRecharge)/maxERRoll)

    ERRolls = math.ceil((config["ERThreshold"]-baseEnergyRecharge)/maxERRoll)
    ER = int((math.ceil(ERRolls)*maxERRoll+baseEnergyRecharge)*10000)/100

else: 
    ERRolls = 0
    ER = int(baseEnergyRecharge*10000)/100



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
ATKPercent = int((baseATKPercent + ATKRolls * maxATKRoll)*10000)/100
ATK = round(baseATK * (1 + baseATKPercent + ATKRolls * maxATKRoll) + artifactMainStats["ATK"] + buffs["FlatATK"],2)

CRRolls = optimisedRolls[1][1]
CR = int((baseCritRate + CRRolls * maxCRRoll)*10000)/100

CDRolls = optimisedRolls[1][2]
CD = int((baseCritDMG + CDRolls * maxCDRoll)*10000)/100

EMRolls = optimisedRolls[1][3]
EM = int((baseEM + EMRolls * maxEMRoll)*100)/100


resultantDMGValue = round(optimisedRolls[0],2)



print("""\n
Ideal Stat Ratio:

ATK = %s, %s ATK%%, %d ATK rolls,
%s%% CR, %d CR rolls,
%s%% CD, %d CD rolls,
%s EM, %d EM rolls,
%s%% ER, %d ER rolls,

Resultant DMG Value = %s""" % (ATK,ATKPercent,ATKRolls,CR,CRRolls,CD,CDRolls,EM,EMRolls,ER,ERRolls,resultantDMGValue))

#Ideal Artifact

def calcOccur(stat):
    occur = 5
    for type in ["sands","goblet","circlet"]:
        if artifactMainStatChoice[type] == stat:
            occur -= 1
    return occur

avgATKRolls = round(ATKRolls/calcOccur("ATKPercent"))
artiATK = int(avgATKRolls*maxATKRoll*10000)/100

avgCRRolls = round(CRRolls/calcOccur("CritRate"))
artiCR = int(avgCRRolls*maxCRRoll*10000)/100

avgCDRolls = round(CDRolls/calcOccur("CritDMG"))
artiCD = int(avgCDRolls*maxCDRoll*10000)/100

avgEMRolls = round(EMRolls/calcOccur("EM"))
artiEM = int(avgEMRolls*maxEMRoll*100)/100

avgERRolls = round(ERRolls/calcOccur("EnergyRecharge"))
artiER = int(avgERRolls*maxERRoll*10000)/100


print("""
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

Sample Requirement per Artifact on Average

%s ATK%%, %d ATK rolls,
%s%% CR, %d CR rolls,
%s%% CD, %d CD rolls,
%s EM, %d EM rolls,
%s%% ER, %d ER rolls,

""" % (artiATK,avgATKRolls,artiCR,avgCRRolls,artiCD,avgCDRolls,artiEM,avgEMRolls,artiER,avgERRolls))

print("""
Ideal Stat Ratio:

%s
%s%%
%s%% 
%s%%


Resultant DMG Value = %s""" % (ATK,ATKPercent,CR,CD,resultantDMGValue))


input("Press Enter to Exit.")
