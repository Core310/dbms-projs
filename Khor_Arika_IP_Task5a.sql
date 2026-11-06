-- =============================================================================
-- CS/DSAI-4513 Database Management Systems - Fall 2026
-- Individual Project: A Job-Shop Accounting System
-- Task 5a: SQL Statements & Transact-SQL Stored Procedures (Queries 1-14)
-- Student Name: Arika Khor (ID: 113540292, Email: Arika.S.Khor-1@ou.edu)
-- Engine: Microsoft Azure SQL Database (Transact-SQL)
-- =============================================================================

-- Drop existing procedures if they exist
IF OBJECT_ID('sp_insert_process', 'P') IS NOT NULL DROP PROCEDURE sp_insert_process;
IF OBJECT_ID('sp_insert_assembly', 'P') IS NOT NULL DROP PROCEDURE sp_insert_assembly;
IF OBJECT_ID('sp_create_account', 'P') IS NOT NULL DROP PROCEDURE sp_create_account;
IF OBJECT_ID('sp_complete_job', 'P') IS NOT NULL DROP PROCEDURE sp_complete_job;
IF OBJECT_ID('sp_record_cost_transaction', 'P') IS NOT NULL DROP PROCEDURE sp_record_cost_transaction;
IF OBJECT_ID('sp_get_assembly_cost', 'P') IS NOT NULL DROP PROCEDURE sp_get_assembly_cost;
IF OBJECT_ID('sp_get_dept_labor_time', 'P') IS NOT NULL DROP PROCEDURE sp_get_dept_labor_time;
IF OBJECT_ID('sp_get_assembly_process_history', 'P') IS NOT NULL DROP PROCEDURE sp_get_assembly_process_history;
IF OBJECT_ID('sp_get_customers_in_category_range', 'P') IS NOT NULL DROP PROCEDURE sp_get_customers_in_category_range;
IF OBJECT_ID('sp_delete_cut_jobs_in_range', 'P') IS NOT NULL DROP PROCEDURE sp_delete_cut_jobs_in_range;
IF OBJECT_ID('sp_change_paint_job_color', 'P') IS NOT NULL DROP PROCEDURE sp_change_paint_job_color;
GO

-- -----------------------------------------------------------------------------
-- Query 1: Enter a new customer (30/day)
-- -----------------------------------------------------------------------------
-- Standard Parameterized Template:
-- INSERT INTO Customer (name, address, category) VALUES (@name, @address, @category);

-- -----------------------------------------------------------------------------
-- Query 2: Enter a new department (infrequent)
-- -----------------------------------------------------------------------------
-- Standard Parameterized Template:
-- INSERT INTO Department (dept_no, dept_data) VALUES (@dept_no, @dept_data);

