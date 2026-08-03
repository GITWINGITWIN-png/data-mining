BEGIN TRANSACTION;
CREATE TABLE Club (
    ClubID       INTEGER      PRIMARY KEY,
    ClubName     VARCHAR(80)  NOT NULL,
    Address      VARCHAR(150),
    Phone        VARCHAR(20),
    Region       VARCHAR(40),
    ManagerName  VARCHAR(80)
);
INSERT INTO "Club" VALUES(1,'DAKDL Bangkok Central','221 Sukhumvit Rd, Bangkok','02-111-2201','Central','Manop Srisuk');
INSERT INTO "Club" VALUES(2,'DAKDL Chiang Mai Hub','55 Nimmana Rd, Chiang Mai','053-222-330','North','Pornthip Chai');
INSERT INTO "Club" VALUES(3,'DAKDL Phuket Bay','9 Patong Beach Rd, Phuket','076-333-440','South','Surachai Nak');
INSERT INTO "Club" VALUES(4,'DAKDL Khon Kaen','18 Mittraphap Rd, Khon Kaen','043-444-550','Northeast','Ratana Dee');
INSERT INTO "Club" VALUES(5,'DAKDL Hat Yai','7 Niphat Uthit Rd, Hat Yai','074-555-660','South','Adul Sri');
CREATE TABLE Customer (
    CustomerID    INTEGER      PRIMARY KEY,
    CustomerName  VARCHAR(80)  NOT NULL,
    Address       VARCHAR(150),
    Phone         VARCHAR(20),
    RegDate       DATE
);
INSERT INTO "Customer" VALUES(101,'Anon Chaiya','12 Silom Rd, Bangkok','081-200-1101','2024-06-10');
INSERT INTO "Customer" VALUES(102,'Benjawan Rak','88 Ratchada Rd, Bangkok','081-200-1102','2024-07-22');
INSERT INTO "Customer" VALUES(103,'Chalermchai Phong','4 Tha Phae Rd, Chiang Mai','089-300-1103','2024-09-01');
INSERT INTO "Customer" VALUES(104,'Duangkamol Sri','30 Kata Rd, Phuket','086-400-1104','2024-10-15');
INSERT INTO "Customer" VALUES(105,'Ekachai Meesuk','77 Karon Rd, Phuket','086-400-1105','2024-11-03');
CREATE TABLE Dim_Club (
    club_key      INTEGER      PRIMARY KEY,
    club_id       INTEGER      NOT NULL,
    club_name     VARCHAR(80)  NOT NULL,
    region        VARCHAR(40),
    manager_name  VARCHAR(80)
);
INSERT INTO "Dim_Club" VALUES(1,1,'DAKDL Bangkok Central','Central','Manop Srisuk');
INSERT INTO "Dim_Club" VALUES(2,2,'DAKDL Chiang Mai Hub','North','Pornthip Chai');
INSERT INTO "Dim_Club" VALUES(3,3,'DAKDL Phuket Bay','South','Surachai Nak');
INSERT INTO "Dim_Club" VALUES(4,4,'DAKDL Khon Kaen','Northeast','Ratana Dee');
INSERT INTO "Dim_Club" VALUES(5,5,'DAKDL Hat Yai','South','Adul Sri');
CREATE TABLE Dim_Customer (
    customer_key   INTEGER      PRIMARY KEY,
    customer_id    INTEGER      NOT NULL,
    customer_name  VARCHAR(80)  NOT NULL,
    address        VARCHAR(150),
    phone          VARCHAR(20),
    reg_date       DATE
);
INSERT INTO "Dim_Customer" VALUES(1,101,'Anon Chaiya','12 Silom Rd, Bangkok','081-200-1101','2024-06-10');
INSERT INTO "Dim_Customer" VALUES(2,102,'Benjawan Rak','88 Ratchada Rd, Bangkok','081-200-1102','2024-07-22');
INSERT INTO "Dim_Customer" VALUES(3,103,'Chalermchai Phong','4 Tha Phae Rd, Chiang Mai','089-300-1103','2024-09-01');
INSERT INTO "Dim_Customer" VALUES(4,104,'Duangkamol Sri','30 Kata Rd, Phuket','086-400-1104','2024-10-15');
INSERT INTO "Dim_Customer" VALUES(5,105,'Ekachai Meesuk','77 Karon Rd, Phuket','086-400-1105','2024-11-03');
CREATE TABLE Dim_Date (
    date_key      INTEGER      PRIMARY KEY,
    full_date     DATE         NOT NULL,
    day_of_week   VARCHAR(10)  NOT NULL,
    week_of_year  INTEGER      NOT NULL,
    month_num     INTEGER      NOT NULL,
    month_name    VARCHAR(12)  NOT NULL,
    quarter       INTEGER      NOT NULL,
    year          INTEGER      NOT NULL,
    is_holiday    INTEGER      NOT NULL,
    holiday_name  VARCHAR(60)
);
INSERT INTO "Dim_Date" VALUES(20250101,'2025-01-01','Wednesday',0,1,'January',1,2025,1,'New Year''s Day');
INSERT INTO "Dim_Date" VALUES(20250115,'2025-01-15','Wednesday',2,1,'January',1,2025,0,NULL);
INSERT INTO "Dim_Date" VALUES(20250210,'2025-02-10','Monday',6,2,'February',1,2025,0,NULL);
INSERT INTO "Dim_Date" VALUES(20250305,'2025-03-05','Wednesday',9,3,'March',1,2025,0,NULL);
INSERT INTO "Dim_Date" VALUES(20250320,'2025-03-20','Thursday',11,3,'March',1,2025,0,NULL);
INSERT INTO "Dim_Date" VALUES(20250413,'2025-04-13','Sunday',14,4,'April',2,2025,1,'Songkran Festival');
INSERT INTO "Dim_Date" VALUES(20250622,'2025-06-22','Sunday',24,6,'June',2,2025,0,NULL);
INSERT INTO "Dim_Date" VALUES(20250708,'2025-07-08','Tuesday',27,7,'July',3,2025,0,NULL);
INSERT INTO "Dim_Date" VALUES(20250915,'2025-09-15','Monday',37,9,'September',3,2025,0,NULL);
INSERT INTO "Dim_Date" VALUES(20251110,'2025-11-10','Monday',45,11,'November',4,2025,0,NULL);
CREATE TABLE Dim_Employee (
    employee_key    INTEGER      PRIMARY KEY,
    employee_id     INTEGER      NOT NULL,
    employee_name   VARCHAR(80)  NOT NULL,
    position        VARCHAR(50),
    hire_date       DATE,
    home_club_name  VARCHAR(80)
);
INSERT INTO "Dim_Employee" VALUES(1,201,'Somsri Boonmee','Senior Sitter','2022-03-01','DAKDL Bangkok Central');
INSERT INTO "Dim_Employee" VALUES(2,202,'Nattapong Sri','Sitter','2023-05-12','DAKDL Bangkok Central');
INSERT INTO "Dim_Employee" VALUES(3,203,'Pimchanok Lee','Senior Sitter','2022-08-19','DAKDL Chiang Mai Hub');
INSERT INTO "Dim_Employee" VALUES(4,204,'Kittisak Wong','Sitter','2023-01-25','DAKDL Phuket Bay');
INSERT INTO "Dim_Employee" VALUES(5,205,'Achara Meesap','Sitter','2024-02-10','DAKDL Khon Kaen');
CREATE TABLE Dim_JobType (
    job_type_key  INTEGER        PRIMARY KEY,
    job_type_id   INTEGER        NOT NULL,
    type_name     VARCHAR(60)    NOT NULL,
    base_rate     DECIMAL(10,2)  NOT NULL
);
INSERT INTO "Dim_JobType" VALUES(1,301,'Infant Care',250);
INSERT INTO "Dim_JobType" VALUES(2,302,'Toddler Care',200);
INSERT INTO "Dim_JobType" VALUES(3,303,'Child Care',180);
INSERT INTO "Dim_JobType" VALUES(4,304,'Special Needs Care',350);
INSERT INTO "Dim_JobType" VALUES(5,305,'Overnight Care',150);
CREATE TABLE Employee (
    EmployeeID    INTEGER      PRIMARY KEY,
    EmployeeName  VARCHAR(80)  NOT NULL,
    Position      VARCHAR(50),
    HireDate      DATE,
    ClubID        INTEGER      NOT NULL,
    Phone         VARCHAR(20),
    FOREIGN KEY (ClubID) REFERENCES Club (ClubID)
);
INSERT INTO "Employee" VALUES(201,'Somsri Boonmee','Senior Sitter','2022-03-01',1,'090-701-2201');
INSERT INTO "Employee" VALUES(202,'Nattapong Sri','Sitter','2023-05-12',1,'090-701-2202');
INSERT INTO "Employee" VALUES(203,'Pimchanok Lee','Senior Sitter','2022-08-19',2,'090-701-2203');
INSERT INTO "Employee" VALUES(204,'Kittisak Wong','Sitter','2023-01-25',3,'090-701-2204');
INSERT INTO "Employee" VALUES(205,'Achara Meesap','Sitter','2024-02-10',4,'090-701-2205');
CREATE TABLE Fact_Babysitting_Job (
    babysitting_job_key  INTEGER        PRIMARY KEY,
    date_key             INTEGER        NOT NULL,
    customer_key         INTEGER        NOT NULL,
    employee_key         INTEGER        NOT NULL,
    club_key             INTEGER        NOT NULL,
    job_type_key         INTEGER        NOT NULL,
    job_number           INTEGER        NOT NULL,
    status               VARCHAR(20)    NOT NULL,
    amount_paid          DECIMAL(10,2)  NOT NULL,
    working_hours        DECIMAL(6,2)   NOT NULL,
    FOREIGN KEY (date_key)     REFERENCES Dim_Date (date_key),
    FOREIGN KEY (customer_key) REFERENCES Dim_Customer (customer_key),
    FOREIGN KEY (employee_key) REFERENCES Dim_Employee (employee_key),
    FOREIGN KEY (club_key)     REFERENCES Dim_Club (club_key),
    FOREIGN KEY (job_type_key) REFERENCES Dim_JobType (job_type_key)
);
INSERT INTO "Fact_Babysitting_Job" VALUES(1,20250101,1,1,1,1,1001,'Completed',1650,6);
INSERT INTO "Fact_Babysitting_Job" VALUES(2,20250115,2,2,1,3,1002,'Completed',720,4);
INSERT INTO "Fact_Babysitting_Job" VALUES(3,20250210,3,3,2,2,1003,'Completed',1200,6);
INSERT INTO "Fact_Babysitting_Job" VALUES(4,20250305,4,4,3,4,1004,'Completed',2800,8);
INSERT INTO "Fact_Babysitting_Job" VALUES(5,20250320,5,5,4,3,1005,'Completed',900,5);
INSERT INTO "Fact_Babysitting_Job" VALUES(6,20250413,1,1,1,1,1006,'Completed',750,3);
INSERT INTO "Fact_Babysitting_Job" VALUES(7,20250622,2,3,2,2,1007,'Completed',1600,8);
INSERT INTO "Fact_Babysitting_Job" VALUES(8,20250708,3,4,3,2,1008,'Completed',800,4);
INSERT INTO "Fact_Babysitting_Job" VALUES(9,20250915,4,5,4,3,1009,'Completed',720,4);
INSERT INTO "Fact_Babysitting_Job" VALUES(10,20251110,5,2,1,4,1010,'Completed',1925,5.5);
CREATE TABLE Job (
    JobNumber   INTEGER        PRIMARY KEY,
    CustomerID  INTEGER        NOT NULL,
    EmployeeID  INTEGER        NOT NULL,
    ClubID      INTEGER        NOT NULL,
    JobTypeID   INTEGER        NOT NULL,
    Date        DATE           NOT NULL,
    TimeBegin   VARCHAR(5)     NOT NULL,
    TimeEnd     VARCHAR(5)     NOT NULL,
    Amount      DECIMAL(10,2)  NOT NULL,
    Status      VARCHAR(20)    NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer (CustomerID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee (EmployeeID),
    FOREIGN KEY (ClubID)     REFERENCES Club (ClubID),
    FOREIGN KEY (JobTypeID)  REFERENCES JobType (JobTypeID)
);
INSERT INTO "Job" VALUES(1001,101,201,1,301,'2025-01-01','08:00','14:00',1650,'Completed');
INSERT INTO "Job" VALUES(1002,102,202,1,303,'2025-01-15','09:00','13:00',720,'Completed');
INSERT INTO "Job" VALUES(1003,103,203,2,302,'2025-02-10','10:00','16:00',1200,'Completed');
INSERT INTO "Job" VALUES(1004,104,204,3,304,'2025-03-05','07:30','15:30',2800,'Completed');
INSERT INTO "Job" VALUES(1005,105,205,4,303,'2025-03-20','13:00','18:00',900,'Completed');
INSERT INTO "Job" VALUES(1006,101,201,1,301,'2025-04-13','09:00','12:00',750,'Completed');
INSERT INTO "Job" VALUES(1007,102,203,2,302,'2025-06-22','09:00','17:00',1600,'Completed');
INSERT INTO "Job" VALUES(1008,103,204,3,302,'2025-07-08','08:00','12:00',800,'Completed');
INSERT INTO "Job" VALUES(1009,104,205,4,303,'2025-09-15','10:00','14:00',720,'Completed');
INSERT INTO "Job" VALUES(1010,105,202,1,304,'2025-11-10','13:00','18:30',1925,'Completed');
CREATE TABLE JobType (
    JobTypeID  INTEGER        PRIMARY KEY,
    TypeName   VARCHAR(60)    NOT NULL,
    BaseRate   DECIMAL(10,2)  NOT NULL
);
INSERT INTO "JobType" VALUES(301,'Infant Care',250);
INSERT INTO "JobType" VALUES(302,'Toddler Care',200);
INSERT INTO "JobType" VALUES(303,'Child Care',180);
INSERT INTO "JobType" VALUES(304,'Special Needs Care',350);
INSERT INTO "JobType" VALUES(305,'Overnight Care',150);
COMMIT;
