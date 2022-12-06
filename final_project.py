import streamlit as st
import openai
from st_clickable_images import clickable_images
import numpy as np
from PIL import Image
import requests
import base64

if "main" not in st.session_state:
		st.session_state.main=0
if "prompt" not in st.session_state:
		st.session_state.prompt = ""
if "images" not in st.session_state:
		st.session_state.images = []
if "index" not in st.session_state:
		st.session_state.index = 0
if "clothing" not in st.session_state:
		st.session_state.clothing = 0
if "final" not in st.session_state:
		st.session_state.final = 0


def nextpage(): st.session_state.main += 1
def restart():	st.session_state.main = 0
def backpage():	st.session_state.main -=1

	


def getdalleimg(stpromt):
	openai.api_key = "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"

	response = openai.Image.create(
		prompt=stpromt,
		n=6,
		size="256x256", 
		)
	image_url=[]
	for i in range(6):
		image_url.append(response['data'][i]["url"])
	return image_url


def saveimg(url):
	response = requests.get(url)
	if response.status_code:
		fp = open('files/temp/chosen_img.png', 'wb')
		fp.write(response.content)
		fp.close()


def coloredpath(clothingpath):
	temp=[clothingpath]
	for i in range (1,10):
		if "Tshirt" in clothingpath:
			temp.append("files/Tshirt_colored/Untitled-"+str(i)+".png")
		elif "crewneck" in clothingpath:
			temp.append("files/crewneck_colored/Untitled-"+str(i)+".png")
		elif "hoodie" in clothingpath:
			temp.append("files/hoodie_colored/Untitled-"+str(i)+".png")
	return temp


def editimage(coloredpath):
	overlayedpath=[]
	for index, path in enumerate(coloredpath):
		img1 = Image.open(path)
		img2 = Image.open("files/temp/chosen_img.png")
		back_im = img1.copy()
		if "Tshirt" in path:
			back_im.paste(img2, (250, 230))
		elif "crewneck" in path:
			back_im.paste(img2, (215, 200))
		elif "hoodie" in path: 
			back_im.paste(img2, (220, 310))
		back_im.save('files/temp/overlayed-'+str(index)+'.png', quality=95)
		overlayedpath.append('files/temp/overlayed-'+str(index)+'.png')

	return overlayedpath


def main_page():
	st.header("Welcome to fashion designing platform inspired by OpenAI's DALL-E")
	st.subheader("You can prompt AI to generate a graphic image, which you can put on a piece of clothing")
	st.subheader("Describe graphic image you want on a piece of clothing and click enter:")
	text_placeholder = st.empty()
	placeholder = st.empty()
	
	prompt = text_placeholder.text_input(label="Example: Cosmic dust", key="p1_text_input")
	if prompt:
		placeholder.success("It will take some time to generate the images, hang tight!")
		st.session_state.prompt = prompt
		try:
			imgs = getdalleimg(prompt)
		except:
			placeholder.subheader("Sometimes the OpenAI server is overloaded. If you see the message about that, please try again.")

		st.session_state.images = imgs
		btn = placeholder.button("Click to see the images", key="main_generate", on_click=nextpage, disabled=False)
		if btn:
			text_placeholder.empty()
			placeholder.empty()
			
		
		
def p1(text):
	placeholder_1 = st.empty()
	placeholder_1.header("Double-click on your favorite image to continue:")
	imgarray = st.session_state.images
	clicked = clickable_images(
		[
			imgarray[0],
			imgarray[1],
			imgarray[2], 
			imgarray[3], 
			imgarray[4],
			imgarray[5]
		],
		titles=[f"Image #{str(i)}" for i in range(6)],
		div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
		img_style={"margin": "10px", "height": "450px"},
	)
	st.session_state.index = clicked
	saveimg(imgarray[clicked])

	if clicked>-1:
		placeholder_1.empty()
		nextpage()
	
	placeholder_2=st.empty()
	placeholder_2.button("go back to the prompt", key="p1_1_back", on_click=backpage, disabled=False)

def p2(text):
	placeholder_3=st.empty()
	placeholder_3.header("Double-click to choose piece of clothing you want your grapics on:")

	clothing=["files/Tshirt.png", "files/crewneck.png", "files/hoodie.png"]
	images = []
	for file in clothing:
		with open(file, "rb") as image:
			encoded = base64.b64encode(image.read()).decode()
			images.append(f"data:image/jpeg;base64,{encoded}")

	clicked_clothing = clickable_images(
		images,
		titles=[f"Image #{str(i)}" for i in range(3)],
		div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
		img_style={"margin": "10px", "height": "450px"},
	)

	if clicked_clothing>-1:
		placeholder_3.empty()
		nextpage()
	st.session_state.clothing=clothing[clicked_clothing]
	placeholder_4 = st.empty()
	placeholder_4.button("go back to image options", key="p2_back", on_click=backpage, disabled=False)


def p3(text):
	placeholder_5=st.empty()
	placeholder_5.header("Double-click on your favorite colored clothing:")
	
	coloredclothes=coloredpath(st.session_state.clothing)
	editedclothes=editimage(coloredclothes)

	images = []
	for file in editedclothes:
		with open(file, "rb") as image:
			encoded = base64.b64encode(image.read()).decode()
			images.append(f"data:image/jpeg;base64,{encoded}")

	clicked_final = clickable_images(
		images,
		titles=[f"Image #{str(i)}" for i in range(10)],
		div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
		img_style={"margin": "10px", "height": "500px"},
	)

	if clicked_final>-1:
		placeholder_5.empty()
		nextpage()
	st.session_state.final = editedclothes[clicked_final]

	placeholder_6=st.empty()
	placeholder_6.button("go back to clothing options", key="p3_back", on_click=backpage, disabled=False)

def p4(text):
	st.header("Save your design")
	image=Image.open(st.session_state.final)
	st.image(image)
	st.download_button(label="Click to download the final design", data="png", file_name=st.session_state.final)

	placeholder_8= st.empty()
	col1, col2=placeholder_8.columns(2)
	col1.button("go back to color options", key="p4_back", on_click=backpage, disabled=False)
	col2.button("make a new design", key="p4_main", on_click=restart, disabled=False)

def main():
	st.set_page_config(layout="wide")
	if st.session_state.main == 0:
		main_page()
	elif st.session_state.main == 1:
		p1(st.session_state.prompt)
	elif st.session_state.main == 2:
		p2(st.session_state.prompt)
	elif st.session_state.main == 3 :
		p3(st.session_state.prompt)
	elif st.session_state.main == 4:
		p4(st.session_state.prompt)


if __name__ == "__main__":
	main()






	




