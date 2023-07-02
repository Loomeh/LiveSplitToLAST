import xml.etree.ElementTree as ET
import os

lssFilePath = input("Input the file path of your .lss file: ")
with open(lssFilePath, 'r') as fp:
    lines = fp.readlines()
width = input("Input the width you want to have for the LAST window: ")
height = input("Input the height you want to have for the LAST window: ")

fileName = os.path.splitext(os.path.basename(lssFilePath))[0] + ".json"
lastDir = os.path.expanduser("~") + "/.last/splits/"

if not os.path.exists(lastDir):
    os.makedirs(lastDir)
    
json = open(lastDir + fileName, "a")

splitsTitle = ""
splitsCategory = ""
game_name = ""
attemptCount = 0
startDelay = ""
name_list = []  # Store the extracted names
names_without_numbers = []
text = ''
has_game_times = False
has_segment_times = False

best_time_list = []

# Get game name, category, attempt count
for line in lines:
    if '<GameName>' in line:
        start_index = line.index('<GameName>') + len('<GameName>')
        end_index = line.index('</GameName>')
        game_name = line[start_index:end_index].strip()

    if '<CategoryName>' in line:
        start_index = line.index('<CategoryName>') + len('<CategoryName>')
        end_index = line.index('</CategoryName>')
        splitsCategory = line[start_index:end_index].strip()
        
    if '<AttemptCount>' in line:
        start_index = line.index('<AttemptCount>') + len('<AttemptCount>')
        end_index = line.index('</AttemptCount>')
        attemptCount = line[start_index:end_index].strip()

    if '<Offset>' in line:
        start_index = line.index('<Offset>') + len('<Offset>')
        end_index = line.index('</Offset>')
        startDelay = line[start_index:end_index].strip()

    if '<Name>' in line and '</Name>' in line:
        start_index = line.index('<Name>') + len('<Name>')
        end_index = line.index('</Name>')
        name = line[start_index:end_index].strip()
        name_list.append(name)
    
    if '<GameTime>' in line:
        has_game_times = True
    
    if '<BestSegmentTime>' in line:
        has_segment_times = True
    
def returnBestGameTime(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    best_game_times = []

    for segment in root.findall(".//Segment"):
        best_game_time_element = segment.find(".//SplitTime/GameTime")
        if best_game_time_element is not None:
            game_time = best_game_time_element.text
            best_game_times.append(game_time)

    return best_game_times

def returnBestSegmentTime(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    best_segment_times = []

    for segment in root.findall(".//Segment"):
        best_segment_time_element = segment.find(".//BestSegmentTime/GameTime")
        if best_segment_time_element is not None:
            segment_time = best_segment_time_element.text
            best_segment_times.append(segment_time)

    return best_segment_times

file_path = lssFilePath
game_times = returnBestGameTime(file_path)
segment_times = returnBestSegmentTime(file_path)

json.write("{\n")
json.write(f"  \"title\": " + "\"" + game_name + ": " + splitsCategory  + "\"" + "," + "\n")
json.write(f"  \"attempt_count\": " + attemptCount + "," + "\n")
json.write(f"  \"start_delay\": " + "\"" + startDelay + "\"" + "," + "\n")
json.write("  \"splits\": [\n")


for name in name_list:
    index = name.find(' ')
    name_without_numbers = name[index+1:]
    names_without_numbers.append(name_without_numbers)


for i in range(len(names_without_numbers)):

    json.write("   {\n")
    json.write(f"    \"title\": " + "\"" + names_without_numbers[i] + "\"")
    if has_game_times == True or has_segment_times == True:
        json.write(f",")
    json.write(f"\n")
    
    if i == (len(names_without_numbers) - 1):
        if has_game_times == True:
            json.write(f"    \"time\": " + "\"" + game_times[i] + "\"" + "," + "\n")
            json.write(f"    \"time\": " + "\"" + game_times[i] + "\"" + "," + "\n")
            json.write(f"    \"best_time\": " + "\"\"" + "," + "\n")
        if has_segment_times == True:
            json.write(f"    \"best_segment\": " + "\"" + segment_times[i] + "\"" + "\n")
        json.write("   }\n")
        json.write("  ],\n")
        json.write(f"  \"width\": " + width + "," + "\n")
        json.write(f"  \"height\": " + height + "\n")
        json.write("}")
    else:
        if has_game_times == True:
            json.write(f"    \"time\": " + "\"" + game_times[i] + "\"" + "," + "\n")
            json.write(f"    \"best_time\": " + "\"\"" + "," + "\n")
        if has_segment_times == True:
            json.write(f"    \"best_segment\": " + "\"" + segment_times[i] + "\"" + "\n")
        json.write("   },\n")
        

    if has_game_times == True:
        print("The current PB time for " + names_without_numbers[i] + " is: " + game_times[i] + " and the best segment time is: " + segment_times[i])

