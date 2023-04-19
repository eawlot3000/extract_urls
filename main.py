#!/usr/bin/env python3
import re
import webbrowser
import subprocess
import sys

def user_input():
  print("Enter the text to extract URLs from (press <ENTER> following <CTRL+E> to end input):")
  text = ""
  while True:
    line = input("")
    if line == "\x05": # CTRL+E to end
      break
    text += line + "\n"
  return text

def is_valid_url(url):
  result = subprocess.run(["curl", "-I", "-s", "-o", "/dev/null", "-w", "%{http_code}", url], capture_output=True, text=True)
  return True if result.returncode == 0 and result.stdout.strip() in ["200", "301"] else False # idk 301, cuz they moved it?

def check(matches):
  urls = []
  for i, url in enumerate(matches):
    if is_valid_url(url):
      urls.append(url)
      print("[{}, VALID]: {}".format(i+1, url))
    else:
      print("[{}, INVALID] {}".format(i+1, url))
  return urls

def with_text(text):
  matches = re.findall(r"(?P<url>https?://[^\s]+)" , text) # find all matches with 'https'
  if not matches:
    print("No URLs found in the input text.")
    return
  
  print("\n\033[32m==== that's what I found: ====\033[0m")
  for i, url in enumerate(matches): # Print each URL with its index
    print("[{}]: {}".format(i+1, url))
  
  if input("\nCheck validity of each URL using curl? (y/n): ").lower() == "y": # Check the validity of each URL and update the matches list
    print("status of each URL:")
    matches = check(matches)
  
  selection = input("\nEnter index numbers separated by spaces to open in browser (or press Enter to quit): ") # Prompt the user to select a URL by index
  if selection:
    indexes = [int(index) for index in selection.split() if index.isdigit()]
    urls = [matches[index-1] for index in indexes if index > 0 and index <= len(matches)]
    if urls:
      for url in urls: # Open the selected URLs in the default web browser
        webbrowser.open(url)
    else:
      print("No valid indexes selected.")

if __name__ == "__main__":
  if len(sys.argv) == 2:
    with open(sys.argv[1], "r") as f:
      text = f.read()
  else:
    text = user_input()
  with_text(text)