-- -----------------------------------------------------------------------------
-- Query 3: Enter a new process-id and its department together with its type
--          and information relevant to the type (infrequent)
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_insert_process
    @process_id INT,
    @process_data VARCHAR(255),
    @dept_no INT,
    @type VARCHAR(20),                -- 'fit', 'paint', or 'cut'
    @type_param1 VARCHAR(50) = NULL,  -- fit_type / paint_type / cutting_type
    @type_param2 VARCHAR(50) = NULL   -- painting_method / machine_type
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        -- Insert base process
        INSERT INTO Process (process_id, process_data, dept_no)
        VALUES (@process_id, @process_data, @dept_no);

        -- Insert subclass based on process type
        IF LOWER(@type) = 'fit'
        BEGIN
            INSERT INTO Fit_Process (process_id, fit_type)
            VALUES (@process_id, @type_param1);
        END
        ELSE IF LOWER(@type) = 'paint'
        BEGIN
            INSERT INTO Paint_Process (process_id, paint_type, painting_method)
            VALUES (@process_id, @type_param1, @type_param2);
        END
        ELSE IF LOWER(@type) = 'cut'
        BEGIN
            INSERT INTO Cut_Process (process_id, cutting_type, machine_type)
            VALUES (@process_id, @type_param1, @type_param2);
        END
        ELSE
        BEGIN
            RAISERROR('Invalid process type. Must be fit, paint, or cut.', 16, 1);
        END

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- -----------------------------------------------------------------------------
-- Query 4: Enter a new assembly with its customer-name, assembly-details,
--          assembly-id, and date-ordered and associate it with one or more
--          processes (40/day)
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_insert_assembly
    @assembly_id INT,
    @date_ordered DATE,
    @assembly_details VARCHAR(255),
    @customer_name VARCHAR(100),
    @process_id INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        -- Insert Assembly if it does not already exist
        IF NOT EXISTS (SELECT 1 FROM Assembly WHERE assembly_id = @assembly_id)
        BEGIN
            INSERT INTO Assembly (assembly_id, date_ordered, assembly_details, customer_name)
            VALUES (@assembly_id, @date_ordered, @assembly_details, @customer_name);
        END

        -- Associate with the given process
        IF NOT EXISTS (SELECT 1 FROM Manufacture WHERE assembly_id = @assembly_id AND process_id = @process_id)
        BEGIN
            INSERT INTO Manufacture (assembly_id, process_id)
            VALUES (@assembly_id, @process_id);
        END

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- -----------------------------------------------------------------------------
-- Query 5: Create a new account and associate it with the process, assembly,
--          or department to which it is applicable (10/day)
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_create_account
    @account_no INT,
    @date_established DATE,
    @account_type VARCHAR(20), -- 'assembly', 'department', or 'process'
    @target_id INT             -- assembly_id, dept_no, or process_id
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        INSERT INTO Account (account_no, date_established)
        VALUES (@account_no, @date_established);

        IF LOWER(@account_type) = 'assembly'
        BEGIN
            INSERT INTO Assembly_Account (account_no, assembly_id, details_1)
            VALUES (@account_no, @target_id, 0.00);
        END
        ELSE IF LOWER(@account_type) = 'department'
        BEGIN
            INSERT INTO Department_Account (account_no, dept_no, details_2)
            VALUES (@account_no, @target_id, 0.00);
        END
        ELSE IF LOWER(@account_type) = 'process'
        BEGIN
            INSERT INTO Process_Account (account_no, process_id, details_3)
            VALUES (@account_no, @target_id, 0.00);
        END
        ELSE
        BEGIN
            RAISERROR('Invalid account type. Must be assembly, department, or process.', 16, 1);
        END

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- -----------------------------------------------------------------------------
-- Query 6: Enter a new job, given its job-no, assembly-id, process-id,
--          and date the job commenced (50/day)
-- -----------------------------------------------------------------------------
-- Standard Parameterized Template:
-- INSERT INTO Job (job_no, assembly_id, process_id, commence_date, complete_date)
-- VALUES (@job_no, @assembly_id, @process_id, @commence_date, NULL);

-- -----------------------------------------------------------------------------
-- Query 7: At the completion of a job, enter the date it completed and the
--          information relevant to the type of job (50/day)
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_complete_job
    @job_no INT,
    @complete_date DATE,
    @job_type VARCHAR(20),           -- 'cut', 'paint', or 'fit'
    @param1 VARCHAR(50) = NULL,       -- Cut: machine_type_used | Paint: color
    @param2 DECIMAL(8,2) = 0.0,      -- Cut: machine_time_used | Paint: volume
    @param3 VARCHAR(100) = NULL,      -- Cut: material_used
    @labor_time DECIMAL(8,2) = 0.0   -- Labor time for all job types
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        -- Update job completion date
        UPDATE Job
        SET complete_date = @complete_date
        WHERE job_no = @job_no;

        IF @@ROWCOUNT = 0
            RAISERROR('Job number does not exist.', 16, 1);

        -- Insert subclass details
        IF LOWER(@job_type) = 'cut'
        BEGIN
            INSERT INTO Cut_Job (job_no, machine_type_used, machine_time_used, material_used, labor_time)
            VALUES (@job_no, @param1, @param2, @param3, @labor_time);
        END
        ELSE IF LOWER(@job_type) = 'paint'
        BEGIN
            INSERT INTO Paint_Job (job_no, color, volume, labor_time)
            VALUES (@job_no, @param1, @param2, @labor_time);
        END
        ELSE IF LOWER(@job_type) = 'fit'
        BEGIN
            INSERT INTO Fit_Job (job_no, labor_time)
            VALUES (@job_no, @labor_time);
        END
        ELSE
        BEGIN
            RAISERROR('Invalid job type. Must be cut, paint, or fit.', 16, 1);
        END

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- -----------------------------------------------------------------------------
-- Query 8: Enter a transaction-no and its sup-cost and update all the costs
--          (details) of the affected accounts by adding sup-cost to their
--          current values of details (50/day)
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_record_cost_transaction
    @trans_no INT,
    @job_no INT,
    @sup_cost DECIMAL(12,2)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        -- Verify job existence and resolve assembly and process
        DECLARE @assembly_id INT;
        DECLARE @process_id INT;
        DECLARE @dept_no INT;

        SELECT @assembly_id = j.assembly_id,
               @process_id = j.process_id,
               @dept_no = p.dept_no
        FROM Job j
        INNER JOIN Process p ON j.process_id = p.process_id
        WHERE j.job_no = @job_no;

        IF @assembly_id IS NULL
            RAISERROR('Referenced Job or associated Process does not exist.', 16, 1);

        -- 1. Insert transaction record
        INSERT INTO Cost_Transaction (trans_no, job_no, sup_cost)
        VALUES (@trans_no, @job_no, @sup_cost);

        -- 2. Update affected Assembly Account
        UPDATE Assembly_Account
        SET details_1 = details_1 + @sup_cost
        WHERE assembly_id = @assembly_id;

        -- 3. Update affected Process Account
        UPDATE Process_Account
        SET details_3 = details_3 + @sup_cost
        WHERE process_id = @process_id;

        -- 4. Update affected Department Account
        UPDATE Department_Account
        SET details_2 = details_2 + @sup_cost
        WHERE dept_no = @dept_no;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- -----------------------------------------------------------------------------
