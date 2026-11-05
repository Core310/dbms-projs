-- =============================================================================
-- CS/DSAI-4513 Database Management Systems - Fall 2026
-- Individual Project: A Job-Shop Accounting System
-- Task 4: DDL Table Creation and Physical Storage Structure Implementation
-- Student Name: Arika Khor (ID: 113540292, Email: Arika.S.Khor-1@ou.edu)
-- Engine: Microsoft Azure SQL Database (Transact-SQL)
-- =============================================================================

-- Clean up existing tables in reverse dependency order
IF OBJECT_ID('Cost_Transaction', 'U') IS NOT NULL DROP TABLE Cost_Transaction;
IF OBJECT_ID('Process_Account', 'U') IS NOT NULL DROP TABLE Process_Account;
IF OBJECT_ID('Department_Account', 'U') IS NOT NULL DROP TABLE Department_Account;
IF OBJECT_ID('Assembly_Account', 'U') IS NOT NULL DROP TABLE Assembly_Account;
IF OBJECT_ID('Account', 'U') IS NOT NULL DROP TABLE Account;
IF OBJECT_ID('Fit_Job', 'U') IS NOT NULL DROP TABLE Fit_Job;
IF OBJECT_ID('Paint_Job', 'U') IS NOT NULL DROP TABLE Paint_Job;
IF OBJECT_ID('Cut_Job', 'U') IS NOT NULL DROP TABLE Cut_Job;
IF OBJECT_ID('Job', 'U') IS NOT NULL DROP TABLE Job;
IF OBJECT_ID('Manufacture', 'U') IS NOT NULL DROP TABLE Manufacture;
IF OBJECT_ID('Assembly', 'U') IS NOT NULL DROP TABLE Assembly;
IF OBJECT_ID('Cut_Process', 'U') IS NOT NULL DROP TABLE Cut_Process;
IF OBJECT_ID('Paint_Process', 'U') IS NOT NULL DROP TABLE Paint_Process;
IF OBJECT_ID('Fit_Process', 'U') IS NOT NULL DROP TABLE Fit_Process;
IF OBJECT_ID('Process', 'U') IS NOT NULL DROP TABLE Process;
IF OBJECT_ID('Department', 'U') IS NOT NULL DROP TABLE Department;
IF OBJECT_ID('Customer', 'U') IS NOT NULL DROP TABLE Customer;
GO

-- -----------------------------------------------------------------------------
-- 1. Customer Table
-- Physical Structure: Clustered B-tree on PK (name); Secondary B-tree on category
-- -----------------------------------------------------------------------------
CREATE TABLE Customer (
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    category INT NOT NULL,
    CONSTRAINT pk_customer PRIMARY KEY CLUSTERED (name),
    CONSTRAINT chk_customer_category CHECK (category BETWEEN 1 AND 10)
);
GO

CREATE NONCLUSTERED INDEX idx_customer_category
ON Customer (category)
INCLUDE (address);
GO

-- -----------------------------------------------------------------------------
-- 2. Department Table
-- Physical Structure: Clustered B-tree on PK (dept_no)
-- -----------------------------------------------------------------------------
CREATE TABLE Department (
    dept_no INT NOT NULL,
    dept_data VARCHAR(255) NOT NULL,
    CONSTRAINT pk_department PRIMARY KEY CLUSTERED (dept_no)
);
GO

-- -----------------------------------------------------------------------------
-- 3. Process Table
-- Physical Structure: Clustered B-tree on PK (process_id); Secondary B-tree on dept_no
-- -----------------------------------------------------------------------------
CREATE TABLE Process (
    process_id INT NOT NULL,
    process_data VARCHAR(255) NOT NULL,
    dept_no INT NOT NULL,
    CONSTRAINT pk_process PRIMARY KEY CLUSTERED (process_id),
    CONSTRAINT fk_process_dept FOREIGN KEY (dept_no)
        REFERENCES Department(dept_no)
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);
GO

CREATE NONCLUSTERED INDEX idx_process_dept
ON Process (dept_no);
GO

