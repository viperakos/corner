import time
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import datetime


def getdriver():

    co = Options()
    co.add_argument('--no-sandbox')
    co.add_argument('--disable-dev-shm-usage')
    co.add_argument('disable-blink-features=AutomationControlled')
    co.add_argument('user-agent=Chrome/81.0.4044.138')
    co.add_argument("--start-maximized")
    prefs = {
        "translate_whitelists": {"gr": "en"},
        "translate": {"enabled": "True"}
    }
    co.add_experimental_option('prefs',prefs)
    co.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    co.add_argument("-lang= sl")
    # caps = co.to_capabilities()
    driver = webdriver.Chrome(options=co)

    return driver

def login(driver):

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'hm-MainHeaderRHSLoggedOutWide_LoginContainer')))
    except:
        time.sleep(10)
    loginbtn = driver.find_element_by_class_name("hm-MainHeaderRHSLoggedOutWide_LoginContainer")
    ActionChains(driver).move_to_element(loginbtn).click(loginbtn).perform()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'lms-StandardLogin_UsernameControl')))
    except Exception as error:
        # print(error,"Check username -- login")
        loginbtn = driver.find_element_by_class_name("hm-MainHeaderRHSLoggedOutWide_LoginContainer")
        ActionChains(driver).move_to_element(loginbtn).click(loginbtn).perform()
    username = driver.find_element_by_class_name("lms-StandardLogin_Username ")
    time.sleep(4)
    try:
        username_control = driver.find_element_by_class_name("lms-StandardLogin_UsernameControl")
        ActionChains(driver).move_to_element(username_control).click(username_control).perform()
        time.sleep(1)
    except Exception as error:
        print(error)
    time.sleep(2)
    username.send_keys("username")
    time.sleep(2)
    pwd = driver.find_element_by_class_name("lms-StandardLogin_Password")
    pwd.send_keys("password")
    time.sleep(2)
    login = driver.find_element_by_class_name("lms-StandardLogin_LoginButtonText")
    ActionChains(driver).move_to_element(login).click(login).perform()
    time.sleep(10)
    return driver

def loginout(driver):

    loginoutbtn = driver.find_element_by_class_name("hm-MainHeaderMembersWide_MembersMenuIcon ")
    ActionChains(driver).move_to_element(loginoutbtn).click(loginoutbtn).perform()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'um-GeneralTab ')))
    except Exception as error:
        # print(error,"Check username")
        loginoutbtn = driver.find_element_by_class_name("hm-MainHeaderMembersWide_MembersMenuIcon ")
        ActionChains(driver).move_to_element(loginoutbtn).click(loginoutbtn).perform()
    lists = driver.find_element_by_class_name('um-GeneralTab ').find_elements_by_class_name("um-MembersLinkRow ")
    for list in lists:
        # print(list.text)
        if "Log Out" == str(list.text).strip(" "):
            ActionChains(driver).move_to_element(list).click(list).perform()
            break
        else:
            pass
    time.sleep(3)
    return driver

def readconfig():

    with open('config.json',encoding="UTF-8") as json_file:
        p = json.load(json_file)
        print('Match Condition : ')
        print(p['match'])
        print('Attack : ' + str(p['attack'][0]))
        print('Dangerattak : ' + str(p['dangerattak'][0]))
        print('Corner : ' + str(p['corner'][0]))
        print("Shot : " + str(p["shot"][0]))
        print("Starttime : " + str(p["starttime"][0]))
        print("Endtime : " + str(p["endtime"][0]))
        print("Team1_score : " + str(p["team1_score"][0]))
        print("Team2_score : " + str(p["team2_score"][0]))
    config = [p['match'],p['attack'][0],p['dangerattak'][0],p['corner'][0],p["shot"][0],p["starttime"][0],p["endtime"][0],p["team1_score"][0],p["team2_score"][0]]
    return  config

def ready(baseurl):

    driver = getdriver()
    driver.get(baseurl)
    while True:
        try:
            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'fm-Menu_Language')))
            time.sleep(3)
            langbtn = driver.find_element_by_class_name("fm-Menu_Language")
            driver.execute_script('arguments[0].scrollIntoView(true);', langbtn)
            ActionChains(driver).move_to_element(langbtn).click(langbtn).perform()
            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'fm-LanguageDropDownItem')))
            time.sleep(3)
            engbtn = driver.find_element_by_class_name("fm-LanguageDropDownItem")
            ActionChains(driver).move_to_element(engbtn).click(engbtn).perform()
            time.sleep(10)
            # overview = driver.find_elements_by_class_name("ip-ControlBar_BBarItem")[0]
            # ActionChains(driver).move_to_element(overview).click(overview).perform()
            # time.sleep(1)
            return driver
        except Exception as error:
            print(error)
            driver.quit()
            time.sleep(15)
            driver = getdriver()
            driver.get(baseurl)