-- Query 9: Retrieve the total cost incurred on an assembly-id (200/day)
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_get_assembly_cost
    @assembly_id INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT assembly_id, details_1 AS total_cost_incurred
    FROM Assembly_Account
    WHERE assembly_id = @assembly_id;
END;
GO

-- -----------------------------------------------------------------------------
-- Query 10: Retrieve the total labor time within a department for jobs
--           completed in the department during a given date (20/day)
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_get_dept_labor_time
    @dept_no INT,
    @complete_date DATE
AS
BEGIN
    SET NOCOUNT ON;
    SELECT 
        @dept_no AS dept_no,
        @complete_date AS complete_date,
        ISNULL(SUM(combined.labor_time), 0.0) AS total_labor_time
    FROM (
        SELECT cj.labor_time
        FROM Job j
        INNER JOIN Process p ON j.process_id = p.process_id
        INNER JOIN Cut_Job cj ON j.job_no = cj.job_no
        WHERE p.dept_no = @dept_no AND j.complete_date = @complete_date

        UNION ALL

        SELECT pj.labor_time
        FROM Job j
        INNER JOIN Process p ON j.process_id = p.process_id
        INNER JOIN Paint_Job pj ON j.job_no = pj.job_no
        WHERE p.dept_no = @dept_no AND j.complete_date = @complete_date

        UNION ALL

        SELECT fj.labor_time
        FROM Job j
        INNER JOIN Process p ON j.process_id = p.process_id
        INNER JOIN Fit_Job fj ON j.job_no = fj.job_no
        WHERE p.dept_no = @dept_no AND j.complete_date = @complete_date
    ) AS combined;
END;
GO

-- -----------------------------------------------------------------------------
-- Query 11: Retrieve the processes through which a given assembly-id has
--           passed so far (in date-commenced order) and the department
--           responsible for each process (100/day)
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_get_assembly_process_history
    @assembly_id INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT 
        j.commence_date,
        j.job_no,
        p.process_id,
        p.process_data,
        d.dept_no,
        d.dept_data
    FROM Job j
    INNER JOIN Process p ON j.process_id = p.process_id
    INNER JOIN Department d ON p.dept_no = d.dept_no
    WHERE j.assembly_id = @assembly_id
    ORDER BY j.commence_date ASC, j.job_no ASC;
END;
GO

-- -----------------------------------------------------------------------------
-- Query 12: Retrieve the customers (in name order) whose category is in a
--           given range (100/day)
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_get_customers_in_category_range
    @min_category INT,
    @max_category INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT name, address, category
    FROM Customer
    WHERE category BETWEEN @min_category AND @max_category
    ORDER BY name ASC;
END;
GO

-- -----------------------------------------------------------------------------
-- Query 13: Delete all cut-jobs whose job-no is in a given range (1/month)
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_delete_cut_jobs_in_range
    @min_job_no INT,
    @max_job_no INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        -- Cascading FK deletes Cut_Job when deleted from Job
        DELETE FROM Job
        WHERE job_no IN (
            SELECT job_no 
            FROM Cut_Job 
            WHERE job_no BETWEEN @min_job_no AND @max_job_no
        );

        SELECT @@ROWCOUNT AS cut_jobs_deleted;
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- -----------------------------------------------------------------------------
-- Query 14: Change the color of a given paint job (1/week)
-- -----------------------------------------------------------------------------
CREATE PROCEDURE sp_change_paint_job_color
    @job_no INT,
    @new_color VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Paint_Job
    SET color = @new_color
    WHERE job_no = @job_no;

    IF @@ROWCOUNT = 0
        RAISERROR('Paint job not found.', 16, 1);
END;
GO
