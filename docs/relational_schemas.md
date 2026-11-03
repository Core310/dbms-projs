# Task 2: Relational Database Schemas & Normalization Analysis

## 1. Formal Relational Reduction (Silberschatz Reduction Rules)

Applying the formal Silberschatz reduction algorithm to the Job-Shop Accounting System ER model yields the following relational schemas. Primary keys are marked with `(PK)` and foreign keys are marked with `(FK)`.

### 1. Customer
- **Schema**: `Customer(name, address, category)`
- **Primary Key**: `name`
- **Candidate Keys**: `{name}`
- **Foreign Keys**: None
- **Domain Constraints**: `category` is an INTEGER with `CHECK (category BETWEEN 1 AND 10)`

### 2. Assembly
- **Schema**: `Assembly(assembly_id, date_ordered, assembly_details, customer_name)`
- **Primary Key**: `assembly_id`
- **Candidate Keys**: `{assembly_id}`
- **Foreign Keys**:
  - `customer_name` REFERENCES `Customer(name)` ON UPDATE CASCADE ON DELETE NO ACTION
- **Reduction Derivation**: Derived from the many-to-one relationship `Orders` with total participation on `Assembly`. The primary key of `Customer` (`name`) is embedded in `Assembly` as a foreign key.

### 3. Department
- **Schema**: `Department(dept_no, dept_data)`
- **Primary Key**: `dept_no`
- **Candidate Keys**: `{dept_no}`
- **Foreign Keys**: None

### 4. Process
- **Schema**: `Process(process_id, process_data, dept_no)`
- **Primary Key**: `process_id`
- **Candidate Keys**: `{process_id}`
- **Foreign Keys**:
  - `dept_no` REFERENCES `Department(dept_no)` ON UPDATE CASCADE ON DELETE NO ACTION
- **Reduction Derivation**: Derived from the many-to-one relationship `Supervises` with total participation on `Process`. The primary key of `Department` (`dept_no`) is embedded in `Process` as a foreign key.

### 5. Process Specialization Subclasses
- **Fit_Process**: `Fit_Process(process_id, fit_type)`
  - **Primary Key**: `process_id`
  - **Foreign Keys**: `process_id` REFERENCES `Process(process_id)` ON UPDATE CASCADE ON DELETE CASCADE
- **Paint_Process**: `Paint_Process(process_id, paint_type, painting_method)`
  - **Primary Key**: `process_id`
  - **Foreign Keys**: `process_id` REFERENCES `Process(process_id)` ON UPDATE CASCADE ON DELETE CASCADE
- **Cut_Process**: `Cut_Process(process_id, cutting_type, machine_type)`
  - **Primary Key**: `process_id`
  - **Foreign Keys**: `process_id` REFERENCES `Process(process_id)` ON UPDATE CASCADE ON DELETE CASCADE
- **Reduction Derivation**: Modeled using the standard Silberschatz method for partial, disjoint ISA specialization hierarchies. The superclass primary key forms the subclass primary key and referential constraint.

### 6. Planned Manufacture Association
- **Schema**: `Manufacture(assembly_id, process_id)`
- **Primary Key**: `(assembly_id, process_id)`
- **Candidate Keys**: `{(assembly_id, process_id)}`
- **Foreign Keys**:
  - `assembly_id` REFERENCES `Assembly(assembly_id)` ON UPDATE CASCADE ON DELETE CASCADE
  - `process_id` REFERENCES `Process(process_id)` ON UPDATE CASCADE ON DELETE NO ACTION
- **Reduction Derivation**: Standalone associative junction table representing the many-to-many relationship `Manufacture` (Query 4 association between assembly and planned processes).

### 7. Job
- **Schema**: `Job(job_no, assembly_id, process_id, commence_date, complete_date)`
- **Primary Key**: `job_no`
- **Candidate Keys**: `{job_no}`
- **Foreign Keys**:
  - `assembly_id` REFERENCES `Assembly(assembly_id)` ON UPDATE CASCADE ON DELETE NO ACTION
  - `process_id` REFERENCES `Process(process_id)` ON UPDATE CASCADE ON DELETE NO ACTION
- **Domain Constraints**: `complete_date IS NULL OR complete_date >= commence_date`
- **Reduction Derivation**: An entity set assigned each time a process begins on an assembly. Connects `assembly_id` and `process_id` with execution timestamps.

### 8. Job Specialization Subclasses
- **Cut_Job**: `Cut_Job(job_no, machine_type_used, machine_time_used, material_used, labor_time)`
  - **Primary Key**: `job_no`
  - **Foreign Keys**: `job_no` REFERENCES `Job(job_no)` ON UPDATE CASCADE ON DELETE CASCADE
  - **Constraints**: `machine_time_used >= 0`, `labor_time >= 0`
- **Paint_Job**: `Paint_Job(job_no, color, volume, labor_time)`
  - **Primary Key**: `job_no`
  - **Foreign Keys**: `job_no` REFERENCES `Job(job_no)` ON UPDATE CASCADE ON DELETE CASCADE
  - **Constraints**: `volume >= 0`, `labor_time >= 0`
