#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 18:17:44 2019

@author: keiji2
"""

import cv2
import numpy as np
import tkinter as tk
import requests

font = cv2.FONT_HERSHEY_COMPLEX
cap = cv2.VideoCapture(0)
white = (255, 255, 255)
bool = True

root = tk.Tk()

buf = tk.StringVar()
buf.set("")

def ifttt_webhook(eventid):
    payload = {"value1":"done","value2":"ok","value3":"good"}
    url = "https://maker.ifttt.com/trigger/"+ eventid +"/with/key/<key>"
    response = requests.post(url, data=payload)


def quit():
    if buf.get():
        buf.set(buf.get())
        root.quit()


def capture(cap):
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([80, 50, 50])
    upper_blue = np.array([100, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    score = np.count_nonzero(res)
    cv2.putText(res, str(score), (10, 200), font, 2, white, 2, cv2.LINE_AA)
    cv2.namedWindow('evl', cv2.WINDOW_NORMAL)
    cv2.namedWindow('norm', cv2.WINDOW_NORMAL)
    cv2.imshow('norm', frame)
    cv2.imshow('evl', res)
    return score


while (bool):
    capture(cap)
    key = cv2.waitKey(0) & 0xFF
    while key not in [ord('q'), ord('k')]:
        key = cv2.waitKey(0)
    if key == ord('q'):
        break
EntBox = tk.Entry(root, textvariable = buf)
EntBox.pack()
EntBox.focus_set()

button = tk.Button(root, text = "OK", command = quit)
button.pack()
root.mainloop()

threshold = int(buf.get())

while (bool):
    capture(cap)
    if threshold > capture(cap):
        ifttt_webhook("battery_has_charged")
        bool = False
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
