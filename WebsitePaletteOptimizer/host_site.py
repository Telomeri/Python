from math import comb, sqrt
import subprocess
import time
import itertools
from turtle import color
from PIL import ImageColor
from saliency_estimate import get_saliency
import xml.etree.cElementTree as ET

#Other things to consider. Is the text readable? Should we optimize this to take less time, e.g. assign the lowest brigthness to background, assign the loudest ones to elements?
#colors = ["#EFEDEA","#90A3A1","#DFF0EE","#D8D9F0","#9090A3"]
#site_url = 'http://localhost:8080/'
#elements = ["background","header","button","sidebar","footer"]
#other options Footer and Header
#Possibly buttons

def load_xml():
    palettes=[]
    palette_names=[]
    site_url = 'http://localhost:'
    elements = []
    tree = ET.parse('site_parameters.xml')
    root = tree.getroot()
    root_elements = root.find("elements")
    for element in root_elements:
        elements.append((element.tag,element.attrib["prioritize"]))
    root_colors = root.findall("colors")
    for palette in root_colors:
        colors = []
        palette_names.append((palette.attrib["type"]))
        for color in palette:
            colors.append(color.attrib["code"])
        palettes.append(colors)
    site_url += root.find("site").attrib["port"] + "/"
    return (elements, palettes,palette_names, site_url)

def create_xml():
    #colors = ["#EFEDEA","#90A3A1","#DFF0EE","#D8D9F0","#9090A3"]
    #site_url = 'http://localhost:8080/'
    #elements = ["background","header","button","sidebar","footer"]
    #root = ET.Element("root")
    #root_elements = ET.SubElement(root, "elements")
    #for element in elements:
       # ET.SubElement(root_elements, element, prioritize="False")
   # root_colors = ET.SubElement(root, "colors", type="Relaxing")
    #for color in colors:
     #   ET.SubElement(root_colors, "color",code=color)
    #root_site = ET.SubElement(root, "site", port="8080")
    #tree = ET.ElementTree(root)
    #tree.write("site_parameters.xml")
    pass

#elements_amount = 5
def start_iteration(site_url, elements,best_sal,palette_name):
    pro = subprocess.Popen(['node', 'server.js'])
    saliencyVal = get_saliency(site_url,elements,best_sal,palette_name)
    pro.kill()
    return saliencyVal

def orderByBrightness(colors):
    orderColors = []
    for color in colors:
        orderColors.append(ImageColor.getcolor(color, "RGB")) 
    orderColors.sort()
    colors = []
    for color in orderColors:
        colors.append(("#"+'%02x%02x%02x' % color).upper())
    return colors
        
    #takes away 7 minutes, or 3,5 minutes per element on each palette
def findPermutations(colors, elements):
    permutations = list(itertools.permutations(colors, len(elements)))
    approvedPerm = []
    priority = []
    keys = []
    backgroundExists = False
    for key, value in elements:
        priority.append(value)
        keys.append(key)
        if key.lower() == "background":
            backgroundExists = True
    for perm in permutations:
        for k in range(len(elements)):
            #remove this prio
            #if (colors[0] == perm[k] or colors[-1] == perm[k]) and priority[k] == "True":
               # approvedPerm.append(perm)
               # break
            if backgroundExists:
                if keys[k].lower() == "background" and (colors[-1] == perm[k] or colors[0] == perm[k]):
                    approvedPerm.append(perm)
                    break
            else:
                if (colors[0] == perm[k] or colors[-1] == perm[k]) and priority[k] == "True":
                     approvedPerm.append(perm)
                     break
                    
    return approvedPerm

def try_colors():
    (elements, palettes,palette_names, site_url) = load_xml()
    start = time.time()
    root = ET.Element("root")
    #colors?
    ET.SubElement(root, "InitialInformation", element=str(elements))
    root_results = ET.SubElement(root, "Results")
    k=0
    for colors in palettes:
        colors_tried = []
        best_palette = ["", 0]
        colors = orderByBrightness(colors)
        color_combinations = findPermutations(colors, elements)
        print(len(color_combinations))
        root_combinations = ET.SubElement(root, "Combinations",name=str(palette_names[k]),palette=str(colors))
        #f = open("logCombination.txt", "w")
        i = 1
        for combination in color_combinations:
            edit_css(combination, elements)
            saliencyVal = start_iteration(site_url, elements,best_palette[1],palette_names[k])
            #f.write(str(combination) + "  " + str(saliencyVal))
            ET.SubElement(root_combinations,"Combination"+str(i), combination=str(combination), saliencyVal=str(saliencyVal))
            print("Combination tried: " + str(combination) + " with a value of " + str(saliencyVal))
            colors_tried.append((combination,saliencyVal))
            if best_palette[1] < saliencyVal:
                best_palette[0] = combination
                best_palette[1] = saliencyVal
                print("New best palette found with a value of " + str(saliencyVal))
            i+=1
        print("Best option for "+str(palette_names[k])+" is " + str(best_palette[0]) + " with value " + str(best_palette[1]))
        ET.SubElement(root_results, "BestPalette"+str(palette_names[k]), combination=str(best_palette[0]), saliencyVal=str(best_palette[1]))
        k+=1
    end = time.time()
    print("it took:" + str(end - start))
    ET.SubElement(root_results, "TimeTaken", time=str(end - start))
    ET.indent(root)
    tree = ET.ElementTree(root)
    tree.write("site_results.xml")
    edit_css(best_palette[0], elements)
    print("Process finished")
    #pro = subprocess.Popen(['node', 'server.js'])

def edit_css(combination,elements):
    file = open("css/style.css","r") 
    data = file.readlines()
    #print(data)
    i = 0
    for key,value in elements:
        data[i+2] = "--{}: {}; \n".format(key, combination[i])
        i+=1
    file.close()
    with open("css/style.css", "w") as file:
        file.writelines(data)

    '''/*COLORS*/
    :root {
    --background: #EFEDEA;
    --header: #90A3A1; 
    --button: #DFF0EE;
    --content: #D8D9F0;
    --holder: #9090A3;
    }
    /*ENDCOLORS*/'''
    #2 to 6


try_colors()