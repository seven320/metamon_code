file_name = "./data2.txt"

try:
    file = open(file_name, 'w')
    file.write("This is new data")
except Exception as e:
    print(e)
finally:
    file.close()