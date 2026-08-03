DROP DATABASE IF EXISTS dakdl_dwh;
CREATE DATABASE dakdl_dwh;
USE dakdl_dwh;

CREATE TABLE Club (
    ClubID       INT           PRIMARY KEY,
    ClubName     VARCHAR(80)   NOT NULL,
    Address      VARCHAR(150),
    Phone        VARCHAR(20),
    Region       VARCHAR(40),
    ManagerName  VARCHAR(80)
) ENGINE=InnoDB;

CREATE TABLE Customer (
    CustomerID    INT          PRIMARY KEY,
    CustomerName  VARCHAR(80)  NOT NULL,
    Address       VARCHAR(150),
    Phone         VARCHAR(20),
    RegDate       DATE
) ENGINE=InnoDB;

CREATE TABLE JobType (
    JobTypeID  INT            PRIMARY KEY,
    TypeName   VARCHAR(60)    NOT NULL,
    BaseRate   DECIMAL(10,2)  NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Employee (
    EmployeeID    INT          PRIMARY KEY,
    EmployeeName  VARCHAR(80)  NOT NULL,
    Position      VARCHAR(50),
    HireDate      DATE,
    ClubID        INT          NOT NULL,
    Phone         VARCHAR(20),
    FOREIGN KEY (ClubID) REFERENCES Club (ClubID)
) ENGINE=InnoDB;

CREATE TABLE Job (
    JobNumber   INT            PRIMARY KEY,
    CustomerID  INT            NOT NULL,
    EmployeeID  INT            NOT NULL,
    ClubID      INT            NOT NULL,
    JobTypeID   INT            NOT NULL,
    `Date`      DATE           NOT NULL,
    TimeBegin   TIME           NOT NULL,
    TimeEnd     TIME           NOT NULL,
    Amount      DECIMAL(10,2)  NOT NULL,
    Status      VARCHAR(20)    NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer (CustomerID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee (EmployeeID),
    FOREIGN KEY (ClubID)     REFERENCES Club (ClubID),
    FOREIGN KEY (JobTypeID)  REFERENCES JobType (JobTypeID)
) ENGINE=InnoDB;

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
    (JobNumber, CustomerID, EmployeeID, ClubID, JobTypeID, `Date`, TimeBegin, TimeEnd, Amount, Status) VALUES
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

CREATE TABLE Dim_Date (
    date_key      INT          PRIMARY KEY,
    full_date     DATE         NOT NULL,
    day_of_week   VARCHAR(10)  NOT NULL,
    week_of_year  INT          NOT NULL,
    month_num     INT          NOT NULL,
    month_name    VARCHAR(12)  NOT NULL,
    quarter       INT          NOT NULL,
    year          INT          NOT NULL,
    is_holiday    INT          NOT NULL,
    holiday_name  VARCHAR(60)
) ENGINE=InnoDB;

CREATE TABLE Dim_Customer (
    customer_key   INT          AUTO_INCREMENT PRIMARY KEY,
    customer_id    INT          NOT NULL,
    customer_name  VARCHAR(80)  NOT NULL,
    address        VARCHAR(150),
    phone          VARCHAR(20),
    reg_date       DATE
) ENGINE=InnoDB;

CREATE TABLE Dim_Employee (
    employee_key    INT          AUTO_INCREMENT PRIMARY KEY,
    employee_id     INT          NOT NULL,
    employee_name   VARCHAR(80)  NOT NULL,
    position        VARCHAR(50),
    hire_date       DATE,
    home_club_name  VARCHAR(80)
) ENGINE=InnoDB;

CREATE TABLE Dim_Club (
    club_key      INT          AUTO_INCREMENT PRIMARY KEY,
    club_id       INT          NOT NULL,
    club_name     VARCHAR(80)  NOT NULL,
    region        VARCHAR(40),
    manager_name  VARCHAR(80)
) ENGINE=InnoDB;

CREATE TABLE Dim_JobType (
    job_type_key  INT            AUTO_INCREMENT PRIMARY KEY,
    job_type_id   INT            NOT NULL,
    type_name     VARCHAR(60)    NOT NULL,
    base_rate     DECIMAL(10,2)  NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Fact_Babysitting_Job (
    babysitting_job_key  INT            AUTO_INCREMENT PRIMARY KEY,
    date_key             INT            NOT NULL,
    customer_key         INT            NOT NULL,
    employee_key         INT            NOT NULL,
    club_key             INT            NOT NULL,
    job_type_key         INT            NOT NULL,
    job_number           INT            NOT NULL,
    status               VARCHAR(20)    NOT NULL,
    amount_paid          DECIMAL(10,2)  NOT NULL,
    working_hours        DECIMAL(6,2)   NOT NULL,
    FOREIGN KEY (date_key)     REFERENCES Dim_Date (date_key),
    FOREIGN KEY (customer_key) REFERENCES Dim_Customer (customer_key),
    FOREIGN KEY (employee_key) REFERENCES Dim_Employee (employee_key),
    FOREIGN KEY (club_key)     REFERENCES Dim_Club (club_key),
    FOREIGN KEY (job_type_key) REFERENCES Dim_JobType (job_type_key)
) ENGINE=InnoDB;

INSERT INTO Dim_Customer (customer_id, customer_name, address, phone, reg_date)
SELECT CustomerID, CustomerName, Address, Phone, RegDate
FROM Customer ORDER BY CustomerID;

INSERT INTO Dim_Employee (employee_id, employee_name, position, hire_date, home_club_name)
SELECT e.EmployeeID, e.EmployeeName, e.Position, e.HireDate, c.ClubName
FROM Employee e JOIN Club c ON c.ClubID = e.ClubID
ORDER BY e.EmployeeID;

INSERT INTO Dim_Club (club_id, club_name, region, manager_name)
SELECT ClubID, ClubName, Region, ManagerName
FROM Club ORDER BY ClubID;

INSERT INTO Dim_JobType (job_type_id, type_name, base_rate)
SELECT JobTypeID, TypeName, BaseRate
FROM JobType ORDER BY JobTypeID;

INSERT INTO Dim_Date
    (date_key, full_date, day_of_week, week_of_year, month_num, month_name, quarter, year, is_holiday, holiday_name)
SELECT
    CAST(DATE_FORMAT(jd.d, '%Y%m%d') AS UNSIGNED),
    jd.d,
    DAYNAME(jd.d),
    WEEK(jd.d, 3),
    MONTH(jd.d),
    MONTHNAME(jd.d),
    QUARTER(jd.d),
    YEAR(jd.d),
    IF(h.d IS NULL, 0, 1),
    h.name
FROM (SELECT DISTINCT `Date` AS d FROM Job) jd
LEFT JOIN (
    SELECT DATE('2025-01-01') AS d, 'New Year''s Day'    AS name
    UNION ALL SELECT DATE('2025-04-13'), 'Songkran Festival'
) h ON h.d = jd.d
ORDER BY jd.d;

INSERT INTO Fact_Babysitting_Job
    (date_key, customer_key, employee_key, club_key, job_type_key,
     job_number, status, amount_paid, working_hours)
SELECT
    dd.date_key, dc.customer_key, de.employee_key, dcl.club_key, djt.job_type_key,
    j.JobNumber, j.Status, j.Amount,
    ROUND(TIME_TO_SEC(TIMEDIFF(j.TimeEnd, j.TimeBegin)) / 3600, 2)
FROM Job j
JOIN Dim_Customer dc  ON dc.customer_id  = j.CustomerID
JOIN Dim_Employee de  ON de.employee_id  = j.EmployeeID
JOIN Dim_Club     dcl ON dcl.club_id     = j.ClubID
JOIN Dim_JobType  djt ON djt.job_type_id = j.JobTypeID
JOIN Dim_Date     dd  ON dd.date_key = CAST(DATE_FORMAT(j.`Date`, '%Y%m%d') AS UNSIGNED)
ORDER BY j.JobNumber;
