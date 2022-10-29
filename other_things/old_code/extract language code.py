
# script to read from a json all language code and prepare is as a dictionary

file = open('codici.txt', 'r', encoding='utf-8')

my_dict = dict()

# unify everything as a single strin
my_string = ''
for f in file:
    my_string += f


for s in my_string.split("}"):  # split to divide all sections

    t = s.split(" ")  

    if len(t) < 2:  # end of document
        break
    

    key = t[2][:2]  # take language code witouth dirty things
    value = t[8].split(",")[0]  # tanke language withouth dirty things
    
    # if language code has only 2 carather and value is a string, the language, add to dictionary
    if len(key) == 2 and str(type(value)) == "<class 'str'>":
        my_dict[key] = value.split("'")[1]  # leave the ' from the string



# write dictionary on a txt file
new_file = open("language_code.txt","w", encoding = "UTF-8")

for k in my_dict.keys():
    new_file.write("{}:{}\n".format(k, my_dict[k]))

