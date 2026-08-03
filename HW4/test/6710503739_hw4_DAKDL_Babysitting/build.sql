PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Job;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS JobType;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Club;

CREATE TABLE Club (
    ClubID       INTEGER      PRIMARY KEY,
    ClubName     VARCHAR(80)  NOT NULL,
    Address      VARCHAR(150),
    Phone        VARCHAR(20),
    Region       VARCHAR(40),
    ManagerName  VARCHAR(80)
);

CREATE TABLE Customer (
    CustomerID    INTEGER      PRIMARY KEY,
    CustomerName  VARCHAR(80)  NOT NULL,
    Address       VARCHAR(150),
    Phone         VARCHAR(20),
    RegDate       DATE
);

CREATE TABLE JobType (
    JobTypeID  INTEGER        PRIMARY KEY,
    TypeName   VARCHAR(60)    NOT NULL,
    BaseRate   DECIMAL(10,2)  NOT NULL
);

CREATE TABLE Employee (
    EmployeeID    INTEGER      PRIMARY KEY,
    EmployeeName  VARCHAR(80)  NOT NULL,
    Position      VARCHAR(50),
    HireDate      DATE,
    ClubID        INTEGER      NOT NULL,
    Phone         VARCHAR(20),
    FOREIGN KEY (ClubID) REFERENCES Club (ClubID)
);

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

INSERT INTO Club (ClubID, ClubName, Address, Phone, Region, ManagerName) VALUES
    (1, 'DAKDL Bangkok Central', '221 Sukhumvit Rd, Bangkok',   '02-111-2201', 'Central',   'Manop Srisuk'),
    (2, 'DAKDL Chiang Mai Hub',  '55 Nimmana Rd, Chiang Mai',   '053-222-330', 'North',     'Pornthip Chai'),
    (3, 'DAKDL Phuket Bay',      '9 Patong Beach Rd, Phuket',   '076-333-440', 'South',     'Surachai Nak'),
    (4, 'DAKDL Khon Kaen',       '18 Mittraphap Rd, Khon Kaen', '043-444-550', 'Northeast', 'Ratana Dee'),
    (5, 'DAKDL Hat Yai',         '7 Niphat Uthit Rd, Hat Yai',  '074-555-660', 'South',     'Adul Sri');

INSERT INTO Customer (CustomerID, CustomerName, Address, Phone, RegDate) VALUES
    (101, 'Anon Chaiya',       '12 Silom Rd, Bangkok',        '081-200-1101', '2024-06-10'),
    (102, 'Benjawan Rak',      '88 Ratchada Rd, Bangkok',     '081-200-1102', '2024-07-22'),
    (103, 'Chalermchai Phong', '4 Tha Phae Rd, Chiang Mai',   '089-300-1103', '2024-09-01'),
    (104, 'Duangkamol Sri',    '30 Kata Rd, Phuket',          '086-400-1104', '2024-10-15'),
    (105, 'Ekachai Meesuk',    '77 Karon Rd, Phuket',         '086-400-1105', '2024-11-03');

INSERT INTO JobType (JobTypeID, TypeName, BaseRate) VALUES
    (301, 'Infant Care',        250.00),
    (302, 'Toddler Care',       200.00),
    (303, 'Child Care',         180.00),
    (304, 'Special Needs Care', 350.00),
    (305, 'Overnight Care',     150.00);

INSERT INTO Employee (EmployeeID, EmployeeName, Position, HireDate, ClubID, Phone) VALUES
    (201, 'Somsri Boonmee',  'Senior Sitter', '2022-03-01', 1, '090-701-2201'),
    (202, 'Nattapong Sri',   'Sitter',        '2023-05-12', 1, '090-701-2202'),
    (203, 'Pimchanok Lee',   'Senior Sitter', '2022-08-19', 2, '090-701-2203'),
    (204, 'Kittisak Wong',   'Sitter',        '2023-01-25', 3, '090-701-2204'),
    (205, 'Achara Meesap',   'Sitter',        '2024-02-10', 4, '090-701-2205');

INSERT INTO Job
    (JobNumber, CustomerID, EmployeeID, ClubID, JobTypeID, Date, TimeBegin, TimeEnd, Amount, Status) VALUES
    (1001, 101, 201, 1, 301, '2025-01-01', '08:00', '14:00', 1650.00, 'Completed'),
    (1002, 102, 202, 1, 303, '2025-01-15', '09:00', '13:00',  720.00, 'Completed'),
    (1003, 103, 203, 2, 302, '2025-02-10', '10:00', '16:00', 1200.00, 'Completed'),
    (1004, 104, 204, 3, 304, '2025-03-05', '07:30', '15:30', 2800.00, 'Completed'),
    (1005, 105, 205, 4, 303, '2025-03-20', '13:00', '18:00',  900.00, 'Completed'),
    (1006, 101, 201, 1, 301, '2025-04-13', '09:00', '12:00',  750.00, 'Completed'),
    (1007, 102, 203, 2, 302, '2025-06-22', '09:00', '17:00', 1600.00, 'Completed'),
    (1008, 103, 204, 3, 302, '2025-07-08', '08:00', '12:00',  800.00, 'Completed'),
    (1009, 104, 205, 4, 303, '2025-09-15', '10:00', '14:00',  720.00, 'Completed'),
    (1010, 105, 202, 1, 304, '2025-11-10', '13:00', '18:30', 1925.00, 'Completed');

