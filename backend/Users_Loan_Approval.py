import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
from backend.settings import CSV_ROOT
class SVM:
    def __init__(self,file_name,model_name):
        self.model_name = model_name
        self.file_name = file_name
        self.df = pd.read_csv(CSV_ROOT)
    def Fill_Up_Empty_Values(self):
        self.df["Number of years of employment"].fillna(
            self.df["Number of years of employment"].mode()[0], inplace=True)
        self.df["Purpose of taking loan"].fillna(
            self.df["Purpose of taking loan"].mode()[0], inplace=True)
        self.df["1=defaulted"].fillna(self.df["1=defaulted"].mode()[0], inplace=True)
    def Train_Model(self):  # trainig model
        self.Fill_Up_Empty_Values()
        
        for feature in self.df:
            le = LabelEncoder()
            if self.df[feature].dtype == "object":
                self.df[feature] = le.fit_transform(self.df[feature])
        x = self.df.drop(["Loan Defaulted or not","Unnamed: 0","1=defaulted"], axis=1)
        print(x)
        y = self.df["Loan Defaulted or not"]
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=2023)
        knn = RandomForestClassifier()
        knn.fit(x_train, y_train)
        pickle.dump(knn, open(self.model_name, 'wb'))

class Predicting_Loan:
    def __init__(self, file_name, Users_Input):
        self.file_name = file_name  # making file_name a class variable
        self.Users_Input = Users_Input  # making users_input as a class variable
        # making the model_name a class variable
        self.model_name = 'Load_Approval_Model.sav'
        self.test_list = []  # making an empty list for future use whose name is test_lsit
        self.test_dict = {}  # making an empty dictionary for future use whose name is test_dict
    def Decode_User_Input(self):
        df = pd.read_csv(CSV_ROOT)  # reading the csv file
        for col in df:  # running a for loop on df which gives all the column names
            le = LabelEncoder()  # deining a label encoder
            if df[col].dtype == "object":  # if the column is of type object i.e string
                # change the type object to an int type
                df[col] = le.fit_transform(df[col])
                # append different types of features available in that respective column into an empty list called test_list
                self.test_list.append(
                    list(le.inverse_transform([i for i in set(df[col])])))
        
        for i in self.test_list:  # running a for loop on test_list
            count = 0  # init count=0
            for j in i:  # since test_list is a nested list running for loop on the innermost list
                # replacing the values of the nested lists with integers
                self.test_dict[j] = count
                count = count + 1  # increasing count by 1
       
        for i in range(len(self.Users_Input)):
          
            if self.Users_Input[i] in self.test_dict.keys():
                self.Users_Input[i] = self.test_dict[self.Users_Input[i]]
            
            elif type(self.Users_Input[i]) is str:
                self.Users_Input[i] = int(self.Users_Input[i])
     
    def Predict_Result(self):
        self.Decode_User_Input()
        model = pickle.load(open(self.model_name, 'rb'))
        predictions = model.predict(np.array([self.Users_Input]))
        return predictions

# dont forget to train your model before you use this
# model = SVM(r"C:\Users\Pradeep Kumar\Desktop\enosium project\backend\backend\Track_1.csv","Load_Approval_Model.sav")
# model.Train_Model()



# ['2', 'all loans at this bank paid back duly', 'Education Loan', '2', 'co-applicant', 'between 1 and 4 years', 'female and divorced/seperated/married', '2', '3', 'between 0 and 200', 'between 100 and 500', '2', 'bank', 'No', 'No', '2', 'No property', 'management/ self-employed/highly qualified employee/ officer', 'for free', '2']

# [1, 'critical account/other loans existing (not at this bank)','New Car Purchase', 1028, 'none', 'between 1 and 4 years','female and divorced/seperated/married', 2, 36,'no current account', 'less than 100', 4, 'none', 'Yes', 'No', 18,'Real Estate', 'skilled employee / official', 'own', 3]

# {'0': '1', '1': 'all loans at this bank paid back duly', '2': 'Education Loan', '3': '2', '4': 'co-applicant', '5': 'between 1 and 4 years', '6': 'female and divorced/seperated/married', '7': '1', '8': '1', '9': 'between 0 and 200', '10': 'between 100 and 500', '11': '1', '12': 'bank', '13': 'No', '14': 'No', '15': '1', '16': 'No property', '17': 'management/ self-employed/highly qualified employee/ officer','18': 'for free', '19': '3'}