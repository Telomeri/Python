from concurrent.futures import thread
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from PIL import Image
from saliency_models import gbvs
import cv2

'''colors = {"background": "#EFEDEA",
    "header": "#90A3A1",
    "button": "#DFF0EE",
    "content": "#D8D9F0",
    "holder": "#9090A3"}'''

#colors = ["#EFEDEA","#90A3A1","#DFF0EE","#D8D9F0","#9090A3"]
#site_url = 'http://localhost:8080/'
#https://www.free-css.com/free-css-templates/page271/autowash
def locate_element(site_url,id):
    #s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome("./chromedriver.exe")
    driver.maximize_window()
    print("The url is  "+  site_url)
    #driver.implicitly_wait(4)
    #driver.set_page_load_timeout(2)
    driver.get(site_url) 
    element = driver.find_element(By.ID, id)
    location = element.location
    size = element.size
    #driver.implicitly_wait(4)
    sleep(0.5)
    driver.save_screenshot("./images/website.png")

    #x = location['x']
    #y = location['y']
    #w = size['width']
    #h = size['height']
    #width = x + w
    #height = y + h
    #im = Image.open('./images/website.png')
    #im = im.crop((int(x), int(y), int(width), int(height)))
    #im.save("element_{}_out.png".format(x))
    return (location,size)

def calculate_area(salience_map,coordinates_top,coordinates_bot):
    salience = []
    for y in range(coordinates_top[1],coordinates_bot[1],2):
        for x in range(coordinates_top[0],coordinates_bot[0],2):
            salience.append(salience_map[y][x])
    return sum(salience)/len(salience)

def get_saliency(site_url, elements,best_saliency,palette_name):
    i = "website"
    priority = []
    for key, value in elements:
        if value == "True":
            priority.append(key)
    #imname = "./images/{}.jpg".format(i)
    #img = cv2.imread(imname)
    #saliency_map_ikn = ittikochneibur.compute_saliency(img)
    #oname = "./outputs/{}_out.jpg".format(i)
    #cv2.imwrite(oname, saliency_map_ikn)
    salience = 0
    for element in priority:
        location, size = locate_element(site_url,element)
        coordinates_top=[location["x"],location["y"]]
        coordinates_bot=[location["x"]+size["width"],location["y"]+size["height"]]
        #testSalience = CalculateArea(saliency_map_ikn,coordinates_top,coordinates_bot)
        #loop trough the colors
        #print("Calculating salience for the color " + color)
        #get the original image for change area
        imname = "./images/{}.png".format(i)
        #ChangeArea(imname,color,coordinates_top,coordinates_bot)
        #get the edited image for salience calculations
        #imname = "./images/{}.png".format("1_edit")
        img = cv2.imread(imname)
        #calculate gbvs
        saliency_map_gbvs = gbvs.compute_saliency(img)
        #saliency_map_ikn = ittikochneibur.compute_saliency(img)
        #calculate gbvs average on a certain area
        salience += calculate_area(saliency_map_gbvs,coordinates_top,coordinates_bot)
    #normalize saliency
    salience = salience / len(priority)
    #if the found saliance is better, use that
    #save the latest outcome, since it was fun to watch happen in real time
    if salience > 0:
        oname = "./outputs/{}_out.png".format(i)
        cv2.imwrite(oname, saliency_map_gbvs)
        if salience > best_saliency:
            cv2.imwrite("./outputs/{}_best_out.png".format(palette_name), saliency_map_gbvs)
            img_src = cv2.imread(imname)
            possName = "./images/{}_best.png".format(palette_name)
            img = cv2.imwrite(possName,img_src)
    return salience