DROP TABLE IF EXISTS Fact_Babysitting_Job;
DROP TABLE IF EXISTS Dim_Date;
DROP TABLE IF EXISTS Dim_Customer;
DROP TABLE IF EXISTS Dim_Employee;
DROP TABLE IF EXISTS Dim_Club;
DROP TABLE IF EXISTS Dim_JobType;

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

CREATE TABLE Dim_Customer (
    customer_key   INTEGER      PRIMARY KEY,
    customer_id    INTEGER      NOT NULL,
    customer_name  VARCHAR(80)  NOT NULL,
    address        VARCHAR(150),
    phone          VARCHAR(20),
    reg_date       DATE
);

CREATE TABLE Dim_Employee (
    employee_key    INTEGER      PRIMARY KEY,
    employee_id     INTEGER      NOT NULL,
    employee_name   VARCHAR(80)  NOT NULL,
    position        VARCHAR(50),
    hire_date       DATE,
    home_club_name  VARCHAR(80)
);

CREATE TABLE Dim_Club (
    club_key      INTEGER      PRIMARY KEY,
    club_id       INTEGER      NOT NULL,
    club_name     VARCHAR(80)  NOT NULL,
    region        VARCHAR(40),
    manager_name  VARCHAR(80)
);

CREATE TABLE Dim_JobType (
    job_type_key  INTEGER        PRIMARY KEY,
    job_type_id   INTEGER        NOT NULL,
    type_name     VARCHAR(60)    NOT NULL,
    base_rate     DECIMAL(10,2)  NOT NULL
);

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

INSERT INTO Dim_Customer (customer_key, customer_id, customer_name, address, phone, reg_date)
SELECT ROW_NUMBER() OVER (ORDER BY CustomerID),
       CustomerID, CustomerName, Address, Phone, RegDate
FROM Customer;

INSERT INTO Dim_Employee (employee_key, employee_id, employee_name, position, hire_date, home_club_name)
SELECT ROW_NUMBER() OVER (ORDER BY e.EmployeeID),
       e.EmployeeID, e.EmployeeName, e.Position, e.HireDate, c.ClubName
FROM Employee e JOIN Club c ON c.ClubID = e.ClubID;

INSERT INTO Dim_Club (club_key, club_id, club_name, region, manager_name)
SELECT ROW_NUMBER() OVER (ORDER BY ClubID),
       ClubID, ClubName, Region, ManagerName
FROM Club;

INSERT INTO Dim_JobType (job_type_key, job_type_id, type_name, base_rate)
SELECT ROW_NUMBER() OVER (ORDER BY JobTypeID),
       JobTypeID, TypeName, BaseRate
FROM JobType;

INSERT INTO Dim_Date
    (date_key, full_date, day_of_week, week_of_year, month_num, month_name, quarter, year, is_holiday, holiday_name)
WITH job_dates AS (SELECT DISTINCT Date AS d FROM Job),
     holidays(d, name) AS (VALUES
        ('2025-01-01', 'New Year''s Day'),
        ('2025-04-13', 'Songkran Festival'))
SELECT
    CAST(strftime('%Y%m%d', jd.d) AS INTEGER),
    jd.d,
    CASE strftime('%w', jd.d)
        WHEN '0' THEN 'Sunday'   WHEN '1' THEN 'Monday'   WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'WHEN '4' THEN 'Thursday' WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday' END,
    CAST(strftime('%W', jd.d) AS INTEGER),
    CAST(strftime('%m', jd.d) AS INTEGER),
    CASE CAST(strftime('%m', jd.d) AS INTEGER)
        WHEN 1 THEN 'January' WHEN 2 THEN 'February' WHEN 3 THEN 'March'
        WHEN 4 THEN 'April'   WHEN 5 THEN 'May'      WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'    WHEN 8 THEN 'August'   WHEN 9 THEN 'September'
        WHEN 10 THEN 'October'WHEN 11 THEN 'November'WHEN 12 THEN 'December' END,
    (CAST(strftime('%m', jd.d) AS INTEGER) + 2) / 3,
    CAST(strftime('%Y', jd.d) AS INTEGER),
    CASE WHEN h.d IS NOT NULL THEN 1 ELSE 0 END,
    h.name
FROM job_dates jd
LEFT JOIN holidays h ON h.d = jd.d;

INSERT INTO Fact_Babysitting_Job
    (babysitting_job_key, date_key, customer_key, employee_key, club_key,
     job_type_key, job_number, status, amount_paid, working_hours)
SELECT
    ROW_NUMBER() OVER (ORDER BY j.JobNumber),
    dd.date_key, dc.customer_key, de.employee_key, dcl.club_key, djt.job_type_key,
    j.JobNumber, j.Status, j.Amount,
    ROUND((julianday('2000-01-01 ' || j.TimeEnd)
         - julianday('2000-01-01 ' || j.TimeBegin)) * 24.0, 2)
FROM Job j
JOIN Dim_Customer dc  ON dc.customer_id  = j.CustomerID
JOIN Dim_Employee de  ON de.employee_id  = j.EmployeeID
JOIN Dim_Club     dcl ON dcl.club_id     = j.ClubID
JOIN Dim_JobType  djt ON djt.job_type_id = j.JobTypeID
JOIN Dim_Date     dd  ON dd.date_key     = CAST(strftime('%Y%m%d', j.Date) AS INTEGER);
