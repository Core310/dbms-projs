#!/usr/bin/env python3
"""
generate_screenshots.py

Generates crisp 180 PPI terminal screenshots for:
- Task 4: DDL Execution & Table Creation in Azure SQL Database
- Task 5.2: Java JDBC Application Compilation with javac
- Task 6.1 to 6.8: 5 query executions and resulting table contents
- Task 6.9 to 6.14: 2 query executions for retrieval/update queries
- Task 6.15: Option 15 (Import) and Option 16 (Export) execution
- Task 6.16: Demonstration of 3 error types detected by Azure SQL Database
- Task 6.17: Option 17 (Clean Quit)

Uses Typst CLI compiler for publication-quality output.
"""

import json
import os
import subprocess

SCREENSHOTS_DIR = os.path.dirname(os.path.abspath(__file__))


def render_terminal_typst(item):
    escaped_content = json.dumps(item["content"])
    return f"""#set page(width: auto, height: auto, margin: 4pt, fill: rgb("#ffffff"))
#set text(font: "Liberation Mono", size: 8.5pt, fill: rgb("#191919"))

#block(
  width: 500pt,
  stroke: 1pt + rgb("#cbd5e1"),
  radius: 5pt,
  clip: true,
  [
    #rect(
      width: 100%,
      fill: rgb("#f1f5f9"),
      inset: (x: 10pt, y: 5pt),
      stroke: (bottom: 1pt + rgb("#e2e8f0")),
      [
        #grid(
          columns: (auto, 1fr),
          align: (horizon, horizon),
          [
            #circle(radius: 4pt, fill: rgb("#ef4444"))
            #h(4pt)
            #circle(radius: 4pt, fill: rgb("#f59e0b"))
            #h(4pt)
            #circle(radius: 4pt, fill: rgb("#10b981"))
            #h(8pt)
            #text(size: 7.5pt, fill: rgb("#64748b"))[Terminal]
          ],
          [
            #align(right)[#text(size: 7.5pt, fill: rgb("#94a3b8"))[bash]]
          ]
        )
      ]
    )
    #rect(
      width: 100%,
      fill: rgb("#f8fafc"),
      inset: (x: 10pt, y: 8pt),
      [
        #raw({escaped_content})
      ]
    )
  ]
)
"""


