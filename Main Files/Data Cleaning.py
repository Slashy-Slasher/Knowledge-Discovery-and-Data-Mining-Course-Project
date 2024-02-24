# Alexander Mortillite, Chairs Metz, Christian McGee
import pandas as pd


# Cleans data question by question for a specific state rather than all with the same average
def questionBasedCleaner(state_data):
    column_name = "QuestionID"
    current_row = 0
    for i in state_data[column_name]:
        if not pd.notna(state_data.iloc[current_row, state_data.columns.get_loc("Data_Value")]):
            state_data.iloc[current_row, state_data.columns.get_loc("Data_Value")] = surveyQuestionAverager(state_data,
                                                                                                            i)
        current_row += 1
    return state_data


# Isolates all rows from a specific state into its own category
def stateSeparator(state_data, tag):
    column_name = "LocationAbbr"
    selected_rows = pd.DataFrame(columns=state_data.columns)  # Create an empty DataFrame with the same columns

    if column_name in state_data.columns:
        for index, row in state_data.iterrows():
            if row[column_name] == tag:
                selected_rows = pd.concat([selected_rows, pd.DataFrame([row])])
    return selected_rows


# Averages all the Data_Values per the given question
def surveyQuestionAverager(data, question):
    column_name = "QuestionID"
    cumulative = 0
    totalQuestions = 0
    current_row = 0
    if column_name in data.columns:
        for index, row in data.iterrows():
            if row[column_name] == question and pd.notna(data.iloc[current_row, data.columns.get_loc("Data_Value")]):
                cumulative += data.iloc[current_row, data.columns.get_loc("Data_Value")]
                totalQuestions += 1
            current_row += 1
    if totalQuestions != 0:
        # print(f"{question} {cumulative/totalQuestions}")
        return cumulative / totalQuestions
    else:
        print("Null Question")
    return 0


# Runs a List comparison script which returns a list of differences
def stateComparator(state1, state2):
    differencesList = []
    print(f"Difference between {state1} and {state2}")
    for i in range(len(state1)):
        differencesList.append(state1[i] - state2[i])
        print(f"{i}: {state1[i] - state2[i]}")
    return differencesList


# Runs an algorithm that collects all the question data for the .csv key
def generateQuestionList(data, question):
    column_name = "QuestionID"
    current_row = 0
    if column_name in data.columns:
        for index, row in data.iterrows():
            if row[column_name] == question:
                return data.iloc[current_row, data.columns.get_loc("Question")]
            current_row += 1
    return ""


# Combines all lists into a new .csv which is more readable humans
def toCombinedToCSV(QuestionIDList, TopicQuestionList, state1, state2, differencesList):
    data = {
        'Question': QuestionIDList,
        'Topic': TopicQuestionList,
        f'state1': state1,
        f'state2': state2,
        'Difference': differencesList
    }
    newDf = pd.DataFrame(data)
    newDf.to_csv('StateComparison.csv', index=False)
    print()


# Declarations and Initialization
file = "OG Data.csv"
NYFile = "NewYork.csv"
MSFile = "Mississippi.csv"
pd.set_option('display.max_columns', None)
data_file = pd.read_csv(file)
dataNYFile = pd.read_csv(NYFile)
dataMSFile = pd.read_csv(MSFile)

questionID_list = [f'Q{i:02d}' for i in range(1, 47)]
nyList = []
msList = []
question_list = []
differenceList = []

# Separates the original dataset into two separate datasets
result_df = stateSeparator(data_file, 'NY')
result_df.to_csv('NewYork.csv', index=False)
print("NY discriminated")
result_df = stateSeparator(data_file, 'MS')
result_df.to_csv('Mississippi.csv', index=False)
print("MS discriminated")

# Runs both of the separated Datasets through our improved cleaner
df = questionBasedCleaner(dataNYFile)
df.to_csv('cleanNewYork.csv', index=False)
print("NY Cleaned")
df = questionBasedCleaner(dataMSFile)
df.to_csv('cleanMississippi.csv', index=False)
print("MS Cleaned")

# Takes the average for each question in both states and generates the question list, then lastly calculates the diff
print("Listing Started")
for x in questionID_list:
    nyList.append(surveyQuestionAverager(dataNYFile, x))
    msList.append(surveyQuestionAverager(dataMSFile, x))
    question_list.append(generateQuestionList(dataNYFile, x))
differenceList = stateComparator(nyList, msList)
print("Listing Finished")

# Combines all generated values into one .csv file
toCombinedToCSV(questionID_list, question_list, nyList, msList, differenceList)
print("All Algorithms Completed")
