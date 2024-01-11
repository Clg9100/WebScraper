import csv
import os


"""
Function: createCsv
Args: theData(list of lists )
Usage theData - the list of products

Function is used to write to a csv file named 'fullData.csv' the data scraped from all the user search queries. IF
information was found for the query

Gripes: Might want to find a way to allow user to specify what they want the name of their csv file to be, should be easy enough
The way it is now is merely so it's easy to delete the file if it already exists on subsequent runs as I didn't want to bloat
User directory with csv files (Although, this could just the same be done with them having the ability to name it themselves,
them being able to name it themselves actually further allows for flexibility to have multiple data points if for example they
run it on various different days - while still not bloating if they opt to use a filename they've already used before)
"""
def createCSV(theData):
    with open('fullData.csv', 'a',newline='') as file:
        write = csv.writer(file)
        write.writerows(theData)
        file.close() #Close resource



"""
Function: createBudgetCSV
Args: itemBudgets(dictionary of String to int mapping)
Usage itemBudgets - dictionary of budgets imposed on the search items both supplied by the user.

Function is used to write to a csv file named 'budgetData.csv' which will only contain items checked against the full data list
that fall within (rather under) the budget supplied by the user for each individual item

Gripes: Similar gripes in terms of allowing user to name the budget csv file.
"""
def createBudgetCSV(itemBudgets):
    #budgetData = []
    createBudgetCSVHeader()  # Create csv file for budgeted items with just the header
    #Reading full data, appending to bugetData (Because it already has the header, append to it)
    with open('fullData.csv', mode='r') as infile, open ('budgetData.csv', mode='a', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        next(reader, None)  # skip the headers
        for lines in reader:
            #Testing purpose print
            #print(lines)

            price = lines[2]
            # Testing purpose prints, a bit important - don't want to remove them just yet.
            # print("Search item being checked: "+lines[0])
            # print("Price of said item: "+str(price[1:]))
            # print("Budget being checked: "+str(float(itemBudgets.get(lines[0]))))

            # If the price of the search term item being looked at is LESS than the budget,
            # it's good to add it do our budgeted items list of data
            # Otherwise don't add it, it goes over user's budget on its own
            if(float(price[1:]) < float(itemBudgets.get(lines[0]))):
                writer.writerow(lines)
                #Testing purpose print to make sure we're getting correct data
                #budgetData.append(lines)

    #Testing purpose print
    #for data in range(len(budgetData)):
        #print(budgetData[data])
        infile.close() #Close resource
        outfile.close() #Close resource

"""
Function: createCSVHeader

Function is used to create the initial fullData.csv file with the header needed for column distinction
Will either replace the file if one of the same name is found, or make a new one for the first time
"""
def createCSVHeader():

    if os.path.exists("fullData.csv"):
        os.remove("fullData.csv")
        print("Old CSV file deleted")
        print("Writing new csv file: fullData.csv")
        fields = ['Search Term', 'Product Name', 'Price', 'Link']  # Header row for product data listings
        with open('fullData.csv', 'w',newline='') as file:  # 'w' mode is for writing to a file
            write = csv.writer(file)
            write.writerow(fields)
            file.close()#Close resource
    else:
        print("Writing new csv file: fullData.csv")
        fields = ['Search Term', 'Product Name', 'Price', 'Link']  # Header row for product data listings
        with open('fullData.csv', 'w') as file:  # 'w' mode is for writing to a file
            write = csv.writer(file)
            write.writerow(fields)
            file.close()#Close resource



"""
Function: createBudgetCSVHeader

Function is used to create the initial budgetData.csv file with the header needed for column distinction
Will either replace the file if one of the same name is found, or make a new one for the first time
"""
def createBudgetCSVHeader():

    if os.path.exists("budgetData.csv"):
        os.remove("budgetData.csv")
        print("Old CSV file deleted")
        print("Writing new csv file: budgetData.csv")
        fields = ['Search Term', 'Product Name', 'Price', 'Link']  # Header row for product data listings
        with open('budgetData.csv', 'w',newline='') as outfile:  # 'w' mode is for writing to a file
            write = csv.writer(outfile)
            write.writerow(fields)
            outfile.close()#Close resource
    else:
        print("Writing new csv file: budgetData.csv")
        fields = ['Search Term', 'Product Name', 'Price', 'Link']  # Header row for product data listings
        with open('budgetData.csv', 'w') as outfile:  # 'w' mode is for writing to a file
            write = csv.writer(outfile)
            write.writerow(fields)
            outfile.close()#Close resource