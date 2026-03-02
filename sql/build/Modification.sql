USE master;
GO
ALTER DATABASE BrainRotAnalysis 
MODIFY FILE ( NAME = BrainRotAnalysis, FILEGROWTH = 10% );
GO
ALTER DATABASE BrainRotAnalysis 
MODIFY FILE ( NAME = BrainRotAnalysis_log, FILEGROWTH = 10% );
GO