def main():

    setconf = readconfig()
    leauges = str(setconf[0]).split(",")
    attack_num = setconf[1]
    danattack_num = setconf[2]
    corner_num = setconf[3]
    # corner_num = 11
    shot_num = setconf[4]
    starttime = setconf[5]
    # starttime = 10
    endtime = setconf[6]
    # endtime = 44
    team1_score = setconf[7]
    team2_score = setconf[8]
    print("====================Bot start scrape=======================")
    baseurl = "https://www.bet365.gr/#/HO/"
    driver = ready(baseurl)
    betted_list = []
    while True:
        try:
            time.sleep(15)
            matchnames = []
            leaugelists = driver.find_elements_by_class_name("ovm-Competition-open")
            print("----------------------------------------------")
            for leaugelist in leaugelists:
                leaugetitle = leaugelist.find_element_by_class_name("ovm-CompetitionHeader_Name").text
                print(leaugetitle)
                try:
                    if not leaugetitle:
                        continue
                    else:
                        for leauge in leauges:
                            if leauge in str(leaugetitle):
                                matchs = leaugelist.find_element_by_class_name("ovm-FixtureList").find_elements_by_class_name("ovm-Fixture-horizontal")
                                for match in matchs:
                                    match_time = str(match.find_element_by_class_name("ovm-FixtureDetailsTwoWay_Wrapper").find_element_by_class_name("ovm-FixtureDetailsTwoWay_Timer").text).split(":")[0]
                                    match_score1 = int(match.find_element_by_class_name("ovm-FixtureDetailsTwoWay_Wrapper").find_element_by_class_name("ovm-StandardScores_TeamOne").text)
                                    match_score2 = int(match.find_element_by_class_name("ovm-FixtureDetailsTwoWay_Wrapper").find_element_by_class_name("ovm-StandardScores_TeamTwo").text)
                                    if int(match_time) > endtime or match_score2 >= team2_score or match_score1 >= team1_score:
                                        continue
                                    else:
                                        match_name = str(match.find_element_by_class_name(
                                            "ovm-FixtureDetailsTwoWay_Wrapper").find_elements_by_class_name(
                                            "ovm-FixtureDetailsTwoWay_TeamName")[0].text)
                                        if match_name + str(datetime.datetime.now()).split(" ")[0] in betted_list:
                                            pass
                                        else:
                                            matchnames.append(match_name)
                            else:
                                # print("Pass else")
                                pass
                except:
                    print("Pass else except")
                    pass
            if len(matchnames) == 0:
                print("There is no good Leauges. Wait...")
                time.sleep(15)
                # overview = driver.find_elements_by_class_name("ip-ControlBar_BBarItem")[0]
                # ActionChains(driver).move_to_element(overview).click(overview).perform()
                # time.sleep(3)
                # time.sleep(6)
                continue
            else:
                print("-------------------------------------------------------")
                for matchname in matchnames:
                # play_matchs = driver.find_elements_by_class_name("ovm-Fixture-horizontal")
                    loop_plat_match = True
                    while loop_plat_match:
                        try:
                            play_match = None
                            time.sleep(0.1)
                            play_matchs = driver.find_elements_by_class_name("ovm-Fixture-horizontal")
                            for play_matchs_one in play_matchs:
                                matchnametags = str(play_matchs_one.find_elements_by_class_name("ovm-FixtureDetailsTwoWay_TeamName")[0].text)
                                if matchname in matchnametags:
                                    play_match = play_matchs_one
                                    break
                                else:
                                    pass
                            if play_match:
                                time.sleep(0.5)
                                play_match_time = str(play_match.find_element_by_class_name("ovm-FixtureDetailsTwoWay_Timer").text).split(":")[0]
                                if int(play_match_time) < starttime:
                                    time.sleep(1)
                                    print("== ",matchname," : before attention time")
                                    loop_plat_match = False
                                    continue
                                else:
                                    print( "==",matchname,": Go to detail page")
                                    detailbtn = play_match.find_element_by_class_name("ovm-FixtureDetailsTwoWay_TeamsWrapper")
                                    ActionChains(driver).move_to_element(detailbtn).click(detailbtn).perform()
                                    time.sleep(8)
                                    # livematch = driver.find_element_by_class_name("lv-ButtonBar_MatchLiveText")
                                    # ActionChains(driver).move_to_element(livematch).click(livematch).perform()
                                    # time.sleep(1.5)
                                    print("  ---------- Start to get value")
                                    loop_match = True
                                    while loop_match:
                                        betlistnamestag = None
                                        while betlistnamestag == None:
                                            try:
                                                betlistnamestag = driver.find_elements_by_class_name("sip-MarketGroupButton_Text")
                                            except:
                                                time.sleep(10)
                                                betlistnamestag = driver.find_elements_by_class_name("sip-MarketGroupButton_Text")
                                        betlistnames = []
                                        for betlistname in betlistnamestag:
                                            betlistnames.append(str(betlistname.text))
                                        if "1st Half Asian Corners" in betlistnames:
                                            print("  This match has 1st Half bet----------")
                                            attack = driver.find_elements_by_class_name("ml-WheelChart_Container")[0]
                                            totalattack = int(str(attack.find_element_by_class_name("ml-WheelChart_Team1Text").text)) + int(str(attack.find_element_by_class_name("ml-WheelChart_Team2Text").text))
                                            danattack = driver.find_elements_by_class_name("ml-WheelChart_Container")[1]
                                            totaldanattack = int(str(danattack.find_element_by_class_name("ml-WheelChart_Team1Text").text)) + int(str(danattack.find_element_by_class_name("ml-WheelChart_Team2Text").text))
                                            target1 = driver.find_elements_by_class_name("ml1-StatsLower_MiniBarWrapper ")[0]
                                            target2 = driver.find_elements_by_class_name("ml1-StatsLower_MiniBarWrapper ")[1]
                                            totaltarget = int(str(target1.find_element_by_class_name("ml-ProgressBar_MiniBarValue-1").text)) + int(str(target1.find_element_by_class_name("ml-ProgressBar_MiniBarValue-2").text)) + int(str(target2.find_element_by_class_name("ml-ProgressBar_MiniBarValue-1").text)) + int(str(target2.find_element_by_class_name("ml-ProgressBar_MiniBarValue-2").text))
                                            if totalattack >= attack_num and totaldanattack >= danattack_num and totaltarget >= shot_num:
                                                # WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'fm-Menu_Language')))
                                                # cornernum_tag = driver.find_element_by_class_name("ml-StatButtons_Button-summary")
                                                # ActionChains(driver).move_to_element(cornernum_tag).click(cornernum_tag).perform()
                                                # time.sleep(0.2)
                                                # cornernum_tag = driver.find_element_by_class_name("ipe-SoccerGridColumn_ICorner").find_elements_by_class_name("ipe-SoccerGridCell")
                                                cornernum = int(driver.find_elements_by_class_name("ml1-StatsColumn_MiniCornerWrapper")[0].text)+int(driver.find_elements_by_class_name("ml1-StatsColumn_MiniCornerWrapper")[1].text)
                                                if cornernum >= corner_num:
                                                    print("  It have good condition for betting----------")
                                                    driver = login(driver)
                                                    loop_login = True
                                                    while loop_login:
                                                        try:
                                                            money = float(str(driver.find_element_by_class_name(
                                                                "hm-MainHeaderMembersWide_Balance").text).split("€")[1])
                                                            if money <= 0.1:
                                                                print("  ======== Please deposit money")
                                                                time.sleep(1)
                                                                driver = loginout(driver)
                                                                loop_login = False
                                                            else:
                                                                print("  ======== Bet =================")
                                                                moneyamount = money * 0.05
                                                                if moneyamount < 0.1:
                                                                    moneyamount = 0.1
                                                                else:
                                                                    pass
                                                                betlists = None
                                                                while not betlists:
                                                                    try:
                                                                        betlists = driver.find_elements_by_class_name("sip-MarketGroup")
                                                                    except:
                                                                        time.sleep(10)
                                                                        betlists = driver.find_elements_by_class_name("sip-MarketGroup")
                                                                for betlist in betlists:
                                                                    if "1st Half Asian Corners" in str(betlist.find_element_by_class_name("sip-MarketGroupButton_Text").text):
                                                                        # driver.execute_script('arguments[0].scrollIntoView(true);', betlist)
                                                                        # time.sleep(1)
                                                                        bettext = ""
                                                                        betoverbtn = betlist.find_element_by_class_name("gl-MarketGroupContainer").find_elements_by_class_name("gl-Market_General-columnheader")[1].find_element_by_class_name("gl-ParticipantOddsOnly")
                                                                        while True:
                                                                            try:
                                                                                bettext = betoverbtn.text
                                                                                if bettext != "":
                                                                                    break
                                                                                else:
                                                                                    pass
                                                                            except:
                                                                                time.sleep(4)
                                                                                while not betlists:
                                                                                    try:
                                                                                        betlists = driver.find_elements_by_class_name("sip-MarketGroup")
                                                                                    except:
                                                                                        time.sleep(8)
                                                                                        betlists = driver.find_elements_by_class_name("sip-MarketGroup")
                                                                        ActionChains(driver).move_to_element(betoverbtn).click(betoverbtn).perform()
                                                                        time.sleep(2)
                                                                        break
                                                                    else:
                                                                        pass
                                                                betamount = driver.find_element_by_class_name("bss-StakeBox_StakeValueInput")
                                                                moneyamount = 2
                                                                betamount.send_keys(str(moneyamount))
                                                                time.sleep(1)
                                                                loop_bet = True
                                                                while loop_bet:
                                                                    try:
                                                                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'bss-PlaceBetButton_Wrapper')))
                                                                        betbtn = driver.find_element_by_class_name("bss-PlaceBetButton_Wrapper")
                                                                        ActionChains(driver).move_to_element(betbtn).click(betbtn).perform()
                                                                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'bs-ReceiptContent_Done')))
                                                                        donebet = driver.find_element_by_class_name("bs-ReceiptContent_Done")
                                                                        ActionChains(driver).move_to_element(donebet).click(donebet).perform()
                                                                        time.sleep(2)
                                                                        loop_bet = False
                                                                    except:
                                                                        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME,'bs-AcceptButton')))
                                                                        acceptchange = driver.find_element_by_class_name("bs-AcceptButton")
                                                                        ActionChains(driver).move_to_element(acceptchange).click(acceptchange).perform()
                                                                        time.sleep(1)
                                                                        betamount.send_keys(str(moneyamount))
                                                                betted_list.append(matchname + str(datetime.datetime.now()).split(" ")[0])
                                                                time.sleep(3)
                                                                if moneyamount >= 2:
                                                                    loop_cash = True
                                                                    error_num = 1
                                                                    while loop_cash == True:
                                                                        try:
                                                                            mybetbtn = driver.find_element_by_class_name("hm-HeaderMenuItemMyBets")
                                                                            ActionChains(driver).move_to_element(mybetbtn).click(mybetbtn).perform()
                                                                            time.sleep(1.5)
                                                                            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME,'myb-MyBetsHeader_Container')))
                                                                            cashout_btn = driver.find_element_by_class_name("myb-MyBetsHeader_Container").find_elements_by_class_name("myb-MyBetsHeader_Button")[0]
                                                                            ActionChains(driver).move_to_element(cashout_btn).click(cashout_btn).perform()
                                                                            time.sleep(1)
                                                                            return_amount = round(float(driver.find_elements_by_class_name("myb-OpenBetItemInnerView_BetInformationText")[0].text) * 0.75, 2)
                                                                            try:
                                                                                cash_setbtn = driver.find_elements_by_class_name("myb-CloseBetButtonWithSlider_AutoCashout")[0]
                                                                                ActionChains(driver).move_to_element(cash_setbtn).click(cash_setbtn).perform()
                                                                                time.sleep(1)
                                                                            except Exception as error:
                                                                                print("This bet dont have icon..")
                                                                                loop_cash = False
                                                                                inplay_btn =driver.find_elements_by_class_name("hm-MainHeaderCentreWide_Link")[1]
                                                                                ActionChains(driver).move_to_element(inplay_btn).click(inplay_btn).perform()
                                                                                time.sleep(2)
                                                                                continue
                                                                            autocash_btn = driver.find_elements_by_class_name("myb-CashOutPopup_ButtonText")[1]
                                                                            ActionChains(driver).move_to_element(autocash_btn).click(autocash_btn).perform()
                                                                            time.sleep(1)
                                                                            cash_out_input = driver.find_element_by_class_name("myb-AutoCashOutContainer_Keypad-hide")
                                                                            ActionChains(driver).move_to_element(cash_out_input).click(cash_out_input).perform()
                                                                            time.sleep(0.5)
                                                                            cash_out_input.send_keys(str(return_amount))
                                                                            time.sleep(0.5)
                                                                            create_rule = driver.find_element_by_class_name("myb-AutoCashOutContainer_CreateButton")
                                                                            ActionChains(driver).move_to_element(create_rule).click(create_rule).perform()
                                                                            time.sleep(2)
                                                                            inplay_btn = driver.find_elements_by_class_name("hm-MainHeaderCentreWide_Link")[1]
                                                                            ActionChains(driver).move_to_element(inplay_btn).click(inplay_btn).perform()
                                                                            time.sleep(2)
                                                                            loop_cash = False
                                                                        except Exception as error:
                                                                            if error_num > 10:
                                                                                inplay_btn = driver.find_elements_by_class_name("hm-MainHeaderCentreWide_Link")[1]
                                                                                ActionChains(driver).move_to_element(inplay_btn).click(inplay_btn).perform()
                                                                                time.sleep(2)
                                                                                loop_cash = False
                                                                            else:
                                                                                error_num = error_num + 1
                                                                            print(error, "Cash out step.")
                                                                else:
                                                                    pass
                                                                driver = loginout(driver)
                                                                loop_login = False
                                                        except Exception as error:
                                                            print(error)
                                                            time.sleep(1)
                                                            driver = loginout(driver)
                                                            loop_login = False
                                                    time.sleep(4)
                                                    try:
                                                        overview = driver.find_element_by_class_name("ipe-EventHeader_BreadcrumbText")
                                                        ActionChains(driver).move_to_element(overview).click(overview).perform()
                                                        time.sleep(1)
                                                    except:
                                                        pass
                                                    loop_match = False
                                                else:
                                                    print("  This match have get less corner than I want. --------------------")
                                                    time.sleep(2)
                                                    try:
                                                        overview = driver.find_element_by_class_name("ipe-EventHeader_BreadcrumbText")
                                                        ActionChains(driver).move_to_element(overview).click(overview).perform()
                                                        time.sleep(1)
                                                    except:
                                                        pass
                                                    loop_match = False
                                            else:
                                                time.sleep(3)
                                                try:
                                                    overview = driver.find_element_by_class_name("ipe-EventHeader_BreadcrumbText")
                                                    ActionChains(driver).move_to_element(overview).click(overview).perform()
                                                    time.sleep(1)
                                                except:
                                                    pass
                                                loop_match = False
                                                print("  This match have bad condition now. --------------------")
                                        else:
                                            time.sleep(3)
                                            try:
                                                overview = driver.find_element_by_class_name("ipe-EventHeader_BreadcrumbText")
                                                ActionChains(driver).move_to_element(overview).click(overview).perform()
                                                time.sleep(1)
                                            except:
                                                pass
                                            loop_match = False
                                            print("  This match not have 1st Half Corners--------------------")
                                        # loop_match = False
                                    loop_plat_match = False
                                # time.sleep(3)
                                # overview = driver.find_element_by_class_name("ipe-EventHeader_BreadcrumbText")
                                # ActionChains(driver).move_to_element(overview).click(overview).perform()
                                # time.sleep(1)
                            else:
                                # pass
                                time.sleep(3)
                                try:
                                    overview = driver.find_element_by_class_name("ipe-EventHeader_BreadcrumbText")
                                    ActionChains(driver).move_to_element(overview).click(overview).perform()
                                    time.sleep(1)
                                except:
                                    pass
                                loop_plat_match = False
                        except Exception as error:
                            print(error)
                            print("There is one mistake condition")
                            time.sleep(3)
                            try:
                                overview = driver.find_element_by_class_name("ipe-EventHeader_BreadcrumbText ")
                                ActionChains(driver).move_to_element(overview).click(overview).perform()
                                time.sleep(1)
                            except:
                                pass
                            loop_plat_match=False
        except Exception as error:
            print(error)
            driver.quit()
            time.sleep(15)
            driver = ready(baseurl)

main()
