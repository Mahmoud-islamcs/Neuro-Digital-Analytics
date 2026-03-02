Create database BrainRotAnalysis
use BrainRotAnalysis
-- 2. ÃœÊ· «·„” Œœ„Ì‰ («·√”«”)
CREATE TABLE Users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    age INT NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
    occupation NVARCHAR(100),
    avg_sleep_hours DECIMAL(4,2),
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- 3. ÃœÊ· «·«” Â·«ﬂ «·—ﬁ„Ì
CREATE TABLE Digital_Consumption (
    session_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    platform_name NVARCHAR(50),
    content_format VARCHAR(20) CHECK (content_format IN ('Short-form', 'Long-form', 'Static-Posts')),
    daily_usage_minutes INT,
    scrolling_speed_index INT CHECK (scrolling_speed_index BETWEEN 1 AND 10),
    CONSTRAINT FK_Consumption_Users FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE
);
GO

-- 4. ÃœÊ· «·«Œ »«—«  «·„⁄—›Ì…
CREATE TABLE Cognitive_Metrics (
    test_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    attention_span_score INT CHECK (attention_span_score BETWEEN 1 AND 100),
    memory_recall_accuracy DECIMAL(5,2),
    reaction_time_ms INT,
    test_date DATE,
    CONSTRAINT FK_Cognitive_Users FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE
);
GO

-- 5. ÃœÊ· «·Õ«·… «·‰›”Ì…
CREATE TABLE Psychological_State (
    entry_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    anxiety_level INT CHECK (anxiety_level BETWEEN 1 AND 10),
    loneliness_score INT CHECK (loneliness_score BETWEEN 1 AND 10),
    boredom_tolerance INT CHECK (boredom_tolerance BETWEEN 1 AND 10),
    mood_rating VARCHAR(20) CHECK (mood_rating IN ('Very Low', 'Low', 'Neutral', 'High', 'Very High')),
    CONSTRAINT FK_Psychology_Users FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE
);
GO