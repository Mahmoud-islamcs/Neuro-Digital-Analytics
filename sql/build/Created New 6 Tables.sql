USE BrainRotAnalysis;
GO

-- 1. «·’Õ… «·»œ‰Ì…
CREATE TABLE Physical_Health (
    physical_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    eye_strain_level INT CHECK (eye_strain_level BETWEEN 1 AND 10),
    neck_back_pain BIT, -- 1 = Yes, 0 = No
    daily_steps INT, --  √ÀÌ— «·ﬂ”· «·—ﬁ„Ì
    CONSTRAINT FK_Physical_Users FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 2. «·√œ«¡ «·√ﬂ«œÌ„Ì/«·„Â‰Ì
CREATE TABLE Performance_Metrics (
    perf_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    gpa_or_rating DECIMAL(3,2),
    missed_deadlines_count INT,
    focus_during_work_score INT CHECK (focus_during_work_score BETWEEN 1 AND 10),
    CONSTRAINT FK_Perf_Users FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 3. «·⁄·«ﬁ«  «·«Ã „«⁄Ì…
CREATE TABLE Social_Impact (
    social_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    face_to_face_interaction_hours DECIMAL(4,2),
    social_anxiety_level INT CHECK (social_anxiety_level BETWEEN 1 AND 10),
    family_conflicts_score INT CHECK (family_conflicts_score BETWEEN 1 AND 10),
    CONSTRAINT FK_Social_Users FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 4.  ›«’Ì· «·‰Ê„
CREATE TABLE Sleep_Details (
    sleep_detail_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    latency_to_sleep_minutes INT, -- »Ì«Œœ Êﬁ  ﬁœ ≈ÌÂ ⁄‘«‰ Ì‰«„ »⁄œ „« Ì”Ì» «·„Ê»«Ì·
    night_awakenings INT,
    phone_before_sleep_minutes INT,
    CONSTRAINT FK_Sleep_Users FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 5. ‰Ê⁄ «·„Õ ÊÏ
CREATE TABLE Content_Interests (
    interest_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    primary_category VARCHAR(50), -- Memes, BrainRot-Core, Gaming, News
    is_educational_content BIT,
    daily_video_count INT,
    CONSTRAINT FK_Interest_Users FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 6. «· √ÀÌ— «·„«·Ì
CREATE TABLE Financial_Metrics (
    finance_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    in_app_purchases_usd DECIMAL(10,2),
    impulse_buying_frequency INT CHECK (impulse_buying_frequency BETWEEN 1 AND 10),
    CONSTRAINT FK_Finance_Users FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);
GO