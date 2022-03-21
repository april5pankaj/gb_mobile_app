import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import sys
import json
import random
from datetime import datetime
import collections
import yamlordereddictloader
import yaml
import time
import os
import csv
import pandas as pd
import collections
import os.path
from os import path
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image, ImageGrab, ImageTk
import shutil
import pygame



with open("yaml/resume/match_yaml_pre.yaml") as f:
    match_yaml = yaml.load(f, Loader=yamlordereddictloader.Loader)
with open("empty_team_yaml.yaml") as g:
    team_yaml = yaml.load(g, Loader=yamlordereddictloader.Loader)
with open("deliveries.yaml") as h:
    currdel = yaml.load(h, Loader=yamlordereddictloader.Loader)
with open("deliveries.yaml") as j:
    prevdel = yaml.load(j, Loader=yamlordereddictloader.Loader)
with open("sc_yaml_dummy.yaml") as k:
    sc_yaml_dummy = yaml.load(k, Loader=yamlordereddictloader.Loader)
loop_exit = 0

def CodeCommen():
    import xlrd
    import xlwt
    import scipy.stats as st
    import pyttsx3
    from pydub import AudioSegment
    from pydub.playback import play
    #from playsound import playsound
    import time
    print("commentary started")
    predictor_excel = xlrd.open_workbook('comm/predictor.xls')
    predictorAve = predictor_excel.sheet_by_index(0)
    predictorSD = predictor_excel.sheet_by_index(1)
    commentary_excel = xlrd.open_workbook('comm/COMMENTARY_2P_CHECK.xls')
    firstInningsCommentary = commentary_excel.sheet_by_index(0)
    secondInningsCommentary = commentary_excel.sheet_by_index(1)
    thirdInningsCommentary = commentary_excel.sheet_by_index(2)
    fourthInningsCommentary = commentary_excel.sheet_by_index(3)
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My worksheet')
    with open("comm/commentary_variables.yaml") as f:
        commVar = yaml.load(f, Loader=yamlordereddictloader.Loader)
    any = 9999
    runs = 0
    runsCopy = 0
    runsBatsman = 0
    conseOut = 0
    wicketsBefore = 0
    wicketsAfter = 0
    wicketsAfterCopy = 0
    avgScore = 30
    projScore = 0
    projScbyAvgSc = 0
    delDir = 1
    delta = 0.000000000000001
    probLeadBef = 0
    probLeadAft = 0
    probWinBef = 0
    probWinAft = 0
    projLead = 0
    actLead = 0
    secIScbyFirISc = 0
    predLeadbyAvgSc = 0
    tarSetbyAvgSc = 0
    scbyTar = 0
    projScbyTar = 0
    actScbyTar = 0
    scoreAfter = 0
    firstInningsScore = 0
    secondInningsScore = 0
    thirdInningsScore = 0
    cond = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0]
    condTrue = 0
    curr_innings = int(match_yaml['meta']['innings_completed']) + 1
    if curr_innings == 1:
        innings_info = match_yaml['innings']['first_innings']
        inn_str = 'first_innings'
    elif curr_innings == 2:
        innings_info = match_yaml['innings']['second_innings']
        inn_str = 'second_innings'
    elif curr_innings == 3:
        innings_info = match_yaml['innings']['third_innings']
        inn_str = 'third_innings'
    else:
        innings_info = match_yaml['innings']['fourth_innings']
        inn_str = 'fourth_innings'

    #(innings_info)
    # variables to hold scores and wickets and deliveries
    current_delivery = len(innings_info['deliveries'])
    scoreAfter = int(innings_info['deliveries'][current_delivery - 1][current_delivery]['score_after'])
    wicketsAfter = int(innings_info['deliveries'][current_delivery - 1][current_delivery]['wic_after'])
    valBall = int(innings_info['deliveries'][current_delivery - 1][current_delivery]['valid_ball_no'])

    if curr_innings > 1:
        last_ball = len(match_yaml['innings']['first_innings']['deliveries'])
        firstInningsScore = int(match_yaml['innings']['first_innings']['deliveries'][last_ball - 1][last_ball]['score_after'])
    if curr_innings > 2:
        last_ball = len(match_yaml['innings']['second_innings']['deliveries'])
        secondInningsScore = int(match_yaml['innings']['second_innings']['deliveries'][last_ball - 1][last_ball]['score_after'])
    if curr_innings > 3:
        last_ball = len(match_yaml['innings']['third_innings']['deliveries'])
        thirdInningsScore = int(match_yaml['innings']['third_innings']['deliveries'][last_ball - 1][last_ball]['score_after'])

    if current_delivery == 1:
        wicketsBefore = 0
    else:
        wicketsBefore = int(innings_info['deliveries'][current_delivery - 2][current_delivery - 1]['wic_after'])
        conseOutPrev = int(innings_info['deliveries'][current_delivery - 2][current_delivery - 1]['consecutive_out_flag'])
        if int(innings_info['deliveries'][current_delivery - 2][current_delivery - 1]['out_type_id']) == 0:
            wicketsBefore = wicketsBefore + (conseOutPrev % 2) * 0.25

    ball = current_delivery
    conseOut = int(innings_info['deliveries'][current_delivery - 1][current_delivery]['consecutive_out_flag'])
    wicketsAfter = int(innings_info['deliveries'][current_delivery - 1][current_delivery]['wic_after'])
    if int(innings_info['deliveries'][current_delivery - 1][current_delivery]['out_type_id']) == 0:
        wicketsAfterCopy = wicketsAfter + (conseOut % 2) * 0.25

    runs = int(innings_info['deliveries'][current_delivery - 1][current_delivery]['runs']['total'])
    if int(innings_info['deliveries'][current_delivery - 1][current_delivery]['out_type_id']) != 0:
        runs = 8
    if int(innings_info['deliveries'][current_delivery - 1][current_delivery]['extras']['no_ball']) == 1:
        valBall = -1
    if int(innings_info['deliveries'][current_delivery - 1][current_delivery]['extras']['wides']) == 1:
        valBall = -2
    if valBall < 0:
        runsCopy = (0 - valBall) * 10 + runs  # 10
        valBall = int(innings_info['deliveries'][current_delivery - 1][current_delivery]['valid_ball_no'])
    else:
        runsCopy = runs
    runsBatsman = int(innings_info['deliveries'][current_delivery - 1][current_delivery]['runs']['batsman'])

    if valBall == 0:
        valBallCopy = 1
    else:
        valBallCopy = valBall
    if scoreAfter == 0:
        scoreAfterCopy = 0.25
    else:
        scoreAfterCopy = scoreAfter
    aveResUsed = predictorAve.cell_value(round(valBallCopy), round((wicketsAfter * 2) + (conseOut % 2) + 1))
    sdResUsed = predictorSD.cell_value(round(valBallCopy), round((wicketsAfter * 2) + (conseOut % 2) + 1))
    projScore = round(((scoreAfterCopy / aveResUsed) ** (aveResUsed)) * (avgScore ** (1 - aveResUsed)))
    print("projected Score", projScore)
    projScbyAvgSc = projScore / avgScore
    if curr_innings == 1:
        probWinAft = projScbyAvgSc/2
        if probWinAft >= 1:
            probWinAft = 0.99
        if probWinAft < 0.01:
            probWinAft = 0.01
        match_yaml['innings'][inn_str]['deliveries'][current_delivery - 1][current_delivery]['prob_after'] = round(float(probWinAft),4)
    if curr_innings == 4:
        target = firstInningsScore + thirdInningsScore - secondInningsScore + 1
        probWinBef = float(commVar['probability_win_prev'])
        print("probability win before", probWinBef)
        targetReached = scoreAfter / target
        z_value = (targetReached - aveResUsed) / sdResUsed
        probWinAft = round(st.norm.cdf(z_value),4)
        print("probability win after", probWinAft)
        commVar['probability_win_prev'] = float(str(probWinAft))
        delta = probWinAft - probWinBef
        if delta < 0:
            delDir = -1
            delta = 0 - delta
        else:
            delDir = 1
        scbyTar = target - 1 - scoreAfter
        if target == 1:
            projScbyTar = projScore
        else:
            projScbyTar = projScore / (target - 1)
        if probWinAft >= 1:
            probWinAft = 0.99
        if probWinAft < 0.01:
            probWinAft = 0.01
        match_yaml['innings'][inn_str]['deliveries'][current_delivery - 1][current_delivery]['prob_after'] = round(float(probWinAft),4)
        actScbyTar = scoreAfter / target
    if curr_innings == 3:
        lead = firstInningsScore - secondInningsScore
        predLeadbyAvgSc = (projScore + lead) / avgScore
        tarSetbyAvgSc = (firstInningsScore + scoreAfter - secondInningsScore) / avgScore
        probWinAft = (firstInningsScore + projScore - secondInningsScore) / avgScore/2
        if probWinAft >= 1:
            probWinAft = 0.99
        if probWinAft < 0.01:
            probWinAft = 0.01
        match_yaml['innings'][inn_str]['deliveries'][current_delivery - 1][current_delivery]['prob_after'] = round(float(probWinAft),4)
    if curr_innings == 2:
        target = firstInningsScore + 1
        probLeadBef = float(commVar['probability_lead_prev'])
        targetReached = scoreAfter / target
        print(target)
        print(targetReached)
        print(aveResUsed)
        print(sdResUsed)
        z_value = (targetReached - aveResUsed) / sdResUsed
        probLeadAft = round(st.norm.cdf(z_value),4)
        print(z_value)
        print('prob before', probLeadBef)
        print('prob after', probLeadAft)
        delta = probLeadAft - probLeadBef
        commVar['probability_lead_prev'] = float(str(probLeadAft))
        print('delta', delta)
        if delta < 0:
            delDir = -1
            delta = 0 - delta
        else:
            delDir = 1
        projLead = projScore - firstInningsScore
        actLead = scoreAfter - firstInningsScore
        secIScbyFirISc = firstInningsScore - scoreAfter
        print('projected lead', projLead)
        print('actual lead', actLead)
        print('secibyfisc', secIScbyFirISc)
        if firstInningsScore < 7 and projScore >= 7:
            probWinAft = projScore/14
        elif firstInningsScore < 7 and projScore < 7:
            probWinAft = 0.5
        elif firstInningsScore >= 7:
            probWinAft = projScore/firstInningsScore/2
        if probWinAft >= 1:
            probWinAft = 0.99
        if probWinAft < 0.01:
            probWinAft = 0.01
        match_yaml['innings'][inn_str]['deliveries'][current_delivery - 1][current_delivery]['prob_after'] = round(float(probWinAft),4)
    i = 0
    if curr_innings == 1:
        for r1 in range(1, 193, 1):
            cond[0] = (firstInningsCommentary.cell_value(r1, 2) == any) or (
                        runsCopy == firstInningsCommentary.cell_value(r1, 2))
            cond[1] = (firstInningsCommentary.cell_value(r1, 3) == any) or (
                        conseOut % 2 == firstInningsCommentary.cell_value(r1, 3))
            cond[2] = (firstInningsCommentary.cell_value(r1, 4) == any) or (
                        wicketsBefore == firstInningsCommentary.cell_value(r1, 4))
            cond[3] = (firstInningsCommentary.cell_value(r1, 5) == any) or (
                        projScbyAvgSc > firstInningsCommentary.cell_value(r1, 5))
            cond[4] = (firstInningsCommentary.cell_value(r1, 6) == any) or (
                        projScbyAvgSc <= firstInningsCommentary.cell_value(r1, 6))
            cond[5] = (firstInningsCommentary.cell_value(r1, 7) == any) or (
                        valBall >= firstInningsCommentary.cell_value(r1, 7))
            cond[6] = (firstInningsCommentary.cell_value(r1, 8) == any) or (
                        valBall < firstInningsCommentary.cell_value(r1, 8))
            cond[7] = (firstInningsCommentary.cell_value(r1, 9) == any) or (
                        ball >= firstInningsCommentary.cell_value(r1, 9))
            cond[8] = (firstInningsCommentary.cell_value(r1, 10) == any) or (
                        ball < firstInningsCommentary.cell_value(r1, 10))
            condTrue = 1
            for con in range(0, 9, 1):
                condTrue = condTrue and cond[con]
            #print(condTrue)
            #print(cond)
            # time.sleep(0.05)
            i = i + 1
            #print(i)
            if condTrue:
                # commentarySentence=firstInningsCommentary.cell_value(r1,1)
                commentaryId = firstInningsCommentary.cell_value(r1, 25)
                commentaryPitch = firstInningsCommentary.cell_value(r1, 26)

                # worksheet.write(r,23,commentarySentence)
                # commentaryRate=int(120+(runsCopy%10)*8+conseOut*5+projScbyAvgSc*5+valBall)
                # commentaryVolume=commentaryRate/200
                # commentaryVoice=commentaryRate%4
                # commentaryVoice=commentaryVoice%3
                # print('say it ksdjfkds dksjfsl lsfsldkjf dslfjjdksjf dskfsdkjfsdkjf dslkfhskdhf kdsfkfj')
                # engine.setProperty('rate',commentaryRate)
                # engine.setProperty('voice', voices[commentaryVoice].id)
                # engine.setProperty('volume', commentaryVolume)
                # engine.say(commentarySentence)
                # engine.runAndWait()
                break
    r1 = 1
    if curr_innings == 2:
        for r1 in range(1, 382, 1):
            cond[0] = (secondInningsCommentary.cell_value(r1, 2) == any) or (
                        runsCopy == secondInningsCommentary.cell_value(r1, 2))
            cond[1] = (secondInningsCommentary.cell_value(r1, 3) == any) or (
                        conseOut % 2 == secondInningsCommentary.cell_value(r1, 3))
            cond[2] = (secondInningsCommentary.cell_value(r1, 4) == any) or (
                        wicketsBefore == secondInningsCommentary.cell_value(r1, 4))
            cond[3] = (secondInningsCommentary.cell_value(r1, 5) == any) or (
                        delDir == secondInningsCommentary.cell_value(r1, 5))
            cond[4] = (secondInningsCommentary.cell_value(r1, 6) == any) or (
                        delta > secondInningsCommentary.cell_value(r1, 6) / 100)
            cond[5] = (secondInningsCommentary.cell_value(r1, 7) == any) or (
                        delta <= secondInningsCommentary.cell_value(r1, 7) / 100)
            cond[6] = (secondInningsCommentary.cell_value(r1, 8) == any) or (
                        probLeadBef > secondInningsCommentary.cell_value(r1, 8) / 100)
            cond[7] = (secondInningsCommentary.cell_value(r1, 9) == any) or (
                        probLeadBef <= secondInningsCommentary.cell_value(r1, 9) / 100)
            cond[8] = (secondInningsCommentary.cell_value(r1, 10) == any) or (
                        probLeadAft > secondInningsCommentary.cell_value(r1, 10) / 100)
            cond[9] = (secondInningsCommentary.cell_value(r1, 11) == any) or (
                        probLeadAft <= secondInningsCommentary.cell_value(r1, 11) / 100)
            cond[10] = (secondInningsCommentary.cell_value(r1, 12) == any) or (
                        projLead > secondInningsCommentary.cell_value(r1, 12))
            cond[11] = (secondInningsCommentary.cell_value(r1, 13) == any) or (
                        projLead <= secondInningsCommentary.cell_value(r1, 13))
            cond[12] = (secondInningsCommentary.cell_value(r1, 14) == any) or (
                        actLead > secondInningsCommentary.cell_value(r1, 14))
            cond[13] = (secondInningsCommentary.cell_value(r1, 15) == any) or (
                        actLead <= secondInningsCommentary.cell_value(r1, 15))
            cond[14] = (secondInningsCommentary.cell_value(r1, 16) == any) or (
                        valBall >= secondInningsCommentary.cell_value(r1, 16))
            cond[15] = (secondInningsCommentary.cell_value(r1, 17) == any) or (
                        valBall < secondInningsCommentary.cell_value(r1, 17))
            cond[16] = (secondInningsCommentary.cell_value(r1, 18) == any) or (
                        ball >= secondInningsCommentary.cell_value(r1, 18))
            cond[17] = (secondInningsCommentary.cell_value(r1, 19) == any) or (
                        ball < secondInningsCommentary.cell_value(r1, 19))
            cond[18] = (secondInningsCommentary.cell_value(r1, 20) == any) or (
                        secIScbyFirISc >= secondInningsCommentary.cell_value(r1, 20))
            cond[19] = (secondInningsCommentary.cell_value(r1, 21) == any) or (
                        secIScbyFirISc < secondInningsCommentary.cell_value(r1, 21))
            condTrue = 1
            for con in range(0, 20, 1):
                #print(r1, ' row ', con + 1, ' column ', cond[con])
                condTrue = condTrue and cond[con]
            # print(r1, cond)
            # print(condTrue)
            # time.sleep(0.05)
            i = i + 1
            # print(i)
            if condTrue:
                # commentarySentence=secondInningsCommentary.cell_value(r1,1)
                commentaryId = secondInningsCommentary.cell_value(r1, 25)
                commentaryPitch = secondInningsCommentary.cell_value(r1, 26)
                # worksheet.write(r, 23, commentarySentence)
                # commentaryRate = int(120 + (runsCopy % 10) * 8 + conseOut * 5 + delta * 5 + valBall)
                # commentaryVolume = commentaryRate / 200
                # commentaryVoice = commentaryRate % 4
                # commentaryVoice = commentaryVoice % 3
                # print('say it ksdjfkds dksjfsl lsfsldkjf dslfjjdksjf dskfsdkjfsdkjf dslkfhskdhf kdsfkfj')
                # engine.setProperty('rate', commentaryRate)
                # engine.setProperty('voice', voices[commentaryVoice].id)
                # engine.setProperty('volume', commentaryVolume)
                # engine.say(commentarySentence)
                # engine.runAndWait()
                break
    if curr_innings == 3:
        for r1 in range(1, 225, 1):
            cond[0] = (thirdInningsCommentary.cell_value(r1, 2) == any) or (
                    runsCopy == thirdInningsCommentary.cell_value(r1, 2))
            cond[1] = (thirdInningsCommentary.cell_value(r1, 3) == any) or (
                    conseOut % 2 == thirdInningsCommentary.cell_value(r1, 3))
            cond[2] = (thirdInningsCommentary.cell_value(r1, 4) == any) or (
                    wicketsBefore == thirdInningsCommentary.cell_value(r1, 4))
            cond[3] = (thirdInningsCommentary.cell_value(r1, 5) == any) or (
                    predLeadbyAvgSc > thirdInningsCommentary.cell_value(r1, 5))
            cond[4] = (thirdInningsCommentary.cell_value(r1, 6) == any) or (
                    predLeadbyAvgSc <= thirdInningsCommentary.cell_value(r1, 6))
            cond[5] = (thirdInningsCommentary.cell_value(r1, 7) == any) or (
                    valBall >= thirdInningsCommentary.cell_value(r1, 7))
            cond[6] = (thirdInningsCommentary.cell_value(r1, 8) == any) or (
                    valBall < thirdInningsCommentary.cell_value(r1, 8))
            cond[7] = (thirdInningsCommentary.cell_value(r1, 9) == any) or (
                    ball >= thirdInningsCommentary.cell_value(r1, 9))
            cond[8] = (thirdInningsCommentary.cell_value(r1, 10) == any) or (
                    ball < thirdInningsCommentary.cell_value(r1, 10))
            cond[9] = (thirdInningsCommentary.cell_value(r1, 11) == any) or (
                    tarSetbyAvgSc > thirdInningsCommentary.cell_value(r1, 11))
            cond[10] = (thirdInningsCommentary.cell_value(r1, 12) == any) or (
                    tarSetbyAvgSc <= thirdInningsCommentary.cell_value(r1, 12))
            condTrue = 1
            for con in range(0, 11, 1):
                # print(r1, ' row ', con + 1, ' column ', cond[con])
                condTrue = condTrue and cond[con]
            # print(condTrue)
            i = i + 1
            # print(i)
            if condTrue:
                # commentarySentence=thirdInningsCommentary.cell_value(r1,1)
                commentaryId = thirdInningsCommentary.cell_value(r1, 25)
                commentaryPitch = thirdInningsCommentary.cell_value(r1, 26)
                # worksheet.write(r, 23, commentarySentence)
                # commentaryRate = int(120 + (runsCopy % 10) * 8 + conseOut * 5 + predLeadbyAvgSc * 5 + valBall)
                # commentaryVolume = commentaryRate / 200
                # commentaryVoice = commentaryRate % 4
                # commentaryVoice = commentaryVoice % 3
                # print('say it ksdjfkds dksjfsl lsfsldkjf dslfjjdksjf dskfsdkjfsdkjf dslkfhskdhf kdsfkfj')
                # engine.setProperty('rate', commentaryRate)
                # engine.setProperty('voice', voices[commentaryVoice].id)
                # engine.setProperty('volume', commentaryVolume)
                # engine.say(commentarySentence)
                # engine.runAndWait()
                break
    if curr_innings == 4:
        for r1 in range(1, 298, 1):
            cond[0] = (fourthInningsCommentary.cell_value(r1, 2) == any) or (
                    runsCopy == fourthInningsCommentary.cell_value(r1, 2))
            cond[1] = (fourthInningsCommentary.cell_value(r1, 3) == any) or (
                    conseOut % 2 == fourthInningsCommentary.cell_value(r1, 3))
            cond[2] = (fourthInningsCommentary.cell_value(r1, 4) == any) or (
                    wicketsBefore == fourthInningsCommentary.cell_value(r1, 4))
            cond[3] = (fourthInningsCommentary.cell_value(r1, 5) == any) or (
                    delDir == fourthInningsCommentary.cell_value(r1, 5))
            cond[4] = (fourthInningsCommentary.cell_value(r1, 6) == any) or (
                    delta > fourthInningsCommentary.cell_value(r1, 6) / 100)
            cond[5] = (fourthInningsCommentary.cell_value(r1, 7) == any) or (
                    delta <= fourthInningsCommentary.cell_value(r1, 7) / 100)
            cond[6] = (fourthInningsCommentary.cell_value(r1, 8) == any) or (
                    probWinBef > fourthInningsCommentary.cell_value(r1, 8) / 100)
            cond[7] = (fourthInningsCommentary.cell_value(r1, 9) == any) or (
                    probWinBef <= fourthInningsCommentary.cell_value(r1, 9) / 100)
            cond[8] = (fourthInningsCommentary.cell_value(r1, 10) == any) or (
                    probWinAft > fourthInningsCommentary.cell_value(r1, 10) / 100)
            cond[9] = (fourthInningsCommentary.cell_value(r1, 11) == any) or (
                    probWinAft <= fourthInningsCommentary.cell_value(r1, 11) / 100)
            cond[10] = (fourthInningsCommentary.cell_value(r1, 12) == any) or (
                    valBall >= fourthInningsCommentary.cell_value(r1, 12))
            cond[11] = (fourthInningsCommentary.cell_value(r1, 13) == any) or (
                    valBall < fourthInningsCommentary.cell_value(r1, 13))
            cond[12] = (fourthInningsCommentary.cell_value(r1, 14) == any) or (
                    ball >= fourthInningsCommentary.cell_value(r1, 14))
            cond[13] = (fourthInningsCommentary.cell_value(r1, 15) == any) or (
                    ball < fourthInningsCommentary.cell_value(r1, 15))
            cond[14] = (fourthInningsCommentary.cell_value(r1, 16) == any) or (
                    scbyTar >= fourthInningsCommentary.cell_value(r1, 16))
            cond[15] = (fourthInningsCommentary.cell_value(r1, 17) == any) or (
                    scbyTar < fourthInningsCommentary.cell_value(r1, 17))
            cond[16] = (fourthInningsCommentary.cell_value(r1, 18) == any) or (
                    projScbyTar >= fourthInningsCommentary.cell_value(r1, 18))
            cond[17] = (fourthInningsCommentary.cell_value(r1, 19) == any) or (
                    projScbyTar < fourthInningsCommentary.cell_value(r1, 19))
            cond[18] = (fourthInningsCommentary.cell_value(r1, 20) == any) or (
                    actScbyTar >= fourthInningsCommentary.cell_value(r1, 20))
            cond[19] = (fourthInningsCommentary.cell_value(r1, 21) == any) or (
                    actScbyTar < fourthInningsCommentary.cell_value(r1, 21))

            condTrue = 1
            for con in range(0, 20, 1):
                # print(r1, ' row ', con + 1, ' column ', cond[con])
                condTrue = condTrue and cond[con]
            # print(condTrue)
            # time.sleep(0.05)
            i = i + 1
            # print(i)
            if condTrue:
                # commentarySentence=fourthInningsCommentary.cell_value(r1,1)
                commentaryId = fourthInningsCommentary.cell_value(r1, 25)
                commentaryPitch = fourthInningsCommentary.cell_value(r1, 26)
                # worksheet.write(r, 23, commentarySentence)
                # commentaryRate = int(120 + (runsCopy % 10) * 8 + conseOut * 5 + delta * 5 + valBall)
                # commentaryVolume = commentaryRate / 200
                # commentaryVoice = commentaryRate % 4
                # commentaryVoice = commentaryVoice % 3
                # print('say it ksdjfkds dksjfsl lsfsldkjf dslfjjdksjf dskfsdkjfsdkjf dslkfhskdhf kdsfkfj')
                # engine.setProperty('rate', commentaryRate)
                # engine.setProperty('voice', voices[commentaryVoice].id)
                # engine.setProperty('volume', commentaryVolume)
                # engine.say(commentarySentence)
                # engine.runAndWait()
                break
    yaml.dump(
        commVar,
        open('comm/commentary_variables.yaml', 'w'),
        Dumper=yamlordereddictloader.Dumper,
        default_flow_style=False)
    #with open('commentary_variables.yaml', 'w') as file:
    #    yaml.dump(commVar, file)

    commentFileName = "comm/line" + str(int(commentaryId)) + ".wav"
    if commentaryPitch == 0:
        commentaryPitch = 20
    if conseOut == 1:  # this is deliberately done for woooohhh
        commentaryPitch = 10
    clapFileName = "comm/clap" + str(int(commentaryPitch / 10 - 1)) + ".wav"
    audio1 = AudioSegment.from_file(commentFileName)
    audio2 = AudioSegment.from_file(clapFileName)  # your second audio file
    audio22 = audio2 - 10
    audio11 = audio1 + 10
    # audio3 = AudioSegment.from_file("PinkPanther30.wav") #your third audio file

    mixed = audio11.overlay(audio22)  # combine , superimpose audio files
    # mixed1 = mixed.overlay(audio3)          #Further combine , superimpose audio files
    # If you need to save mixed file
    mixed_name = "audio/mixed" + str(current_delivery) + "000" + str(curr_innings) + ".wav"
    mixed.export(mixed_name, format='wav')  # export mixed  audio file
    #play(mixed)
    #playsound(mixed_name)# play mixed audio file
    wave_obj = sa.WaveObject.from_wave_file(mixed_name)
    play_obj = wave_obj.play()
    print("commentary spoken")
    return commentaryId

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 18:03:49 2020

