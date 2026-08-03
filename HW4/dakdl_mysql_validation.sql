USE dakdl_dwh;

SELECT cl.club_name, d.year, d.month_name,
       COUNT(*) AS num_jobs, SUM(f.amount_paid) AS total_revenue
FROM Fact_Babysitting_Job f
JOIN Dim_Club cl ON cl.club_key = f.club_key
JOIN Dim_Date d  ON d.date_key  = f.date_key
GROUP BY cl.club_name, d.year, d.month_num, d.month_name
ORDER BY cl.club_name, d.year, d.month_num;

SELECT e.employee_name,
       COUNT(*) AS num_jobs, SUM(f.amount_paid) AS total_revenue
FROM Fact_Babysitting_Job f
JOIN Dim_Employee e ON e.employee_key = f.employee_key
JOIN Dim_Date d     ON d.date_key     = f.date_key
WHERE d.year = 2025
GROUP BY e.employee_name
ORDER BY total_revenue DESC
LIMIT 5;

SELECT jt.type_name,
       COUNT(*) AS num_jobs, ROUND(AVG(f.working_hours), 2) AS avg_working_hours
FROM Fact_Babysitting_Job f
JOIN Dim_JobType jt ON jt.job_type_key = f.job_type_key
GROUP BY jt.type_name
ORDER BY avg_working_hours DESC;

SELECT c.customer_name, d.year, d.quarter,
       COUNT(*) AS num_jobs, SUM(f.amount_paid) AS total_paid
FROM Fact_Babysitting_Job f
JOIN Dim_Customer c ON c.customer_key = f.customer_key
JOIN Dim_Date d     ON d.date_key     = f.date_key
WHERE c.customer_id = 101
GROUP BY c.customer_name, d.year, d.quarter
ORDER BY d.year, d.quarter;

SELECT e.employee_name, d.full_date, d.holiday_name, f.working_hours
FROM Fact_Babysitting_Job f
JOIN Dim_Employee e ON e.employee_key = f.employee_key
JOIN Dim_Date d     ON d.date_key     = f.date_key
WHERE d.is_holiday = 1
ORDER BY d.full_date;
