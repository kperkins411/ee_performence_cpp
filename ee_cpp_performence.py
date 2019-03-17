import os
import pandas as pd

def getMergedDataframe(columns_to_delete = None,useHeader = None, *,filelist, dir ):
    '''
    generates a raw list of all students and their associated info, students who fail will be listed twice

    :param filelist: a list of the files containg student info
    :param dir:     directory where these files are
    :param columns_to_delete: extraneous stuff to dump
    :return: dataframe, containing all students and their majors
    '''
    all = None
    for fle in filelist:
        if useHeader==True:
            people = pd.read_csv(os.path.join(dir, fle))
        else:
            people = pd.read_csv(os.path.join(dir, fle), header = None)

        # lets add a column and insert the name of the file this came from
        people[people.shape[1]] = fle

        #get rid of rubbish columns
        if columns_to_delete is not None:
            people.drop(people.columns[columns_to_delete], axis=1, inplace=True)

        #build the dataframe
        all = people if all is None else pd.concat([all,people])

    return all

def show(prompt, data):
    print("*"*75)
    print(prompt)
    print(data.to_string())

DATA_MAJORS_DIR = "/home/keith/Desktop/ee_performence_cpp/data/majors"
DATA_GRADES_DIR = "/home/keith/Desktop/ee_performence_cpp/data/grades"
SAVE_FILE='327_grades.csv'

#get the list of files containing the people and the grades
grades = os.listdir(DATA_GRADES_DIR)
majors = os.listdir(DATA_MAJORS_DIR)

#build the dataframe
allmajors = getMergedDataframe(filelist= majors, dir = DATA_MAJORS_DIR,columns_to_delete =  [0,3,4,5,6,8,9,10] )
allmajors.rename(columns={1:"Name", 2:"Username", 7:"Major", 11:"Term"}, inplace=True)

allgrades = getMergedDataframe(filelist= grades, dir = DATA_GRADES_DIR, useHeader = True )
allgrades.rename(columns={7:"Term"}, inplace=True)

#sort by section and major
allmajors.sort_values(by=["Term","Major"], inplace=True)

#number of unique courses
u_courses = allmajors.Term.unique()
print("For the following courses (18_*_fall courses are not finished)")
for course in u_courses:
    print(course)

#unique users
u_users = allmajors.Username.unique()

prompt = "These are the people who failed,their majors and when they retook"
fail_people = allmajors[allmajors.Username.duplicated(keep=False)]
show(prompt, fail_people)

prompt = "Just the names and majors"
fail_people_unique = fail_people.drop_duplicates(subset=['Username'])
show(prompt, fail_people_unique)

#merge dataframes
merged = pd.merge(allgrades, allmajors, on=["Username","Term"], how="left")

#drop the extra name field
merged.drop(['Name'], axis=1, inplace=True)

#sort by major
merged.sort_values(by=["Term","Major"], inplace=True)

#extract all majors
majors = merged.Major.unique()

#save for further analysis
merged.to_csv(SAVE_FILE, sep=',')

print("*" * 75)
print("General Stats by major")
for major in majors:
    print("For major=" + major)
    data = merged.loc[merged['Major']==major]
    print("     Total students " + str(data.shape[0]))
    print("     The mean grade is " + str(data['class_grade'].mean()))
    print("     The proj_avg is " + str(data['proj_avg'].mean()))
    print("     The mean test1 is " + str(data['test1'].mean()))

pass