-- -----------------------------------------------------------------------------
-- 4. Process Specialization Subclasses (Disjoint, Partial)
-- Physical Structure: Clustered B-tree on PK (process_id)
-- -----------------------------------------------------------------------------
CREATE TABLE Fit_Process (
    process_id INT NOT NULL,
    fit_type VARCHAR(50) NOT NULL,
    CONSTRAINT pk_fit_process PRIMARY KEY CLUSTERED (process_id),
    CONSTRAINT fk_fit_process FOREIGN KEY (process_id)
        REFERENCES Process(process_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
GO

CREATE TABLE Paint_Process (
    process_id INT NOT NULL,
    paint_type VARCHAR(50) NOT NULL,
    painting_method VARCHAR(50) NOT NULL,
    CONSTRAINT pk_paint_process PRIMARY KEY CLUSTERED (process_id),
    CONSTRAINT fk_paint_process FOREIGN KEY (process_id)
        REFERENCES Process(process_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
GO

CREATE TABLE Cut_Process (
    process_id INT NOT NULL,
    cutting_type VARCHAR(50) NOT NULL,
    machine_type VARCHAR(50) NOT NULL,
    CONSTRAINT pk_cut_process PRIMARY KEY CLUSTERED (process_id),
    CONSTRAINT fk_cut_process FOREIGN KEY (process_id)
        REFERENCES Process(process_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
GO

-- -----------------------------------------------------------------------------
-- 5. Assembly Table
-- Physical Structure: Clustered B-tree on PK (assembly_id)
-- -----------------------------------------------------------------------------
CREATE TABLE Assembly (
    assembly_id INT NOT NULL,
    date_ordered DATE NOT NULL,
    assembly_details VARCHAR(255) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    CONSTRAINT pk_assembly PRIMARY KEY CLUSTERED (assembly_id),
    CONSTRAINT fk_assembly_customer FOREIGN KEY (customer_name)
        REFERENCES Customer(name)
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);
GO

-- -----------------------------------------------------------------------------
-- 6. Manufacture Association Table (Many-to-Many Planned Processes)
-- Physical Structure: Clustered B-tree on Composite PK (assembly_id, process_id)
-- -----------------------------------------------------------------------------
CREATE TABLE Manufacture (
    assembly_id INT NOT NULL,
    process_id INT NOT NULL,
    CONSTRAINT pk_manufacture PRIMARY KEY CLUSTERED (assembly_id, process_id),
    CONSTRAINT fk_manufacture_assembly FOREIGN KEY (assembly_id)
        REFERENCES Assembly(assembly_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_manufacture_process FOREIGN KEY (process_id)
        REFERENCES Process(process_id)
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);
GO

-- -----------------------------------------------------------------------------
-- 7. Job Table
-- Physical Structure: Clustered B-tree on PK (job_no); Composite Secondary B-tree
-- -----------------------------------------------------------------------------
CREATE TABLE Job (
    job_no INT NOT NULL,
    assembly_id INT NOT NULL,
    process_id INT NOT NULL,
    commence_date DATE NOT NULL,
    complete_date DATE NULL,
    CONSTRAINT pk_job PRIMARY KEY CLUSTERED (job_no),
    CONSTRAINT fk_job_assembly FOREIGN KEY (assembly_id)
        REFERENCES Assembly(assembly_id)
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT fk_job_process FOREIGN KEY (process_id)
        REFERENCES Process(process_id)
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT chk_job_dates CHECK (complete_date IS NULL OR complete_date >= commence_date)
);
GO

CREATE NONCLUSTERED INDEX idx_job_asm_commence
ON Job (assembly_id, commence_date);
GO

-- -----------------------------------------------------------------------------
-- 8. Job Specialization Subclasses (Disjoint, Partial)
-- Physical Structure: Clustered B-tree on PK (job_no)
-- -----------------------------------------------------------------------------
CREATE TABLE Cut_Job (
    job_no INT NOT NULL,
    machine_type_used VARCHAR(50) NOT NULL,
    machine_time_used DECIMAL(8,2) NOT NULL,
    material_used VARCHAR(100) NOT NULL,
    labor_time DECIMAL(8,2) NOT NULL,
    CONSTRAINT pk_cut_job PRIMARY KEY CLUSTERED (job_no),
    CONSTRAINT fk_cut_job FOREIGN KEY (job_no)
        REFERENCES Job(job_no)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT chk_cut_job_mach_time CHECK (machine_time_used >= 0),
    CONSTRAINT chk_cut_job_labor_time CHECK (labor_time >= 0)
);
GO

CREATE TABLE Paint_Job (
    job_no INT NOT NULL,
    color VARCHAR(50) NOT NULL,
    volume DECIMAL(8,2) NOT NULL,
    labor_time DECIMAL(8,2) NOT NULL,
    CONSTRAINT pk_paint_job PRIMARY KEY CLUSTERED (job_no),
    CONSTRAINT fk_paint_job FOREIGN KEY (job_no)
        REFERENCES Job(job_no)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT chk_paint_job_volume CHECK (volume >= 0),
    CONSTRAINT chk_paint_job_labor_time CHECK (labor_time >= 0)
);
GO

CREATE TABLE Fit_Job (
    job_no INT NOT NULL,
    labor_time DECIMAL(8,2) NOT NULL,
    CONSTRAINT pk_fit_job PRIMARY KEY CLUSTERED (job_no),
    CONSTRAINT fk_fit_job FOREIGN KEY (job_no)
        REFERENCES Job(job_no)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT chk_fit_job_labor_time CHECK (labor_time >= 0)
);
GO

-- -----------------------------------------------------------------------------
-- 9. Account Table & Subclasses
-- Physical Structure: Clustered B-tree on PK (account_no)
-- -----------------------------------------------------------------------------
CREATE TABLE Account (
    account_no INT NOT NULL,
    date_established DATE NOT NULL,
    CONSTRAINT pk_account PRIMARY KEY CLUSTERED (account_no)
);
GO

CREATE TABLE Assembly_Account (
    account_no INT NOT NULL,
    assembly_id INT NOT NULL,
    details_1 DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT pk_assembly_account PRIMARY KEY CLUSTERED (account_no),
    CONSTRAINT fk_assembly_account_act FOREIGN KEY (account_no)
        REFERENCES Account(account_no)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_assembly_account_asm FOREIGN KEY (assembly_id)
        REFERENCES Assembly(assembly_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT uq_assembly_account_asm UNIQUE (assembly_id),
    CONSTRAINT chk_details_1_nonneg CHECK (details_1 >= 0)
);
GO

CREATE TABLE Department_Account (
    account_no INT NOT NULL,
    dept_no INT NOT NULL,
    details_2 DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT pk_dept_account PRIMARY KEY CLUSTERED (account_no),
    CONSTRAINT fk_dept_account_act FOREIGN KEY (account_no)
        REFERENCES Account(account_no)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_dept_account_dept FOREIGN KEY (dept_no)
        REFERENCES Department(dept_no)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT uq_dept_account_dept UNIQUE (dept_no),
    CONSTRAINT chk_details_2_nonneg CHECK (details_2 >= 0)
);
GO

CREATE TABLE Process_Account (
    account_no INT NOT NULL,
    process_id INT NOT NULL,
    details_3 DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT pk_process_account PRIMARY KEY CLUSTERED (account_no),
    CONSTRAINT fk_process_account_act FOREIGN KEY (account_no)
        REFERENCES Account(account_no)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_process_account_proc FOREIGN KEY (process_id)
        REFERENCES Process(process_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT uq_process_account_proc UNIQUE (process_id),
    CONSTRAINT chk_details_3_nonneg CHECK (details_3 >= 0)
);
GO

-- -----------------------------------------------------------------------------
-- 10. Cost_Transaction Table
-- Physical Structure: Clustered B-tree on PK (trans_no); Secondary B-tree on job_no
-- -----------------------------------------------------------------------------
CREATE TABLE Cost_Transaction (
    trans_no INT NOT NULL,
    job_no INT NOT NULL,
    sup_cost DECIMAL(12,2) NOT NULL,
    CONSTRAINT pk_cost_transaction PRIMARY KEY CLUSTERED (trans_no),
    CONSTRAINT fk_cost_transaction_job FOREIGN KEY (job_no)
        REFERENCES Job(job_no)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT chk_cost_transaction_sup_cost CHECK (sup_cost >= 0)
);
GO

CREATE NONCLUSTERED INDEX idx_trans_job
ON Cost_Transaction (job_no);
GO
