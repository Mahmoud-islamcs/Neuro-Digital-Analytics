CREATE TABLE Dim_Users (
    UserKey INT PRIMARY KEY,
    Username VARCHAR(50),
    Age INT,
    Age_Group VARCHAR(20),
    Region VARCHAR(50),
    Device_Type VARCHAR(20),
    Is_Smoker BIT,
    Base_Focus_Level INT
);

CREATE TABLE Dim_Date (
    DateKey INT PRIMARY KEY,
    FullDate DATE,
    Is_Late_Night BIT,
    Is_Exam_Season BIT,
    Is_Weekend BIT
);

CREATE TABLE Dim_MentalState (
    StateKey INT PRIMARY KEY,
    Attention_Span_Level VARCHAR(20),
    Brainrot_Stage VARCHAR(20),
    Aura_Color_Code VARCHAR(10)
);

CREATE TABLE Dim_Habits (
    HabitKey INT PRIMARY KEY,
    Coffee_Level VARCHAR(20),
    Smoking_Status VARCHAR(20)
);

CREATE TABLE Fact_User_Activity (
    ActivityID INT PRIMARY KEY IDENTITY(1,1),
    UserKey INT FOREIGN KEY REFERENCES Dim_Users(UserKey),
    DateKey INT FOREIGN KEY REFERENCES Dim_Date(DateKey),
    StateKey INT FOREIGN KEY REFERENCES Dim_MentalState(StateKey),
    HabitKey INT FOREIGN KEY REFERENCES Dim_Habits(HabitKey),
    Study_Hours FLOAT,
    Coffee_Consumed_Per_Day INT,
    Smoking_Breaks_Count INT,
    Total_Reels_Watched INT,
    Short_Content_Percentage FLOAT,
    Peak_Hour INT,
    Focus_Sessions_Count INT,
    Brainrot_Exposure_Score FLOAT,
    Wellbeing_Score FLOAT
);
GO