- **Fit_Job**: `Fit_Job(job_no, labor_time)`
  - **Primary Key**: `job_no`
  - **Foreign Keys**: `job_no` REFERENCES `Job(job_no)` ON UPDATE CASCADE ON DELETE CASCADE
  - **Constraints**: `labor_time >= 0`

### 9. Account
- **Schema**: `Account(account_no, date_established)`
- **Primary Key**: `account_no`
- **Candidate Keys**: `{account_no}`
- **Foreign Keys**: None

### 10. Account Specialization Subclasses
- **Assembly_Account**: `Assembly_Account(account_no, assembly_id, details_1)`
  - **Primary Key**: `account_no`
  - **Foreign Keys**:
    - `account_no` REFERENCES `Account(account_no)` ON UPDATE CASCADE ON DELETE CASCADE
    - `assembly_id` REFERENCES `Assembly(assembly_id)` ON UPDATE CASCADE ON DELETE CASCADE
  - **Constraints**: `details_1 >= 0` (cost balance)
- **Department_Account**: `Department_Account(account_no, dept_no, details_2)`
  - **Primary Key**: `account_no`
  - **Foreign Keys**:
    - `account_no` REFERENCES `Account(account_no)` ON UPDATE CASCADE ON DELETE CASCADE
    - `dept_no` REFERENCES `Department(dept_no)` ON UPDATE CASCADE ON DELETE CASCADE
  - **Constraints**: `details_2 >= 0` (cost balance)
- **Process_Account**: `Process_Account(account_no, process_id, details_3)`
  - **Primary Key**: `account_no`
  - **Foreign Keys**:
    - `account_no` REFERENCES `Account(account_no)` ON UPDATE CASCADE ON DELETE CASCADE
    - `process_id` REFERENCES `Process(process_id)` ON UPDATE CASCADE ON DELETE CASCADE
  - **Constraints**: `details_3 >= 0` (cost balance)

### 11. Cost_Transaction
- **Schema**: `Cost_Transaction(trans_no, job_no, sup_cost)`
- **Primary Key**: `trans_no`
- **Candidate Keys**: `{trans_no}`
- **Foreign Keys**:
  - `job_no` REFERENCES `Job(job_no)` ON UPDATE CASCADE ON DELETE CASCADE
- **Domain Constraints**: `CHECK (sup_cost >= 0)`
- **Reduction Derivation**: Recorded against `job_no`. Atomically cascades expenditure updates across the three linked accounts (`Assembly_Account`, `Department_Account`, `Process_Account`).

---

## 2. Normalization Analysis (BCNF & 3NF Verification)

For each relation schema $R$, we determine the set of functional dependencies $F$ and verify Boyce-Codd Normal Form (BCNF) and Third Normal Form (3NF):

1. **Customer**:
   - $FD$: $\text{name} \to \text{address}, \text{category}$
   - Since $\{\text{name}\}$ is the primary key, all determinants are superkeys.
   - Status: BCNF and 3NF.

2. **Assembly**:
   - $FD$: $\text{assembly\_id} \to \text{date\_ordered}, \text{assembly\_details}, \text{customer\_name}$
   - Determinant is the primary key.
   - Status: BCNF and 3NF.

3. **Department**:
   - $FD$: $\text{dept\_no} \to \text{dept\_data}$
   - Determinant is the primary key.
   - Status: BCNF and 3NF.

4. **Process**:
   - $FD$: $\text{process\_id} \to \text{process\_data}, \text{dept\_no}$
   - Determinant is the primary key.
   - Status: BCNF and 3NF.

5. **Process Subclasses (Fit_Process, Paint_Process, Cut_Process)**:
   - $FD$: $\text{process\_id} \to \text{subclass attributes}$
   - Determinant is the primary key.
   - Status: BCNF and 3NF.

6. **Manufacture**:
   - $FD$: None non-trivial ($\text{assembly\_id}, \text{process\_id} \to \text{assembly\_id}, \text{process\_id}$)
   - All attributes belong to the candidate key.
   - Status: BCNF and 3NF.

7. **Job**:
   - $FD$: $\text{job\_no} \to \text{assembly\_id}, \text{process\_id}, \text{commence\_date}, \text{complete\_date}$
   - Determinant is the primary key.
   - Status: BCNF and 3NF.

8. **Job Subclasses (Cut_Job, Paint_Job, Fit_Job)**:
   - $FD$: $\text{job\_no} \to \text{subclass attributes}$
   - Determinant is the primary key.
   - Status: BCNF and 3NF.

9. **Account & Subclasses (Assembly_Account, Department_Account, Process_Account)**:
   - $FD$: $\text{account\_no} \to \text{target\_id}, \text{details}$
   - Determinant is the primary key.
   - Status: BCNF and 3NF.

10. **Cost_Transaction**:
    - $FD$: $\text{trans\_no} \to \text{job\_no}, \text{sup\_cost}$
    - Determinant is the primary key.
    - Status: BCNF and 3NF.

**Conclusion**: Every non-trivial functional dependency $X \to Y$ holds on a determinant $X$ that is a superkey of relation $R$. Therefore, all schemas are strictly in Boyce-Codd Normal Form (BCNF) and Third Normal Form (3NF), guaranteeing zero data redundancy and zero update, insertion, or deletion anomalies.
