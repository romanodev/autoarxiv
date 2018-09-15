from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import urllib.request, urllib.parse, urllib.error
from selenium.webdriver.chrome.options import Options
import time
import re
import getpass
import zipfile


def pick_categories():

 arxiv = ['Astrophysics','Condensed Matter','General Relativity and Quantum Cosmology','High Energy Physics - Experiments','High Energy Physics - Lattice','High Energy Physics - Phenomology','High Energy Physics - Theory',
'Mathematical Physics','Nonlinear Sciences','Nuclear Experiments','Nuclear Theory','Physics','Quantum Physics']

 sc = []
 sc.append(['Astrophysics of Galaxies',
 'Cosmology and Nonalactic Astrophysics',
 'Earth and Planetary Astrophysics',
 'High Energy Astrophysics Phenomena',
 'Instrumentation and Methods for Astrophysics',
 'Solar and Stellar Astrophysics'])


 sc.append(['Disordered Systems and Neural Network',
  'Materials Science',
  'Mesoscale and Nanoscale Physics',
  'Other Condensed Matter',
  'Quantum Gases',
  'Soft Condensed Matter',
  'Statistical Mechanics',
  'Strongly Correlated Electrons',
  'Superconductivity'])

 sc.append([])
 sc.append([])
 sc.append([])
 sc.append([])
 sc.append([])
 sc.append([])


 sc.append(['Adaptation and Self-Organizing Systems',
 'Cellular Automata and Lattice Gases',
 'Chaotic dynamics',
 'Exactly Solvable and Integratable Systems',
 'Patterm Formation and Solitons'])

 sc.append([])
 sc.append([])

 sc.append(['Accelerator Physics',
 'Applied Physics',
 'Atmospheric and Oceanic Physics',
 'Atomic and Molecular Cluster',
 'Atomic Physics',
 'Biological Physics',
 'Chemical Physics',
 'Classical Physics',
 'Computational Physics',
 'Data Analysis, Statistics and Probability',
 'Fluid Dynamics',
 'General Physics',
 'Geophysics',
 'Hystory and Philosophy of Physics',
 'Instrumentation and Detectors',
 'Medical Physics',
 'Optics',
 'Physics and Society',
 'Physics Education',
 'Plasma Physics',
 'Popular Physics',
 'Space Physics'])

 sc.append([])

 print('Enter arxiv')
 print(" ")
 for n,ar in enumerate(arxiv):
  print((str(n) + ': ' + ar ))
  print(" ")
 n = int(input())
 ar_name = arxiv[n]

 if len(sc[n]) == 0 :
  sc_name = '-1'
 else:
  print(" ")
  print(('Enter subject class within ' + ar_name))
  print(" ")
  for g,ar in enumerate(sc[n]):
   print((str(g) + ': ' + ar ))
   print(" ")
  g = int(input())
  sc_name = sc[n][g]

 return ar_name,sc_name


def main():
 print(' ')
 print('''AutoArXiv is a tool to submit manuscripts to arXiv without interacting with a broswer. You'll need an arXiv username (your email), the arXiv password and a zip file containing at least a *.tex file. Lastly, you'll need Chromedriver in your PATH. The manuscript will be sumbitted once you are asked so at the end of the process. Happy disseminating your research!''')
 print(' ')


 chrome_options = webdriver.ChromeOptions()
 chrome_options.add_experimental_option("prefs", {"download.prompt_for_download": False, "plugins.always_open_pdf_externally": True,'download.default_directory':os.getcwd()})

 chrome_options.add_argument('--headless')

 b = webdriver.Chrome(chrome_options=chrome_options)
 b.get("https://arxiv.org/login")

 print('Enter email:')
 email = input()
 p = getpass.getpass()


 b.find_element_by_id("username").send_keys(email)
 b.find_element_by_id("password").send_keys(p)
 b.find_element_by_id("password").submit()
 print(' ')
 print('Logged in to arXiv')

 b.find_element_by_class_name("linkbutton").click()
 b.find_element_by_name("userinfo").click()
 b.find_element_by_xpath("//input[@name='is_author' and @value='1']").click()
 b.find_element_by_xpath("//input[@name='license' and @value='http://arxiv.org/licenses/nonexclusive-distrib/1.0/']").click()
 b.find_element_by_xpath("//input[@name='agree_policy']").click()





 (ar_name,sc_name) = pick_categories()

 b.find_element_by_xpath(r'''//select[@id='select_arch']/option[text()="''' + ar_name + r'''"]''').click()

 if not sc_name == '-1':
  try:
   element = WebDriverWait(b, 10).until(EC.text_to_be_present_in_element((By.ID, "select_sc"), "Materials Science"))
   b.find_element_by_xpath(r'''//select[@id='select_sc']/option[text()="''' + sc_name + r'''"]''').click()
  except TimeoutException:
         print("Wrong subject category within the archive")
 b.find_element_by_class_name("sub-process-button").click()


 print('Enter zipfile (with extension):')
 name = input()

 b.find_element_by_id("fileinput").send_keys(os.getcwd() + "/" + name)
 b.find_element_by_name("uploadButton").click()
 b.find_element_by_class_name("sub-process-button").click()
 b.find_element_by_id("viewpdf").click()


 while not os.path.isfile('view.pdf'):
  time.sleep(0.01)

 os.system('open view.pdf')

 print('Do you want to submit the manuscriprt? [y,n]')
 a = input()
 if not a == 'y':
  print('Submission Aborted')
  quit()



 #Get tex file---
 z = zipfile.ZipFile(os.getcwd() + "/" + name)
 for filename in z.namelist():
  if filename[-3:] == 'tex':
   data = z.open(filename).read()
   data = data.replace('\n', '')
   data = re.sub(' +',' ',data)
   abstract = re.findall(r'\\begin{abstract}(.*?)\\end{abstract}', data, re.S)[0]
   authors = re.findall(r'\\author{(.*?)}', data, re.S)
   title = re.findall(r'\\title{(.*?)}', data, re.S)[0]
   break
 z.close()
 #-----------------------------


 b.find_element_by_class_name("sub-process-button").click()

 print(' ')
 print('Is the title correct?')
 print(title)
 a = input()
 if not a == 'y':
  print('Submission Aborted')
  quit()
 b.find_element_by_name("title").send_keys(title)

 print(' ')
 print('Are the authors correct?')
 print((' and '.join(authors)))
 a = input()
 if not a == 'y':
  print('Submission Aborted')
  quit()
 b.find_element_by_name("authors").send_keys(' and '.join(authors))

 print(' ')
 print('Is the abstract correct?')
 print(abstract)
 a = input()
 if not a == 'y':
  print('Submission Aborted')
  quit()
 b.find_element_by_name("abstract").send_keys(abstract)

 b.find_element_by_class_name("sub-process-button").click()

 print(' ')
 print('Are you ready to submit?')
 a = input()
 if not a == 'y':
  print('Submission Aborted')
  quit()
 b.find_element_by_name("Submit").click()
 print(' ')
 print('Paper submitted, congratulations!')