@author: Harsh Chaudhary
"""


def central_logic():
    global currdel
    global prevdel
    global current_delivery
    global curr_innings
    global bowled_flag
    ball_flag = 1
    global loop_exit
    print("central logic started")
    currdel['ts'] = int(time.time())
    batbody_impact_flag = 0
    foot_no_ball_flag = 0
    height_no_ball_flag = 0
    consecutive_pocket = 0
    # 11
    if currdel['extras']['no_ball'] == 1:
        height_no_ball_flag = 1

    # 12
    if currdel['bat_body_impact'] == 1:
        batbody_impact_flag = 1

    # 36
    # time.sleep(1)
    # print("just before bowled", time.time())
    # bowled_file = "\\\DESKTOP-V06BSS7\\bowled\\bowled.txt"
    # mod_time = os.path.getmtime(bowled_file)
    # print(mod_time)
    # #mod_timestamp = datetime.timestamp(mod_time)
    # now = datetime.now()
    # print(now)
    # curr_timestamp = datetime.timestamp(now)
    # print(curr_timestamp)
    # if (curr_timestamp - mod_time) < 5:
    #     bowled_flag = 1
    # else:
    #     bowled_flag = 0
    # bowled_flag = 0

    # 8 and 9
    # x axis is always along the wall
    # y axis is always perpendicular to wall and positive inside the wall
    if currdel['zone_id'] == 3920:
        consecutive_pocket = 1
        print("it was consecutive")
    currdel['consecutive_out_flag'] = 0
    currdel['extras']['no_ball'] = 0
    currdel['extras']['wides'] = 0
    currdel['runs']['batsman'] = 0
    currdel['out_type_id'] = 0
    print("yaml creation started", time.time())
    if ball_flag == 1:  # 7y
        if foot_no_ball_flag == 1:  # 10y
            currdel['extras']['no_ball'] = 1
            if bowled_flag == 1:  # 36y
                currdel['out_type_id'] = -2
                # dc1
                currdel['zone_id'] = -1
                currdel['bat_body_impact'] = 0
                currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras']['wides']
                if currdel['out_type_id'] > 0:
                    currdel['wic_after'] = prevdel['wic_after'] + 1
                else:
                    currdel['wic_after'] = prevdel['wic_after']
                currdel['valid_ball_no'] = prevdel['valid_ball_no']
            else:  # 36n
                if batbody_impact_flag == 0:  # 12n
                    currdel['bat_body_impact'] = 0
                    if consecutive_pocket == 1:  # 8,9n
                        currdel['consecutive_out_flag'] = (prevdel['consecutive_out_flag'] % 2)
                        if currdel['consecutive_out_flag'] == 1:  # 37y
                            # dc3
                            currdel['out_type_id'] = -4
                            currdel['zone_id'] = 3920
                            currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                'wides']
                            if currdel['out_type_id'] > 0:
                                currdel['wic_after'] = prevdel['wic_after'] + 1
                            else:
                                currdel['wic_after'] = prevdel['wic_after']
                                currdel['valid_ball_no'] = prevdel['valid_ball_no']
                        else:  # 37n
                            # dc4
                            currdel['out_type_id'] = 0
                            currdel['zone_id'] = 3920
                            currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                'wides']
                            if currdel['out_type_id'] > 0:
                                currdel['wic_after'] = prevdel['wic_after'] + 1
                            else:
                                currdel['wic_after'] = prevdel['wic_after']
                            currdel['valid_ball_no'] = prevdel['valid_ball_no']
                    else:  # 8,9y
                        curr_time = time.time()
                        curr_time_int = int(curr_time)
                        print("first 8,9y", curr_time)
                        # dc2
                        currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras']['wides']
                        currdel['consecutive_out_flag'] = (prevdel['consecutive_out_flag'] % 2)
                        if currdel['out_type_id'] > 0:
                            currdel['wic_after'] = prevdel['wic_after'] + 1
                        else:
                            currdel['wic_after'] = prevdel['wic_after']
                        currdel['valid_ball_no'] = prevdel['valid_ball_no']
                else:  # 12y
                    if consecutive_pocket == 1:  # 8,9n
                        currdel['consecutive_out_flag'] = (prevdel['consecutive_out_flag'] % 2)
                        if currdel['consecutive_out_flag'] == 1:  # 37y
                            # dc5
                            currdel['out_type_id'] = -4
                            currdel['zone_id'] = 3920
                            currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                'wides']
                            if currdel['out_type_id'] > 0:
                                currdel['wic_after'] = prevdel['wic_after'] + 1
                            else:
                                currdel['wic_after'] = prevdel['wic_after']
                            currdel['valid_ball_no'] = prevdel['valid_ball_no']
                        else:  # 37n
                            # dc6
                            currdel['out_type_id'] = 0
                            currdel['zone_id'] = 3920
                            currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                'wides']
                            if currdel['out_type_id'] > 0:
                                currdel['wic_after'] = prevdel['wic_after'] + 1
                            else:
                                currdel['wic_after'] = prevdel['wic_after']
                            currdel['valid_ball_no'] = prevdel['valid_ball_no']
                    else:  # 8,9y new logic
                        curr_time = time.time()
                        curr_time_int = int(curr_time)

                        currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras']['wides']
                        currdel['consecutive_out_flag'] = (prevdel['consecutive_out_flag'] % 2)
                        if currdel['out_type_id'] > 0:
                            currdel['wic_after'] = prevdel['wic_after'] + 1
                        else:
                            currdel['wic_after'] = prevdel['wic_after']
                        currdel['valid_ball_no'] = prevdel['valid_ball_no']
        else:  # 10n
            print("bowled", time.time())
            if bowled_flag == 1:  # 36y
                currdel['out_type_id'] = 2
                # dc7
                if currdel['out_type_id'] > 0:
                    currdel['wic_after'] = prevdel['wic_after'] + 1
                else:
                    currdel['wic_after'] = prevdel['wic_after']
                currdel['zone_id'] = -1
                currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras']['wides']
                currdel['valid_ball_no'] = prevdel['valid_ball_no'] + 1
            else:  # 36n
                if height_no_ball_flag == 1:  # 11y
                    currdel['extras']['no_ball'] = 1
                    if batbody_impact_flag == 0:  # 12n
                        currdel['bat_body_impact'] = 0
                        if consecutive_pocket == 1:  # 8,9n
                            currdel['consecutive_out_flag'] = (prevdel['consecutive_out_flag'] % 2)
                            if currdel['consecutive_out_flag'] == 1:  # 37y
                                # dc3
                                currdel['out_type_id'] = -4
                                currdel['zone_id'] = 3920
                                currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                    'wides']
                                if currdel['out_type_id'] > 0:
                                    currdel['wic_after'] = prevdel['wic_after'] + 1
                                else:
                                    currdel['wic_after'] = prevdel['wic_after']
                                currdel['valid_ball_no'] = prevdel['valid_ball_no']
                            else:  # 37n
                                # dc4
                                currdel['out_type_id'] = 0
                                currdel['zone_id'] = 3920
                                currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                    'wides']
                                if currdel['out_type_id'] > 0:
                                    currdel['wic_after'] = prevdel['wic_after'] + 1
                                else:
                                    currdel['wic_after'] = prevdel['wic_after']
                                currdel['valid_ball_no'] = prevdel['valid_ball_no']
                        else:  # 8,9y
                            curr_time = time.time()
                            curr_time_int = int(curr_time)

                            # dc2
                            currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                'wides']
                            currdel['consecutive_out_flag'] = (prevdel['consecutive_out_flag'] % 2)
                            if currdel['out_type_id'] > 0:
                                currdel['wic_after'] = prevdel['wic_after'] + 1
                            else:
                                currdel['wic_after'] = prevdel['wic_after']
                            currdel['valid_ball_no'] = prevdel['valid_ball_no']
                    else:  # 12y
                        if consecutive_pocket == 1:  # 8,9n
                            currdel['consecutive_out_flag'] = (prevdel['consecutive_out_flag'] % 2)
                            if currdel['consecutive_out_flag'] == 1:  # 37y
                                # dc5
                                currdel['out_type_id'] = -4
                                currdel['zone_id'] = 3920
                                currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                    'wides']
                                if currdel['out_type_id'] > 0:
                                    currdel['wic_after'] = prevdel['wic_after'] + 1
                                else:
                                    currdel['wic_after'] = prevdel['wic_after']
                                currdel['valid_ball_no'] = prevdel['valid_ball_no']
                            else:  # 37n
                                # dc6
                                currdel['out_type_id'] = 0
                                currdel['zone_id'] = 3920
                                currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                    'wides']
                                if currdel['out_type_id'] > 0:
                                    currdel['wic_after'] = prevdel['wic_after'] + 1
                                else:
                                    currdel['wic_after'] = prevdel['wic_after']
                                currdel['valid_ball_no'] = prevdel['valid_ball_no']
                        else:  # 8,9y new logic
                            curr_time = time.time()
                            curr_time_int = int(curr_time)

                            currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                'wides']
                            currdel['consecutive_out_flag'] = (prevdel['consecutive_out_flag'] % 2)
                            if currdel['out_type_id'] > 0:
                                currdel['wic_after'] = prevdel['wic_after'] + 1
                            else:
                                currdel['wic_after'] = prevdel['wic_after']
                            currdel['valid_ball_no'] = prevdel['valid_ball_no']
                else:  # 11n
                    print("batbodyimpact", time.time())
                    if batbody_impact_flag == 0:  # 12n
                        if consecutive_pocket == 0:  # 8,9y
                            curr_time = time.time()
                            print("8,9y", curr_time)
                            curr_time_int = int(curr_time)
                            currdel['extras']['wides'] = 1
                            currdel['consecutive_out_flag'] = prevdel['consecutive_out_flag']
                            currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                'wides']
                            if currdel['out_type_id'] > 0:
                                currdel['wic_after'] = prevdel['wic_after'] + 1
                            else:
                                currdel['wic_after'] = prevdel['wic_after']
                            currdel['valid_ball_no'] = prevdel['valid_ball_no']
                        else:  # 8,9n
                            currdel['consecutive_out_flag'] = (prevdel['consecutive_out_flag'] % 2) + 1
                            if currdel['consecutive_out_flag'] == 2:  # 37y
                                # dc10
                                currdel['out_type_id'] = 4
                                currdel['zone_id'] = 3920
                                currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                    'wides']
                                if currdel['out_type_id'] > 0:
                                    currdel['wic_after'] = prevdel['wic_after'] + 1
                                else:
                                    currdel['wic_after'] = prevdel['wic_after']
                                currdel['valid_ball_no'] = prevdel['valid_ball_no'] + 1
                            else:  # 37n
                                # dc9
                                currdel['out_type_id'] = 0
                                currdel['zone_id'] = 3920
                                currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                    'wides']
                                if currdel['out_type_id'] > 0:
                                    currdel['wic_after'] = prevdel['wic_after'] + 1
                                else:
                                    currdel['wic_after'] = prevdel['wic_after']
                                    currdel['valid_ball_no'] = prevdel['valid_ball_no'] + 1
                    else:  # 12y
                        if consecutive_pocket == 1:  # 8,9n
                            currdel['consecutive_out_flag'] = (prevdel['consecutive_out_flag'] % 2) + 1
                            if currdel['consecutive_out_flag'] == 2:  # 37y
                                # dc11
                                currdel['out_type_id'] = 4
                                currdel['zone_id'] = 3920
                                currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                    'wides']
                                if currdel['out_type_id'] > 0:
                                    currdel['wic_after'] = prevdel['wic_after'] + 1
                                else:
                                    currdel['wic_after'] = prevdel['wic_after']
                                currdel['valid_ball_no'] = prevdel['valid_ball_no'] + 1
                            else:  # 37n
                                # dc12
                                currdel['out_type_id'] = 0
                                currdel['zone_id'] = 3920
                                currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                    'wides']
                                if currdel['out_type_id'] > 0:
                                    currdel['wic_after'] = prevdel['wic_after'] + 1
                                else:
                                    currdel['wic_after'] = prevdel['wic_after']
                                currdel['valid_ball_no'] = prevdel['valid_ball_no'] + 1
                        else:  # 8,9y new logic
                            # time.sleep(1.5)
                            curr_time = time.time()
                            print("second 8,9y", curr_time)
                            curr_time_int = int(curr_time)

                            currdel['runs']['extras'] = currdel['extras']['no_ball'] + currdel['extras'][
                                'wides']
                            if currdel['out_type_id'] > 0:
                                currdel['wic_after'] = prevdel['wic_after'] + 1
                            else:
                                currdel['wic_after'] = prevdel['wic_after']
                            currdel['valid_ball_no'] = prevdel['valid_ball_no'] + 1
    if currdel['zone_id'] == 'null':
        currdel['zone_id'] = 9999
    a = currdel['zone_id']
    print("run decided")
    batrun = int(a)
    run0 = [9999]
    run1 = [1312, 1412, 1512, 3412, 3212, 3312, 3217, 3317, 3417, 3617, 1117, 3517, 1217, 1317, 1417, 1517]
    run3 = [1613, 1713, 1813, 1913, 2013, 2113, 2613, 2713, 2813, 2913, 3013, 3113]
    run4 = [2214, 2414]
    run6 = [2315]
    run2 = [3818, 3718, 4118, 4218, 1111, 1211, 3611, 3511, 2616, 2716, 2816, 2916, 3016, 3116, 1616, 1716,
            1816,
            1916, 2016, 2116, 4221, 4121, 3721, 3821]
    # print(detectionListWallCameras)
    if batbody_impact_flag == 1:
        if batrun in run0:
            currdel['runs']['batsman'] = 0
            print("run0")
        if batrun in run1:
            currdel['runs']['batsman'] = 1
        if batrun in run2:
            currdel['runs']['batsman'] = 2
        if batrun in run3:
            currdel['runs']['batsman'] = 3
        if batrun in run4:
            currdel['runs']['batsman'] = 4
        if batrun in run6:
            currdel['runs']['batsman'] = 6
        if foot_no_ball_flag == 1 or height_no_ball_flag == 1:
            if int(currdel['zone_id']) % 100 == currdel['out_zone_id']:
                currdel['runs']['batsman'] = 0
                currdel['out_type_id'] = -1
                currdel['runs']['total'] = int(currdel['runs']['extras']) + int(currdel['runs']['batsman'])
                currdel['score_after'] = int(prevdel['score_after']) + int(currdel['runs']['total'])
                if currdel['out_type_id'] > 0:
                    currdel['wic_after'] = int(prevdel['wic_after']) + 1
                else:
                    currdel['wic_after'] = prevdel['wic_after']
            else:
                currdel['runs']['total'] = int(currdel['runs']['extras']) + int(currdel['runs']['batsman'])
                currdel['score_after'] = int(prevdel['score_after']) + int(currdel['runs']['total'])
                if currdel['out_type_id'] > 0:
                    currdel['wic_after'] = int(prevdel['wic_after']) + 1
                else:
                    currdel['wic_after'] = prevdel['wic_after']
        else:
            if int(currdel['zone_id']) % 100 == currdel['out_zone_id']:
                currdel['out_type_id'] = 1
                currdel['runs']['batsman'] = 0
                currdel['runs']['total'] = int(currdel['runs']['extras']) + int(currdel['runs']['batsman'])
                currdel['score_after'] = int(prevdel['score_after']) + int(currdel['runs']['total'])
                if currdel['out_type_id'] > 0:
                    currdel['wic_after'] = int(prevdel['wic_after']) + 1
                else:
                    currdel['wic_after'] = prevdel['wic_after']
            else:
                currdel['runs']['total'] = int(currdel['runs']['extras']) + int(currdel['runs']['batsman'])
                currdel['score_after'] = int(prevdel['score_after']) + int(currdel['runs']['total'])
                if currdel['out_type_id'] > 0:
                    currdel['wic_after'] = int(prevdel['wic_after']) + 1
                else:
                    currdel['wic_after'] = prevdel['wic_after']

    currdel['runs']['total'] = int(currdel['runs']['extras']) + int(currdel['runs']['batsman'])
    currdel['score_after'] = int(prevdel['score_after']) + int(currdel['runs']['total'])
    print(currdel)
    currdel = collections.OrderedDict([(current_delivery, currdel)])

    yaml.dump(
        match_yaml,
        open('yaml/resume/match_yaml_pre.yaml', 'w'),
        Dumper=yamlordereddictloader.Dumper,
        default_flow_style=False)



    match_yaml['meta']['deliveries_completed'] = int(match_yaml['meta']['deliveries_completed']) + 1
    if curr_innings == 1:
        if current_delivery == 1:
            match_yaml['innings']['first_innings']['deliveries'][0] = currdel
        else:
            match_yaml['innings']['first_innings']['deliveries'].append(currdel)
    if curr_innings == 2:
        if current_delivery == 1:
            match_yaml['innings']['second_innings']['deliveries'][0] = currdel
        else:
            match_yaml['innings']['second_innings']['deliveries'].append(currdel)
    if curr_innings == 3:
        if current_delivery == 1:
            match_yaml['innings']['third_innings']['deliveries'][0] = currdel
        else:
            match_yaml['innings']['third_innings']['deliveries'].append(currdel)
    if curr_innings == 4:
        if current_delivery == 1:
            match_yaml['innings']['fourth_innings']['deliveries'][0] = currdel
        else:
            match_yaml['innings']['fourth_innings']['deliveries'].append(currdel)
    comm_id = CodeCommen()

    if curr_innings == 1:
        match_yaml['innings']['first_innings']['deliveries'][current_delivery - 1][current_delivery][
            'commentary_line_id'] = int(comm_id)
    if curr_innings == 2:
        match_yaml['innings']['second_innings']['deliveries'][current_delivery - 1][current_delivery][
            'commentary_line_id'] = int(comm_id)
    if curr_innings == 3:
        match_yaml['innings']['third_innings']['deliveries'][current_delivery - 1][current_delivery][
            'commentary_line_id'] = int(comm_id)
    if curr_innings == 4:
        match_yaml['innings']['fourth_innings']['deliveries'][current_delivery - 1][current_delivery][
            'commentary_line_id'] = int(comm_id)

    off1 = [1312, 1412, 1512, 3412, 3212, 3312]
    off2 = [1111, 1211, 3611, 3511]
    off3 = [1613, 1713, 1813, 1913, 2013, 2113, 2613, 2713, 2813, 2913, 3013, 3113]
    leg1 = [3217, 3317, 3417, 3517, 1217, 1317, 1417, 1517, 3617, 1117]
    leg2 = [2616, 2716, 2816, 2916, 3016, 3116, 1616, 1716, 1816, 1916, 2016, 2116]
    backoff2 = [4221, 4121, 3721, 3821]
    backleg2 = [3718, 3818, 4218, 4118]
    four = [2214, 2414]
    six = [2315]
    if curr_innings == 1:
        currdel = match_yaml['innings']['first_innings']['deliveries'][current_delivery - 1][current_delivery]
    if curr_innings == 2:
        currdel = match_yaml['innings']['second_innings']['deliveries'][current_delivery - 1][current_delivery]
    if curr_innings == 3:
        currdel = match_yaml['innings']['third_innings']['deliveries'][current_delivery - 1][current_delivery]
    if curr_innings == 4:
        currdel = match_yaml['innings']['fourth_innings']['deliveries'][current_delivery - 1][current_delivery]
    if curr_innings == 1:
        if match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['out_method'] = currdel[
                    'out_type_id']
            match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['runs_scored'] = \
                int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['runs_scored']) + \
                currdel['runs']['batsman']
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['balls_faced'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['balls_faced'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['off1_runs_scored'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                            'off1_runs_scored']) + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['off2_runs_scored'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                            'off2_runs_scored']) + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['off3_runs_scored'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                            'off3_runs_scored']) + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['leg1_runs_scored'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                            'leg1_runs_scored']) + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['leg2_runs_scored'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                            'leg2_runs_scored']) + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['backoff2_runs_scored'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                            'backoff2_runs_scored']) + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['backleg2_runs_scored'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                            'backleg2_runs_scored']) + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['four_runs_scored'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                            'four_runs_scored']) + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['six_runs_scored'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                            'six_runs_scored']) + \
                    currdel['runs'][
                        'batsman']
        elif match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['out_method'] = currdel[
                    'out_type_id']
            match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['runs_scored'] = \
                currdel['runs'][
                    'batsman'] + \
                int(match_yaml['innings'][
                        'first_innings'][
                        'batting_players_involved'][
                        'batsman2'][
                        'runs_scored'])
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['balls_faced'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman2'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['balls_faced'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['off1_runs_scored'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman2'][
                            'off1_runs_scored']) + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['off2_runs_scored'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman2'][
                            'off2_runs_scored']) + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['off3_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['off3_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['leg1_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['leg1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['leg2_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['leg2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['backoff2_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman2'][
                        'backoff2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['backleg2_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman2'][
                        'backleg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['four_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['four_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['six_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['six_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
        elif match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['out_method'] = currdel[
                    'out_type_id']
            match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['runs_scored'] = \
                currdel['runs'][
                    'batsman'] + \
                match_yaml['innings'][
                    'first_innings'][
                    'batting_players_involved'][
                    'batsman3'][
                    'runs_scored']
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['balls_faced'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman3'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman']['balls_faced'] = \
                    int(match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['off1_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['off1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['off2_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['off2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['off3_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['off3_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['leg1_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['leg1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['leg2_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['leg2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['backoff2_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman3'][
                        'backoff2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['backleg2_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman3'][
                        'backleg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['four_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['four_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['six_runs_scored'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman3']['six_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
    elif curr_innings == 2:
        if match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['out_method'] = currdel[
                    'out_type_id']
            else:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['out_method'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['out_method']
            match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['runs_scored'] = \
                currdel['runs'][
                    'batsman'] + \
                match_yaml['innings'][
                    'second_innings'][
                    'batting_players_involved'][
                    'batsman1'][
                    'runs_scored']
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['balls_faced'] = \
                    int(match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['balls_faced'] = \
                    int(match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['off1_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                        'off1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['off2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                        'off2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['off3_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                        'off3_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['leg1_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                        'leg1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['leg2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                        'leg2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                    'backoff2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                        'backoff2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                    'backleg2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                        'backleg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['four_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                        'four_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['six_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['six_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
        elif match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['out_method'] = currdel[
                    'out_type_id']
            else:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['out_method'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['out_method']
            match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['runs_scored'] = \
                currdel['runs'][
                    'batsman'] + \
                match_yaml['innings'][
                    'second_innings'][
                    'batting_players_involved'][
                    'batsman2'][
                    'runs_scored']
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['balls_faced'] = \
                    int(match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['balls_faced'] = \
                    int(match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['off1_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                        'off1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['off2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                        'off2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['off3_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                        'off3_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['leg1_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                        'leg1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['leg2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                        'leg2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                    'backoff2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                        'backoff2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                    'backleg2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                        'backleg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['four_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                        'four_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['six_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['six_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
        elif match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['out_method'] = currdel[
                    'out_type_id']
            else:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['out_method'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['out_method']
            match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['runs_scored'] = \
                currdel['runs'][
                    'batsman'] + \
                match_yaml['innings'][
                    'second_innings'][
                    'batting_players_involved'][
                    'batsman3'][
                    'runs_scored']
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['balls_faced'] = \
                    int(match_yaml['innings']['second_innings']['batting_players_involved']['batsman3'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['balls_faced'] = \
                    int(match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['off1_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman3'][
                        'off1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['off2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman3'][
                        'off2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['off3_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman3'][
                        'off3_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['leg1_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman3'][
                        'leg1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['leg2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman3'][
                        'leg2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3'][
                    'backoff2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman3'][
                        'backoff2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3'][
                    'backleg2_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman3'][
                        'backleg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['four_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman3'][
                        'four_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['six_runs_scored'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman3']['six_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
    elif curr_innings == 3:
        if match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['out_method'] = currdel[
                    'out_type_id']
            else:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['out_method'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['out_method']
            match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['runs_scored'] = \
                currdel['runs'][
                    'batsman'] + \
                match_yaml['innings'][
                    'third_innings'][
                    'batting_players_involved'][
                    'batsman1'][
                    'runs_scored']
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['balls_faced'] = \
                    int(match_yaml['innings']['third_innings']['batting_players_involved']['batsman1'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['balls_faced'] = \
                    int(match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['off1_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['off1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['off2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['off2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['off3_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['off3_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['leg1_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['leg1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['leg2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['leg2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['backoff2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1'][
                        'backoff2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['backleg2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1'][
                        'backleg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['four_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['four_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['six_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['six_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
        elif match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['out_method'] = currdel[
                    'out_type_id']
            else:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['out_method'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['out_method']
            match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['runs_scored'] = \
                currdel['runs'][
                    'batsman'] + \
                match_yaml['innings'][
                    'third_innings'][
                    'batting_players_involved'][
                    'batsman2'][
                    'runs_scored']
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['balls_faced'] = \
                    int(match_yaml['innings']['third_innings']['batting_players_involved']['batsman2'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['balls_faced'] = \
                    int(match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['off1_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['off1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['off2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['off2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['off3_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['off3_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['leg1_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['leg1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['leg2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['leg2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['backoff2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2'][
                        'backoff2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['backleg2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2'][
                        'backleg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['four_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['four_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['six_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['six_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
        elif match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['out_method'] = currdel[
                    'out_type_id']
            else:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['out_method'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['out_method']
            match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['runs_scored'] = \
                currdel['runs'][
                    'batsman'] + \
                match_yaml['innings'][
                    'third_innings'][
                    'batting_players_involved'][
                    'batsman3'][
                    'runs_scored']
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['balls_faced'] = \
                    int(match_yaml['innings']['third_innings']['batting_players_involved']['batsman3'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['balls_faced'] = \
                    int(match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['off1_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['off1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['off2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['off2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['off3_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['off3_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['leg1_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['leg1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['leg2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['leg2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['backoff2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman3'][
                        'backoff2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['backleg2_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman3'][
                        'backleg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['four_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['four_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['six_runs_scored'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman3']['six_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
    elif curr_innings == 4:
        if match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['out_method'] = currdel[
                    'out_type_id']
            else:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['out_method'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['out_method']
            match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['runs_scored'] = \
                currdel['runs'][
                    'batsman'] + \
                match_yaml['innings'][
                    'fourth_innings'][
                    'batting_players_involved'][
                    'batsman1'][
                    'runs_scored']
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['balls_faced'] = \
                    int(match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['balls_faced'] = \
                    int(match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['off1_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                        'off1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['off2_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                        'off2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['off3_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                        'off3_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['leg1_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                        'leg1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['leg2_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                        'leg2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                    'backoff2_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                        'backoff2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                    'backleg2_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                        'backleg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['four_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                        'four_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['six_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['six_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
        elif match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['out_method'] = currdel[
                    'out_type_id']
            else:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['out_method'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['out_method']
            match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['runs_scored'] = \
                currdel['runs'][
                    'batsman'] + \
                match_yaml['innings'][
                    'fourth_innings'][
                    'batting_players_involved'][
                    'batsman2'][
                    'runs_scored']
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['balls_faced'] = \
                    int(match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['balls_faced'] = \
                    int(match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['off1_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                        'off1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['off2_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                        'off2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['off3_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                        'off3_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['leg1_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                        'leg1_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['leg2_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                        'leg2_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                    'backoff2_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                        'backoff2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                    'backleg2_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                        'backleg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['four_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                        'four_runs_scored'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['six_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['six_runs_scored'] + \
                    currdel['runs']['batsman']
        elif match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['player_id'] == currdel[
            'batsman_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['out_method'] = currdel[
                    'out_type_id']
            else:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['out_method'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['out_method']
            match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['runs_scored'] = \
                currdel['runs'][
                    'batsman'] + \
                match_yaml['innings'][
                    'fourth_innings'][
                    'batting_players_involved'][
                    'batsman3'][
                    'runs_scored']
            if currdel['extras']['wides'] == 0:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['balls_faced'] = \
                    int(match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3'][
                            'balls_faced']) + 1
            else:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['balls_faced'] = \
                    int(match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['balls_faced'])
            if currdel['zone_id'] in off1:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['off1_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3'][
                        'off1_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['off2_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3'][
                        'off2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['off3_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3'][
                        'off3_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['leg1_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3'][
                        'leg1_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['leg2_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3'][
                        'leg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3'][
                    'backoff2_runs_scored'] = \
                    match_yaml['fourth_innings']['batting_players_involved']['batsman3'][
                        'backoff2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3'][
                    'backleg2_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3'][
                        'backleg2_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['four_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3'][
                        'four_runs_scored'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['six_runs_scored'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman3']['six_runs_scored'] + \
                    currdel['runs']['batsman']
    if curr_innings == 1:
        if match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wickets_taken'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + 1
                if match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wickets_taken'] == 1:
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wickets_taken'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['balls_bowled'] + 1
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['balls_bowled']
            match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['runs_given'] = \
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
                currdel['runs'][
                    'total']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['off1_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['off2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['off3_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['off3_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['leg1_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['leg2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['backoff2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['backleg2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['four_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['six_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['no_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['no_balls_bowled'] + 1
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['no_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled']
        if match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wickets_taken'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wickets_taken'] + 1
                if match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wickets_taken'] == 1:
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wickets_taken'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['balls_bowled'] + 1
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['balls_bowled']
            match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['runs_given'] = \
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['runs_given'] + \
                currdel['runs'][
                    'total']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['off1_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['off2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['off3_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['off3_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['leg1_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['leg2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['backoff2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['backleg2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['four_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['six_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['no_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['no_balls_bowled'] + 1
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['no_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled']
        if match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['wickets_taken'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['wickets_taken'] + 1
                if match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['wickets_taken'] == 1:
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['wickets_taken'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['balls_bowled'] + 1
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['balls_bowled']
            match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['runs_given'] = \
            currdel['runs'][
                'total'] + match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['runs_given']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['off1_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['off2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['off3_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['off3_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['leg1_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['leg2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['backoff2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['backleg2_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['four_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['six_runs_given'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['no_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['no_balls_bowled'] + 1
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['no_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled']
    elif curr_innings == 2:
        if match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wickets_taken'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + 1
                if match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wickets_taken'] == 1:
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wickets_taken'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['balls_bowled'] + 1
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['balls_bowled']
            match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['runs_given'] = \
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
                currdel['runs'][
                    'total']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['off1_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['off2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['off3_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['off3_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['leg1_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['leg2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['backoff2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['backleg2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['four_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['six_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['no_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1'][
                        'no_balls_bowled'] + 1
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['no_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled']
        if match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wickets_taken'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wickets_taken'] + 1
                if match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wickets_taken'] == 1:
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wickets_taken'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['balls_bowled'] + 1
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['balls_bowled']
            match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['runs_given'] = \
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['runs_given'] + \
                currdel['runs'][
                    'total']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['off1_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['off2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['off3_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['off3_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['leg1_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['leg2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['backoff2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['backleg2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['four_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['six_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['no_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2'][
                        'no_balls_bowled'] + 1
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['no_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled']
        if match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['wickets_taken'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['wickets_taken'] + 1
                if match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['wickets_taken'] == 1:
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['wickets_taken'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['balls_bowled'] + 1
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['balls_bowled']
            match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['runs_given'] = \
            currdel['runs'][
                'total'] + match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['runs_given']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['off1_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['off2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['off3_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['off3_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['leg1_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['leg2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['backoff2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['backleg2_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['four_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['six_runs_given'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['no_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3'][
                        'no_balls_bowled'] + 1
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['no_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled']
    elif curr_innings == 3:
        if match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wickets_taken'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + 1
                if match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wickets_taken'] == 1:
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wickets_taken'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['balls_bowled'] + 1
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['balls_bowled']
            match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['runs_given'] = \
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
                currdel['runs'][
                    'total']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['off1_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['off2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['off3_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['off3_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['leg1_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['leg2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['backoff2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['backleg2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['four_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['six_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['no_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['no_balls_bowled'] + 1
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['no_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled']
        if match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wickets_taken'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wickets_taken'] + 1
                if match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wickets_taken'] == 1:
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wickets_taken'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['balls_bowled'] + 1
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['balls_bowled']
            match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['runs_given'] = \
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['runs_given'] + \
                currdel['runs'][
                    'total']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['off1_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['off2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['off3_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['off3_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['leg1_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['leg2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['backoff2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['backleg2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['four_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['six_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['no_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['no_balls_bowled'] + 1
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['no_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled']
        if match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['wickets_taken'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['wickets_taken'] + 1
                if match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['wickets_taken'] == 1:
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['wickets_taken'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['balls_bowled'] + 1
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['balls_bowled']
            match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['runs_given'] = \
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['runs_given'] + \
                currdel['runs'][
                    'total']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['off1_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['off2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['off3_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['off3_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['leg1_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['leg2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['backoff2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['backleg2_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['four_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['six_runs_given'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['no_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['no_balls_bowled'] + 1
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['no_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled']
    elif curr_innings == 4:
        if match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['wickets_taken'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + 1
                if match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['wickets_taken'] == 1:
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['wickets_taken'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['balls_bowled'] + 1
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['balls_bowled']
            match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['runs_given'] = \
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
                currdel['runs'][
                    'total']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['off1_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['off2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['off3_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['off3_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['leg1_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['leg2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['backoff2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['backleg2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['four_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['six_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['no_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1'][
                        'no_balls_bowled'] + 1
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['no_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['wide_balls_bowled']
        if match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wickets_taken'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wickets_taken'] + 1
                if match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wickets_taken'] == 1:
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wickets_taken'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['balls_bowled'] + 1
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['balls_bowled']
            match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['runs_given'] = \
            currdel['runs'][
                'total'] + \
            match_yaml['innings']['fourth_innings']['bowling_players_involved'][
                'bowler2'][
                'runs_given']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['off1_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['off2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['off3_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['off3_runs_given'] + \
                    currdel['runs']['batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['leg1_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['leg2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['backoff2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['backleg2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['four_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['six_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['no_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2'][
                        'no_balls_bowled'] + 1
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['no_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wide_balls_bowled']
        if match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['player_id'] == currdel[
            'bowler_player_id']:
            if currdel['out_type_id'] > 0:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['wickets_taken'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['wickets_taken'] + 1
                if match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['wickets_taken'] == 1:
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['wicket1_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3'][
                    'wickets_taken'] == 2:
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['wicket2_method'] = \
                        currdel[
                            'out_type_id']
                elif match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3'][
                    'wickets_taken'] == 3:
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['wicket3_method'] = \
                        currdel[
                            'out_type_id']
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['wickets_taken'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['wickets_taken']
            if currdel['runs']['extras'] == 0:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['balls_bowled'] + 1
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['balls_bowled']
            match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['runs_given'] = \
            currdel['runs'][
                'total'] + match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['runs_given']
            if currdel['zone_id'] in off1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['off1_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['off1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['off2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['off2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in off3:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['off3_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['off3_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['leg1_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['leg1_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in leg2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['leg2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['leg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backoff2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['backoff2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3'][
                        'backoff2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in backleg2:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['backleg2_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3'][
                        'backleg2_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in four:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['four_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['four_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            elif currdel['zone_id'] in six:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['six_runs_given'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['six_runs_given'] + \
                    currdel['runs'][
                        'batsman']
            if currdel['extras']['no_ball'] == 1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['no_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3'][
                        'no_balls_bowled'] + 1
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['no_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['no_balls_bowled']
            if currdel['extras']['wides'] == 1:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3'][
                        'wide_balls_bowled'] + 1
            else:
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler3']['wide_balls_bowled']
    print("yaml creation")
    yaml.dump(
        match_yaml,
        open('yaml/match_yaml_dump.yaml', 'w'),
        Dumper=yamlordereddictloader.Dumper,
        default_flow_style=False)
    yaml.dump(
        match_yaml,
        open('yaml/resume/match_yaml_dump.yaml', 'w'),
        Dumper=yamlordereddictloader.Dumper,
        default_flow_style=False)



    with open("empty_sc_yaml.yaml") as f:
        sc_yaml = yaml.load(f, Loader=yamlordereddictloader.Loader)

    sc_yaml['meta']['created'] = match_yaml['meta']['created']

    def findInningOvers(innings_check):
        if innings_check == 1:
            no_of_deliveries = len(match_yaml['innings']['first_innings']['deliveries'])
            valid_balls = match_yaml['innings']['first_innings']['deliveries'][no_of_deliveries - 1][no_of_deliveries][
                'valid_ball_no']
            return str(valid_balls // 6) + '.' + str(valid_balls % 6)
        elif innings_check == 2:
            no_of_deliveries = len(match_yaml['innings']['second_innings']['deliveries'])
            valid_balls = match_yaml['innings']['second_innings']['deliveries'][no_of_deliveries - 1][no_of_deliveries][
                'valid_ball_no']
            return str(valid_balls // 6) + '.' + str(valid_balls % 6)
        elif innings_check == 3:
            no_of_deliveries = len(match_yaml['innings']['third_innings']['deliveries'])
            valid_balls = match_yaml['innings']['third_innings']['deliveries'][no_of_deliveries - 1][no_of_deliveries][
                'valid_ball_no']
            return str(valid_balls // 6) + '.' + str(valid_balls % 6)
        else:
            no_of_deliveries = len(match_yaml['innings']['fourth_innings']['deliveries'])
            valid_balls = match_yaml['innings']['fourth_innings']['deliveries'][no_of_deliveries - 1][no_of_deliveries][
                'valid_ball_no']
            return str(valid_balls // 6) + '.' + str(valid_balls % 6)

    sc_yaml['meta']['innings_completed'] = match_yaml['meta']['innings_completed']
    sc_yaml['meta']['deliveries_completed'] = match_yaml['meta']['deliveries_completed']
    sc_yaml['info']['no_of_players'] = match_yaml['info']['no_of_players']
    sc_yaml['info']['total_overs'] = match_yaml['info']['overs']
    if match_yaml['info']['toss_winner'] == 1 and match_yaml['info']['toss_decision'] == 1:
        sc_yaml['info']['toss_winner'] = "अपनी गली"
        sc_yaml['info']['decision'] = 'BAT'
        sc_yaml['info']['batteam1'] = "अपनी गली"
        sc_yaml['info']['batteam2'] = "बाजू गली"
    elif match_yaml['info']['toss_winner'] == 1 and match_yaml['info']['toss_decision'] == 2:
        sc_yaml['info']['toss_winner'] = "अपनी गली"
        sc_yaml['info']['decision'] = 'BOWL'
        sc_yaml['info']['batteam1'] = "बाजू गली"
        sc_yaml['info']['batteam2'] = "अपनी गली"
    elif match_yaml['info']['toss_winner'] == 2 and match_yaml['info']['toss_decision'] == 1:
        sc_yaml['info']['toss_winner'] = "बाजू गली"
        sc_yaml['info']['decision'] = 'BAT'
        sc_yaml['info']['batteam1'] = "बाजू गली"
        sc_yaml['info']['batteam2'] = "अपनी गली"
    else:
        sc_yaml['info']['toss_winner'] = "बाजू गली"
        sc_yaml['info']['decision'] = 'BOWL'
        sc_yaml['info']['batteam1'] = "अपनी गली"
        sc_yaml['info']['batteam2'] = "बाजू गली"
    sc_yaml['info']['overs'] = match_yaml['info']['overs']
    sc_yaml['info']['innings'] = match_yaml['info']['innings']
    innings = int(match_yaml['meta']['innings_completed']) + 1
    if innings == 1:
        innings_info = match_yaml['innings']['first_innings']
    elif innings == 2:
        innings_info = match_yaml['innings']['second_innings']
        sc_yaml['info']['outcome']['t1i1_score'] = match_yaml['info']['outcome']['t1i1_score']
        sc_yaml['info']['outcome']['t1i1_wicket'] = match_yaml['info']['outcome']['t1i1_wicket']
        sc_yaml['info']['outcome']['t1i1_overs'] = findInningOvers(1)
    elif innings == 3:
        innings_info = match_yaml['innings']['third_innings']
        sc_yaml['info']['outcome']['t1i1_score'] = match_yaml['info']['outcome']['t1i1_score']
        sc_yaml['info']['outcome']['t1i1_wicket'] = match_yaml['info']['outcome']['t1i1_wicket']
        sc_yaml['info']['outcome']['t2i1_score'] = match_yaml['info']['outcome']['t2i1_score']
        sc_yaml['info']['outcome']['t2i1_wicket'] = match_yaml['info']['outcome']['t2i1_wicket']
        sc_yaml['info']['outcome']['t1i1_overs'] = findInningOvers(1)
        sc_yaml['info']['outcome']['t2i1_overs'] = findInningOvers(2)
        sc_yaml['info']['outcome']['t1i2_overs'] = findInningOvers(3)
    else:
        innings_info = match_yaml['innings']['fourth_innings']
        current_delivery = len(innings_info['deliveries'])
        sc_yaml['info']['outcome']['t1i1_score'] = match_yaml['info']['outcome']['t1i1_score']
        sc_yaml['info']['outcome']['t1i1_wicket'] = match_yaml['info']['outcome']['t1i1_wicket']
        sc_yaml['info']['outcome']['t2i1_score'] = match_yaml['info']['outcome']['t2i1_score']
        sc_yaml['info']['outcome']['t2i1_wicket'] = match_yaml['info']['outcome']['t2i1_wicket']
        sc_yaml['info']['outcome']['t1i2_score'] = match_yaml['info']['outcome']['t1i2_score']
        sc_yaml['info']['outcome']['t1i2_wicket'] = match_yaml['info']['outcome']['t1i2_wicket']
        sc_yaml['info']['outcome']['t2i2_score'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['score_after']
        sc_yaml['info']['outcome']['t2i2_wicket'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['wic_after']
        sc_yaml['info']['outcome']['t1i1_overs'] = findInningOvers(1)
        sc_yaml['info']['outcome']['t2i1_overs'] = findInningOvers(2)
        sc_yaml['info']['outcome']['t1i2_overs'] = findInningOvers(3)
        sc_yaml['info']['outcome']['t2i2_overs'] = findInningOvers(4)


    # variables to hold scores and wickets and deliveries
    current_delivery = len(innings_info['deliveries'])
    sc_yaml['info']['current_score'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['score_after']
    sc_yaml['info']['current_wic'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['wic_after']
    sc_yaml['info']['current_valid_ball'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['valid_ball_no']
    sc_yaml['info']['current_cf'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['consecutive_out_flag']
    sc_yaml['info']['prob_after'] = innings_info['deliveries'][current_delivery - 1][current_delivery][
        'prob_after']
    if innings_info['deliveries'][current_delivery - 1][current_delivery]['extras']['wides'] == 1:
        sc_yaml['info']['nb_wd_con'] = "wd"
    elif innings_info['deliveries'][current_delivery - 1][current_delivery]['extras']['no_ball'] == 1:
        sc_yaml['info']['nb_wd_con'] = "nb"
    elif innings_info['deliveries'][current_delivery - 1][current_delivery]['consecutive_out_flag'] == 1:
        sc_yaml['info']['nb_wd_con'] = "con"
    else:
        sc_yaml['info']['nb_wd_con'] = "  "
    batting_team_no = int(innings_info['batteam'])
    if batting_team_no == 1:
        sc_yaml['info']['bat_team_name'] = match_yaml['info']['teams']['team1']['player1']['player_name'][0:7] + " & " + \
                        match_yaml['info']['teams']['team1']['player2']['player_name'][0:7]
    else:
        sc_yaml['info']['bat_team_name'] = match_yaml['info']['teams']['team2']['player1']['player_name'][0:7] + " & " + \
                        match_yaml['info']['teams']['team2']['player2']['player_name'][0:7]
    curr_bowl_id = innings_info['deliveries'][current_delivery - 1][current_delivery]['bowler_player_id']
    curr_batsman_id = innings_info['deliveries'][current_delivery - 1][current_delivery]['batsman_player_id']
    sc_yaml['info']['curr_batsman'] = curr_batsman_id
    sc_yaml['info']['curr_bowler'] = curr_bowl_id

    # loop for batsman'stats
    if innings_info['batting_players_involved']['batsman1']['player_id'] == curr_batsman_id:
        sc_yaml['info']['runs_curr_bat'] = innings_info['batting_players_involved']['batsman1']['runs_scored']
        sc_yaml['info']['bowls_curr_bat'] = innings_info['batting_players_involved']['batsman1']['balls_faced']
    elif innings_info['batting_players_involved']['batsman2']['player_id'] == curr_batsman_id:
        sc_yaml['info']['runs_curr_bat'] = innings_info['batting_players_involved']['batsman2']['runs_scored']
        sc_yaml['info']['bowls_curr_bat'] = innings_info['batting_players_involved']['batsman2']['balls_faced']
    else:
        sc_yaml['info']['runs_curr_bat'] = innings_info['batting_players_involved']['batsman3']['runs_scored']
        sc_yaml['info']['bowls_curr_bat'] = innings_info['batting_players_involved']['batsman3']['balls_faced']

    if innings_info['bowling_players_involved']['bowler1']['player_id'] == curr_bowl_id:
        sc_yaml['info']['runs_curr_bow'] = innings_info['bowling_players_involved']['bowler1']['runs_given']
        sc_yaml['info']['bowls_curr_bow'] = innings_info['bowling_players_involved']['bowler1']['balls_bowled']
        sc_yaml['info']['wics_curr_bow'] = innings_info['bowling_players_involved']['bowler1']['wickets_taken']
    elif innings_info['bowling_players_involved']['bowler2']['player_id'] == curr_bowl_id:
        sc_yaml['info']['runs_curr_bow'] = innings_info['bowling_players_involved']['bowler2']['runs_given']
        sc_yaml['info']['bowls_curr_bow'] = innings_info['bowling_players_involved']['bowler2']['balls_bowled']
        sc_yaml['info']['wics_curr_bow'] = innings_info['bowling_players_involved']['bowler2']['wickets_taken']
    else:
        sc_yaml['info']['runs_curr_bow'] = innings_info['bowling_players_involved']['bowler3']['runs_given']
        sc_yaml['info']['bowls_curr_bow'] = innings_info['bowling_players_involved']['bowler3']['balls_bowled']
        sc_yaml['info']['wics_curr_bow'] = innings_info['bowling_players_involved']['bowler3']['wickets_taken']

    sc_yaml['info']['curr_out_type_id'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['out_type_id']
    sc_yaml['info']['curr_ball_run'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['runs']['total']





    yaml.dump(sc_yaml, open('yaml/sc_yaml.yaml', 'w'), Dumper=yamlordereddictloader.Dumper,
              default_flow_style=False)

    #yaml.dump(sc_yaml,open('\\\LAPTOP-NBIUC8KC\\yaml/sc_yaml.yaml', 'w'),Dumper=yamlordereddictloader.Dumper,default_flow_style=False)
    #time.sleep(0.5)
    #os.system('\\\DESKTOP-9CO7JQ3\\Score_Card\\ScoreCard.py')
    #time.sleep(5)
    fall_of_wicket = currdel['wic_after'] == 1 and currdel['out_type_id'] > 0
    if fall_of_wicket:
        len_btpc = len(match_yaml['info']['batting_player_choice'])
        btpc = collections.OrderedDict(
            [('deliveries_done', 0), ('old_batsman_id', -999), ('new_batsman_id', 10000001),
             ('change_type', 1)])
        btpc['deliveries_done'] = current_delivery
        btpc['old_batsman_id'] = currdel['batsman_player_id']
        if curr_innings == 1:
            if currdel['batsman_player_id'] == \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                        'player_id']:
                btpc['new_batsman_id'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['player_id']
            elif currdel['batsman_player_id'] == \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman2'][
                        'player_id']:
                btpc['new_batsman_id'] = \
                    match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['player_id']
        if curr_innings == 2:
            if currdel['batsman_player_id'] == \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                        'player_id']:
                btpc['new_batsman_id'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['player_id']
            elif currdel['batsman_player_id'] == \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                        'player_id']:
                btpc['new_batsman_id'] = \
                    match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['player_id']
        if curr_innings == 3:
            if currdel['batsman_player_id'] == \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1'][
                        'player_id']:
                btpc['new_batsman_id'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['player_id']
            elif currdel['batsman_player_id'] == \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman2'][
                        'player_id']:
                btpc['new_batsman_id'] = \
                    match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['player_id']
        if curr_innings == 4:
            if currdel['batsman_player_id'] == \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                        'player_id']:
                btpc['new_batsman_id'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['player_id']
            elif currdel['batsman_player_id'] == \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                        'player_id']:
                btpc['new_batsman_id'] = \
                    match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['player_id']
        bat_arm = 2
        if btpc['new_batsman_id'] == match_yaml['info']['teams']['team1']['player1']['player_id']:
            bat_arm = match_yaml['info']['teams']['team1']['player1']['batting_arm']
        if btpc['new_batsman_id'] == match_yaml['info']['teams']['team1']['player2']['player_id']:
            bat_arm = match_yaml['info']['teams']['team1']['player2']['batting_arm']
        if btpc['new_batsman_id'] == match_yaml['info']['teams']['team2']['player1']['player_id']:
            bat_arm = match_yaml['info']['teams']['team2']['player1']['batting_arm']
        if btpc['new_batsman_id'] == match_yaml['info']['teams']['team2']['player2']['player_id']:
            bat_arm = match_yaml['info']['teams']['team2']['player2']['batting_arm']
        f = open("yaml/flap.txt")
        con = f.read()
        f.close
        con1 = str(int(bat_arm) - 1) + con[1] + con[2]
        with open("yaml/flap.txt", 'w', encoding='utf-8') as f:
            f.write(con1)
        btpc = collections.OrderedDict([((len_btpc+1), btpc)])
        match_yaml['info']['batting_player_choice'].append(btpc)

    fourth_inn_end = False
    third_inn_end = False
    second_inn_end = False
    first_inn_end = False
    third_inn_match_end = False
    if curr_innings == 4:
        fourth_inn_end = currdel['wic_after'] == 2 or currdel['valid_ball_no'] == 24 or currdel['score_after'] > (
                    match_yaml['info']['outcome']['t1i1_score'] + match_yaml['info']['outcome']['t1i2_score'] -
                    match_yaml['info']['outcome']['t2i1_score'])
    if curr_innings == 3:
        third_inn_end = currdel['wic_after'] == 2 or currdel['valid_ball_no'] == 24
        third_inn_match_end = third_inn_end and match_yaml['info']['outcome']['t2i1_score'] > (
                    match_yaml['info']['outcome']['t1i1_score'] + currdel['score_after'])
    if curr_innings == 2:
        second_inn_end = currdel['wic_after'] == 2 or currdel['valid_ball_no'] == 24
    if curr_innings == 1:
        first_inn_end = currdel['wic_after'] == 2 or currdel['valid_ball_no'] == 24
    if fourth_inn_end or third_inn_match_end:
        loop_exit = 1
        match_yaml['meta']['NEE'] = 0
        if curr_innings == 4:
            match_yaml['info']['outcome']['t2i2_wicket'] = \
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1'][
                    'wickets_taken'] + \
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wickets_taken']
            match_yaml['info']['outcome']['t2i2_score'] = \
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['runs_given']
            team2_total_score = match_yaml['info']['outcome']['t2i1_score'] + match_yaml['info']['outcome'][
                't2i2_score']
        else:
            match_yaml['info']['outcome']['t1i2_wicket'] = \
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + \
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wickets_taken']
            match_yaml['info']['outcome']['t1i2_score'] = \
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['runs_given']
            team2_total_score = match_yaml['info']['outcome']['t2i1_score']

        team1_total_score = match_yaml['info']['outcome']['t1i1_score'] + match_yaml['info']['outcome'][
            't1i2_score']
        if team1_total_score > team2_total_score:
            match_yaml['info']['outcome']['result_type'] = 1
        elif team2_total_score > team1_total_score:
            match_yaml['info']['outcome']['result_type'] = 2
        elif team1_total_score == team2_total_score:
            match_yaml['info']['outcome']['result_type'] = 3


        if third_inn_match_end:
            match_yaml['info']['outcome']['innings_win'] = 1
        else:
            match_yaml['info']['outcome']['innings_win'] = 0

        if team1_total_score > team2_total_score:
            match_yaml['info']['outcome']['win_margin_runs'] = int(team1_total_score - team2_total_score)
            winner_team_id = 1
        else:
            match_yaml['info']['outcome']['win_margin_runs'] = int(team2_total_score - team1_total_score)
            winner_team_id = 2
        # Below 22 lines to be added to 3p, 4p...
        if match_yaml['info']['toss_winner'] == 1:
            if match_yaml['info']['toss_decision'] == 1:
                if winner_team_id == 1:
                    match_yaml['info']['outcome']['winner_team_id'] = 1
                else:
                    match_yaml['info']['outcome']['winner_team_id'] = 2
            else:
                if winner_team_id == 1:
                    match_yaml['info']['outcome']['winner_team_id'] = 2
                else:
                    match_yaml['info']['outcome']['winner_team_id'] = 1
        else:
            if match_yaml['info']['toss_decision'] == 2:
                if winner_team_id == 1:
                    match_yaml['info']['outcome']['winner_team_id'] = 1
                else:
                    match_yaml['info']['outcome']['winner_team_id'] = 2
            else:
                if winner_team_id == 1:
                    match_yaml['info']['outcome']['winner_team_id'] = 2
                else:
                    match_yaml['info']['outcome']['winner_team_id'] = 1

        if match_yaml['info']['outcome']['innings_win'] == 0:
            if team2_total_score > team1_total_score:
                match_yaml['info']['outcome']['win_margin_balls_left'] = (
                        24 - currdel['valid_ball_no'])
                match_yaml['info']['outcome']['win_margin_wickets_left'] = (
                        2 - currdel['wic_after'])
            else:
                match_yaml['info']['outcome']['win_margin_runs'] = int(team1_total_score - team2_total_score)
        else:
            match_yaml['info']['outcome']['win_margin_runs'] = int(team2_total_score - team1_total_score)
        # these 7 lines to be added to 3p, 4p...
        sc_yaml['info']['outcome']['result_type'] = match_yaml['info']['outcome']['result_type']
        sc_yaml['info']['outcome']['innings_win'] = match_yaml['info']['outcome']['innings_win']
        sc_yaml['info']['outcome']['winner_team_id'] = match_yaml['info']['outcome']['winner_team_id']
        sc_yaml['info']['outcome']['win_margin_runs'] = match_yaml['info']['outcome']['win_margin_runs']
        sc_yaml['info']['outcome']['win_margin_wickets_left'] = match_yaml['info']['outcome']['win_margin_wickets_left']
        sc_yaml['info']['outcome']['win_margin_balls_left'] = match_yaml['info']['outcome']['win_margin_balls_left']
        yaml.dump(sc_yaml, open('yaml/sc_yaml.yaml', 'w'), Dumper=yamlordereddictloader.Dumper,
                  default_flow_style=False)
    elif first_inn_end:
        loop_exit = 1
        match_yaml['info']['earlier_selected_out_zones'] = []
        match_yaml['info']['outcome']['t1i1_wicket'] = \
            match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + \
            match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wickets_taken']
        match_yaml['info']['outcome']['t1i1_score'] = \
            match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
            match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['runs_given']
        match_yaml['meta']['NEE'] = 345
        match_yaml['meta']['innings_completed'] = 1
        match_yaml['meta']['deliveries_completed'] = 0

    elif second_inn_end:
        loop_exit = 1
        match_yaml['info']['earlier_selected_out_zones'] = []
        match_yaml['info']['outcome']['t2i1_wicket'] = \
            match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + \
            match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wickets_taken']
        match_yaml['info']['outcome']['t2i1_score'] = \
            match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
            match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['runs_given']
        match_yaml['meta']['NEE'] = 345
        match_yaml['meta']['innings_completed'] = 2
        match_yaml['meta']['deliveries_completed'] = 0

    elif third_inn_end:
        loop_exit = 1
        match_yaml['info']['earlier_selected_out_zones'] = []
        match_yaml['info']['outcome']['t1i2_wicket'] = \
            match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + \
            match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wickets_taken']
        match_yaml['info']['outcome']['t1i2_score'] = \
            match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
            match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['runs_given']
        match_yaml['meta']['NEE'] = 345
        match_yaml['meta']['innings_completed'] = 3
        match_yaml['meta']['deliveries_completed'] = 0

    elif currdel['valid_ball_no'] % 6 == 0 and currdel['runs']['extras'] == 0:
        loop_exit = 1
        match_yaml['meta']['NEE'] = 5
        # match_yaml['info']['bowling_player_choice']['current_change'] = int(current_delivery / 6 + 1)
        len_bwpc = len(match_yaml['info']['bowling_player_choice'])
        bwpc = collections.OrderedDict(
            [('deliveries_done', 0), ('old_bowler_id', -999), ('new_bowler_id', 10000001)])
        bwpc['deliveries_done'] = current_delivery
        bwpc['old_bowler_id'] = currdel['bowler_player_id']
        if curr_innings == 1:
            if currdel['bowler_player_id'] == \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1'][
                        'player_id']:
                bwpc['new_bowler_id'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['player_id']
            elif currdel['bowler_player_id'] == \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2'][
                        'player_id']:
                bwpc['new_bowler_id'] = \
                    match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['player_id']
        if curr_innings == 2:
            if currdel['bowler_player_id'] == \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1'][
                        'player_id']:
                bwpc['new_bowler_id'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['player_id']
            elif currdel['bowler_player_id'] == \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2'][
                        'player_id']:
                bwpc['new_bowler_id'] = \
                    match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['player_id']
        if curr_innings == 3:
            if currdel['bowler_player_id'] == \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1'][
                        'player_id']:
                bwpc['new_bowler_id'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['player_id']
            elif currdel['bowler_player_id'] == \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2'][
                        'player_id']:
                bwpc['new_bowler_id'] = \
                    match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['player_id']
        if curr_innings == 4:
            if currdel['bowler_player_id'] == \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1'][
                        'player_id']:
                bwpc['new_bowler_id'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['player_id']
            elif currdel['bowler_player_id'] == \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2'][
                        'player_id']:
                bwpc['new_bowler_id'] = \
                    match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['player_id']
        bwpc = collections.OrderedDict([((len_bwpc+1), bwpc)])
        match_yaml['info']['bowling_player_choice'].append(bwpc)

def umpire_decision_righthandbat():
    global bowled_flag
    bowled_flag = 0
    def R_bowled():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        global bowled_flag
        currdel['bat_body_impact'] = 0
        currdel['zone_id'] = 9999
        bowled_flag = 1
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)
        central_logic()

    def assign_right_off_wide():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['bat_body_impact'] = 0
        currdel['zone_id'] = 4121
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)
        central_logic()

    def assign_right_leg_wide():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['bat_body_impact'] = 0
        currdel['zone_id'] = 3818
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def Rassign_no_ball():
        global RNo_Ball
        currdel['extras']['no_ball'] = 1
        RNo_Ball['state'] = 'disabled'

    def Rassign_no_zone():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 9999
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def Rassign_keeper():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 3920
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def rassign_off1():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 1412
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def rassign_off2():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 1111
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def rassign_off3():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 1813
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def rassign_leg1():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 3417
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def rassign_leg2():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 2916
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def rassign_offback2():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 4121
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def rassign_legback2():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 3818
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def rassign_st4_1():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 2214
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def rassign_st4_2():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 2414
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    def rassign_st6():
        global Roffwide
        global Rlegwide
        global RNo_Ball
        global RNo_Zone
        global RKeeper
        global RLB2
        global ROB2
        global RO1
        global RO2
        global RO3
        global RL1
        global RL2
        global RST4_1
        global RST4_2
        global RST6
        global Rbowled
        currdel['zone_id'] = 2315
        RNo_Zone['state'] = 'disabled'
        RKeeper['state'] = 'disabled'
        RLB2['state'] = 'disabled'
        ROB2['state'] = 'disabled'
        RO1['state'] = 'disabled'
        RO2['state'] = 'disabled'
        RO3['state'] = 'disabled'
        RL1['state'] = 'disabled'
        RL2['state'] = 'disabled'
        RST4_1['state'] = 'disabled'
        RST4_2['state'] = 'disabled'
        RST6['state'] = 'disabled'
        RNo_Ball['state'] = 'disabled'
        Rlegwide['state'] = 'disabled'
        Roffwide['state'] = 'disabled'
        Rbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.58)

        central_logic()

    global Roffwide
    global Rlegwide
    global RNo_Ball
    global RNo_Zone
    global RKeeper
    global RLB2
    global ROB2
    global RO1
    global RO2
    global RO3
    global RL1
    global RL2
    global RST4_1
    global RST4_2
    global RST6
    global Rbowled
    top = tk.Tk()
    top.geometry("800x480+1+1")
    top.resizable(0, 0)
    top.title("New Toplevel")
    top.configure(background="#d9d9d9")
    notebook = ttk.Notebook(top)
    notebook.place(relx=0, rely=0, relheight=1.0, relwidth=1.0)
    umpire_pane = tk.Frame(notebook)
    notebook.add(umpire_pane, text='Umpire Decision')

    img1 = Image.open("backgroundblur.jpg")
    tk1_image = ImageTk.PhotoImage(img1)
    labelback = tk.Label(umpire_pane, image=tk1_image)
    labelback.pack()

    Label1 = tk.Label(umpire_pane)
    Label1.place(relx=0.312, rely=0.177, height=285, width=300)
    Label1.configure(font=font9)
    Label1.configure(bg='green')
    Label2 = tk.Label(umpire_pane)
    Label2.place(relx=0.312, rely=0.308, height=68, width=300)
    Label2.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Label2.configure(text='''Right-hand Batsman''', bg='green')

    Rbowled = tk.Button(umpire_pane, command=R_bowled)
    Rbowled.place(relx=0.88, rely=0.46, height=50, width=90)
    Rbowled.configure(activebackground="#ececec")
    Rbowled.configure(activeforeground="#000000")
    Rbowled.configure(background="#d9d9d9")
    Rbowled.configure(disabledforeground="#a3a3a3")
    Rbowled.configure(foreground="#000000")
    Rbowled.configure(highlightbackground="#d9d9d9")
    Rbowled.configure(highlightcolor="black")
    Rbowled.configure(pady="0")
    Rbowled.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Rbowled.configure(text='''Bowled''')

    Roffwide = tk.Button(umpire_pane, command=assign_right_off_wide)
    Roffwide.place(relx=0.312, rely=0.179, height=55, width=145)
    Roffwide.configure(activebackground="#ececec")
    Roffwide.configure(activeforeground="#000000")
    Roffwide.configure(background="#d9d9d9")
    Roffwide.configure(disabledforeground="#a3a3a3")
    Roffwide.configure(foreground="#000000")
    Roffwide.configure(highlightbackground="#d9d9d9")
    Roffwide.configure(highlightcolor="black")
    Roffwide.configure(pady="0")
    Roffwide.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Roffwide.configure(text='''Off Wide''')

    Rlegwide = tk.Button(umpire_pane, command=assign_right_leg_wide)
    Rlegwide.place(relx=0.502, rely=0.179, height=55, width=150)
    Rlegwide.configure(activebackground="#ececec")
    Rlegwide.configure(activeforeground="#000000")
    Rlegwide.configure(background="#d9d9d9")
    Rlegwide.configure(disabledforeground="#a3a3a3")
    Rlegwide.configure(foreground="#000000")
    Rlegwide.configure(highlightbackground="#d9d9d9")
    Rlegwide.configure(highlightcolor="black")
    Rlegwide.configure(pady="0")
    Rlegwide.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Rlegwide.configure(text='''Leg Wide''')

    RNo_Ball = tk.Button(umpire_pane, command=Rassign_no_ball)
    RNo_Ball.place(relx=0.4, rely=0.625, height=50, width=170)
    RNo_Ball.configure(activebackground="#ececec")
    RNo_Ball.configure(activeforeground="#000000")
    RNo_Ball.configure(background="#d9d9d9")
    RNo_Ball.configure(disabledforeground="#a3a3a3")
    RNo_Ball.configure(foreground="#000000")
    RNo_Ball.configure(highlightbackground="#d9d9d9")
    RNo_Ball.configure(highlightcolor="black")
    RNo_Ball.configure(pady="0")
    RNo_Ball.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RNo_Ball.configure(text='''No Ball''')

    ROB2 = tk.Button(umpire_pane, command=rassign_offback2)
    ROB2.place(relx=0.125, rely=0.0, height=85, width=200)
    ROB2.configure(activebackground="#ececec")
    ROB2.configure(activeforeground="#000000")
    ROB2.configure(background="#d9d9d9")
    ROB2.configure(disabledforeground="#a3a3a3")
    ROB2.configure(foreground="#000000")
    ROB2.configure(highlightbackground="#d9d9d9")
    ROB2.configure(highlightcolor="black")
    ROB2.configure(pady="0")
    ROB2.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    ROB2.configure(text='''Off Slip \n (2 Runs)''')

    RKeeper = tk.Button(umpire_pane, command=Rassign_keeper)
    RKeeper.place(relx=0.375, rely=0.0, height=85, width=200)
    RKeeper.configure(activebackground="#ececec")
    RKeeper.configure(activeforeground="#000000")
    RKeeper.configure(background="#d9d9d9")
    RKeeper.configure(disabledforeground="#a3a3a3")
    RKeeper.configure(foreground="#000000")
    RKeeper.configure(highlightbackground="#d9d9d9")
    RKeeper.configure(highlightcolor="black")
    RKeeper.configure(pady="0")
    RKeeper.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RKeeper.configure(text='''Keeper \n Zone''')

    RLB2 = tk.Button(umpire_pane, command=rassign_legback2)
    RLB2.place(relx=0.625, rely=0.0, height=85, width=200)
    RLB2.configure(activebackground="#ececec")
    RLB2.configure(activeforeground="#000000")
    RLB2.configure(background="#d9d9d9")
    RLB2.configure(disabledforeground="#a3a3a3")
    RLB2.configure(foreground="#000000")
    RLB2.configure(highlightbackground="#d9d9d9")
    RLB2.configure(highlightcolor="black")
    RLB2.configure(pady="0")
    RLB2.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RLB2.configure(text='''Fine Leg \n (2 Runs)''')

    RO2 = tk.Button(umpire_pane, command=rassign_off2)
    RO2.place(relx=0.125, rely=0.177, height=95, width=150)
    RO2.configure(activebackground="#ececec")
    RO2.configure(activeforeground="#000000")
    RO2.configure(background="#d9d9d9")
    RO2.configure(disabledforeground="#a3a3a3")
    RO2.configure(foreground="#000000")
    RO2.configure(highlightbackground="#d9d9d9")
    RO2.configure(highlightcolor="black")
    RO2.configure(pady="0")
    RO2.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RO2.configure(text='''Square \n Off \n (2 Runs)''')

    RO1 = tk.Button(umpire_pane, command=rassign_off1)
    RO1.configure(activebackground="#ececec")
    RO1.place(relx=0.125, rely=0.375, height=95, width=150)
    RO1.configure(activeforeground="#000000")
    RO1.configure(background="#d9d9d9")
    RO1.configure(disabledforeground="#a3a3a3")
    RO1.configure(foreground="#000000")
    RO1.configure(highlightbackground="#d9d9d9")
    RO1.configure(highlightcolor="black")
    RO1.configure(pady="0")
    RO1.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RO1.configure(text='''Cover \n (1 Run)''')

    RO3 = tk.Button(umpire_pane, command=rassign_off3)
    RO3.place(relx=0.125, rely=0.572, height=95, width=150)
    RO3.configure(activebackground="#ececec")
    RO3.configure(activeforeground="#000000")
    RO3.configure(background="#d9d9d9")
    RO3.configure(disabledforeground="#a3a3a3")
    RO3.configure(foreground="#000000")
    RO3.configure(highlightbackground="#d9d9d9")
    RO3.configure(highlightcolor="black")
    RO3.configure(pady="0")
    RO3.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RO3.configure(text='''Extra \n Cover \n (3 Runs)''')

    RST4_1 = tk.Button(umpire_pane, command=rassign_st4_1)
    RST4_1.place(relx=0.125, rely=0.771, height=95, width=200)
    RST4_1.configure(activebackground="#ececec")
    RST4_1.configure(activeforeground="#000000")
    RST4_1.configure(background="#d9d9d9")
    RST4_1.configure(disabledforeground="#a3a3a3")
    RST4_1.configure(foreground="#000000")
    RST4_1.configure(highlightbackground="#d9d9d9")
    RST4_1.configure(highlightcolor="black")
    RST4_1.configure(pady="0")
    RST4_1.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RST4_1.configure(text='''Mid Off \n (4 Runs)''')

    RST6 = tk.Button(umpire_pane, command=rassign_st6)
    RST6.place(relx=0.375, rely=0.771, height=95, width=200)
    RST6.configure(activebackground="#ececec")
    RST6.configure(activeforeground="#000000")
    RST6.configure(background="#d9d9d9")
    RST6.configure(disabledforeground="#a3a3a3")
    RST6.configure(foreground="#000000")
    RST6.configure(highlightbackground="#d9d9d9")
    RST6.configure(highlightcolor="black")
    RST6.configure(pady="0")
    RST6.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RST6.configure(text='''Straight \n (6 Runs)''')

    RST4_2 = tk.Button(umpire_pane, command=rassign_st4_2)
    RST4_2.place(relx=0.625, rely=0.771, height=95, width=200)
    RST4_2.configure(activebackground="#ececec")
    RST4_2.configure(activeforeground="#000000")
    RST4_2.configure(background="#d9d9d9")
    RST4_2.configure(disabledforeground="#a3a3a3")
    RST4_2.configure(foreground="#000000")
    RST4_2.configure(highlightbackground="#d9d9d9")
    RST4_2.configure(highlightcolor="black")
    RST4_2.configure(pady="0")
    RST4_2.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RST4_2.configure(text='''Mid On \n (4 Runs)''')

    RL1 = tk.Button(umpire_pane, command=rassign_leg1)
    RL1.place(relx=0.687, rely=0.177, height=143, width=150)
    RL1.configure(activebackground="#ececec")
    RL1.configure(activeforeground="#000000")
    RL1.configure(background="#d9d9d9")
    RL1.configure(disabledforeground="#a3a3a3")
    RL1.configure(foreground="#000000")
    RL1.configure(highlightbackground="#d9d9d9")
    RL1.configure(highlightcolor="black")
    RL1.configure(pady="0")
    RL1.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RL1.configure(text='''Square \n Leg \n (1 Run)''')

    RL2 = tk.Button(umpire_pane, command=rassign_leg2)
    RL2.place(relx=0.687, rely=0.475, height=135, width=150)
    RL2.configure(activebackground="#ececec")
    RL2.configure(activeforeground="#000000")
    RL2.configure(background="#d9d9d9")
    RL2.configure(disabledforeground="#a3a3a3")
    RL2.configure(foreground="#000000")
    RL2.configure(highlightbackground="#d9d9d9")
    RL2.configure(highlightcolor="black")
    RL2.configure(pady="0")
    RL2.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RL2.configure(text='''Mid \n Wicket \n (2 Runs)''')

    RNo_Zone = tk.Button(umpire_pane, command=Rassign_no_zone)
    RNo_Zone.place(relx=0.4, rely=0.466, height=50, width=170)
    RNo_Zone.configure(activebackground="#ececec")
    RNo_Zone.configure(activeforeground="#000000")
    RNo_Zone.configure(background="#d9d9d9")
    RNo_Zone.configure(disabledforeground="#a3a3a3")
    RNo_Zone.configure(foreground="#000000")
    RNo_Zone.configure(highlightbackground="#d9d9d9")
    RNo_Zone.configure(highlightcolor="black")
    RNo_Zone.configure(pady="0")
    RNo_Zone.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    RNo_Zone.configure(text='''Dot Ball \n (0 Runs)''')

    def disable_event():
        pass

    top.protocol("WM_DELETE_WINDOW", disable_event)

    tk.mainloop()

def umpire_decision_lefthandbat():
    global bowled_flag
    bowled_flag = 0
    def L_bowled():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        global bowled_flag
        bowled_flag = 1
        currdel['bat_body_impact'] = 0
        currdel['zone_id'] = 9999
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)
        central_logic()

    def assign_left_off_wide():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['bat_body_impact'] = 0
        currdel['zone_id'] = 3821
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def assign_left_leg_wide():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['bat_body_impact'] = 0
        currdel['zone_id'] = 4118
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def Lassign_no_ball():
        global LNo_Ball
        currdel['extras']['no_ball'] = 1
        LNo_Ball['state'] = 'disabled'

    def Lassign_no_zone():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 9999
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def Lassign_keeper():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 3920
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def lassign_off1():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 3312
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def lassign_off2():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 3611
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def lassign_off3():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 2913
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def lassign_leg1():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 1317
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def lassign_leg2():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 1816
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def lassign_offback2():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 3821
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def lassign_legback2():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 4118
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def lassign_st4_1():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 2214
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def lassign_st4_2():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 2414
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    def lassign_st6():
        global Loffwide
        global Llegwide
        global LNo_Ball
        global LNo_Zone
        global LKeeper
        global LLB2
        global LOB2
        global LO1
        global LO2
        global LO3
        global LL1
        global LL2
        global LST4_1
        global LST4_2
        global LST6
        global Lbowled
        currdel['zone_id'] = 2315
        LNo_Zone['state'] = 'disabled'
        LKeeper['state'] = 'disabled'
        LLB2['state'] = 'disabled'
        LOB2['state'] = 'disabled'
        LO1['state'] = 'disabled'
        LO2['state'] = 'disabled'
        LO3['state'] = 'disabled'
        LL1['state'] = 'disabled'
        LL2['state'] = 'disabled'
        LST4_1['state'] = 'disabled'
        LST4_2['state'] = 'disabled'
        LST6['state'] = 'disabled'
        Loffwide['state'] = 'disabled'
        Llegwide['state'] = 'disabled'
        LNo_Ball['state'] = 'disabled'
        Lbowled['state'] = 'disabled'

        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx=0.46, rely=0.4)

        central_logic()

    global Loffwide
    global Llegwide
    global LNo_Ball
    global LNo_Zone
    global LKeeper
    global LLB2
    global LOB2
    global LO1
    global LO2
    global LO3
    global LL1
    global LL2
    global LST4_1
    global LST4_2
    global LST6
    global Lbowled
    top = tk.Tk()
    top.geometry("800x480+1+1")
    top.resizable(0, 0)
    top.title("New Toplevel")
    top.configure(background="#d9d9d9")
    notebook = ttk.Notebook(top)
    notebook.place(relx=0, rely=0, relheight=1.0, relwidth=1.0)
    umpire_pane = tk.Frame(notebook)
    notebook.add(umpire_pane, text='Umpire Decision')

    img1 = Image.open("backgroundblur.jpg")
    tk1_image = ImageTk.PhotoImage(img1)
    labelback = tk.Label(umpire_pane, image=tk1_image)
    labelback.pack()

    Label1 = tk.Label(umpire_pane)
    Label1.place(relx=0.312, rely=0.177, height=285, width=300)
    Label1.configure(font=font9)
    Label1.configure(bg='green')

    Label2 = tk.Label(umpire_pane)
    Label2.place(relx=0.312, rely=0.308, height=68, width=300)
    Label2.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Label2.configure(text='''Left-hand Batsman''', bg='green')

    Lbowled = tk.Button(umpire_pane, command=L_bowled)
    Lbowled.place(relx=0.88, rely=0.46, height=50, width=90)
    Lbowled.configure(activebackground="#ececec")
    Lbowled.configure(activeforeground="#000000")
    Lbowled.configure(background="#d9d9d9")
    Lbowled.configure(disabledforeground="#a3a3a3")
    Lbowled.configure(foreground="#000000")
    Lbowled.configure(highlightbackground="#d9d9d9")
    Lbowled.configure(highlightcolor="black")
    Lbowled.configure(pady="0")
    Lbowled.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Lbowled.configure(text='''Bowled''')

    Llegwide = tk.Button(umpire_pane, command=assign_left_leg_wide)
    Llegwide.place(relx=0.312, rely=0.177, height=55, width=145)
    Llegwide.configure(activebackground="#ececec")
    Llegwide.configure(activeforeground="#000000")
    Llegwide.configure(background="#d9d9d9")
    Llegwide.configure(disabledforeground="#a3a3a3")
    Llegwide.configure(foreground="#000000")
    Llegwide.configure(highlightbackground="#d9d9d9")
    Llegwide.configure(highlightcolor="black")
    Llegwide.configure(pady="0")
    Llegwide.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Llegwide.configure(text='''Leg Wide''')

    Loffwide = tk.Button(umpire_pane, command=assign_left_off_wide)
    Loffwide.place(relx=0.502, rely=0.177, height=55, width=150)
    Loffwide.configure(activebackground="#ececec")
    Loffwide.configure(activeforeground="#000000")
    Loffwide.configure(background="#d9d9d9")
    Loffwide.configure(disabledforeground="#a3a3a3")
    Loffwide.configure(foreground="#000000")
    Loffwide.configure(highlightbackground="#d9d9d9")
    Loffwide.configure(highlightcolor="black")
    Loffwide.configure(pady="0")
    Loffwide.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Loffwide.configure(text='''Off Wide''')

    LNo_Ball = tk.Button(umpire_pane, command=Lassign_no_ball)
    LNo_Ball.place(relx=0.4, rely=0.625, height=50, width=170)
    LNo_Ball.configure(activebackground="#ececec")
    LNo_Ball.configure(activeforeground="#000000")
    LNo_Ball.configure(background="#d9d9d9")
    LNo_Ball.configure(disabledforeground="#a3a3a3")
    LNo_Ball.configure(foreground="#000000")
    LNo_Ball.configure(highlightbackground="#d9d9d9")
    LNo_Ball.configure(highlightcolor="black")
    LNo_Ball.configure(pady="0")
    LNo_Ball.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LNo_Ball.configure(text='''No Ball''')

    LLB2 = tk.Button(umpire_pane, command=lassign_legback2)
    LLB2.place(relx=0.125, rely=0.0, height=85, width=200)
    LLB2.configure(activebackground="#ececec")
    LLB2.configure(activeforeground="#000000")
    LLB2.configure(background="#d9d9d9")
    LLB2.configure(disabledforeground="#a3a3a3")
    LLB2.configure(foreground="#000000")
    LLB2.configure(highlightbackground="#d9d9d9")
    LLB2.configure(highlightcolor="black")
    LLB2.configure(pady="0")
    LLB2.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LLB2.configure(text='''Fine Leg \n (2 Runs)''')

    LKeeper = tk.Button(umpire_pane, command=Lassign_keeper)
    LKeeper.place(relx=0.375, rely=0.0, height=85, width=200)
    LKeeper.configure(activebackground="#ececec")
    LKeeper.configure(activeforeground="#000000")
    LKeeper.configure(background="#d9d9d9")
    LKeeper.configure(disabledforeground="#a3a3a3")
    LKeeper.configure(foreground="#000000")
    LKeeper.configure(highlightbackground="#d9d9d9")
    LKeeper.configure(highlightcolor="black")
    LKeeper.configure(pady="0")
    LKeeper.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LKeeper.configure(text='''Keeper \n Zone''')

    LOB2 = tk.Button(umpire_pane, command=lassign_offback2)
    LOB2.place(relx=0.625, rely=0.0, height=85, width=200)
    LOB2.configure(activebackground="#ececec")
    LOB2.configure(activeforeground="#000000")
    LOB2.configure(background="#d9d9d9")
    LOB2.configure(disabledforeground="#a3a3a3")
    LOB2.configure(foreground="#000000")
    LOB2.configure(highlightbackground="#d9d9d9")
    LOB2.configure(highlightcolor="black")
    LOB2.configure(pady="0")
    LOB2.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LOB2.configure(text='''Off Slip \n (2 Runs)''')

    LO2 = tk.Button(umpire_pane, command=lassign_off2)
    LO2.place(relx=0.687, rely=0.177, height=95, width=150)
    LO2.configure(activebackground="#ececec")
    LO2.configure(activeforeground="#000000")
    LO2.configure(background="#d9d9d9")
    LO2.configure(disabledforeground="#a3a3a3")
    LO2.configure(foreground="#000000")
    LO2.configure(highlightbackground="#d9d9d9")
    LO2.configure(highlightcolor="black")
    LO2.configure(pady="0")
    LO2.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LO2.configure(text='''Square \n Off \n (2 Runs)''')

    LO1 = tk.Button(umpire_pane, command=lassign_off1)
    LO1.place(relx=0.687, rely=0.375, height=95, width=150)
    LO1.configure(activebackground="#ececec")
    LO1.configure(activeforeground="#000000")
    LO1.configure(background="#d9d9d9")
    LO1.configure(disabledforeground="#a3a3a3")
    LO1.configure(foreground="#000000")
    LO1.configure(highlightbackground="#d9d9d9")
    LO1.configure(highlightcolor="black")
    LO1.configure(pady="0")
    LO1.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LO1.configure(text='''Cover \n (1 Run)''')

    LO3 = tk.Button(umpire_pane, command=lassign_off3)
    LO3.place(relx=0.687, rely=0.572, height=95, width=150)
    LO3.configure(activebackground="#ececec")
    LO3.configure(activeforeground="#000000")
    LO3.configure(background="#d9d9d9")
    LO3.configure(disabledforeground="#a3a3a3")
    LO3.configure(foreground="#000000")
    LO3.configure(highlightbackground="#d9d9d9")
    LO3.configure(highlightcolor="black")
    LO3.configure(pady="0")
    LO3.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LO3.configure(text='''Extra \n Cover \n (3 Runs)''')

    LST4_1 = tk.Button(umpire_pane, command=lassign_st4_1)
    LST4_1.place(relx=0.125, rely=0.771, height=95, width=200)
    LST4_1.configure(activebackground="#ececec")
    LST4_1.configure(activeforeground="#000000")
    LST4_1.configure(background="#d9d9d9")
    LST4_1.configure(disabledforeground="#a3a3a3")
    LST4_1.configure(foreground="#000000")
    LST4_1.configure(highlightbackground="#d9d9d9")
    LST4_1.configure(highlightcolor="black")
    LST4_1.configure(pady="0")
    LST4_1.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LST4_1.configure(text='''Mid On \n (4 Runs)''')

    LST6 = tk.Button(umpire_pane, command=lassign_st6)
    LST6.place(relx=0.375, rely=0.771, height=95, width=200)
    LST6.configure(activebackground="#ececec")
    LST6.configure(activeforeground="#000000")
    LST6.configure(background="#d9d9d9")
    LST6.configure(disabledforeground="#a3a3a3")
    LST6.configure(foreground="#000000")
    LST6.configure(highlightbackground="#d9d9d9")
    LST6.configure(highlightcolor="black")
    LST6.configure(pady="0")
    LST6.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LST6.configure(text='''Straight \n (6 Runs)''')

    LST4_2 = tk.Button(umpire_pane, command=lassign_st4_2)
    LST4_2.place(relx=0.625, rely=0.771, height=95, width=200)
    LST4_2.configure(activebackground="#ececec")
    LST4_2.configure(activeforeground="#000000")
    LST4_2.configure(background="#d9d9d9")
    LST4_2.configure(disabledforeground="#a3a3a3")
    LST4_2.configure(foreground="#000000")
    LST4_2.configure(highlightbackground="#d9d9d9")
    LST4_2.configure(highlightcolor="black")
    LST4_2.configure(pady="0")
    LST4_2.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LST4_2.configure(text='''Mid Off \n (4 Runs)''')

    LL1 = tk.Button(umpire_pane, command=lassign_leg1)
    LL1.place(relx=0.125, rely=0.177, height=141, width=150)
    LL1.configure(activebackground="#ececec")
    LL1.configure(activeforeground="#000000")
    LL1.configure(background="#d9d9d9")
    LL1.configure(disabledforeground="#a3a3a3")
    LL1.configure(foreground="#000000")
    LL1.configure(highlightbackground="#d9d9d9")
    LL1.configure(highlightcolor="black")
    LL1.configure(pady="0")
    LL1.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LL1.configure(text='''Square \n Leg \n (1 Run)''')

    LL2 = tk.Button(umpire_pane, command=lassign_leg2)
    LL2.place(relx=0.125, rely=0.475, height=130, width=150)
    LL2.configure(activebackground="#ececec")
    LL2.configure(activeforeground="#000000")
    LL2.configure(background="#d9d9d9")
    LL2.configure(disabledforeground="#a3a3a3")
    LL2.configure(foreground="#000000")
    LL2.configure(highlightbackground="#d9d9d9")
    LL2.configure(highlightcolor="black")
    LL2.configure(pady="0")
    LL2.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LL2.configure(text='''Mid \n Wicket \n (2 Runs)''')

    LNo_Zone = tk.Button(umpire_pane, command=Lassign_no_zone)
    LNo_Zone.place(relx=0.312, rely=0.45, height=68, width=300)
    LNo_Zone.configure(activebackground="#ececec")
    LNo_Zone.configure(activeforeground="#000000")
    LNo_Zone.configure(background="#d9d9d9")
    LNo_Zone.configure(disabledforeground="#a3a3a3")
    LNo_Zone.configure(foreground="#000000")
    LNo_Zone.configure(highlightbackground="#d9d9d9")
    LNo_Zone.configure(highlightcolor="black")
    LNo_Zone.configure(pady="0")
    LNo_Zone.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    LNo_Zone.configure(text='''Dot Ball \n(0 Runs)''')

    def disable_event():
        pass

    top.protocol("WM_DELETE_WINDOW", disable_event)

    tk.mainloop()

def arena_central():
    global currdel
    global prevdel

    print("arena central start")
    consecutive_pocket = 0

    global loop_exit
    global current_delivery
    global curr_innings

    loop_exit = 0

    while loop_exit == 0:
        ball_flag = 1
        curr_innings = int(match_yaml['meta']['innings_completed']) + 1
        if curr_innings == 1:
            innings_info = match_yaml['innings']['first_innings']
        elif curr_innings == 2:
            innings_info = match_yaml['innings']['second_innings']
        elif curr_innings == 3:
            innings_info = match_yaml['innings']['third_innings']
        else:
            innings_info = match_yaml['innings']['fourth_innings']
        print("line 683 print", time.time())

        # variables to hold scores and wickets and deliveries
        if len(innings_info['deliveries']) == 1 and innings_info['deliveries'][0] == None:
            current_delivery = 1
            prevdel = collections.OrderedDict(
                [('valid_ball_no', 0), ('batsman_player_id', 10000004), ('bowler_player_id', 10000001),
                 ('fielder1_player_id', -9999), ('fielder2_player_id', -9999), ('consecutive_out_flag', 0),
                 ('zone_id', 9999), ('out_zone_id', 5), ('out_type_id', -1), ('catch_player_id', -9999),
                 ('bat_body_impact', 1), ('body_touch', -9999), ('bat_touch', -9999),
                 ('extras', collections.OrderedDict([('wides', 0), ('no_ball', 0)])),
                 ('runs', collections.OrderedDict([('batsman', 0), ('extras', 0), ('total', 0)])), ('score_after', 0),
                 ('wic_after', 0), ('commentary_line_id', 99999999)])
        else:
            current_delivery = len(innings_info['deliveries']) + 1
            prevdel = innings_info['deliveries'][current_delivery - 2][current_delivery - 1]
        print("just before currdel assignment", time.time())

        currdel = collections.OrderedDict(
            [('valid_ball_no', 0), ('batsman_player_id', 10000004), ('bowler_player_id', 10000001),
             ('fielder1_player_id', -9999), ('fielder2_player_id', -9999), ('consecutive_out_flag', 0),
             ('zone_id', 9999), ('out_zone_id', 5), ('out_type_id', -1), ('catch_player_id', -9999),
             ('bat_body_impact', 1), ('body_touch', -9999), ('bat_touch', -9999),
             ('extras', collections.OrderedDict([('wides', 0), ('no_ball', 0)])),
             ('runs', collections.OrderedDict([('batsman', 0), ('extras', 0), ('total', 0)])), ('score_after', 0),
             ('wic_after', 0), ('commentary_line_id', 99999999)])

        print("just after currdel assignment", time.time())
        len_btpc = len(match_yaml['info']['batting_player_choice'])
        print("len btpc", len_btpc)
        currdel['batsman_player_id'] = match_yaml['info']['batting_player_choice'][len_btpc-1][len_btpc]['new_batsman_id']
        len_bwpc = len(match_yaml['info']['bowling_player_choice'])
        print("len bwpc", len_bwpc)
        currdel['bowler_player_id'] = match_yaml['info']['bowling_player_choice'][len_bwpc - 1][len_bwpc]['new_bowler_id']
        currdel['out_zone_id'] = match_yaml['info']['current_outzone_selected']
        if currdel['batsman_player_id'] == match_yaml['info']['teams']['team1']['player1']['player_id']:
            batsman_hand = match_yaml['info']['teams']['team1']['player1']['batting_arm']
        if currdel['batsman_player_id'] == match_yaml['info']['teams']['team1']['player2']['player_id']:
            batsman_hand = match_yaml['info']['teams']['team1']['player2']['batting_arm']
        if currdel['batsman_player_id'] == match_yaml['info']['teams']['team1']['player3']['player_id']:
            batsman_hand = match_yaml['info']['teams']['team1']['player3']['batting_arm']
        if currdel['batsman_player_id'] == match_yaml['info']['teams']['team2']['player1']['player_id']:
            batsman_hand = match_yaml['info']['teams']['team2']['player1']['batting_arm']
        if currdel['batsman_player_id'] == match_yaml['info']['teams']['team2']['player2']['player_id']:
            batsman_hand = match_yaml['info']['teams']['team2']['player2']['batting_arm']
        if currdel['batsman_player_id'] == match_yaml['info']['teams']['team2']['player3']['player_id']:
            batsman_hand = match_yaml['info']['teams']['team2']['player3']['batting_arm']



        if int(batsman_hand) == 1:
            umpire_decision_lefthandbat()
        elif int(batsman_hand) == 2:
            umpire_decision_righthandbat()




json_file = json.load(open('excelfirstlinedata.json', 'r'))
slot_details = {}
DICT = {'innings': 1}
batsman_selected = False
bowler_selected = False
outZoneCode = {12: 'OFF 1',
               19: 'OFF BACK 2',
               18: 'LEG BACK 2',
               11: 'OFF 2',
               14: 'ST 4',
               17: 'LEG 1',
               13: 'OFF 3',
               15: 'ST 6',
               16: 'LEG 2'}

font9 = "-family {Segoe UI Black} -size 24 -weight bold"
_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = '#d9d9d9'  # X11 color: 'gray85'
_ana1color = '#d9d9d9'  # X11 color: 'gray85'
_ana2color = '#ececec'  # Closest X11 color: 'gray92'
# style = ttk.Style()
# if sys.platform == "win32":
#     style.theme_use('winnative')
# style.configure('.', background=_bgcolor)
# style.configure('.', foreground=_fgcolor)
# style.configure('.', font="TkDefaultFont")
# style.map('.', background=
# [('selected', _compcolor), ('active', _ana2color)])
#
# style.configure('TNotebook.Tab', background=_bgcolor)
# style.configure('TNotebook.Tab', foreground=_fgcolor)
# style.map('TNotebook.Tab', background=
# [('selected', _compcolor), ('active', _ana2color)])


def _1_and_2():

    def makeKeyboard():
        # top = tk.Tk()
        otp_pane = tk.Tk()
        # top.geometry("1366x768+1+1")
        otp_pane.geometry("800x480+1+1")

        otp_pane.resizable(0, 0)
        otp_pane.title("OTP Pane")

        otp_pane.configure(background="azure3")

        def validateOtp(otp):
            global slot_details
            if otp == json_file['booking_data']['prev1_time_slot']['otp_web']:
                slot_details = json_file['booking_data']['prev1_time_slot']
            elif otp == json_file['booking_data']['prev2_time_slot']['otp_web']:
                slot_details = json_file['booking_data']['prev2_time_slot']
            elif otp == json_file['booking_data']['curr_time_slot']['otp_web']:
                slot_details = json_file['booking_data']['curr_time_slot']
            else:
                print("condition not possible")

            current_date_time = datetime.now()
            match_yaml['info']['date'][0] = current_date_time.strftime("%Y%m%d")
            match_yaml['info']['arena_id'] = 24401
            curr_time = current_date_time.strftime("%H:%M")
            hour, minutes = int(curr_time.split(':')[0]), int(curr_time.split(':')[1])
            if hour < 24:
                if minutes <= 15:
                    minute_phase = 1
                elif minutes > 15 and minutes <= 30:
                    minute_phase = 2
                elif minutes > 30 and minutes <= 45:
                    minute_phase = 3
                elif minutes > 45:
                    minute_phase = 4
            match_yaml['info']['slots'][0] = hour * 4 + minute_phase
            match_yaml['info']['no_of_players'] = slot_details['no_of_players']
            match_yaml['info']['limited_overs'] = slot_details['limited_overs']
            match_yaml['info']['tournament_id'] = slot_details['tournament_id']
            if slot_details['no_of_players'] == 6:
                if slot_details['team1']['player1']['gender'] == slot_details['team1']['player2']['gender'] == \
                        slot_details['team1']['player3']['gender'] == slot_details['team2']['player1']['gender'] == \
                        slot_details['team2']['player2']['gender'] == slot_details['team2']['player3']['gender'] == 1:
                    match_yaml['info']['gender'] = 1
                elif slot_details['team1']['player1']['gender'] == slot_details['team1']['player2']['gender'] == \
                        slot_details['team1']['player3']['gender'] == slot_details['team2']['player1']['gender'] == \
                        slot_details['team2']['player2']['gender'] == slot_details['team2']['player3']['gender'] == 2:
                    match_yaml['info']['gender'] = 2
                else:
                    match_yaml['info']['gender'] = 3
            # for 4 players
            elif slot_details['no_of_players'] == 4:
                if slot_details['team1']['player1']['gender'] == slot_details['team1']['player2']['gender'] == \
                        slot_details['team2']['player1']['gender'] == slot_details['team2']['player2']['gender'] == 1:
                    match_yaml['info']['gender'] = 1
                elif slot_details['team1']['player1']['gender'] == slot_details['team1']['player2']['gender'] == \
                        slot_details['team2']['player1']['gender'] == slot_details['team2']['player2']['gender'] == 2:
                    match_yaml['info']['gender'] = 2
                else:
                    match_yaml['info']['gender'] = 3
            # for 2 players
            elif slot_details['no_of_players'] == 2:
                if slot_details['team1']['player1']['gender'] == slot_details['team2']['player1']['gender'] == 1:
                    match_yaml['info']['gender'] = 1
                elif slot_details['team1']['player1']['gender'] == slot_details['team2']['player1']['gender'] == 2:
                    match_yaml['info']['gender'] = 2
                else:
                    match_yaml['info']['gender'] = 3
            match_yaml['meta']['match_id'] = int(
                current_date_time.strftime("%y%m%d") + str(match_yaml['info']['arena_id']) + \
                str(match_yaml['info']['slots'][0]))
            match_yaml['meta']['created'] = int(time.time())
            match_yaml['info']['innings'] = 4
            if slot_details['no_of_players'] == 6:
                match_yaml['info']['overs'] = 5
            elif slot_details['no_of_players'] == 4:
                match_yaml['info']['overs'] = 4
            elif slot_details['no_of_players'] == 2:
                match_yaml['info']['overs'] = 2
            match_yaml['info']['teams']['team1']['player1']['player_id'] = slot_details['team1']['player1']['player_id']
            match_yaml['info']['teams']['team1']['player1']['player_name'] = slot_details['team1']['player1'][
                'player_name']
            team_yaml['teams']['team1']['player1']['player_id'] = slot_details['team1']['player1']['player_id']
            team_yaml['teams']['team1']['player1']['player_name'] = slot_details['team1']['player1']['player_name']
            sc_yaml_dummy['info']['curr_batsman'] = slot_details['team1']['player1']['player_id']
            match_yaml['info']['teams']['team1']['player1']['batting_arm'] = slot_details['team1']['player1'][
                'batting_arm']
            match_yaml['info']['teams']['team1']['player1']['bowling_arm'] = slot_details['team1']['player1'][
                'bowling_arm']
            match_yaml['info']['teams']['team1']['player1']['player_rating_string_before'] = \
                slot_details['team1']['player1']['player_rating_string_before']
            match_yaml['info']['teams']['team1']['player1']['batsman_rating_string_before'] = \
                slot_details['team1']['player1']['batsman_rating_string_before']
            match_yaml['info']['teams']['team1']['player1']['bowler_rating_string_before'] = \
                slot_details['team1']['player1']['bowler_rating_string_before']
            match_yaml['info']['teams']['team1']['player2']['player_id'] = slot_details['team1']['player2']['player_id']
            match_yaml['info']['teams']['team1']['player2']['player_name'] = slot_details['team1']['player2'][
                'player_name']
            team_yaml['teams']['team1']['player2']['player_id'] = slot_details['team1']['player2']['player_id']
            team_yaml['teams']['team1']['player2']['player_name'] = slot_details['team1']['player2']['player_name']
            match_yaml['info']['teams']['team1']['player2']['batting_arm'] = slot_details['team1']['player2'][
                'batting_arm']
            match_yaml['info']['teams']['team1']['player2']['bowling_arm'] = slot_details['team1']['player2'][
                'bowling_arm']
            match_yaml['info']['teams']['team1']['player2']['player_rating_string_before'] = \
                slot_details['team1']['player2']['player_rating_string_before']
            match_yaml['info']['teams']['team1']['player2']['batsman_rating_string_before'] = \
                slot_details['team1']['player2']['batsman_rating_string_before']
            match_yaml['info']['teams']['team1']['player2']['bowler_rating_string_before'] = \
                slot_details['team1']['player2']['bowler_rating_string_before']
            # match_yaml['info']['teams']['team1']['player3']['player_id'] = slot_details['team1']['player3']['player_id']
            # match_yaml['info']['teams']['team1']['player3']['player_name'] = slot_details['team1']['player3']['player_name']
            # match_yaml['info']['teams']['team1']['player3']['batting_arm'] = slot_details['team1']['player3']['batting_arm']
            # match_yaml['info']['teams']['team1']['player3']['bowling_arm'] = slot_details['team1']['player3']['bowling_arm']
            # match_yaml['info']['teams']['team1']['player3']['player_rating_string_before'] = \
            #    slot_details['team1']['player3']['player_rating_string_before']
            # match_yaml['info']['teams']['team1']['player3']['batsman_rating_string_before'] = \
            #    slot_details['team1']['player3']['batsman_rating_string_before']
            # match_yaml['info']['teams']['team1']['player3']['bowler_rating_string_before'] = \
            #    slot_details['team1']['player3']['bowler_rating_string_before']
            match_yaml['info']['teams']['team2']['player1']['player_id'] = slot_details['team2']['player1']['player_id']
            match_yaml['info']['teams']['team2']['player1']['player_name'] = slot_details['team2']['player1'][
                'player_name']
            team_yaml['teams']['team2']['player1']['player_id'] = slot_details['team2']['player1']['player_id']
            team_yaml['teams']['team2']['player1']['player_name'] = slot_details['team2']['player1']['player_name']
            sc_yaml_dummy['info']['curr_bowler'] = slot_details['team2']['player1']['player_id']
            match_yaml['info']['teams']['team2']['player1']['batting_arm'] = slot_details['team2']['player1'][
                'batting_arm']
            match_yaml['info']['teams']['team2']['player1']['bowling_arm'] = slot_details['team2']['player1'][
                'bowling_arm']
            match_yaml['info']['teams']['team2']['player1']['player_rating_string_before'] = \
                slot_details['team2']['player1']['player_rating_string_before']
            match_yaml['info']['teams']['team2']['player1']['batsman_rating_string_before'] = \
                slot_details['team2']['player1']['batsman_rating_string_before']
            match_yaml['info']['teams']['team2']['player1']['bowler_rating_string_before'] = \
                slot_details['team2']['player1']['bowler_rating_string_before']
            match_yaml['info']['teams']['team2']['player2']['player_id'] = slot_details['team2']['player2']['player_id']
            match_yaml['info']['teams']['team2']['player2']['player_name'] = slot_details['team2']['player2'][
                'player_name']
            team_yaml['teams']['team2']['player2']['player_id'] = slot_details['team2']['player2']['player_id']
            team_yaml['teams']['team2']['player2']['player_name'] = slot_details['team2']['player2']['player_name']
            match_yaml['info']['teams']['team2']['player2']['batting_arm'] = slot_details['team2']['player2'][
                'batting_arm']
            match_yaml['info']['teams']['team2']['player2']['bowling_arm'] = slot_details['team2']['player2'][
                'bowling_arm']
            match_yaml['info']['teams']['team2']['player2']['player_rating_string_before'] = \
                slot_details['team2']['player2']['player_rating_string_before']
            match_yaml['info']['teams']['team2']['player2']['batsman_rating_string_before'] = \
                slot_details['team2']['player2']['batsman_rating_string_before']
            match_yaml['info']['teams']['team2']['player2']['bowler_rating_string_before'] = \
                slot_details['team2']['player2']['bowler_rating_string_before']

            # match_yaml['info']['teams']['team2']['player3']['player_id'] = slot_details['team2']['player3']['player_id']
            # match_yaml['info']['teams']['team2']['player3']['player_name'] = slot_details['team2']['player3']['player_name']
            # match_yaml['info']['teams']['team2']['player3']['batting_arm'] = slot_details['team2']['player3']['batting_arm']
            # match_yaml['info']['teams']['team2']['player3']['bowling_arm'] = slot_details['team2']['player3']['bowling_arm']
            # match_yaml['info']['teams']['team2']['player3']['player_rating_string_before'] = \
            #    slot_details['team2']['player3']['player_rating_string_before']
            # match_yaml['info']['teams']['team2']['player3']['batsman_rating_string_before'] = \
            #    slot_details['team2']['player3']['batsman_rating_string_before']
            # match_yaml['info']['teams']['team2']['player3']['bowler_rating_string_before'] = \
            #    slot_details['team2']['player3']['bowler_rating_string_before']

            yaml.dump(team_yaml, open('yaml/team_yaml.yaml', 'w'),
                      Dumper=yamlordereddictloader.Dumper, default_flow_style=False)
            yaml.dump(sc_yaml_dummy, open('yaml/sc_yaml.yaml', 'w'),
                      Dumper=yamlordereddictloader.Dumper, default_flow_style=False)
            otp_pane.destroy()

            showTeamInfo()




        def pressed(x):
            if x == 'BACK':
                box.delete(1.0, tk.END)
            elif x == 'CONFIRM':
                if int(box.get(1.0, tk.END)) == json_file['booking_data']['prev1_time_slot']['otp_web'] \
                        or int(box.get(1.0, tk.END)) == json_file['booking_data']['prev2_time_slot']['otp_web'] \
                        or int(box.get(1.0, tk.END)) == json_file['booking_data']['curr_time_slot']['otp_web']:
                    validateOtp(int(box.get(1.0, tk.END)))
                else:
                    box.delete(1.0, tk.END)
            else:
                box.insert(tk.INSERT, x)

        box = tk.Text(otp_pane, width=15, height=10)
        print("box made")
        box.grid(row=0, column=0, columnspan=5)
        buttons = ['1', '2', '3',
                    '4', '5', '6',
                    '7', '8', '9',
                    '0',
                   'BACK',  'CONFIRM']
        varRow = 5
        varColumn = 0
        for button in buttons:
            command = lambda x=button: pressed(x)
            if varRow < 9:
                tk.Button(otp_pane, text=button, width=12, height= 3, bg='black', fg='white', command=command).grid(row=varRow,
                                                                                                         column=varColumn)
                varColumn += 1
                if varColumn > 4:
                    varColumn = 0
                    varRow += 1
            else:
                tk.Button(otp_pane, text=button, width=192, bg='black', fg='white', command=command).grid(columnspan=9,
                                                                                                          row=varRow,
                                                                                                          column=0)
                varRow += 1
        tk.mainloop()

    def showDecesionPane():
        global DICT
        def winnerIsBatting():
            def close_win():
                decesion_pane.destroy()
            btn = ttk.Button(decesion_pane, text="Next", command=close_win)
            btn.place(relx=0.46, rely=0.6)
            global batting_button
            global bowling_button
            batting_button['state'] = ['disabled']
            bowling_button['state'] = ['disabled']
            DICT['toss_decision'] = 1
            if DICT['toss_winner'] == 1:
                DICT['batting_team'] = 1
                audioapnibat = AudioSegment.from_file("comm/apni_bat.wav")
                temp = "apnibat.wav"
                audioapnibat.export(temp, format="wav")
                wave_obj = sa.WaveObject.from_wave_file(temp)
                abt = wave_obj.play()
                match_yaml['info']['toss_decision'] = 1
                match_yaml['innings']['first_innings']['batteam'] = 1
                match_yaml['innings']['second_innings']['batteam'] = 2
                match_yaml['innings']['third_innings']['batteam'] = 1
                match_yaml['innings']['fourth_innings']['batteam'] = 2
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']

            else:
                DICT['batting_team'] = 2
                audioabajubat = AudioSegment.from_file("comm/baju_bat.wav")
                temp = "bajubat.wav"
                audioabajubat.export(temp, format="wav")
                wave_obj = sa.WaveObject.from_wave_file(temp)
                bb = wave_obj.play()
                match_yaml['info']['toss_decision'] = 1
                match_yaml['innings']['first_innings']['batteam'] = 2
                match_yaml['innings']['second_innings']['batteam'] = 1
                match_yaml['innings']['third_innings']['batteam'] = 2
                match_yaml['innings']['fourth_innings']['batteam'] = 1
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']

        def winnerIsBowling():


            def close_win():
                decesion_pane.destroy()

            btn = ttk.Button(decesion_pane, text="Next", command=close_win)
            btn.place(relx=0.46, rely=0.6)
            global batting_button
            global bowling_button
            batting_button['state'] = ['disabled']
            bowling_button['state'] = ['disabled']
            DICT['toss_decision'] = 2
            if DICT['toss_winner'] == 1:
                DICT['batting_team'] = 2
                audioapnibowl = AudioSegment.from_file("comm/apni_bowl.wav")
                temp = "apnibowl.wav"
                audioapnibowl.export(temp, format="wav")
                wave_obj = sa.WaveObject.from_wave_file(temp)
                abl = wave_obj.play()
                match_yaml['info']['toss_decision'] = 2
                match_yaml['innings']['first_innings']['batteam'] = 2
                match_yaml['innings']['second_innings']['batteam'] = 1
                match_yaml['innings']['third_innings']['batteam'] = 2
                match_yaml['innings']['fourth_innings']['batteam'] = 1
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
            else:
                DICT['batting_team'] = 1
                audiobajubowl = AudioSegment.from_file("comm/baju_bowl.wav")
                temp = "bajubowl.wav"
                audiobajubowl.export(temp, format="wav")
                wave_obj = sa.WaveObject.from_wave_file(temp)
                bbw = wave_obj.play()
                match_yaml['info']['toss_decision'] = 2
                match_yaml['innings']['first_innings']['batteam'] = 1
                match_yaml['innings']['second_innings']['batteam'] = 2
                match_yaml['innings']['third_innings']['batteam'] = 1
                match_yaml['innings']['fourth_innings']['batteam'] = 2
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player1']['player_id']
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['player_id'] = \
                    match_yaml['info']['teams']['team2']['player2']['player_id']
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player1']['player_id']
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['player_id'] = \
                    match_yaml['info']['teams']['team1']['player2']['player_id']

        decesion_pane = tk.Tk()
        decesion_pane.geometry("800x480+1+1")

        decesion_pane.resizable(0, 0)
        decesion_pane.title("CHOOSE BAT OR BOWL")
        img1 = Image.open("bckgrnd.jpg")
        tk1_image = ImageTk.PhotoImage(img1)
        labelback = tk.Label(decesion_pane, image=tk1_image)
        labelback.pack()
        # top.configure(background="#d9d9d9")
        global batting_button
        global bowling_button

        batting_button = tk.Button(decesion_pane, command=winnerIsBatting)
        batting_button.place(relx=0.25, rely=0.18, height=80, width=400)
        batting_button.configure(background="black")
        batting_button.configure(foreground="gold")
        batting_button.configure(font=font9)
        batting_button.configure(text='''BATTING''')

        bowling_button = tk.Button(decesion_pane, command=winnerIsBowling)
        bowling_button.place(relx=0.25, rely=0.38, height=80, width=400)
        bowling_button.configure(background="black")
        bowling_button.configure(foreground="gold")
        bowling_button.configure(font=font9)
        bowling_button.configure(text='''BOWLING''')

        tk.mainloop()


    def openTossPane():
        def killwin_toss():
            toss_pane.destroy()
            showDecesionPane()
        toss_pane = tk.Tk()
        toss_pane.geometry("800x480+1+1")

        toss_pane.resizable(0, 0)
        toss_pane.title("TOSS")
        # top.configure(background="#d9d9d9")
        img1 = Image.open("bckgrnd.jpg")
        tk1_image = ImageTk.PhotoImage(img1)
        labelback = tk.Label(toss_pane, image=tk1_image)
        labelback.pack()
        global DICT

        winnerteam = tk.Label(toss_pane)
        winnerteam.place(relx=0.32, rely=0.163, height=50, width=299)
        winnerteam.configure(background="black")
        winnerteam.configure(disabledforeground="#a3a3a3")
        winnerteam.configure(font="-family {Segoe UI Black} -size 24 -weight bold -slant roman -underline 0 -overstrike 0")
        winnerteam.configure(foreground="gold")
        winner = random.choice(['अपनी गली', 'बाजू गली'])
        winnerteam.configure(text=winner)
        if winner == 'अपनी गली':
            DICT['toss_winner'] = 1
            match_yaml['info']['toss_winner'] = 1
        else:
            DICT['toss_winner'] = 2
            match_yaml['info']['toss_winner'] = 2
        wonthetoss = tk.Label(toss_pane)
        wonthetoss.place(relx=0.280, rely=0.29, height=66, width=359)
        wonthetoss.configure(background="#d9d9d9")
        wonthetoss.configure(disabledforeground="#a3a3a3")
        wonthetoss.configure(background="black")
        wonthetoss.configure(foreground="gold")
        wonthetoss.configure(font=font9)
        wonthetoss.configure(text='''WON THE TOSS''')

        take_decesion = tk.Button(toss_pane, command=killwin_toss)
        take_decesion.place(relx=0.39, rely=0.7, width=175, height=50)
        take_decesion.configure(text = '''NEXT''')
        take_decesion.configure(
            font="-family {Segoe UI Black} -size 24 -weight bold -slant roman -underline 0 -overstrike 0")
        take_decesion.configure(background="black")
        take_decesion.configure(foreground="gold")
        tk.mainloop()


    def showTeamInfo():
        def killwin_team():
            #imgteam = ImageGrab.grab()
            #imgteam = imgteam.crop((5, 30, 800, 480))
            #ts = time.time()
            #imgteam.save("yaml/screenshot/" + str(int(ts)) + ".jpg")
            team_view_pane.destroy()
            openTossPane()

        team_view_pane = tk.Tk()
        team_view_pane.geometry("800x480+1+1")

        team_view_pane.resizable(0, 0)
        team_view_pane.title("TEAM INFO")
        # top.configure(background="#d9d9d9")

        #team_view_pane.configure(background="DarkOliveGreen1")
        img1 = Image.open("bckgrnd.jpg")
        tk1_image = ImageTk.PhotoImage(img1)
        labelback = tk.Label(team_view_pane, image=tk1_image)
        labelback.pack()

        Label2 = tk.Label(team_view_pane)
        Label2.place(relx=0.145, rely=0.054, height=80, width=200)
        Label2.configure(background="midnight blue")
        Label2.configure(disabledforeground="#a3a3a3")
        Label2.configure(font=font9)
        Label2.configure(foreground="white")
        Label2.configure(text='''अपनी गली''')

        Label3 = tk.Label(team_view_pane)
        Label3.place(relx=0.595, rely=0.054, height=80, width=200)
        Label3.configure(background="magenta4")
        Label3.configure(disabledforeground="#a3a3a3")
        Label3.configure(font=font9)
        Label3.configure(foreground="white")
        Label3.configure(text='''बाजू गली''')

        label_p1 = tk.Label(team_view_pane)
        label_p1.place(relx=0.1, rely=0.312, height=50, width=300)
        label_p1.configure(background="midnight blue")
        label_p1.configure(disabledforeground="#a3a3a3")
        label_p1.configure(font=font9)
        label_p1.configure(foreground="white")

        label_p2 = tk.Label(team_view_pane)
        label_p2.place(relx=0.1, rely=0.448, height=50, width=300)
        label_p2.configure(activebackground="#f9f9f9")
        label_p2.configure(activeforeground="black")
        label_p2.configure(background="midnight blue")
        label_p2.configure(disabledforeground="#a3a3a3")
        label_p2.configure(
            font="-family {Segoe UI Black} -size 24 -weight bold -slant roman -underline 0 -overstrike 0")
        label_p2.configure(foreground="white")
        label_p2.configure(highlightbackground="#d9d9d9")
        label_p2.configure(highlightcolor="black")

        # label_p3 = tk.Label(team_view_pane)
        # label_p3.place(relx=0.095, rely=0.583, height=50, width=401)
        # label_p3.configure(activebackground="#f9f9f9")
        # label_p3.configure(activeforeground="black")
        # label_p3.configure(background="#d9d9d9")
        # label_p3.configure(disabledforeground="#a3a3a3")
        # label_p3.configure(
        #     font="-family {Segoe UI Black} -size 24 -weight bold -slant roman -underline 0 -overstrike 0")
        # label_p3.configure(foreground="#000000")
        # label_p3.configure(highlightbackground="#d9d9d9")
        # label_p3.configure(highlightcolor="black")

        label_p4 = tk.Label(team_view_pane)
        label_p4.place(relx=0.55, rely=0.312, height=50, width=300)
        label_p4.configure(activebackground="#f9f9f9")
        label_p4.configure(activeforeground="black")
        label_p4.configure(background="magenta4")
        label_p4.configure(disabledforeground="#a3a3a3")
        label_p4.configure(
            font="-family {Segoe UI Black} -size 24 -weight bold -slant roman -underline 0 -overstrike 0")
        label_p4.configure(foreground="white")
        label_p4.configure(highlightbackground="#d9d9d9")
        label_p4.configure(highlightcolor="black")

        label_p5 = tk.Label(team_view_pane)
        label_p5.place(relx=0.55, rely=0.448, height=50, width=300)
        label_p5.configure(activebackground="#f9f9f9")
        label_p5.configure(activeforeground="black")
        label_p5.configure(background="magenta4")
        label_p5.configure(disabledforeground="#a3a3a3")
        label_p5.configure(
            font="-family {Segoe UI Black} -size 24 -weight bold -slant roman -underline 0 -overstrike 0")
        label_p5.configure(foreground="white")
        label_p5.configure(highlightbackground="#d9d9d9")
        label_p5.configure(highlightcolor="black")

        # label_p6 = tk.Label(team_view_pane)
        # label_p6.place(relx=0.573, rely=0.583, height=50, width=401)
        # label_p6.configure(activebackground="#f9f9f9")
        # label_p6.configure(activeforeground="black")
        # label_p6.configure(background="#d9d9d9")
        # label_p6.configure(disabledforeground="#a3a3a3")
        # label_p6.configure(
        #     font="-family {Segoe UI Black} -size 24 -weight bold -slant roman -underline 0 -overstrike 0")
        # label_p6.configure(foreground="#000000")
        # label_p6.configure(highlightbackground="#d9d9d9")
        # label_p6.configure(highlightcolor="black")

        team_confirm_button = tk.Button(team_view_pane, command=killwin_team)
        team_confirm_button.place(relx=0.372, rely=0.637, height=83, width=286)
        team_confirm_button.configure(background="black")
        team_confirm_button.configure(foreground="gold")
        team_confirm_button.configure(text='''Teams Confirmed''')
        team_confirm_button.configure(relief='raised')
        team_confirm_button.configure(font="-family {Segoe UI Black} -size 20 -weight bold -slant roman -underline 0 -overstrike 0")


        if slot_details['no_of_players'] >= 2:
            label_p1.configure(text=slot_details['team1']['player1']['player_name'])
            label_p4.configure(text=slot_details['team2']['player1']['player_name'])
        if slot_details['no_of_players'] >= 4:
            label_p2.configure(text=slot_details['team1']['player2']['player_name'])
            label_p5.configure(text=slot_details['team2']['player2']['player_name'])
        # if slot_details['no_of_players'] == 6:
        #     label_p3.configure(text=slot_details['team1']['player3']['player_name'])
        #     label_p6.configure(text=slot_details['team2']['player3']['player_name'])
        tk.mainloop()

    makeKeyboard()

    #def disable_event():
    #    pass
    #top.protocol("WM_DELETE_WINDOW", disable_event)


# note: new methods will only work when _1_and_2() has been executed
# new
def _3():
    global DICT
    top = tk.Tk()
    top.geometry("800x480+1+1")

    top.resizable(0, 0)
    top.title("New Toplevel")
    top.configure(background="#d9d9d9")

    notebook = ttk.Notebook(top)
    notebook.place(relx=0, rely=0, relheight=1.0, relwidth=1.0)

    batsman_selection_pane = tk.Frame(notebook)

    notebook.add(batsman_selection_pane, text='BATTING TEAM')
    img1 = Image.open("bckgrnd.jpg")
    tk1_image = ImageTk.PhotoImage(img1)
    labelback = tk.Label(batsman_selection_pane, image=tk1_image)
    labelback.pack()

    Label1 = tk.Label(batsman_selection_pane)
    Label1.place(relx=0.1, rely=0.054, height=96, width=602)
    Label1.configure(font=font9)
    Label1.configure(background="black")
    Label1.configure(foreground="gold")
    Label1.configure(text='''SELECT A PLAYER TO BAT''')

    def batsman1Selected():
        print('Clicked')
        # batsman_1['state'] = 'disabled'
        DICT['current_batsman'] = batsman_1['text']
        len_btpc = len(match_yaml['info']['batting_player_choice'])
        btpc = collections.OrderedDict([('deliveries_done', 0), ('old_batsman_id', -999), ('new_batsman_id', 10000001), ('change_type', 1)])
        if DICT['batting_team'] == 1:
            btpc['new_batsman_id'] = \
                slot_details['team1']['player3']['player_id']
        else:
            btpc['new_batsman_id'] = \
                slot_details['team2']['player3']['player_id']
        btpc = collections.OrderedDict([(len_btpc, btpc)])
        if len_btpc == 1 and match_yaml['info']['batting_player_choice'][0] == None:
            match_yaml['info']['batting_player_choice'][0] = btpc
        else:
            match_yaml['info']['batting_player_choice'].append(btpc)



    def batsman2Selected():
        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx = 0.45, rely = 0.75)
        batsman_2['state'] = 'disabled'
        batsman_3['state'] = 'disabled'
        DICT['current_batsman'] = batsman_2['text']
        len_btpc = len(match_yaml['info']['batting_player_choice'])
        btpc = collections.OrderedDict(
            [('deliveries_done', 0), ('old_batsman_id', -999), ('new_batsman_id', 10000001), ('change_type', 1)])
        if DICT['batting_team'] == 1:
            if match_yaml['meta']['innings_completed'] % 2 == 0:
                btpc['new_batsman_id'] = \
                    slot_details['team1']['player1']['player_id']
            else:
                btpc['new_batsman_id'] = \
                    slot_details['team2']['player1']['player_id']
        else:
            if match_yaml['meta']['innings_completed'] % 2 == 0:
                btpc['new_batsman_id'] = \
                    slot_details['team2']['player1']['player_id']
            else:
                btpc['new_batsman_id'] = \
                    slot_details['team1']['player1']['player_id']

        if len_btpc == 1 and match_yaml['info']['batting_player_choice'][0] == None:
            btpc = collections.OrderedDict([(len_btpc, btpc)])
            match_yaml['info']['batting_player_choice'][0] = btpc
            print("assign hua")
        else:
            btpc = collections.OrderedDict([((len_btpc+1), btpc)])
            match_yaml['info']['batting_player_choice'].append(btpc)
            print("append hua")
        len_btpc = len(match_yaml['info']['batting_player_choice'])
        bat_arm = 2
        if match_yaml['info']['batting_player_choice'][len_btpc-1][len_btpc]['new_batsman_id'] == \
                match_yaml['info']['teams']['team1']['player1']['player_id']:
            bat_arm = match_yaml['info']['teams']['team1']['player1']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc-1][len_btpc]['new_batsman_id'] == \
                match_yaml['info']['teams']['team1']['player2']['player_id']:
            bat_arm = match_yaml['info']['teams']['team1']['player2']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc-1][len_btpc]['new_batsman_id'] == \
                match_yaml['info']['teams']['team2']['player1']['player_id']:
            bat_arm = match_yaml['info']['teams']['team2']['player1']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc-1][len_btpc]['new_batsman_id'] == \
                match_yaml['info']['teams']['team2']['player2']['player_id']:
            bat_arm = match_yaml['info']['teams']['team2']['player2']['batting_arm']
        f = open("yaml/flap.txt")
        con = f.read()
        f.close
        con1 = str(int(bat_arm) - 1) + con[1] + con[2]
        with open("yaml/flap.txt", 'w', encoding='utf-8') as f:
            f.write(con1)

    def batsman3Selected():
        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx = 0.45, rely = 0.75)
        batsman_2['state'] = 'disabled'
        batsman_3['state'] = 'disabled'
        DICT['current_batsman'] = batsman_3['text']
        len_btpc = len(match_yaml['info']['batting_player_choice'])
        btpc = collections.OrderedDict(
            [('deliveries_done', 0), ('old_batsman_id', -999), ('new_batsman_id', 10000001), ('change_type', 1)])
        if DICT['batting_team'] == 1:
            if match_yaml['meta']['innings_completed'] % 2 == 0:
                btpc['new_batsman_id'] = \
                    slot_details['team1']['player2']['player_id']
            else:
                btpc['new_batsman_id'] = \
                    slot_details['team2']['player2']['player_id']
        else:
            if match_yaml['meta']['innings_completed'] % 2 == 0:
                btpc['new_batsman_id'] = \
                    slot_details['team2']['player2']['player_id']
            else:
                btpc['new_batsman_id'] = \
                    slot_details['team1']['player2']['player_id']

        if len_btpc == 1 and match_yaml['info']['batting_player_choice'][0] == None:
            btpc = collections.OrderedDict([(len_btpc, btpc)])
            match_yaml['info']['batting_player_choice'][0] = btpc
            print("assign hua")
        else:
            btpc = collections.OrderedDict([((len_btpc+1), btpc)])
            match_yaml['info']['batting_player_choice'].append(btpc)
            print("append hua")
        len_btpc = len(match_yaml['info']['batting_player_choice'])
        bat_arm = 2
        if match_yaml['info']['batting_player_choice'][len_btpc-1][len_btpc]['new_batsman_id'] == \
                match_yaml['info']['teams']['team1']['player1']['player_id']:
            bat_arm = match_yaml['info']['teams']['team1']['player1']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc-1][len_btpc]['new_batsman_id'] == \
                match_yaml['info']['teams']['team1']['player2']['player_id']:
            bat_arm = match_yaml['info']['teams']['team1']['player2']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc-1][len_btpc]['new_batsman_id'] == \
                match_yaml['info']['teams']['team2']['player1']['player_id']:
            bat_arm = match_yaml['info']['teams']['team2']['player1']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc-1][len_btpc]['new_batsman_id'] == \
                match_yaml['info']['teams']['team2']['player2']['player_id']:
            bat_arm = match_yaml['info']['teams']['team2']['player2']['batting_arm']
        f = open("yaml/flap.txt")
        con = f.read()
        f.close
        con1 = str(int(bat_arm) - 1) + con[1] + con[2]
        with open("yaml/flap.txt", 'w', encoding='utf-8') as f:
            f.write(con1)

    # batsman_1 = tk.Button(batsman_selection_pane, command=batsman1Selected)
    # batsman_1.place(relx=0.301, rely=0.271, height=93, width=606)
    # batsman_1.configure(font=font9)

    batsman_2 = tk.Button(batsman_selection_pane, command=batsman2Selected)
    batsman_2.place(relx=0.2, rely=0.3, height=70, width=400)
    batsman_2.configure(font=font9)
    batsman_2.configure(background="black")
    batsman_2.configure(foreground="gold")

    batsman_3 = tk.Button(batsman_selection_pane, command=batsman3Selected)
    batsman_3.place(relx=0.2, rely=0.5, height=70, width=400)
    batsman_3.configure(
        font="-family {Segoe UI Black} -size 24 -weight bold -slant roman -underline 0 -overstrike 0")
    batsman_3.configure(background="black")
    batsman_3.configure(foreground="gold")
    def setNameOnButtons():
        if slot_details['no_of_players'] >= 2:
            if DICT['batting_team'] == 1:
                if match_yaml['meta']['innings_completed'] % 2 == 0:
                    batsman_2.configure(text=slot_details['team1']['player1']['player_name'])
                else:
                    batsman_2.configure(text=slot_details['team2']['player1']['player_name'])
            else:
                if match_yaml['meta']['innings_completed'] % 2 == 0:
                    batsman_2.configure(text=slot_details['team2']['player1']['player_name'])
                else:
                    batsman_2.configure(text=slot_details['team1']['player1']['player_name'])

        if slot_details['no_of_players'] >= 4:
            if DICT['batting_team'] == 1:
                if match_yaml['meta']['innings_completed'] % 2 == 0:
                    batsman_3.configure(text=slot_details['team1']['player2']['player_name'])
                else:
                    batsman_3.configure(text=slot_details['team2']['player2']['player_name'])

            else:
                if match_yaml['meta']['innings_completed'] % 2 == 0:
                    batsman_3.configure(text=slot_details['team2']['player2']['player_name'])
                else:
                    batsman_3.configure(text=slot_details['team1']['player2']['player_name'])

        #if slot_details['no_of_players'] == 6:
        #    if DICT['batting_team'] == 1:
        #        batsman_1.configure(text=slot_details['team1']['player3']['player_name'])

        #    else:
        #        batsman_1.configure(text=slot_details['team2']['player3']['player_name'])

    setNameOnButtons()

    #if slot_details['no_of_players'] < 6:
    #    batsman_1.place_forget()
    #if slot_details['no_of_players'] < 4:
    #    batsman_3.place_forget()
    def disable_event():
        pass

    top.protocol("WM_DELETE_WINDOW", disable_event)

    tk.mainloop()


# new
def _4():
    global DICT
    top = tk.Tk()
    top.geometry("800x480+1+1")

    top.resizable(0, 0)
    top.title("New Toplevel")
    top.configure(background="#d9d9d9")

    notebook = ttk.Notebook(top)
    notebook.place(relx=0, rely=0, relheight=1.0, relwidth=1.0)

    bowler_selection_pane = tk.Frame(notebook)

    notebook.add(bowler_selection_pane, text='BOWLING TEAM')
    img1 = Image.open("bckgrnd.jpg")
    tk1_image = ImageTk.PhotoImage(img1)
    labelback = tk.Label(bowler_selection_pane, image=tk1_image)
    labelback.pack()

    Label1 = tk.Label(bowler_selection_pane)
    Label1.place(relx=0.0, rely=0.054, height=96, width=800)
    Label1.configure(font=font9)
    Label1.configure(text='''SELECT A PLAYER TO BOWL''')
    Label1.configure(background="black")
    Label1.configure(foreground="gold")

    def bowler1Selected():
        print('Clicked')
        # bowler_1['state'] = 'disabled'
        bowler_2['state'] = 'normal'
        bowler_3['state'] = 'normal'
        DICT['current_bowler'] = bowler_1['text']
        len_bwpc = len(match_yaml['info']['bowling_player_choice'])
        bwpc = collections.OrderedDict(
            [('deliveries_done', 0), ('old_bowler_id', -999), ('new_bowler_id', 10000001)])
        if DICT['batting_team'] == 1:
            bwpc['new_bowler_id'] = \
                slot_details['team2']['player3']['player_id']
        else:
            bwpc['new_bowler_id'] = \
                slot_details['team1']['player3']['player_id']
        bwpc = collections.OrderedDict([(len_bwpc, bwpc)])
        if len_bwpc == 1 and match_yaml['info']['bowling_player_choice'][0] == None:
            match_yaml['info']['bowling_player_choice'][0] = bwpc
        else:
            match_yaml['info']['bowling_player_choice'].append(bwpc)

    def bowler2Selected():
        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx = 0.45, rely = 0.75)
        # bowler_1['state'] = 'normal'
        bowler_2['state'] = 'disabled'
        bowler_3['state'] = 'disabled'
        DICT['current_bowler'] = bowler_2['text']
        len_bwpc = len(match_yaml['info']['bowling_player_choice'])
        bwpc = collections.OrderedDict(
            [('deliveries_done', 0), ('old_bowler_id', -999), ('new_bowler_id', 10000001)])
        if DICT['batting_team'] == 1:
            if match_yaml['meta']['innings_completed'] % 2 == 0:
                bwpc['new_bowler_id'] = \
                    slot_details['team2']['player1']['player_id']
            else:
                bwpc['new_bowler_id'] = \
                    slot_details['team1']['player1']['player_id']

        else:
            if match_yaml['meta']['innings_completed'] % 2 == 0:
                bwpc['new_bowler_id'] = \
                    slot_details['team1']['player1']['player_id']
            else:
                bwpc['new_bowler_id'] = \
                    slot_details['team2']['player1']['player_id']

        if len_bwpc == 1 and match_yaml['info']['bowling_player_choice'][0] == None:
            bwpc = collections.OrderedDict([(len_bwpc, bwpc)])
            match_yaml['info']['bowling_player_choice'][0] = bwpc
        else:
            bwpc = collections.OrderedDict([((len_bwpc+1), bwpc)])
            match_yaml['info']['bowling_player_choice'].append(bwpc)

    def bowler3Selected():
        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx = 0.45, rely = 0.75)
        # bowler_1['state'] = 'normal'
        bowler_2['state'] = 'disabled'
        bowler_3['state'] = 'disabled'
        DICT['current_bowler'] = bowler_3['text']
        len_bwpc = len(match_yaml['info']['bowling_player_choice'])
        bwpc = collections.OrderedDict(
            [('deliveries_done', 0), ('old_bowler_id', -999), ('new_bowler_id', 10000001)])
        if DICT['batting_team'] == 1:
            if match_yaml['meta']['innings_completed'] % 2 == 0:
                bwpc['new_bowler_id'] = \
                    slot_details['team2']['player2']['player_id']
            else:
                bwpc['new_bowler_id'] = \
                    slot_details['team1']['player2']['player_id']
        else:
            if match_yaml['meta']['innings_completed'] % 2 == 0:
                bwpc['new_bowler_id'] = \
                    slot_details['team1']['player2']['player_id']
            else:
                bwpc['new_bowler_id'] = \
                    slot_details['team2']['player2']['player_id']

        if len_bwpc == 1 and match_yaml['info']['bowling_player_choice'][0] == None:
            bwpc = collections.OrderedDict([(len_bwpc, bwpc)])
            match_yaml['info']['bowling_player_choice'][0] = bwpc
        else:
            bwpc = collections.OrderedDict([((len_bwpc+1), bwpc)])
            match_yaml['info']['bowling_player_choice'].append(bwpc)

    # bowler_1 = tk.Button(bowler_selection_pane, command=bowler1Selected)
    # bowler_1.place(relx=0.301, rely=0.271, height=93, width=606)
    # bowler_1.configure(font=font9)

    bowler_2 = tk.Button(bowler_selection_pane, command=bowler2Selected)
    bowler_2.place(relx=0.2, rely=0.3, height=70, width=400)
    bowler_2.configure(font=font9)
    bowler_2.configure(background="black")
    bowler_2.configure(foreground="gold")

    bowler_3 = tk.Button(bowler_selection_pane, command=bowler3Selected)
    bowler_3.place(relx=0.2, rely=0.5, height=70, width=400)
    bowler_3.configure(
        font="-family {Segoe UI Black} -size 24 -weight bold -slant roman -underline 0 -overstrike 0")
    bowler_3.configure(background="black")
    bowler_3.configure(foreground="gold")

    def setNameOnButtons():
        if slot_details['no_of_players'] >= 2:
            if DICT['batting_team'] == 1:
                if match_yaml['meta']['innings_completed'] % 2 == 0:
                    bowler_2.configure(text=slot_details['team2']['player1']['player_name'])
                else:
                    bowler_2.configure(text=slot_details['team1']['player1']['player_name'])
            else:
                if match_yaml['meta']['innings_completed'] % 2 == 0:
                    bowler_2.configure(text=slot_details['team1']['player1']['player_name'])
                else:
                    bowler_2.configure(text=slot_details['team2']['player1']['player_name'])
        if slot_details['no_of_players'] >= 4:
            if DICT['batting_team'] == 1:
                if match_yaml['meta']['innings_completed'] % 2 == 0:
                    bowler_3.configure(text=slot_details['team2']['player2']['player_name'])
                else:
                    bowler_3.configure(text=slot_details['team1']['player2']['player_name'])
            else:
                if match_yaml['meta']['innings_completed'] % 2 == 0:
                    bowler_3.configure(text=slot_details['team1']['player2']['player_name'])
                else:
                    bowler_3.configure(text=slot_details['team2']['player2']['player_name'])
        #if slot_details['no_of_players'] == 6:
        #    if DICT['batting_team'] == 1:
        #        bowler_1.configure(text=slot_details['team2']['player3']['player_name'])
        #    else:
        #        bowler_1.configure(text=slot_details['team1']['player3']['player_name'])

    setNameOnButtons()

    #if slot_details['no_of_players'] < 6:
    #    bowler_1.place_forget()
    #if slot_details['no_of_players'] < 4:
    #    bowler_3.place_forget()
    def disable_event():
        pass

    top.protocol("WM_DELETE_WINDOW", disable_event)

    tk.mainloop()


# new
def _5r():
    global ButtonR2_0
    global ButtonR2_1
    global ButtonR2_2
    global ButtonR2_3
    global ButtonR2_4
    global ButtonR2_5
    global ButtonR2_6
    global ButtonR2_7
    global ButtonR2_8
    global ButtonR2_9
    top = tk.Tk()
    top.geometry("800x480+1+1")

    top.resizable(0, 0)
    top.title("New Toplevel")
    top.configure(background="#d9d9d9")

    notebook = ttk.Notebook(top)
    notebook.place(relx=0, rely=0, relheight=1.0, relwidth=1.0)

    Routzone_pane = tk.Frame(notebook)
    img1 = Image.open("bckgrnd.jpg")
    tk1_image = ImageTk.PhotoImage(img1)
    labelback = tk.Label(Routzone_pane, image=tk1_image)
    labelback.pack()

    def RoutZoneSelected(id):
        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx = 0.46, rely = 0.49)
        global ButtonR2_0
        global ButtonR2_1
        global ButtonR2_2
        global ButtonR2_3
        global ButtonR2_4
        global ButtonR2_5
        global ButtonR2_6
        global ButtonR2_7
        global ButtonR2_8
        global ButtonR2_9
        ButtonR2_0['state'] = 'disabled'
        ButtonR2_1['state'] = 'disabled'
        ButtonR2_2['state'] = 'disabled'
        ButtonR2_3['state'] = 'disabled'
        ButtonR2_4['state'] = 'disabled'
        ButtonR2_5['state'] = 'disabled'
        ButtonR2_6['state'] = 'disabled'
        ButtonR2_7['state'] = 'disabled'
        ButtonR2_8['state'] = 'disabled'
        ButtonR2_9['state'] = 'disabled'
        DICT['current_out_zone'] = outZoneCode[id]
        match_yaml['info']['current_outzone_selected'] = id
        match_yaml['info']['out_zone_selected_at_valid_ball'] = match_yaml['meta']['deliveries_completed']
        match_yaml['info']['out_zone_active_till_valid_ball'] = match_yaml['info']['out_zone_selected_at_valid_ball'] \
                                                                + 6
        # DICT['previously_selected_out_zones'] = DICT.get('previously_selected_out_zones', []) + [outZoneCode[id]]
        match_yaml['info']['earlier_selected_out_zones'].append(id)
        print(match_yaml['info']['earlier_selected_out_zones'])
        f = open("yaml/flap.txt")
        con = f.read()
        f.close
        con1 = con[0] + str(id)
        with open("yaml/flap.txt", 'w', encoding='utf-8') as f:
            f.write(con1)

    notebook.add(Routzone_pane, text='SELECT OUT ZONE')
    Label = tk.Label(Routzone_pane)
    Label.place(relx=0.312, rely=0.177, height=143, width=300)
    Label.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Label.configure(text='''Right-hand Batsman''', bg='lime green')
    Label1 = tk.Label(Routzone_pane)
    Label1.place(relx=0.312, rely=0.475, height=142, width=300)
    Label1.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Label1.configure(text='''Out Zone Selection''', bg='lime green')

    ButtonR2_0 = tk.Button(Routzone_pane, command=lambda: RoutZoneSelected(12))
    ButtonR2_0.place(relx=0.125, rely=0.375, height=95, width=150)
    ButtonR2_0.configure(activebackground="#ececec")
    ButtonR2_0.configure(activeforeground="#000000")
    ButtonR2_0.configure(background="black")
    ButtonR2_0.configure(disabledforeground="#a3a3a3")
    ButtonR2_0.configure(foreground="gold")
    ButtonR2_0.configure(highlightbackground="#d9d9d9")
    ButtonR2_0.configure(highlightcolor="black")
    ButtonR2_0.configure(pady="0")
    ButtonR2_0.configure(text='''Cover \n (1 Run)''')
    ButtonR2_0.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 12 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonR2_0.configure(state='disabled', background='gray25')

    ButtonR2_1 = tk.Button(Routzone_pane, command=lambda: RoutZoneSelected(19))
    ButtonR2_1.place(relx=0.125, rely=0, height=84, width=299)
    ButtonR2_1.configure(activebackground="#ececec")
    ButtonR2_1.configure(activeforeground="#000000")
    ButtonR2_1.configure(background="black")
    ButtonR2_1.configure(disabledforeground="#a3a3a3")
    ButtonR2_1.configure(foreground="gold")
    ButtonR2_1.configure(highlightbackground="#d9d9d9")
    ButtonR2_1.configure(highlightcolor="black")
    ButtonR2_1.configure(pady="0")
    ButtonR2_1.configure(text='''Off Slip \n (2 Runs)''')
    ButtonR2_1.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    ButtonR2_1.configure(state='disabled', background='gray25')

    ButtonR2_2 = tk.Button(Routzone_pane, command=lambda: RoutZoneSelected(18))
    ButtonR2_2.place(relx=0.5, rely=0.0, height=84, width=299)
    ButtonR2_2.configure(activebackground="#ececec")
    ButtonR2_2.configure(activeforeground="#000000")
    ButtonR2_2.configure(background="black")
    ButtonR2_2.configure(disabledforeground="#a3a3a3")
    ButtonR2_2.configure(foreground="gold")
    ButtonR2_2.configure(highlightbackground="#d9d9d9")
    ButtonR2_2.configure(highlightcolor="black")
    ButtonR2_2.configure(pady="0")
    ButtonR2_2.configure(text='''Fine Leg \n (2 Runs)''')
    ButtonR2_2.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    ButtonR2_2.configure(state='disabled', background='gray25')

    ButtonR2_3 = tk.Button(Routzone_pane, command=lambda: RoutZoneSelected(11))
    ButtonR2_3.place(relx=0.125, rely=0.177, height=95, width=150)
    ButtonR2_3.configure(activebackground="#ececec")
    ButtonR2_3.configure(activeforeground="#000000")
    ButtonR2_3.configure(background="black")
    ButtonR2_3.configure(disabledforeground="#a3a3a3")
    ButtonR2_3.configure(foreground="gold")
    ButtonR2_3.configure(highlightbackground="#d9d9d9")
    ButtonR2_3.configure(highlightcolor="black")
    ButtonR2_3.configure(pady="0")
    ButtonR2_3.configure(text='''Square \n Off \n (2 Runs)''')
    ButtonR2_3.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 11 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonR2_3.configure(state='disabled', background='gray25')

    ButtonR2_4 = tk.Button(Routzone_pane, command=lambda: RoutZoneSelected(14))
    ButtonR2_4.place(relx=0.125, rely=0.771, height=90, width=199)
    ButtonR2_4.configure(activebackground="#ececec")
    ButtonR2_4.configure(activeforeground="#000000")
    ButtonR2_4.configure(background="black")
    ButtonR2_4.configure(disabledforeground="#a3a3a3")
    ButtonR2_4.configure(foreground="gold")
    ButtonR2_4.configure(highlightbackground="#d9d9d9")
    ButtonR2_4.configure(highlightcolor="black")
    ButtonR2_4.configure(pady="0")
    ButtonR2_4.configure(text='''Mid Off \n (4 Runs)''')
    ButtonR2_4.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 14 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonR2_4.configure(state='disabled', background='gray25')

    ButtonR2_5 = tk.Button(Routzone_pane, command=lambda: RoutZoneSelected(17))
    ButtonR2_5.place(relx=0.687, rely=0.177, height=143, width=150)
    ButtonR2_5.configure(activebackground="#ececec")
    ButtonR2_5.configure(activeforeground="#000000")
    ButtonR2_5.configure(background="black")
    ButtonR2_5.configure(disabledforeground="#a3a3a3")
    ButtonR2_5.configure(foreground="gold")
    ButtonR2_5.configure(highlightbackground="#d9d9d9")
    ButtonR2_5.configure(highlightcolor="black")
    ButtonR2_5.configure(pady="0")
    ButtonR2_5.configure(text='''Square \n Leg \n (1 Run)''')
    ButtonR2_5.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 17 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonR2_5.configure(state='disabled', background='gray25')

    ButtonR2_6 = tk.Button(Routzone_pane, command=lambda: RoutZoneSelected(13))
    ButtonR2_6.place(relx=0.125, rely=0.572, height=95, width=150)
    ButtonR2_6.configure(activebackground="#ececec")
    ButtonR2_6.configure(activeforeground="#000000")
    ButtonR2_6.configure(background="black")
    ButtonR2_6.configure(disabledforeground="#a3a3a3")
    ButtonR2_6.configure(foreground="gold")
    ButtonR2_6.configure(highlightbackground="#d9d9d9")
    ButtonR2_6.configure(highlightcolor="black")
    ButtonR2_6.configure(pady="0")
    ButtonR2_6.configure(text='''Extra \n Cover \n (3 Runs)''')
    ButtonR2_6.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 13 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonR2_6.configure(state='disabled', background='gray25')

    ButtonR2_7 = tk.Button(Routzone_pane, command=lambda: RoutZoneSelected(15))
    ButtonR2_7.place(relx=0.375, rely=0.771, height=90, width=200)
    ButtonR2_7.configure(activebackground="#ececec")
    ButtonR2_7.configure(activeforeground="#000000")
    ButtonR2_7.configure(background="black")
    ButtonR2_7.configure(disabledforeground="#a3a3a3")
    ButtonR2_7.configure(foreground="gold")
    ButtonR2_7.configure(highlightbackground="#d9d9d9")
    ButtonR2_7.configure(highlightcolor="black")
    ButtonR2_7.configure(pady="0")
    ButtonR2_7.configure(text='''Straight \n (6 Runs)''')
    ButtonR2_7.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 15 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonR2_7.configure(state='disabled', background='gray25')

    ButtonR2_8 = tk.Button(Routzone_pane, command=lambda: RoutZoneSelected(16))
    ButtonR2_8.place(relx=0.687, rely=0.475, height=142, width=150)
    ButtonR2_8.configure(activebackground="#ececec")
    ButtonR2_8.configure(activeforeground="#000000")
    ButtonR2_8.configure(background="black")
    ButtonR2_8.configure(disabledforeground="#a3a3a3")
    ButtonR2_8.configure(foreground="gold")
    ButtonR2_8.configure(highlightbackground="#d9d9d9")
    ButtonR2_8.configure(highlightcolor="black")
    ButtonR2_8.configure(pady="0")
    ButtonR2_8.configure(text='''Mid \n Wicket \n (2 Runs)''')
    ButtonR2_8.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 16 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonR2_8.configure(state='disabled', background='gray25')

    ButtonR2_9 = tk.Button(Routzone_pane, command=lambda: RoutZoneSelected(14))
    ButtonR2_9.place(relx=0.625, rely=0.771, height=90, width=200)
    ButtonR2_9.configure(activebackground="#ececec")
    ButtonR2_9.configure(activeforeground="#000000")
    ButtonR2_9.configure(background="black")
    ButtonR2_9.configure(disabledforeground="#a3a3a3")
    ButtonR2_9.configure(foreground="gold")
    ButtonR2_9.configure(highlightbackground="#d9d9d9")
    ButtonR2_9.configure(highlightcolor="black")
    ButtonR2_9.configure(pady="0")
    ButtonR2_9.configure(text='''Mid On \n (4 Runs)''')
    ButtonR2_9.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 14 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonR2_9.configure(state='disabled', background='gray25')

    def disable_event():
        pass

    top.protocol("WM_DELETE_WINDOW", disable_event)

    tk.mainloop()


def _5l():
    global ButtonL2_0
    global ButtonL2_1
    global ButtonL2_2
    global ButtonL2_3
    global ButtonL2_4
    global ButtonL2_5
    global ButtonL2_6
    global ButtonL2_7
    global ButtonL2_8
    global ButtonL2_9
    top = tk.Tk()
    top.geometry("800x480+1+1")

    top.resizable(0, 0)
    top.title("New Toplevel")
    top.configure(background="#d9d9d9")

    notebook = ttk.Notebook(top)
    notebook.place(relx=0, rely=0, relheight=1.0, relwidth=1.0)

    Loutzone_pane = tk.Frame(notebook)

    def LoutZoneSelected(id):
        def close_win():
            top.destroy()

        btn = ttk.Button(top, text="Next", command=close_win)
        btn.place(relx = 0.46, rely = 0.55)
        global ButtonL2_0
        global ButtonL2_1
        global ButtonL2_2
        global ButtonL2_3
        global ButtonL2_4
        global ButtonL2_5
        global ButtonL2_6
        global ButtonL2_7
        global ButtonL2_8
        global ButtonL2_9
        ButtonL2_0['state'] = 'disabled'
        ButtonL2_1['state'] = 'disabled'
        ButtonL2_2['state'] = 'disabled'
        ButtonL2_3['state'] = 'disabled'
        ButtonL2_4['state'] = 'disabled'
        ButtonL2_5['state'] = 'disabled'
        ButtonL2_6['state'] = 'disabled'
        ButtonL2_7['state'] = 'disabled'
        ButtonL2_8['state'] = 'disabled'
        ButtonL2_9['state'] = 'disabled'
        DICT['current_out_zone'] = outZoneCode[id]
        match_yaml['info']['current_outzone_selected'] = id
        match_yaml['info']['out_zone_selected_at_valid_ball'] = match_yaml['meta']['deliveries_completed']
        match_yaml['info']['out_zone_active_till_valid_ball'] = match_yaml['info']['out_zone_selected_at_valid_ball'] \
                                                                + 6
        # DICT['previously_selected_out_zones'] = DICT.get('previously_selected_out_zones', []) + [outZoneCode[id]]
        match_yaml['info']['earlier_selected_out_zones'].append(id)
        print(match_yaml['info']['earlier_selected_out_zones'])
        f = open("yaml/flap.txt")
        con = f.read()
        f.close
        con1 = con[0] + str(id)
        with open("yaml/flap.txt", 'w', encoding='utf-8') as f:
            f.write(con1)

    notebook.add(Loutzone_pane, text='SELECT OUT ZONE')
    Label = tk.Label(Loutzone_pane)
    Label.place(relx=0.312, rely=0.177, height=142, width=299)
    Label.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Label.configure(text='''Left-hand Batsman''', bg='lime green')
    Label1 = tk.Label(Loutzone_pane)
    Label1.place(relx=0.312, rely=0.475, height=141, width=299)
    Label1.configure(font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    Label1.configure(text='''Out Zone Selection''', bg='lime green')

    ButtonL2_0 = tk.Button(Loutzone_pane, command=lambda: LoutZoneSelected(12))
    ButtonL2_0.place(relx=0.687, rely=0.375, height=94, width=149)
    ButtonL2_0.configure(activebackground="#ececec")
    ButtonL2_0.configure(activeforeground="#000000")
    ButtonL2_0.configure(background="black")
    ButtonL2_0.configure(disabledforeground="#a3a3a3")
    ButtonL2_0.configure(foreground="gold")
    ButtonL2_0.configure(highlightbackground="#d9d9d9")
    ButtonL2_0.configure(highlightcolor="black")
    ButtonL2_0.configure(pady="0")
    ButtonL2_0.configure(text='''Cover \n (1 Run)''')
    ButtonL2_0.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 12 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonL2_0.configure(state='disabled', background='gray25')

    ButtonL2_1 = tk.Button(Loutzone_pane, command=lambda: LoutZoneSelected(19))
    ButtonL2_1.place(relx=0.125, rely=0.0, height=84, width=299)
    ButtonL2_1.configure(activebackground="#ececec")
    ButtonL2_1.configure(activeforeground="#000000")
    ButtonL2_1.configure(background="black")
    ButtonL2_1.configure(disabledforeground="#a3a3a3")
    ButtonL2_1.configure(foreground="gold")
    ButtonL2_1.configure(highlightbackground="#d9d9d9")
    ButtonL2_1.configure(highlightcolor="black")
    ButtonL2_1.configure(pady="0")
    ButtonL2_1.configure(text='''Fine Leg \n (2 Runs)''')
    ButtonL2_1.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    ButtonL2_1.configure(state='disabled', background='gray25')

    ButtonL2_2 = tk.Button(Loutzone_pane, command=lambda: LoutZoneSelected(18))
    ButtonL2_2.place(relx=0.5, rely=0.0, height=84, width=299)
    ButtonL2_2.configure(activebackground="#ececec")
    ButtonL2_2.configure(activeforeground="#000000")
    ButtonL2_2.configure(background="black")
    ButtonL2_2.configure(disabledforeground="#a3a3a3")
    ButtonL2_2.configure(foreground="gold")
    ButtonL2_2.configure(highlightbackground="#d9d9d9")
    ButtonL2_2.configure(highlightcolor="black")
    ButtonL2_2.configure(pady="0")
    ButtonL2_2.configure(text='''Off Slip \n (2 Runs)''')
    ButtonL2_2.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    ButtonL2_2.configure(state='disabled', background='gray25')

    ButtonL2_3 = tk.Button(Loutzone_pane, command=lambda: LoutZoneSelected(11))
    ButtonL2_3.place(relx=0.687, rely=0.177, height=94, width=149)
    ButtonL2_3.configure(activebackground="#ececec")
    ButtonL2_3.configure(activeforeground="#000000")
    ButtonL2_3.configure(background="black")
    ButtonL2_3.configure(disabledforeground="#a3a3a3")
    ButtonL2_3.configure(foreground="gold")
    ButtonL2_3.configure(highlightbackground="#d9d9d9")
    ButtonL2_3.configure(highlightcolor="black")
    ButtonL2_3.configure(pady="0")
    ButtonL2_3.configure(text='''Square \n Off \n (2 Runs)''')
    ButtonL2_3.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 11 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonL2_3.configure(state='disabled', background='gray25')

    ButtonL2_4 = tk.Button(Loutzone_pane, command=lambda: LoutZoneSelected(14))
    ButtonL2_4.place(relx=0.125, rely=0.771, height=89, width=199)
    ButtonL2_4.configure(activebackground="#ececec")
    ButtonL2_4.configure(activeforeground="#000000")
    ButtonL2_4.configure(background="black")
    ButtonL2_4.configure(disabledforeground="#a3a3a3")
    ButtonL2_4.configure(foreground="gold")
    ButtonL2_4.configure(highlightbackground="#d9d9d9")
    ButtonL2_4.configure(highlightcolor="black")
    ButtonL2_4.configure(pady="0")
    ButtonL2_4.configure(text='''Mid On \n (4 Runs)''')
    ButtonL2_4.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 14 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonL2_4.configure(state='disabled', background='gray25')

    ButtonL2_5 = tk.Button(Loutzone_pane, command=lambda: LoutZoneSelected(17))
    ButtonL2_5.place(relx=0.125, rely=0.177, height=142, width=149)
    ButtonL2_5.configure(activebackground="#ececec")
    ButtonL2_5.configure(activeforeground="#000000")
    ButtonL2_5.configure(background="black")
    ButtonL2_5.configure(disabledforeground="#a3a3a3")
    ButtonL2_5.configure(foreground="gold")
    ButtonL2_5.configure(highlightbackground="#d9d9d9")
    ButtonL2_5.configure(highlightcolor="black")
    ButtonL2_5.configure(pady="0")
    ButtonL2_5.configure(text='''Square \n Leg \n (1 Run)''')
    ButtonL2_5.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 17 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonL2_5.configure(state='disabled', background='gray25')

    ButtonL2_6 = tk.Button(Loutzone_pane, command=lambda: LoutZoneSelected(13))
    ButtonL2_6.place(relx=0.687, rely=0.572, height=94, width=149)
    ButtonL2_6.configure(activebackground="#ececec")
    ButtonL2_6.configure(activeforeground="#000000")
    ButtonL2_6.configure(background="black")
    ButtonL2_6.configure(disabledforeground="#a3a3a3")
    ButtonL2_6.configure(foreground="gold")
    ButtonL2_6.configure(highlightbackground="#d9d9d9")
    ButtonL2_6.configure(highlightcolor="black")
    ButtonL2_6.configure(pady="0")
    ButtonL2_6.configure(text='''Extra \n Cover \n (3 Runs)''')
    ButtonL2_6.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 13 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonL2_6.configure(state='disabled', background='gray25')

    ButtonL2_7 = tk.Button(Loutzone_pane, command=lambda: LoutZoneSelected(15))
    ButtonL2_7.place(relx=0.375, rely=0.771, height=89, width=199)
    ButtonL2_7.configure(activebackground="#ececec")
    ButtonL2_7.configure(activeforeground="#000000")
    ButtonL2_7.configure(background="black")
    ButtonL2_7.configure(disabledforeground="#a3a3a3")
    ButtonL2_7.configure(foreground="gold")
    ButtonL2_7.configure(highlightbackground="#d9d9d9")
    ButtonL2_7.configure(highlightcolor="black")
    ButtonL2_7.configure(pady="0")
    ButtonL2_7.configure(text='''Straight \n (6 Runs)''')
    ButtonL2_7.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 15 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonL2_7.configure(state='disabled', background='gray25')

    ButtonL2_8 = tk.Button(Loutzone_pane, command=lambda: LoutZoneSelected(16))
    ButtonL2_8.place(relx=0.125, rely=0.475, height=140, width=149)
    ButtonL2_8.configure(activebackground="#ececec")
    ButtonL2_8.configure(activeforeground="#000000")
    ButtonL2_8.configure(background="black")
    ButtonL2_8.configure(disabledforeground="#a3a3a3")
    ButtonL2_8.configure(foreground="gold")
    ButtonL2_8.configure(highlightbackground="#d9d9d9")
    ButtonL2_8.configure(highlightcolor="black")
    ButtonL2_8.configure(pady="0")
    ButtonL2_8.configure(text='''Mid \n Wicket \n (2 Runs)''')
    ButtonL2_8.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 16 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonL2_8.configure(state='disabled', background='gray25')

    ButtonL2_9 = tk.Button(Loutzone_pane, command=lambda: LoutZoneSelected(14))
    ButtonL2_9.place(relx=0.625, rely=0.771, height=84, width=199)
    ButtonL2_9.configure(activebackground="#ececec")
    ButtonL2_9.configure(activeforeground="#000000")
    ButtonL2_9.configure(background="black")
    ButtonL2_9.configure(disabledforeground="#a3a3a3")
    ButtonL2_9.configure(foreground="gold")
    ButtonL2_9.configure(highlightbackground="#d9d9d9")
    ButtonL2_9.configure(highlightcolor="black")
    ButtonL2_9.configure(pady="0")
    ButtonL2_9.configure(text='''Mid Off \n (4 Runs)''')
    ButtonL2_9.configure(
        font="-family {Segoe UI Black} -size 14 -weight bold -slant roman -underline 0 -overstrike 0")
    if 14 in match_yaml['info']['earlier_selected_out_zones']:
        ButtonL2_9.configure(state='disabled', background='gray25')

    def disable_event():
        pass

    top.protocol("WM_DELETE_WINDOW", disable_event)

    tk.mainloop()
DICT['toss_decision'] = match_yaml['info']['toss_decision']
DICT['toss_winner'] = match_yaml['info']['toss_winner']
DICT['batting_team'] = match_yaml['innings']['first_innings']['batteam']
f = open("slot_detail.txt")
slot = f.read()
f.close
slot = str(slot) + "_time_slot"
slot_details = json_file['booking_data'][slot]
match_yaml['meta']['NEE'] = 1

curr_innings = int(match_yaml['meta']['innings_completed']) + 1
if curr_innings == 1:
    innings_info = match_yaml['innings']['first_innings']
elif curr_innings == 2:
    innings_info = match_yaml['innings']['second_innings']
elif curr_innings == 3:
    innings_info = match_yaml['innings']['third_innings']
else:
    innings_info = match_yaml['innings']['fourth_innings']


# variables to hold scores and wickets and deliveries
if len(innings_info['deliveries']) == 1:
    current_delivery = 1
    prevdel = collections.OrderedDict(
        [('valid_ball_no', 0), ('batsman_player_id', 10000004), ('bowler_player_id', 10000001),
         ('fielder1_player_id', -9999), ('fielder2_player_id', -9999), ('consecutive_out_flag', 0),
         ('zone_id', 9999), ('out_zone_id', 5), ('out_type_id', -1), ('catch_player_id', -9999),
         ('bat_body_impact', 1), ('body_touch', -9999), ('bat_touch', -9999),
         ('extras', collections.OrderedDict([('wides', 0), ('no_ball', 0)])),
         ('runs', collections.OrderedDict([('batsman', 0), ('extras', 0), ('total', 0)])), ('score_after', 0),
         ('wic_after', 0), ('commentary_line_id', 99999999)])
else:
    current_delivery = len(innings_info['deliveries'])
    prevdel = innings_info['deliveries'][current_delivery - 2][current_delivery - 1]

print("current_del",current_delivery)
print("curr_inn", curr_innings)

if curr_innings == 1:
    currdel = match_yaml['innings']['first_innings']['deliveries'][current_delivery - 1][current_delivery]
if curr_innings == 2:
    currdel = match_yaml['innings']['second_innings']['deliveries'][current_delivery - 1][current_delivery]
if curr_innings == 3:
    currdel = match_yaml['innings']['third_innings']['deliveries'][current_delivery - 1][current_delivery]
if curr_innings == 4:
    currdel = match_yaml['innings']['fourth_innings']['deliveries'][current_delivery - 1][current_delivery]

with open("empty_sc_yaml.yaml") as f:
    sc_yaml = yaml.load(f, Loader=yamlordereddictloader.Loader)

sc_yaml['meta']['created'] = match_yaml['meta']['created']

def findInningOvers(innings_check):
    if innings_check == 1:
        no_of_deliveries = len(match_yaml['innings']['first_innings']['deliveries'])
        valid_balls = match_yaml['innings']['first_innings']['deliveries'][no_of_deliveries - 1][no_of_deliveries][
            'valid_ball_no']
        return str(valid_balls // 6) + '.' + str(valid_balls % 6)
    elif innings_check == 2:
        no_of_deliveries = len(match_yaml['innings']['second_innings']['deliveries'])
        valid_balls = match_yaml['innings']['second_innings']['deliveries'][no_of_deliveries - 1][no_of_deliveries][
            'valid_ball_no']
        return str(valid_balls // 6) + '.' + str(valid_balls % 6)
    elif innings_check == 3:
        no_of_deliveries = len(match_yaml['innings']['third_innings']['deliveries'])
        valid_balls = match_yaml['innings']['third_innings']['deliveries'][no_of_deliveries - 1][no_of_deliveries][
            'valid_ball_no']
        return str(valid_balls // 6) + '.' + str(valid_balls % 6)
    else:
        no_of_deliveries = len(match_yaml['innings']['fourth_innings']['deliveries'])
        valid_balls = match_yaml['innings']['fourth_innings']['deliveries'][no_of_deliveries - 1][no_of_deliveries][
            'valid_ball_no']
        return str(valid_balls // 6) + '.' + str(valid_balls % 6)

sc_yaml['meta']['innings_completed'] = match_yaml['meta']['innings_completed']
sc_yaml['meta']['deliveries_completed'] = match_yaml['meta']['deliveries_completed']
sc_yaml['info']['no_of_players'] = match_yaml['info']['no_of_players']
sc_yaml['info']['total_overs'] = match_yaml['info']['overs']
if match_yaml['info']['toss_winner'] == 1 and match_yaml['info']['toss_decision'] == 1:
    sc_yaml['info']['toss_winner'] = "अपनी गली"
    sc_yaml['info']['decision'] = 'BAT'
    sc_yaml['info']['batteam1'] = "अपनी गली"
    sc_yaml['info']['batteam2'] = "बाजू गली"
elif match_yaml['info']['toss_winner'] == 1 and match_yaml['info']['toss_decision'] == 2:
    sc_yaml['info']['toss_winner'] = "अपनी गली"
    sc_yaml['info']['decision'] = 'BOWL'
    sc_yaml['info']['batteam1'] = "बाजू गली"
    sc_yaml['info']['batteam2'] = "अपनी गली"
elif match_yaml['info']['toss_winner'] == 2 and match_yaml['info']['toss_decision'] == 1:
    sc_yaml['info']['toss_winner'] = "बाजू गली"
    sc_yaml['info']['decision'] = 'BAT'
    sc_yaml['info']['batteam1'] = "बाजू गली"
    sc_yaml['info']['batteam2'] = "अपनी गली"
else:
    sc_yaml['info']['toss_winner'] = "बाजू गली"
    sc_yaml['info']['decision'] = 'BOWL'
    sc_yaml['info']['batteam1'] = "अपनी गली"
    sc_yaml['info']['batteam2'] = "बाजू गली"
sc_yaml['info']['overs'] = match_yaml['info']['overs']
sc_yaml['info']['innings'] = match_yaml['info']['innings']
innings = int(match_yaml['meta']['innings_completed']) + 1
if innings == 1:
    innings_info = match_yaml['innings']['first_innings']
elif innings == 2:
    innings_info = match_yaml['innings']['second_innings']
    sc_yaml['info']['outcome']['t1i1_score'] = match_yaml['info']['outcome']['t1i1_score']
    sc_yaml['info']['outcome']['t1i1_wicket'] = match_yaml['info']['outcome']['t1i1_wicket']
    sc_yaml['info']['outcome']['t1i1_overs'] = findInningOvers(1)
elif innings == 3:
    innings_info = match_yaml['innings']['third_innings']
    sc_yaml['info']['outcome']['t1i1_score'] = match_yaml['info']['outcome']['t1i1_score']
    sc_yaml['info']['outcome']['t1i1_wicket'] = match_yaml['info']['outcome']['t1i1_wicket']
    sc_yaml['info']['outcome']['t2i1_score'] = match_yaml['info']['outcome']['t2i1_score']
    sc_yaml['info']['outcome']['t2i1_wicket'] = match_yaml['info']['outcome']['t2i1_wicket']
    sc_yaml['info']['outcome']['t1i1_overs'] = findInningOvers(1)
    sc_yaml['info']['outcome']['t2i1_overs'] = findInningOvers(2)
    sc_yaml['info']['outcome']['t1i2_overs'] = findInningOvers(3)
else:
    innings_info = match_yaml['innings']['fourth_innings']
    current_delivery = len(innings_info['deliveries'])
    sc_yaml['info']['outcome']['t1i1_score'] = match_yaml['info']['outcome']['t1i1_score']
    sc_yaml['info']['outcome']['t1i1_wicket'] = match_yaml['info']['outcome']['t1i1_wicket']
    sc_yaml['info']['outcome']['t2i1_score'] = match_yaml['info']['outcome']['t2i1_score']
    sc_yaml['info']['outcome']['t2i1_wicket'] = match_yaml['info']['outcome']['t2i1_wicket']
    sc_yaml['info']['outcome']['t1i2_score'] = match_yaml['info']['outcome']['t1i2_score']
    sc_yaml['info']['outcome']['t1i2_wicket'] = match_yaml['info']['outcome']['t1i2_wicket']
    sc_yaml['info']['outcome']['t2i2_score'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['score_after']
    sc_yaml['info']['outcome']['t2i2_wicket'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['wic_after']
    sc_yaml['info']['outcome']['t1i1_overs'] = findInningOvers(1)
    sc_yaml['info']['outcome']['t2i1_overs'] = findInningOvers(2)
    sc_yaml['info']['outcome']['t1i2_overs'] = findInningOvers(3)
    sc_yaml['info']['outcome']['t2i2_overs'] = findInningOvers(4)


# variables to hold scores and wickets and deliveries
current_delivery = len(innings_info['deliveries'])
sc_yaml['info']['current_score'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['score_after']
sc_yaml['info']['current_wic'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['wic_after']
sc_yaml['info']['current_valid_ball'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['valid_ball_no']
sc_yaml['info']['current_cf'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['consecutive_out_flag']
sc_yaml['info']['prob_after'] = innings_info['deliveries'][current_delivery - 1][current_delivery][
    'prob_after']
if innings_info['deliveries'][current_delivery - 1][current_delivery]['extras']['wides'] == 1:
    sc_yaml['info']['nb_wd_con'] = "wd"
elif innings_info['deliveries'][current_delivery - 1][current_delivery]['extras']['no_ball'] == 1:
    sc_yaml['info']['nb_wd_con'] = "nb"
elif innings_info['deliveries'][current_delivery - 1][current_delivery]['consecutive_out_flag'] == 1:
    sc_yaml['info']['nb_wd_con'] = "con"
else:
    sc_yaml['info']['nb_wd_con'] = "  "
batting_team_no = int(innings_info['batteam'])
if batting_team_no == 1:
    sc_yaml['info']['bat_team_name'] = match_yaml['info']['teams']['team1']['player1']['player_name'][0:7] + " & " + \
                    match_yaml['info']['teams']['team1']['player2']['player_name'][0:7]
else:
    sc_yaml['info']['bat_team_name'] = match_yaml['info']['teams']['team2']['player1']['player_name'][0:7] + " & " + \
                    match_yaml['info']['teams']['team2']['player2']['player_name'][0:7]
curr_bowl_id = innings_info['deliveries'][current_delivery - 1][current_delivery]['bowler_player_id']
curr_batsman_id = innings_info['deliveries'][current_delivery - 1][current_delivery]['batsman_player_id']
sc_yaml['info']['curr_batsman'] = curr_batsman_id
sc_yaml['info']['curr_bowler'] = curr_bowl_id

# loop for batsman'stats
if innings_info['batting_players_involved']['batsman1']['player_id'] == curr_batsman_id:
    sc_yaml['info']['runs_curr_bat'] = innings_info['batting_players_involved']['batsman1']['runs_scored']
    sc_yaml['info']['bowls_curr_bat'] = innings_info['batting_players_involved']['batsman1']['balls_faced']
elif innings_info['batting_players_involved']['batsman2']['player_id'] == curr_batsman_id:
    sc_yaml['info']['runs_curr_bat'] = innings_info['batting_players_involved']['batsman2']['runs_scored']
    sc_yaml['info']['bowls_curr_bat'] = innings_info['batting_players_involved']['batsman2']['balls_faced']
else:
    sc_yaml['info']['runs_curr_bat'] = innings_info['batting_players_involved']['batsman3']['runs_scored']
    sc_yaml['info']['bowls_curr_bat'] = innings_info['batting_players_involved']['batsman3']['balls_faced']

if innings_info['bowling_players_involved']['bowler1']['player_id'] == curr_bowl_id:
    sc_yaml['info']['runs_curr_bow'] = innings_info['bowling_players_involved']['bowler1']['runs_given']
    sc_yaml['info']['bowls_curr_bow'] = innings_info['bowling_players_involved']['bowler1']['balls_bowled']
    sc_yaml['info']['wics_curr_bow'] = innings_info['bowling_players_involved']['bowler1']['wickets_taken']
elif innings_info['bowling_players_involved']['bowler2']['player_id'] == curr_bowl_id:
    sc_yaml['info']['runs_curr_bow'] = innings_info['bowling_players_involved']['bowler2']['runs_given']
    sc_yaml['info']['bowls_curr_bow'] = innings_info['bowling_players_involved']['bowler2']['balls_bowled']
    sc_yaml['info']['wics_curr_bow'] = innings_info['bowling_players_involved']['bowler2']['wickets_taken']
else:
    sc_yaml['info']['runs_curr_bow'] = innings_info['bowling_players_involved']['bowler3']['runs_given']
    sc_yaml['info']['bowls_curr_bow'] = innings_info['bowling_players_involved']['bowler3']['balls_bowled']
    sc_yaml['info']['wics_curr_bow'] = innings_info['bowling_players_involved']['bowler3']['wickets_taken']

sc_yaml['info']['curr_out_type_id'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['out_type_id']
sc_yaml['info']['curr_ball_run'] = innings_info['deliveries'][current_delivery - 1][current_delivery]['runs']['total']





yaml.dump(sc_yaml, open('yaml/sc_yaml.yaml', 'w'), Dumper=yamlordereddictloader.Dumper,
          default_flow_style=False)

#yaml.dump(sc_yaml,open('\\\LAPTOP-NBIUC8KC\\yaml\\sc_yaml.yaml', 'w'),Dumper=yamlordereddictloader.Dumper,default_flow_style=False)
#time.sleep(0.5)
#os.system('\\\DESKTOP-9CO7JQ3\\Score_Card\\ScoreCard.py')
#time.sleep(5)
fall_of_wicket = currdel['wic_after'] == 1 and currdel['out_type_id'] > 0
if fall_of_wicket:
    len_btpc = len(match_yaml['info']['batting_player_choice'])
    btpc = collections.OrderedDict(
        [('deliveries_done', 0), ('old_batsman_id', -999), ('new_batsman_id', 10000001),
         ('change_type', 1)])
    btpc['deliveries_done'] = current_delivery
    btpc['old_batsman_id'] = currdel['batsman_player_id']
    if curr_innings == 1:
        if currdel['batsman_player_id'] == \
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1'][
                    'player_id']:
            btpc['new_batsman_id'] = \
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2']['player_id']
        elif currdel['batsman_player_id'] == \
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman2'][
                    'player_id']:
            btpc['new_batsman_id'] = \
                match_yaml['innings']['first_innings']['batting_players_involved']['batsman1']['player_id']
    if curr_innings == 2:
        if currdel['batsman_player_id'] == \
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1'][
                    'player_id']:
            btpc['new_batsman_id'] = \
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2']['player_id']
        elif currdel['batsman_player_id'] == \
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman2'][
                    'player_id']:
            btpc['new_batsman_id'] = \
                match_yaml['innings']['second_innings']['batting_players_involved']['batsman1']['player_id']
    if curr_innings == 3:
        if currdel['batsman_player_id'] == \
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1'][
                    'player_id']:
            btpc['new_batsman_id'] = \
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2']['player_id']
        elif currdel['batsman_player_id'] == \
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman2'][
                    'player_id']:
            btpc['new_batsman_id'] = \
                match_yaml['innings']['third_innings']['batting_players_involved']['batsman1']['player_id']
    if curr_innings == 4:
        if currdel['batsman_player_id'] == \
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1'][
                    'player_id']:
            btpc['new_batsman_id'] = \
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2']['player_id']
        elif currdel['batsman_player_id'] == \
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman2'][
                    'player_id']:
            btpc['new_batsman_id'] = \
                match_yaml['innings']['fourth_innings']['batting_players_involved']['batsman1']['player_id']
    bat_arm = 2
    if btpc['new_batsman_id'] == match_yaml['info']['teams']['team1']['player1']['player_id']:
        bat_arm = match_yaml['info']['teams']['team1']['player1']['batting_arm']
    if btpc['new_batsman_id'] == match_yaml['info']['teams']['team1']['player2']['player_id']:
        bat_arm = match_yaml['info']['teams']['team1']['player2']['batting_arm']
    if btpc['new_batsman_id'] == match_yaml['info']['teams']['team2']['player1']['player_id']:
        bat_arm = match_yaml['info']['teams']['team2']['player1']['batting_arm']
    if btpc['new_batsman_id'] == match_yaml['info']['teams']['team2']['player2']['player_id']:
        bat_arm = match_yaml['info']['teams']['team2']['player2']['batting_arm']
    f = open("yaml/flap.txt")
    con = f.read()
    f.close
    con1 = str(int(bat_arm) - 1) + con[1] + con[2]
    with open("yaml/flap.txt", 'w', encoding='utf-8') as f:
        f.write(con1)
    btpc = collections.OrderedDict([((len_btpc+1), btpc)])
    match_yaml['info']['batting_player_choice'].append(btpc)

fourth_inn_end = False
third_inn_end = False
second_inn_end = False
first_inn_end = False
third_inn_match_end = False
if curr_innings == 4:
    fourth_inn_end = currdel['wic_after'] == 2 or currdel['valid_ball_no'] == 24 or currdel['score_after'] > (
                match_yaml['info']['outcome']['t1i1_score'] + match_yaml['info']['outcome']['t1i2_score'] -
                match_yaml['info']['outcome']['t2i1_score'])
if curr_innings == 3:
    third_inn_end = currdel['wic_after'] == 2 or currdel['valid_ball_no'] == 24
    third_inn_match_end = third_inn_end and match_yaml['info']['outcome']['t2i1_score'] > (
                match_yaml['info']['outcome']['t1i1_score'] + currdel['score_after'])
if curr_innings == 2:
    second_inn_end = currdel['wic_after'] == 2 or currdel['valid_ball_no'] == 24
if curr_innings == 1:
    first_inn_end = currdel['wic_after'] == 2 or currdel['valid_ball_no'] == 24
if fourth_inn_end or third_inn_match_end:
    loop_exit = 1
    match_yaml['meta']['NEE'] = 0
    if curr_innings == 4:
        match_yaml['info']['outcome']['t2i2_wicket'] = \
            match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1'][
                'wickets_taken'] + \
            match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['wickets_taken']
        match_yaml['info']['outcome']['t2i2_score'] = \
            match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
            match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['runs_given']
        team2_total_score = match_yaml['info']['outcome']['t2i1_score'] + match_yaml['info']['outcome'][
            't2i2_score']
    else:
        match_yaml['info']['outcome']['t1i2_wicket'] = \
            match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + \
            match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wickets_taken']
        match_yaml['info']['outcome']['t1i2_score'] = \
            match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
            match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['runs_given']
        team2_total_score = match_yaml['info']['outcome']['t2i1_score']

    team1_total_score = match_yaml['info']['outcome']['t1i1_score'] + match_yaml['info']['outcome'][
        't1i2_score']
    if team1_total_score > team2_total_score:
        match_yaml['info']['outcome']['result_type'] = 1
    elif team2_total_score > team1_total_score:
        match_yaml['info']['outcome']['result_type'] = 2
    elif team1_total_score == team2_total_score:
        match_yaml['info']['outcome']['result_type'] = 3

    if third_inn_match_end:
        match_yaml['info']['outcome']['innings_win'] = 1
    else:
        match_yaml['info']['outcome']['innings_win'] = 0

    if team1_total_score > team2_total_score:
        match_yaml['info']['outcome']['win_margin_runs'] = int(team1_total_score - team2_total_score)
        winner_team_id = 1
    else:
        match_yaml['info']['outcome']['win_margin_runs'] = int(team2_total_score - team1_total_score)
        winner_team_id = 2
    # Below 22 lines to be added to 3p, 4p...
    if match_yaml['info']['toss_winner'] == 1:
        if match_yaml['info']['toss_decision'] == 1:
            if winner_team_id == 1:
                match_yaml['info']['outcome']['winner_team_id'] = 1
            else:
                match_yaml['info']['outcome']['winner_team_id'] = 2
        else:
            if winner_team_id == 1:
                match_yaml['info']['outcome']['winner_team_id'] = 2
            else:
                match_yaml['info']['outcome']['winner_team_id'] = 1
    else:
        if match_yaml['info']['toss_decision'] == 2:
            if winner_team_id == 1:
                match_yaml['info']['outcome']['winner_team_id'] = 1
            else:
                match_yaml['info']['outcome']['winner_team_id'] = 2
        else:
            if winner_team_id == 1:
                match_yaml['info']['outcome']['winner_team_id'] = 2
            else:
                match_yaml['info']['outcome']['winner_team_id'] = 1

    if match_yaml['info']['outcome']['innings_win'] == 0:
        if team2_total_score > team1_total_score:
            match_yaml['info']['outcome']['win_margin_balls_left'] = (
                    24 - currdel['valid_ball_no'])
            match_yaml['info']['outcome']['win_margin_wickets_left'] = (
                    2 - currdel['wic_after'])
        else:
            match_yaml['info']['outcome']['win_margin_runs'] = int(team1_total_score - team2_total_score)
    else:
        match_yaml['info']['outcome']['win_margin_runs'] = int(team2_total_score - team1_total_score)
    # these 7 lines to be added to 3p, 4p...
    sc_yaml['info']['outcome']['result_type'] = match_yaml['info']['outcome']['result_type']
    sc_yaml['info']['outcome']['innings_win'] = match_yaml['info']['outcome']['innings_win']
    sc_yaml['info']['outcome']['winner_team_id'] = match_yaml['info']['outcome']['winner_team_id']
    sc_yaml['info']['outcome']['win_margin_runs'] = match_yaml['info']['outcome']['win_margin_runs']
    sc_yaml['info']['outcome']['win_margin_wickets_left'] = match_yaml['info']['outcome']['win_margin_wickets_left']
    sc_yaml['info']['outcome']['win_margin_balls_left'] = match_yaml['info']['outcome']['win_margin_balls_left']
    yaml.dump(sc_yaml, open('yaml/sc_yaml.yaml', 'w'), Dumper=yamlordereddictloader.Dumper,
              default_flow_style=False)
elif first_inn_end:
    loop_exit = 1
    match_yaml['info']['earlier_selected_out_zones'] = []
    match_yaml['info']['outcome']['t1i1_wicket'] = \
        match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + \
        match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['wickets_taken']
    match_yaml['info']['outcome']['t1i1_score'] = \
        match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
        match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['runs_given']
    match_yaml['meta']['NEE'] = 345
    match_yaml['meta']['innings_completed'] = 1
    match_yaml['meta']['deliveries_completed'] = 0

elif second_inn_end:
    loop_exit = 1
    match_yaml['info']['earlier_selected_out_zones'] = []
    match_yaml['info']['outcome']['t2i1_wicket'] = \
        match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + \
        match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['wickets_taken']
    match_yaml['info']['outcome']['t2i1_score'] = \
        match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
        match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['runs_given']
    match_yaml['meta']['NEE'] = 345
    match_yaml['meta']['innings_completed'] = 2
    match_yaml['meta']['deliveries_completed'] = 0

elif third_inn_end:
    loop_exit = 1
    match_yaml['info']['earlier_selected_out_zones'] = []
    match_yaml['info']['outcome']['t1i2_wicket'] = \
        match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['wickets_taken'] + \
        match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['wickets_taken']
    match_yaml['info']['outcome']['t1i2_score'] = \
        match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['runs_given'] + \
        match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['runs_given']
    match_yaml['meta']['NEE'] = 345
    match_yaml['meta']['innings_completed'] = 3
    match_yaml['meta']['deliveries_completed'] = 0

elif currdel['valid_ball_no'] % 6 == 0 and currdel['runs']['extras'] == 0:
    loop_exit = 1
    match_yaml['meta']['NEE'] = 5
    # match_yaml['info']['bowling_player_choice']['current_change'] = int(current_delivery / 6 + 1)
    len_bwpc = len(match_yaml['info']['bowling_player_choice'])
    bwpc = collections.OrderedDict(
        [('deliveries_done', 0), ('old_bowler_id', -999), ('new_bowler_id', 10000001)])
    bwpc['deliveries_done'] = current_delivery
    bwpc['old_bowler_id'] = currdel['bowler_player_id']
    if curr_innings == 1:
        if currdel['bowler_player_id'] == \
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1'][
                    'player_id']:
            bwpc['new_bowler_id'] = \
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2']['player_id']
        elif currdel['bowler_player_id'] == \
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler2'][
                    'player_id']:
            bwpc['new_bowler_id'] = \
                match_yaml['innings']['first_innings']['bowling_players_involved']['bowler1']['player_id']
    if curr_innings == 2:
        if currdel['bowler_player_id'] == \
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1'][
                    'player_id']:
            bwpc['new_bowler_id'] = \
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2']['player_id']
        elif currdel['bowler_player_id'] == \
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler2'][
                    'player_id']:
            bwpc['new_bowler_id'] = \
                match_yaml['innings']['second_innings']['bowling_players_involved']['bowler1']['player_id']
    if curr_innings == 3:
        if currdel['bowler_player_id'] == \
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1'][
                    'player_id']:
            bwpc['new_bowler_id'] = \
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2']['player_id']
        elif currdel['bowler_player_id'] == \
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler2'][
                    'player_id']:
            bwpc['new_bowler_id'] = \
                match_yaml['innings']['third_innings']['bowling_players_involved']['bowler1']['player_id']
    if curr_innings == 4:
        if currdel['bowler_player_id'] == \
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1'][
                    'player_id']:
            bwpc['new_bowler_id'] = \
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2']['player_id']
        elif currdel['bowler_player_id'] == \
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler2'][
                    'player_id']:
            bwpc['new_bowler_id'] = \
                match_yaml['innings']['fourth_innings']['bowling_players_involved']['bowler1']['player_id']
    bwpc = collections.OrderedDict([((len_bwpc+1), bwpc)])
    match_yaml['info']['bowling_player_choice'].append(bwpc)

yesyes = 1
while yesyes == 1:
    if int(match_yaml['meta']['NEE']) == 345:
        _3()
        _4()
        len_btpc5 = len(match_yaml['info']['batting_player_choice'])
        bat_arm5 = 2
        if match_yaml['info']['batting_player_choice'][len_btpc5 - 1][len_btpc5]['new_batsman_id'] == \
                match_yaml['info']['teams']['team1']['player1']['player_id']:
            bat_arm5 = match_yaml['info']['teams']['team1']['player1']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc5 - 1][len_btpc5]['new_batsman_id'] == \
                match_yaml['info']['teams']['team1']['player2']['player_id']:
            bat_arm5 = match_yaml['info']['teams']['team1']['player2']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc5 - 1][len_btpc5]['new_batsman_id'] == \
                match_yaml['info']['teams']['team2']['player1']['player_id']:
            bat_arm5 = match_yaml['info']['teams']['team2']['player1']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc5 - 1][len_btpc5]['new_batsman_id'] == \
                match_yaml['info']['teams']['team2']['player2']['player_id']:
            bat_arm5 = match_yaml['info']['teams']['team2']['player2']['batting_arm']
        if int(bat_arm5) == 1:
            _5l()
        else:
            _5r()

    if int(match_yaml['meta']['NEE']) == 5:
        len_btpc5 = len(match_yaml['info']['batting_player_choice'])
        bat_arm5 = 2
        if match_yaml['info']['batting_player_choice'][len_btpc5 - 1][len_btpc5]['new_batsman_id'] == \
                match_yaml['info']['teams']['team1']['player1']['player_id']:
            bat_arm5 = match_yaml['info']['teams']['team1']['player1']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc5 - 1][len_btpc5]['new_batsman_id'] == \
                match_yaml['info']['teams']['team1']['player2']['player_id']:
            bat_arm5 = match_yaml['info']['teams']['team1']['player2']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc5 - 1][len_btpc5]['new_batsman_id'] == \
                match_yaml['info']['teams']['team2']['player1']['player_id']:
            bat_arm5 = match_yaml['info']['teams']['team2']['player1']['batting_arm']
        if match_yaml['info']['batting_player_choice'][len_btpc5 - 1][len_btpc5]['new_batsman_id'] == \
                match_yaml['info']['teams']['team2']['player2']['player_id']:
            bat_arm5 = match_yaml['info']['teams']['team2']['player2']['batting_arm']
        if int(bat_arm5) == 1:
            _5l()
        else:
            _5r()

    if int(match_yaml['meta']['NEE']) == 0:
        yaml.dump(
            match_yaml,
            open('yaml/match_yaml_dump.yaml', 'w'),
            Dumper=yamlordereddictloader.Dumper,
            default_flow_style=False)

        yaml.dump(
            match_yaml,
            open('yaml/resume/match_yaml_dump.yaml', 'w'),
            Dumper=yamlordereddictloader.Dumper,
            default_flow_style=False)


        yesyes = 0
    if yesyes == 1:
        arena_central()


os.system(f'python CalculateRatings.py')
time.sleep(1)

original = r'yaml/sc_yaml.yaml'
target = r'yaml/sc_yaml_copy.yaml'
shutil.copyfile(original, target)
time.sleep(1)
os.system(f'python update_back_end_tables_from_yaml_file.py')

#vidSt = open("vidst.txt","w")
#vidSt.write("0")
#vidSt.close


#program end