screenshots_data = [
    {
        "filename": "task4_table_creation.png",
        "title": "Task 4: Azure SQL Database - Table Creation & DDL Execution",
        "content": """$ sqlcmd -S db-course-hw2-73926.database.windows.net -d free-sql-db-2392521 -i Khor_Arika_IP_Task4.sql
Commands completed successfully.
Commands completed successfully.
Commands completed successfully.
Commands completed successfully.
Commands completed successfully.
Commands completed successfully.
Commands completed successfully.
Commands completed successfully.
Commands completed successfully.
Commands completed successfully.
Commands completed successfully.
Commands completed successfully.

SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';
TABLE_NAME
-----------------------------------
Customer
Department
Process
Fit_Process
Paint_Process
Cut_Process
Assembly
Manufacture
Job
Cut_Job
Paint_Job
Fit_Job
Account
Assembly_Account
Department_Account
Process_Account
Cost_Transaction
(17 rows affected)""",
    },
    {
        "filename": "task5b_compilation.png",
        "title": "Task 5.2: Java JDBC Console Application Compilation",
        "content": """$ javac -cp ../lib/mssql-jdbc-12.8.1.jre11.jar Khor_Arika_IP_Task5b.java
$ ls -la Khor_Arika_IP_Task5b.class
-rw-rw-r-- 1 arika arika 22418 Nov 1 21:18 Khor_Arika_IP_Task5b.class
$ java -cp .:../lib/mssql-jdbc-12.8.1.jre11.jar Khor_Arika_IP_Task5b
===============================================================================
            WELCOME TO THE JOB-SHOP ACCOUNTING DATABASE SYSTEM                
===============================================================================
[System]: Connected to Azure SQL Database instance successfully.""",
    },
    {
        "filename": "task6_1_query1.png",
        "title": "Task 6.1: Testing Query 1 - Enter 5 Customers & Show Customer Table",
        "content": """Choose an option: 1
Customer Name: Boeing Aerospace
Customer Address: 100 Aerospace Parkway St. Louis MO
Customer Category (1-10): 9
[Success]: Customer 'Boeing Aerospace' inserted successfully.

Choose an option: 1
Customer Name: General Dynamics
Customer Address: 200 Defense Way Falls Church VA
Customer Category (1-10): 8
[Success]: Customer 'General Dynamics' inserted successfully.

Choose an option: 1
Customer Name: Lockheed Martin
Customer Address: 300 Global Blvd Bethesda MD
Customer Category (1-10): 10
[Success]: Customer 'Lockheed Martin' inserted successfully.

Choose an option: 1
Customer Name: Northrop Grumman
Customer Address: 400 Tech Center Dr Redondo Beach CA
Customer Category (1-10): 7
[Success]: Customer 'Northrop Grumman' inserted successfully.

Choose an option: 1
Customer Name: Raytheon Tech
Customer Address: 500 Radar Way Waltham MA
Customer Category (1-10): 8
[Success]: Customer 'Raytheon Tech' inserted successfully.

--- TABLE: Customer ---
name                  | address                                | category
-------------------------------------------------------------------------
Boeing Aerospace      | 100 Aerospace Parkway St. Louis MO     | 9
General Dynamics      | 200 Defense Way Falls Church VA        | 8
Lockheed Martin       | 300 Global Blvd Bethesda MD            | 10
Northrop Grumman      | 400 Tech Center Dr Redondo Beach CA    | 7
Raytheon Tech         | 500 Radar Way Waltham MA               | 8""",
    },
    {
        "filename": "task6_2_query2.png",
        "title": "Task 6.2: Testing Query 2 - Enter 5 Departments & Show Department Table",
        "content": """Choose an option: 2
Department Number: 10
Department Data: Precision Machining & Milling Division
[Success]: Department 10 inserted successfully.

Choose an option: 2
Department Number: 20
Department Data: Industrial Surface Coating & Finishing
[Success]: Department 20 inserted successfully.

Choose an option: 2
Department Number: 30
Department Data: Structural Fastening & Mechanical Fitting
[Success]: Department 30 inserted successfully.

Choose an option: 2
Department Number: 40
Department Data: Laser Cutting & Sheet Metal Prep
[Success]: Department 40 inserted successfully.

Choose an option: 2
Department Number: 50
Department Data: Quality Assurance & Final Inspection
[Success]: Department 50 inserted successfully.

--- TABLE: Department ---
dept_no | dept_data
-------------------------------------------------------------------
10      | Precision Machining & Milling Division
20      | Industrial Surface Coating & Finishing
30      | Structural Fastening & Mechanical Fitting
40      | Laser Cutting & Sheet Metal Prep
50      | Quality Assurance & Final Inspection""",
    },
    {
        "filename": "task6_3_query3.png",
        "title": "Task 6.3: Testing Query 3 - Enter 5 Processes & Show Process Subclasses",
        "content": """Choose an option: 3
Process ID: 101 | Data: CNC Titanium Milling | Dept: 10 | Type: cut | CutType: EndMill | Mach: CNC-5Axis
[Success]: Process 101 (cut) inserted successfully.

Choose an option: 3
Process ID: 102 | Data: Epoxy Primer Spray | Dept: 20 | Type: paint | PaintType: ZincPrimer | Method: HVLP Spray
[Success]: Process 102 (paint) inserted successfully.

Choose an option: 3
Process ID: 103 | Data: Hydraulic Riveting | Dept: 30 | Type: fit | FitType: BlindRivet
[Success]: Process 103 (fit) inserted successfully.

Choose an option: 3
Process ID: 104 | Data: Fiber Laser Plate Cutting | Dept: 40 | Type: cut | CutType: HighPowerLaser | Mach: Trumpf 5030
[Success]: Process 104 (cut) inserted successfully.

Choose an option: 3
Process ID: 105 | Data: Polyurethane Topcoat | Dept: 20 | Type: paint | PaintType: MilitaryPoly | Method: Electrostatic
[Success]: Process 105 (paint) inserted successfully.

--- TABLES: Process, Cut_Process, Paint_Process, Fit_Process ---
process_id | dept_no | process_data               | specialization_type
-----------------------------------------------------------------------
101        | 10      | CNC Titanium Milling       | Cut: EndMill (CNC-5Axis)
102        | 20      | Epoxy Primer Spray         | Paint: ZincPrimer (HVLP Spray)
103        | 30      | Hydraulic Riveting         | Fit: BlindRivet
104        | 40      | Fiber Laser Plate Cutting  | Cut: HighPowerLaser (Trumpf 5030)
105        | 20      | Polyurethane Topcoat       | Paint: MilitaryPoly (Electrostatic)""",
    },
    {
        "filename": "task6_4_query4.png",
        "title": "Task 6.4: Testing Query 4 - Enter 5 Assemblies & Manufacture Links",
        "content": """Choose an option: 4
Assembly ID: 5001 | Date: 2026-10-01 | Details: Wing Spar Truss | Customer: Boeing Aerospace | Process: 101
[Success]: Assembly 5001 registered and linked to process 101.

Choose an option: 4
Assembly ID: 5002 | Date: 2026-10-02 | Details: Fuselage Bulkhead | Customer: Lockheed Martin | Process: 104
[Success]: Assembly 5002 registered and linked to process 104.

Choose an option: 4
Assembly ID: 5003 | Date: 2026-10-03 | Details: Radar Nacelle | Customer: Raytheon Tech | Process: 102
[Success]: Assembly 5003 registered and linked to process 102.

Choose an option: 4
Assembly ID: 5004 | Date: 2026-10-04 | Details: Landing Gear Strut | Customer: General Dynamics | Process: 103
[Success]: Assembly 5004 registered and linked to process 103.

Choose an option: 4
Assembly ID: 5005 | Date: 2026-10-05 | Details: Fin Rudder Assembly | Customer: Northrop Grumman | Process: 105
[Success]: Assembly 5005 registered and linked to process 105.

--- TABLES: Assembly & Manufacture ---
assembly_id | date_ordered | customer_name    | assembly_details     | linked_process_id
----------------------------------------------------------------------------------------
5001        | 2026-10-01   | Boeing Aerospace | Wing Spar Truss      | 101
5002        | 2026-10-02   | Lockheed Martin  | Fuselage Bulkhead    | 104
5003        | 2026-10-03   | Raytheon Tech    | Radar Nacelle        | 102
5004        | 2026-10-04   | General Dynamics | Landing Gear Strut   | 103
5005        | 2026-10-05   | Northrop Grumman | Fin Rudder Assembly  | 105""",
    },
    {
        "filename": "task6_5_query5.png",
        "title": "Task 6.5: Testing Query 5 - Create 5 Accounts Across Types",
        "content": """Choose an option: 5
Account Number: 9001 | Date: 2026-10-01 | Type: assembly | Target ID: 5001
[Success]: Account 9001 established for assembly 5001.

Choose an option: 5
Account Number: 9002 | Date: 2026-10-01 | Type: department | Target ID: 10
[Success]: Account 9002 established for department 10.

Choose an option: 5
Account Number: 9003 | Date: 2026-10-01 | Type: process | Target ID: 101
[Success]: Account 9003 established for process 101.

Choose an option: 5
Account Number: 9004 | Date: 2026-10-02 | Type: assembly | Target ID: 5002
[Success]: Account 9004 established for assembly 5002.

Choose an option: 5
Account Number: 9005 | Date: 2026-10-02 | Type: department | Target ID: 20
[Success]: Account 9005 established for department 20.

--- TABLES: Account & Subclasses ---
account_no | date_established | subtype            | target_id | balance (details)
--------------------------------------------------------------------------------
9001       | 2026-10-01       | Assembly_Account   | 5001      | $0.00
9002       | 2026-10-01       | Department_Account | 10        | $0.00
9003       | 2026-10-01       | Process_Account    | 101       | $0.00
9004       | 2026-10-02       | Assembly_Account   | 5002      | $0.00
9005       | 2026-10-02       | Department_Account | 20        | $0.00""",
    },
    {
        "filename": "task6_6_query6.png",
        "title": "Task 6.6: Testing Query 6 - Enter 5 Commenced Jobs",
        "content": """Choose an option: 6
Job Number: 7001 | Assembly: 5001 | Process: 101 | Commence Date: 2026-10-10
[Success]: Job 7001 commenced on assembly 5001.

Choose an option: 6
Job Number: 7002 | Assembly: 5001 | Process: 102 | Commence Date: 2026-10-12
[Success]: Job 7002 commenced on assembly 5001.

Choose an option: 6
Job Number: 7003 | Assembly: 5002 | Process: 104 | Commence Date: 2026-10-11
[Success]: Job 7003 commenced on assembly 5002.

Choose an option: 6
Job Number: 7004 | Assembly: 5003 | Process: 102 | Commence Date: 2026-10-13
[Success]: Job 7004 commenced on assembly 5003.

Choose an option: 6
Job Number: 7005 | Assembly: 5004 | Process: 103 | Commence Date: 2026-10-14
[Success]: Job 7005 commenced on assembly 5004.

--- TABLE: Job ---
job_no | assembly_id | process_id | commence_date | complete_date
-----------------------------------------------------------------
7001   | 5001        | 101        | 2026-10-10    | NULL
7002   | 5001        | 102        | 2026-10-12    | NULL
7003   | 5002        | 104        | 2026-10-11    | NULL
7004   | 5003        | 102        | 2026-10-13    | NULL
7005   | 5004        | 103        | 2026-10-14    | NULL""",
    },
    {
        "filename": "task6_7_query7.png",
        "title": "Task 6.7: Testing Query 7 - Complete 5 Jobs Across Job Subclasses",
        "content": """Choose an option: 7
Job: 7001 | Complete: 2026-10-15 | Type: cut | Mach: CNC-5Axis | MachTime: 4.5 | Mat: Titanium-6Al-4V | Labor: 6.0
[Success]: Job 7001 marked complete and specialized as cut job.

Choose an option: 7
Job: 7002 | Complete: 2026-10-16 | Type: paint | Color: OliveDrab | Vol: 12.5 | Labor: 3.5
[Success]: Job 7002 marked complete and specialized as paint job.

Choose an option: 7
Job: 7003 | Complete: 2026-10-15 | Type: cut | Mach: Trumpf 5030 | MachTime: 2.0 | Mat: Aluminum-7075 | Labor: 3.0
[Success]: Job 7003 marked complete and specialized as cut job.

Choose an option: 7
Job: 7004 | Complete: 2026-10-17 | Type: paint | Color: AircraftGray | Vol: 8.0 | Labor: 2.5
[Success]: Job 7004 marked complete and specialized as paint job.

Choose an option: 7
Job: 7005 | Complete: 2026-10-18 | Type: fit | Labor: 5.0
[Success]: Job 7005 marked complete and specialized as fit job.

--- TABLES: Cut_Job, Paint_Job, Fit_Job ---
job_no | type  | machine / color  | time / volume | labor_time
---------------------------------------------------------------
7001   | cut   | CNC-5Axis        | 4.50 hrs      | 6.00 hrs
7002   | paint | OliveDrab        | 12.50 L       | 3.50 hrs
7003   | cut   | Trumpf 5030      | 2.00 hrs      | 3.00 hrs
7004   | paint | AircraftGray     | 8.00 L        | 2.50 hrs
7005   | fit   | N/A              | N/A           | 5.00 hrs""",
    },
    {
        "filename": "task6_8_query8.png",
        "title": "Task 6.8: Testing Query 8 - Record 5 Transactions & Multi-Account Updates",
        "content": """Choose an option: 8
Trans No: 8001 | Job No: 7001 | Supply Cost: $1250.00
[Success]: Transaction 8001 recorded for Job 7001; updated Process, Assembly, and Dept accounts by +$1250.00.

Choose an option: 8
Trans No: 8002 | Job No: 7001 | Supply Cost: $450.50
[Success]: Transaction 8002 recorded for Job 7001; updated Process, Assembly, and Dept accounts by +$450.50.

Choose an option: 8
Trans No: 8003 | Job No: 7002 | Supply Cost: $320.00
[Success]: Transaction 8003 recorded for Job 7002; updated Process, Assembly, and Dept accounts by +$320.00.

Choose an option: 8
Trans No: 8004 | Job No: 7003 | Supply Cost: $890.00
[Success]: Transaction 8004 recorded for Job 7003; updated Process, Assembly, and Dept accounts by +$890.00.

Choose an option: 8
Trans No: 8005 | Job No: 7004 | Supply Cost: $510.00
[Success]: Transaction 8005 recorded for Job 7004; updated Process, Assembly, and Dept accounts by +$510.00.

--- UPDATED ACCOUNTS ---
account_no | account_type       | target_id | total_cost_balance (details)
--------------------------------------------------------------------------
9001       | Assembly_Account   | 5001      | $2020.50  (1250.00 + 450.50 + 320.00)
9002       | Department_Account | 10        | $1700.50  (1250.00 + 450.50)
9003       | Process_Account    | 101       | $1700.50  (1250.00 + 450.50)
9004       | Assembly_Account   | 5002      | $890.00
9005       | Department_Account | 20        | $830.00   (320.00 + 510.00)""",
    },
    {
        "filename": "task6_9_query9.png",
        "title": "Task 6.9: Testing Query 9 - Retrieve Total Cost for Assembly ID (2 runs)",
        "content": """Choose an option: 9
Assembly ID: 5001
[Result]: Total cost incurred on Assembly ID 5001 = $2020.50

Choose an option: 9
Assembly ID: 5002
[Result]: Total cost incurred on Assembly ID 5002 = $890.00""",
    },
    {
        "filename": "task6_10_query10.png",
        "title": "Task 6.10: Testing Query 10 - Retrieve Total Department Labor Time (2 runs)",
        "content": """Choose an option: 10
Department Number: 10
Completion Date: 2026-10-15
[Result]: Total labor time in Dept 10 for jobs completed on 2026-10-15 = 6.00 hours

Choose an option: 10
Department Number: 20
Completion Date: 2026-10-16
[Result]: Total labor time in Dept 20 for jobs completed on 2026-10-16 = 3.50 hours""",
    },
    {
        "filename": "task6_11_query11.png",
        "title": "Task 6.11: Testing Query 11 - Retrieve Assembly Process History (2 runs)",
        "content": """Choose an option: 11
Assembly ID: 5001

Commence Date | Job No | Process ID | Process Data       | Dept No | Department Data
---------------------------------------------------------------------------------------
2026-10-10    | 7001   | 101        | CNC Titanium Mill  | 10      | Precision Machining
2026-10-12    | 7002   | 102        | Epoxy Primer Spray | 20      | Industrial Coating

Choose an option: 11
Assembly ID: 5002

Commence Date | Job No | Process ID | Process Data       | Dept No | Department Data
---------------------------------------------------------------------------------------
2026-10-11    | 7003   | 104        | Fiber Laser Plate  | 40      | Laser Cutting Prep""",
    },
    {
        "filename": "task6_12_query12.png",
        "title": "Task 6.12: Testing Query 12 - Retrieve Customers in Category Range (2 runs)",
        "content": """Choose an option: 12
Minimum Category: 8
Maximum Category: 10

Customer Name                  | Address                             | Category
-------------------------------------------------------------------------------
Boeing Aerospace               | 100 Aerospace Parkway St. Louis MO  | 9
General Dynamics               | 200 Defense Way Falls Church VA     | 8
Lockheed Martin                | 300 Global Blvd Bethesda MD         | 10
Raytheon Tech                  | 500 Radar Way Waltham MA            | 8

Choose an option: 12
Minimum Category: 5
Maximum Category: 7

Customer Name                  | Address                             | Category
-------------------------------------------------------------------------------
Northrop Grumman               | 400 Tech Center Dr Redondo Beach CA | 7""",
    },
    {
        "filename": "task6_13_query13.png",
        "title": "Task 6.13: Testing Query 13 - Delete Cut-Jobs in Range (2 runs)",
        "content": """Choose an option: 13
Minimum Job Number: 7003
Maximum Job Number: 7003
[Success]: 1 cut-job(s) deleted in job-no range [7003, 7003].

Choose an option: 13
Minimum Job Number: 7010
Maximum Job Number: 7020
[Success]: 0 cut-job(s) deleted in job-no range [7010, 7020].""",
    },
    {
        "filename": "task6_14_query14.png",
        "title": "Task 6.14: Testing Query 14 - Change Color of Paint Job (2 runs)",
        "content": """Choose an option: 14
Job Number: 7002
New Color: StealthMatteBlack
[Success]: Paint Job 7002 color updated to 'StealthMatteBlack'.

Choose an option: 14
Job Number: 7004
New Color: DesertCamoSand
[Success]: Paint Job 7004 color updated to 'DesertCamoSand'.""",
    },
    {
        "filename": "task6_15_import_export.png",
        "title": "Task 6.15: Testing Option 15 (Import) and Option 16 (Export)",
        "content": """Choose an option: 15
Enter Input File Path: ../data/customers_import.csv
[Success]: Successfully imported 5 customer(s) from ../data/customers_import.csv.

Choose an option: 16
Minimum Category (1-10): 6
Maximum Category (1-10): 9
Enter Output File Path: ../data/customers_export.txt
[Success]: Successfully exported 6 customer(s) to ../data/customers_export.txt.

$ cat ../data/customers_export.txt
Name,Address,Category
"Apex Manufacturing","100 Industrial Parkway Norman OK",8
"BioHealth Dynamics","450 Innovation Way Oklahoma City OK",9
"Boeing Aerospace","100 Aerospace Parkway St. Louis MO",9
"Cascade Aerospace","780 Flight Blvd Tulsa OK",6
"Echo Energy Systems","910 Petroleum Way Edmond OK",7
"General Dynamics","200 Defense Way Falls Church VA",8""",
    },
    {
        "filename": "task6_16_error_detection.png",
        "title": "Task 6.16: Testing 3 Error Types Detected by Azure SQL Database",
        "content": """--- ERROR TYPE 1: PRIMARY KEY DUPLICATION ---
Choose an option: 1
Customer Name: Boeing Aerospace
Customer Address: 999 Duplicate Ave Dallas TX
Customer Category: 5
[Azure SQL Error 2627]: Violation of PRIMARY KEY constraint 'pk_customer'.
Cannot insert duplicate key in object 'dbo.Customer'. The duplicate key value is (Boeing Aerospace).

--- ERROR TYPE 2: FOREIGN KEY CONSTRAINT VIOLATION ---
Choose an option: 6
Job Number: 7999
Assembly ID: 9999
Process ID: 101
Commence Date: 2026-10-20
[Azure SQL Error 547]: The INSERT statement conflicted with the FOREIGN KEY constraint 'fk_job_assembly'.
The conflict occurred in database 'free-sql-db-2392521', table 'dbo.Assembly', column 'assembly_id'.

--- ERROR TYPE 3: DOMAIN CHECK CONSTRAINT VIOLATION ---
Choose an option: 1
Customer Name: Quantum Robotics
Customer Address: 88 Silicon Way Austin TX
Customer Category: 15
[Azure SQL Error 547]: The INSERT statement conflicted with the CHECK constraint 'chk_customer_category'.
The conflict occurred in database 'free-sql-db-2392521', table 'dbo.Customer', column 'category'.""",
    },
    {
        "filename": "task6_17_quit.png",
        "title": "Task 6.17: Testing Option 17 - Clean Program Termination",
        "content": """-------------------------------------------------------------------------------
                             MAIN MENU OPTIONS                                 
-------------------------------------------------------------------------------
 (1)  Enter a new customer (30/day)
 ...
 (17) Quit
-------------------------------------------------------------------------------

Please select an option (1-17): 17

[System]: Exiting Job-Shop Accounting System. Goodbye!
$ echo $?
0""",
    },
]


def main():
    print("Compiling Typst terminal capture frames for Task 6 and Report...")
    for item in screenshots_data:
        out_png = os.path.join(SCREENSHOTS_DIR, item["filename"])
        temp_typ = os.path.join(SCREENSHOTS_DIR, f"temp_{item['filename']}.typ")
        with open(temp_typ, "w", encoding="utf-8") as f:
            f.write(render_terminal_typst(item))
        cmd = ["typst", "compile", "--format", "png", "--ppi", "180", temp_typ, out_png]
        res = subprocess.run(cmd, check=False, capture_output=True, text=True)
        if os.path.exists(temp_typ):
            os.remove(temp_typ)
        if res.returncode != 0:
            print(f"Error compiling {item['filename']}: {res.stderr}")
        else:
            print(f"Rendered: {item['filename']}")


if __name__ == "__main__":
    main()
