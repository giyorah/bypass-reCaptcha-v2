import time
import os
import requests
import random
import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from SpeechRecogUtils import speech_rec_from_file

def sleep_gauss(offset = 1):
    delay = offset + random.gauss(2, 1)
    print(f"[INFO] Sleeping for {delay:.2f} seconds...", end = ' ')
    time.sleep(delay)
    print("Up!")

def bypass_bot_detection(driver):
    try:
        print("[INFO] Checking for bot detection...", end = ' ')
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='reCAPTCHA']"))
            )
    except:
        print("No reCAPTCHA found! Exiting the solver.")
        return
    
    try:
        print("reCAPTCHA detected! Trying to bypass it.")
        logging.info("Clicking the initial checkbox.")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))
            ).click()
        sleep_gauss(2.71)
    except:
        raise Exception("Couldn't click the 'STAGE I' checkbox for some reason.")

    try:
        print("[INFO] Checking for 'STAGE II' reCAPTCHA...", end = ' ')
        # switch to recaptcha frame
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']"))
            )
    except:
        print("No challenge detected. Exiting the solver.")
        return

    try:
        print("Challenge detected! Trying to solve it.")
        sleep_gauss()
        logging.info("Clicking the audio button.")
        # click on audio challenge
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-audio-button"))
            ).click()
    except:
        raise Exception("Couldn't click the audio button for some reason.")

    try:
        # switch to recaptcha audio challenge frame
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge expires in two minutes']"))
            )
        src = driver.find_element(By.ID, "audio-source").get_attribute("src")
        logging.info(f"Found the Audio source: {src[:70]}...")
    except:
        raise Exception("Couldn't find the audio source for some reason.")

    try:
        # download the mp3 audio file from the source
        logging.info("Downloading the audio file.")
        doc = requests.get(src)
        mp3File = 'payload.mp3'
        with open(mp3File, 'wb') as f:
            f.write(doc.content)
    except:
        raise Exception("Couldn't download the audio file.")

    try:
        logging.info("Converting from speech to text.")
        text, audio_duration = speech_rec_from_file(mp3File, 'Houndify')
        logging.info(f"Recaptcha Passcode: \"{text}\"")
        sleep_gauss(audio_duration)
    except:
        raise Exception("Couldn't convert speech to text.")

    try:
        logging.info("Locating the text box and inserting the text.")
        driver.find_element(By.ID, "audio-response").send_keys(text.lower())
        sleep_gauss(0)
    except:
        raise Exception("Couldn't locate the text box.")

    try:
        logging.info("Submitting the reponse.")
        driver.find_element(By.ID, "audio-response").send_keys(Keys.ENTER)
    except:
        raise Exception("Couldn't submit response.")

    try:
        # get rid of the audio files
        if os.path.exists(mp3File):
            logging.info(f"Removing the audio file.")
            os.remove(mp3File)
    except:
        raise Exception("mp3File variable does not exist.")

    logging.info("Challenge solved successfully. Exiting the solver.")