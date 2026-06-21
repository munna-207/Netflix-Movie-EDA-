#------------------------LIBRARIES---------------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------ANALAZING THE DATA-------------------------------------------------------------------------------------------------------------------------

#This function is used to load a CSV file into a Pandas DataFrame.
df = pd.read_csv('mymoviedb.csv', lineterminator = '\n')

# This function Shows the first 5 rows of the DataFrame by default. 
# print(df.head())

# This function wGives a summary of the DataFrame.
# print(df.info())

# This function check for duplicate records
# print(df.duplicated().sum())

# This function Gives statistical information about numerical columns
# print(df.describe())

#-------------------------SUMMARY-----------------------------------------------------------------------------------------------------------------------------------------
# We have a dataframe consisting of 9827 rows and 9 columns.
# Our dataset looks a bit tidy with no NaNs nor duplicated values.
# Realease_Data column needs to be casted into date time and to extract only the year value.
# Overview, Original_Language and Poster-Url would'nt be so useful during analysis, so we'll drop them.
# There is noticable ouliers in Popularity column
# Vote_Average better be categories for poper analysis.
# Genre column has commna saperated values and white spaces that needs to be handled and casted into category. Explortation Summary
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Changing the Data type of Realse Date
df['Release_Date'] = pd.to_datetime(df['Release_Date'])

#We only need year so we removeing the date and month from the date.
df['Release_Date'] = df['Release_Date'].dt.year

#Now we will romve the Columns which we don't need
cols =['Overview', 'Original_Language', 'Poster_Url']

df.drop(cols, axis = 1, inplace= True)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# We would cut the Vote_Average values and make 4 categories: popular average below_avg not_popular to descibe it more using catigorixe_col() function provided above
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def catigorize_col(df, col, labels):

    edges = [df[col].describe()['min'],
             df[col].describe()['25%'],
             df[col].describe()['50%'],
             df[col].describe()['75%'],
             df[col].describe()['max']]
    
    #In Pandas, cut() is used to convert continuous numerical data into categories (bins)
    df[col] = pd.cut(df[col], edges, labels = labels, duplicates = 'drop')
    return df

labels = ['not_popular', 'below_avg', 'average', 'popular']

catigorize_col(df, 'Vote_Average', labels)
df['Vote_Average'].unique()

# print(df.head())
# print(df['Vote_Average'].value_counts())
df.dropna(inplace = True)

# print(df.isna().sum())

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# We'd split genresinto a list and then explode our dataframe to have only one genre per row for each movie
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
df['Genre'] = df['Genre'].str.split(', ')

df = df.explode('Genre').reset_index(drop = True)
# print(df.head())

# casting column into category

df['Genre'] = df['Genre'].astype('category')
# print(df['Genre'].dtypes)
# print(df.head())
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------DATA VISUALIZATION---------------------------------------------------------------------------------------------
sns.set_style('whitegrid')

#Q1. WHAT IS THE MOST FREQUENT GENRE OF MOVIES RELEASED ON NETFLIX?
print(df['Genre'].describe())
sns.catplot(y = 'Genre', data = df, kind = 'count',
            order = df['Genre'].value_counts().index,
            color = '#427f55')
plt.title("Genre column distribution")
plt.show()

#Q2. Which has highest votes in vote avg column?
sns.catplot(y = 'Vote_Average', data = df, kind = 'count',
            order = df['Vote_Average'].value_counts().index,
            color = '#427f55')
plt.title("Votes distribution")
plt.show()

#Q3. What movie got the highest popularity? What's its genre?
print(df[df['Popularity'] == df['Popularity'].max()])

#Q4. What movie got the lowest popularity? What's its genre?
print(df[df['Popularity'] == df['Popularity'].min()])

#Q5. Which year has the most filmmed movies
df["Release_Date"].hist()
plt.title("Release date column distribution")
plt.show()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
