import requests
from bs4 import BeautifulSoup as bs
from bs4.element import Comment, NavigableString
from .gmail_utils import find_nth
from django.core import serializers
from datetime import datetime
from utils.logger import log
import traceback

def parse_job_detail(body):
  """Parse html body and get job posting details
  Args:
    body: email html body
  Returns:
    String values which represent details of job post in JSON format.  
  """
  try:
    link = body[find_nth(body, 'https://www.linkedin.com/comm/jobs/view/', 1) : find_nth(body, '?trk', 1)]
    url = requests.get(link)
    htmltext = url.text
    s = find_nth(htmltext, '<code id="viewJobMetaTagModule">', 1)
    e = htmltext.rfind('--></code>') + 10
    plainData = htmltext[s : e]
    plainData = plainData.replace('<!--','')
    plainData = plainData.replace('-->','')
    soup = bs(plainData, "html.parser")
    try:
        posterInformation = soup.find('code', id='posterInformationModule')
        posterInformationJSON = posterInformation.getText()
    except:  
        posterInformationJSON = '{}' 
    try:     
        decoratedJobPosting = soup.find('code', id='decoratedJobPostingModule')
        decoratedJobPostingJSON = decoratedJobPosting.getText()
    except: 
          decoratedJobPostingJSON = '{}'
    try:      
        topCardV2 = soup.find('code', id='topCardV2Module')
        topCardV2JSON = topCardV2.getText()
    except:
        topCardV2JSON = '{}' 
        
    return posterInformationJSON, decoratedJobPostingJSON, topCardV2JSON
  except Exception as e:
      log(traceback.format_exception(None, e, e.__traceback__), 'e')  
      return '{}','{}','{}'