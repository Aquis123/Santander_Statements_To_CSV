
#This file's goal is to read santander statements (.txt) 
#and send them to an excell file. 
import os
import csv

class santander_reader:

    def __init__(self):
        self.filepath_statement = ""
        self.filepath_output = ""

        self.statements = []
        self.monthlyTransfers = []  
        self.rawMonthlyTransfers = []  
        self.totalMonthlyTransfers = []

        self.accountNum = "NoAccount#"
        self.startDate = [0,0,0]
        self.endDate = [0,0,0]

        self.deposit_words = ["PAYROLL","DEPOSIT","REFUND","INVOICE"]
        
        self.statement_num = 0
        


    def get_statement_list(self,filepath_statement):
        '''
        Looks through the filepath and returns the files it sees
        '''
        
        self.statements = os.listdir(filepath_statement)
        self.filepath_statement = filepath_statement
        return self.statements
       


    def get_statement(self, statement_number):
        '''
        Reads a file from the statements it sees 
        
        '''
        
        self.statement_num = statement_number

        #raise error if not a txt file 
        if not ".txt" in self.statements[statement_number]:
            raise Exception (f"Unexpected filetype in {self.filepath_statement}. \n Expected '.txt', got {self.statements[statement_number]}")
        
        print("---------")
        print("Collecting file: " + self.statements[statement_number])
        file_statement = open(self.filepath_statement + "/" + self.statements[statement_number])
        text = file_statement.readlines()
        
        return text



    def get_rawMonthlyTransfers(self):
        '''returns the section of the statement file that was origionaly read'''
        return self.rawMonthlyTransfers



    def get_monthlyTransfers(self):
        '''returns the filtered statement'''
        return self.monthlyTransfers



    def read_statement(self,text):
        '''takes the raw text from Get_Statement and reads the raw data'''
        
        def int_check(line):
            '''Returns true if the string line contains intigers
            ''' 
            for i in range(0,9):
                if str(i) in line:
                    return True
        
        def date_check(line):
                '''startDate & endDate are strings of dates. ie: 10/17/2020. In month/day/year format
                line is the string that we looking for the dates in.
                '''

                if "-" in line:
                    return True

        info_start = 0
        info_end = 0

        self.rawMonthlyTransfers = []

        print("Reading file")
        #rawMonthlyTransfers = []
        #input File Sanatation

        for j in range(len(text)):
            text[j] = text[j].replace("\n","")

        #looks for date information
        for j in range(len(text)):
            if "Statement Period" in text[j]:
                #parces date & sanitises format
                date_Line = text[j].split(" ")
                self.startDate = date_Line[2].split("/")
                self.endDate = date_Line[4].split("/")
                break 
                
                
        #looks for Account number
        for j in range(len(text)):
            if "Account #" in text[j]:
                self.accountNum = text[j].split(" ")[2]

        #looks for where to start and end data collection.
        for j in range(len(text)):
            if "Beginning Balance" in text[j]:
                info_start = j + 1
                break

        for j in range(len(text)):
            if "Ending Balance" in text[j]:
                info_end = j
                break

        #filter & save data
        for j in range(info_start,info_end):
            #check to see if there is an intiger then an expected date
            if int_check(text[j]) and date_check(text[j]):
                self.rawMonthlyTransfers.append(text[j].split("  "))
    

    
    def parce_statement(self):
        '''Takes the Raw Monthly Transfers, Removes empty Datapoints, Decides if Data is neigitve or positive'''
        #declaration
        dataRow = []
        self.monthlyTransfers = []
        
        currentYear = int(self.startDate[2])
        start_month = int(self.startDate[0])
        

        #detects where in list data is stored & saves to monthly transfers
        for j in range(len(self.rawMonthlyTransfers)):
            
            dataRow = []
            for k in range(len(self.rawMonthlyTransfers[j])):
                
                #remove empty spaces from raw data
                if self.rawMonthlyTransfers[j][k] != '':
                   dataRow.append(self.rawMonthlyTransfers[j][k].replace("$","")) 

            #write to monthly transfers if correct length
            if len(dataRow) == 4:
                self.monthlyTransfers.append(dataRow) 

        
        #for every row in monthly transfers, negate entry if needed & add year to date.
        for j in range(len(self.monthlyTransfers)):
            negate = True

            #detects if entry is negative & corrects if it is
            for k in range(len(self.deposit_words)):
                if (self.deposit_words[k] in self.monthlyTransfers[j][1]):
                    negate = False

            if negate:
                self.monthlyTransfers[j][2] = "-" + self.monthlyTransfers[j][2].replace(" ","")
            else:
                self.monthlyTransfers[j][2] = self.monthlyTransfers[j][2].replace(" ","")


            #adds the current year to the date:
            if (start_month == 12) and int(self.monthlyTransfers[j][0].split("-")[0]) == 1:
                #december - january edge case
                self.monthlyTransfers[j][0] = self.monthlyTransfers[j][0] + "-" + str(currentYear + 1) 
            else:
                self.monthlyTransfers[j][0] = self.monthlyTransfers[j][0] + "-" + str(currentYear)

            
    
            #saves to total Transfers
            self.totalMonthlyTransfers.append(self.monthlyTransfers[j])


    def make_month_xfer(self, filepath_output):
        '''makes & writes to a monthly transfer csv file'''
        
        self.filepath_output = filepath_output

        #grab readable date information
        year = "20" + self.startDate[2] #grabs folder year 
        start = "".join(self.monthlyTransfers[0][0].split("-")[:2]) #grabs starting month & day 
        end = "".join(self.monthlyTransfers[(len(self.monthlyTransfers)-1)][0].split("-")[:2]) #grabs ending month & day 

        #construct filename
        fileName = filepath_output + "\\" +"MthXfer_#" + self.accountNum + "_" + year + "_" + start + "_to_" + end + ".csv"
        
        #write to file
        with open(fileName, "w", newline='') as file_CSV:
            writer = csv.writer(file_CSV, delimiter=',')
            writer.writerows(self.monthlyTransfers)

        print(f"Contents of: {self.filepath_statement}\{self.statements[self.statement_num]} \nWritten to: {fileName}")
        print("---------")


    def make_total_xfer(self, filepath_output):
        '''makes & writes everything in statements folder to a total xfer file'''
        self.filepath_output = filepath_output
        
        fileName = filepath_output + "\\" +"TotalXfer_#" + self.accountNum + ".csv"
        
        with open(fileName, "w", newline='') as file_CSV:
            writer = csv.writer(file_CSV, delimiter=',')
            writer.writerows(self.totalMonthlyTransfers)

        print(f"Contents of: {self.filepath_statement}\... \nWritten to: {fileName}")
        print("---------")



    def parce_folder(self, input_path, output_path):
        ''' Reads and parces over the whole input folder and writes to output folder'''
        statement_list = self.get_statement_list(input_path)
        for i in range(0,len(statement_list)):
            self.read_statement(self.get_statement(i))
            self.parce_statement()
            self.make_month_xfer(output_path)

        #self.make_total_xfer(output_path)



if __name__ == "__main__":
    sant = santander_reader()
    sant.parce_folder("Statements","MonthlyTransfers")
    print("All Done!")



