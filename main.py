import os
import urllib2
import requests
from bs4 import BeautifulSoup
import pafy
import logging

def down(url,plname):								#download karne ke liye
	video=pafy.new(url)
	best=video.getbest(preftype="mp4")
	fo=open("downloaddir","a+")
	path=fo.read()
	fo.close()
	path=path+str(plname)+"/"
	best.download(filepath=path,quiet=False)

def nochange(plname):
	fo=open("downloaddir","a+")
	oldcwd=os.getcwd()
	os.chdir(oldcwd+"/Downloads/")
	try:
		os.mkdir(plname)
	except OSError: None
	os.chdir(oldcwd)
	text=fo.read()
	if text=='':
		cwd=os.getcwd()
		destination=str(cwd)+"/Downloads/"
		fo.write(destination)
	fo.close()

def rectify(word):
	word=word[15:26]
	word="http://www.youtube.com/watch?v="+word
	return word
	
def prepareSoup(url):
	response=requests.get(url)
	html=response.content
	soup=BeautifulSoup(html,"html.parser")
	return soup
	
def pllen(soup):							#finds number of videos in the playlist
	cart=soup.find(id="playlist-length")
	return str(cart.text).split(' ')[0]	
	
def calculate(soup,count,listlink,leng):				#main function
	mello=0
	i=0
	usefultags=soup.find_all(attrs={"data-index":True})		#finds all tags that contain video details
	
	for carlos in usefultags:
		temp.append(carlos)			 		
		usefultags[i]=unicode(carlos)
		i+=1 	
	
	
	for carlos in usefultags:						
		words=carlos.split(' ')					# to collect substrings separated by spaces in the plain strings
		for word in words:
			word=word.encode('utf-8')
			if word.startswith("""href="/watch?v=""")==True:
				q=word.split('index=')[1].split('"')[0].split('&')[0]		
				q=int(q)
				count += 1
			if word.startswith('data-video-id=')==True:
				l=rectify(word)
		listlink[q]=l
		listname[q]=str(temp[count-1]['data-video-title'].encode('utf-8'))		
		mello+=1
		if q>=leng: 
			return
	if(mello==200):
		linknew=l+"&list="+playlistID
		soup2=prepareSoup(linknew)				#ek aur soup tayyar hai
		calculate(soup2,count,listlink,leng)			
	
os.system('clear')
url=raw_input("Paste the link of the playlist : ")


playlistID = url[49:]	
soup=prepareSoup(url)							#taaza soup tayyar hai
leng=pllen(soup)							
leng=int(leng)
listlink={}
listname={}
temp=[]
plname=soup.find_all(attrs={'data-list-title':True})
plname=plname[0]['data-list-title']

f=open(plname+" links","w+")

calculate(soup,0,listlink,leng)

for item in listlink:							#file me write karne ke liye
	f.write(str(item)+".\t"+listname[item]+" : "+listlink[item])
	f.write("\n")
	
print "\nLinks of "+str(leng)+" videos have been saved to the file 'List of Video Links' in the directory same as that of this project :) \n"

f.close()

ans=raw_input("Do you want to download the videos ? Y/N ")
if (ans=='y')or(ans=='Y'):
	r=raw_input("Do you want to set downloads directory ? Y/N ")
	if (r=='y')or(r=='Y'):
		path=raw_input("\nEnter the directory for download : ")
		oldcwd=os.getcwd()
		os.chdir(path)
		try:
			os.mkdir(plname)
		except OSError: None	
		os.chdir(oldcwd)
		fo=open("downloaddir","w+")
		fo.write(path)
		fo.close()
	elif (r=='n')or(r=='N'):
		nochange(str(plname))	
	for item in listlink:
		print "Downloading "+str(item)+" of "+str(leng)+": "
		down(listlink[item],plname)
		logging.getLogger().setLevel(logging.ERROR)
	r=raw_input("\n\n\nVideos have been downloaded! :)")
		
elif (ans=='n')or(ans=='N'):
	print "Koi baat nahi.\nThanks for using. :)"			
