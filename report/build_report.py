#!/usr/bin/env python3
"""build_report.py.

Compiles the master individual project deliverable:
  report.pdf (and Khor_Arika_IP_REPORT.pdf)

Features:
- Formal Cover Page per Section III
- Required Table of Contents per Section IV (100% clickable links)
- Light Theme matching HW1/HW2/HW3 specifications (Inter, answerblue, mysection rules)
- Monospace unbolded relational schemas with foreign key references
- Compact tabular BCNF/3NF normalization analysis
- Topic 4 and Azure SQL storage structures matrix
- Task 4 DDL table creation screenshot
- Task 5a/5b Java compilation and stored procedures
- Minimal student execution screenshot headings for Task 6.1 - 6.17
"""

import os
import shutil
import subprocess
import sys

REPORT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(REPORT_DIR)


def generate_tex():
    tex = []

    # -------------------------------------------------------------------------
    # Preamble (Matching Course Light Theme: HW1/HW2/HW3)
    # -------------------------------------------------------------------------
    tex.append(r"\documentclass[10pt,letterpaper]{article}")
    tex.append(r"\usepackage[margin=0.75in,top=0.75in,bottom=0.75in]{geometry}")
    tex.append(r"\usepackage{amsmath,amssymb}")
    tex.append(r"\usepackage{fontspec}")
    tex.append(r"\setmainfont{Inter}[")
    tex.append(r"    UprightFont = *-Regular,")
    tex.append(r"    BoldFont = *-Bold,")
    tex.append(r"    ItalicFont = *-Regular,")
    tex.append(r"    BoldItalicFont = *-Bold")
    tex.append(r"]")
    tex.append(r"\setmonofont{Liberation Mono}[Scale=0.85]")
    tex.append(r"\usepackage{graphicx}")
    tex.append(r"\usepackage[dvipsnames]{xcolor}")
    tex.append(r"\usepackage{fancyhdr}")
    tex.append(r"\usepackage{listings}")
    tex.append(r"\usepackage{tabularx}")
    tex.append(r"\usepackage{booktabs}")
    tex.append(r"\usepackage{longtable}")
    tex.append(r"\usepackage{float}")
    tex.append(
        r"\usepackage[colorlinks=true,linkcolor=MidnightBlue,urlcolor=MidnightBlue,citecolor=MidnightBlue,linktoc=all]{hyperref}"
    )
    tex.append(r"")
    tex.append(r"% Light Theme Colors (matching HW1/HW2/HW3)")
    tex.append(r"\definecolor{answerblue}{RGB}{0, 70, 204}")
    tex.append(r"\definecolor{headergray}{RGB}{80, 80, 80}")
    tex.append(r"\definecolor{linegray}{RGB}{200, 200, 200}")
    tex.append(r"\definecolor{titlecolor}{RGB}{17, 17, 17}")
    tex.append(r"\definecolor{bodycolor}{RGB}{25, 25, 25}")
    tex.append(r"\definecolor{codebg}{RGB}{246, 248, 252}")
    tex.append(r"\definecolor{codeborder}{RGB}{208, 218, 232}")
    tex.append(r"")
    tex.append(r"% Section styling commands matching course standard")
    tex.append(r"\newcommand{\mysection}[1]{%")
    tex.append(r"    \vspace{6pt}%")
    tex.append(r"    {\large\bfseries\color{titlecolor} #1}\par")
    tex.append(r"    \vspace{-4pt}\rule{\textwidth}{0.6pt}\vspace{4pt}%")
    tex.append(r"}")
    tex.append(r"\newcommand{\mysubsection}[1]{%")
    tex.append(r"    \vspace{4pt}%")
    tex.append(r"    {\normalsize\bfseries\color{titlecolor} #1}\par\vspace{2pt}%")
    tex.append(r"}")
    tex.append(r"\newcommand{\mysubsubsection}[1]{%")
    tex.append(r"    \vspace{3pt}%")
    tex.append(r"    {\small\bfseries\color{titlecolor} #1}\par\vspace{1pt}%")
    tex.append(r"}")
    tex.append(r"")
    tex.append(r"\lstset{")
    tex.append(r"    basicstyle=\ttfamily\scriptsize\color{bodycolor},")
    tex.append(r"    backgroundcolor=\color{codebg},")
    tex.append(r"    frame=single,")
    tex.append(r"    rulecolor=\color{codeborder},")
    tex.append(r"    breaklines=true,")
    tex.append(r"    showstringspaces=false,")
    tex.append(r"    tabsize=2,")
    tex.append(r"    xleftmargin=6pt,")
    tex.append(r"    xrightmargin=6pt,")
    tex.append(r"    framesep=4pt")
    tex.append(r"}")
    tex.append(r"")
    tex.append(r"\pagestyle{fancy}")
    tex.append(r"\fancyhf{}")
    tex.append(r"\setlength{\headheight}{20pt}")
    tex.append(r"\addtolength{\topmargin}{-8pt}")
    tex.append(
        r"\fancyhead[L]{\small\textbf{CS/DSAI-4513 Database Management Systems}}"
    )
    tex.append(
        r"\fancyhead[R]{\small Khor, Arika \quad$|$\quad ID: 113540292 \quad$|$\quad Report}"
    )
    tex.append(r"\fancyfoot[C]{\small\thepage}")
    tex.append(r"\renewcommand{\headrulewidth}{0.4pt}")
    tex.append(r"\renewcommand{\footrulewidth}{0pt}")
    tex.append(r"\setlength{\parindent}{0pt}")
    tex.append(r"\setlength{\parskip}{2.5pt}")
    tex.append(r"")
    tex.append(r"\begin{document}")
    tex.append(r"\color{bodycolor}")
    tex.append(r"")

    # -------------------------------------------------------------------------
    # Cover Page (Section III Requirement)
    # -------------------------------------------------------------------------
    tex.append(r"\begin{titlepage}")
    tex.append(r"\centering")
    tex.append(r"\vspace*{1.5cm}")
    tex.append(r"{\Large\textbf{THE UNIVERSITY OF OKLAHOMA}}\\[0.3cm]")
    tex.append(r"{\large School of Computer Science \& Data Science and AI}\\[2.0cm]")

    tex.append(
        r"{\Huge\textbf{\color{answerblue}A JOB-SHOP ACCOUNTING SYSTEM}}\\[0.5cm]"
    )
    tex.append(
        r"{\Large\textbf{End-to-End Conceptual, Relational \& Cloud DBMS Implementation}}\\[2.5cm]"
    )

    tex.append(r"\begin{tabular}{ll}")
    tex.append(
        r"\textbf{Course Name \& Number:} & CS/DSAI-4513 Database Management Systems \\"
    )
    tex.append(r"\textbf{Section Number:}        & Section 001 \\")
    tex.append(r"\textbf{Semester \& Year:}       & Fall 2026 \\")
    tex.append(r"\textbf{Instructor:}            & Dr. Le Gruenwald \\")
    tex.append(r"\textbf{Author / Student Name:} & Arika Khor \\")
    tex.append(r"\textbf{Student ID:}             & 113540292 \\")
    tex.append(r"\textbf{Student Email:}          & Arika.S.Khor-1@ou.edu \\")
    tex.append(r"\textbf{Due Date:}               & November 10, 2026 (5:00 PM CST) \\")
    tex.append(r"\end{tabular}")
    tex.append(r"\vfill")
    tex.append(
        r"{\small Project Report \quad$|$\quad Microsoft Azure SQL Cloud Database}\\[0.5cm]"
    )
    tex.append(r"\end{titlepage}")
    tex.append(r"")

    # -------------------------------------------------------------------------
    # Section IV: Table of Contents (Auto-Generated by LaTeX)
    # -------------------------------------------------------------------------
    tex.append(r"\newpage")
    tex.append(r"\pdfbookmark[1]{SECTION IV. TABLE OF CONTENTS}{sec:toc}")
    tex.append(r"\mysection{SECTION IV. TABLE OF CONTENTS}")
    tex.append(r"\vspace{0.2cm}")
    tex.append(r"\renewcommand{\contentsname}{\vspace{-24pt}}")
    tex.append(r"{\small")
    tex.append(r"\tableofcontents")
    tex.append(r"}")
    tex.append(r"")

    # -------------------------------------------------------------------------
    # Task 1: ER Diagram
    # -------------------------------------------------------------------------
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task1}\addcontentsline{toc}{section}{Task 1. Entity-Relationship (ER) Diagram}")
    tex.append(r"\mysection{Task 1. Entity-Relationship (ER) Diagram}")
    tex.append(
        r"\noindent The ER diagram models the Job-Shop Accounting System in Silberschatz Chen notation. Rectangles represent entities, diamonds denote relationships, triangles represent ISA specializations, and ovals contain attributes with primary keys underlined."
    )
    tex.append(r"\\[0.2cm]")
    tex.append(
        r"Process, Job, and Account hierarchies use disjoint (d) partial specialization. The Job entity directly links an Assembly and a Process, and Cost Transactions update corresponding accounts when recorded."
    )
    tex.append(r"\vspace{0.4cm}")
    tex.append(r"\begin{figure}[H]")
    tex.append(r"\centering")
    tex.append(r"\includegraphics[width=0.98\textwidth]{../er_diagram/job_shop_er.pdf}")
    tex.append(r"\caption{Silberschatz ER Diagram for Job-Shop Accounting System.}")
    tex.append(r"\end{figure}")
    tex.append(r"")

    # -------------------------------------------------------------------------
    # Task 2: Relational Database Schemas (Unbolded Monospace & Tabular BCNF)
    # -------------------------------------------------------------------------
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task2}\addcontentsline{toc}{section}{Task 2. Relational Database Schemas}")
    tex.append(r"\mysection{Task 2. Relational Database Schemas}")
    tex.append(
        r"\noindent Relational schemas converted from the ER diagram using standard reduction rules. Underlined attributes form primary keys and asterisks denote foreign keys."
    )
    tex.append(r"\\[0.3cm]")

    tex.append(r"\mysubsection{1. Formal Relational Schemas}")
    tex.append(r"\begin{table}[H]")
    tex.append(r"\centering\scriptsize")
    tex.append(r"\renewcommand{\arraystretch}{1.1}")
    tex.append(r"\begin{tabularx}{\textwidth}{p{2.5cm}Xp{4.4cm}}")
    tex.append(r"\toprule")
    tex.append(
        r"\textbf{Table Name} & \textbf{Relational Schema} & \textbf{Foreign Key References} \\"
    )
    tex.append(r"\midrule")
    tex.append(
        r"Customer & \texttt{Customer(\underline{name}, address, category)} & None \\"
    )
    tex.append(
        r"Assembly & \texttt{Assembly(\underline{assembly\_id}, date\_ordered, assembly\_details, customer\_name)} & \texttt{customer\_name} $\to$ \texttt{Customer.name} \\"
    )
    tex.append(
        r"Department & \texttt{Department(\underline{dept\_no}, dept\_data)} & None \\"
    )
    tex.append(
        r"Process & \texttt{Process(\underline{process\_id}, process\_data, dept\_no)} & \texttt{dept\_no} $\to$ \texttt{Department.dept\_no} \\"
    )
    tex.append(
        r"Fit\_Process & \texttt{Fit\_Process(\underline{process\_id}, fit\_type)} & \texttt{process\_id} $\to$ \texttt{Process.process\_id} \\"
    )
    tex.append(
        r"Paint\_Process & \texttt{Paint\_Process(\underline{process\_id}, paint\_type, painting\_method)} & \texttt{process\_id} $\to$ \texttt{Process.process\_id} \\"
    )
    tex.append(
        r"Cut\_Process & \texttt{Cut\_Process(\underline{process\_id}, cutting\_type, machine\_type)} & \texttt{process\_id} $\to$ \texttt{Process.process\_id} \\"
    )
    tex.append(
        r"Manufacture & \texttt{Manufacture(\underline{assembly\_id}, \underline{process\_id})} & \texttt{assembly\_id} $\to$ \texttt{Assembly}, \texttt{process\_id} $\to$ \texttt{Process} \\"
    )
    tex.append(
        r"Job & \texttt{Job(\underline{job\_no}, assembly\_id, process\_id, commence\_date, complete\_date)} & \texttt{assembly\_id} $\to$ \texttt{Assembly}, \texttt{process\_id} $\to$ \texttt{Process} \\"
    )
    tex.append(
        r"Cut\_Job & \texttt{Cut\_Job(\underline{job\_no}, machine\_used, time\_used, material, labor\_time)} & \texttt{job\_no} $\to$ \texttt{Job.job\_no} \\"
    )
    tex.append(
        r"Paint\_Job & \texttt{Paint\_Job(\underline{job\_no}, color, volume, labor\_time)} & \texttt{job\_no} $\to$ \texttt{Job.job\_no} \\"
    )
    tex.append(
        r"Fit\_Job & \texttt{Fit\_Job(\underline{job\_no}, labor\_time)} & \texttt{job\_no} $\to$ \texttt{Job.job\_no} \\"
    )
    tex.append(
        r"Account & \texttt{Account(\underline{account\_no}, date\_established)} & None \\"
    )
    tex.append(
        r"Assembly\_Account & \texttt{Assembly\_Account(\underline{account\_no}, assembly\_id, details\_1)} & \texttt{account\_no} $\to$ \texttt{Account}, \texttt{assembly\_id} $\to$ \texttt{Assembly} \\"
    )
    tex.append(
        r"Department\_Account & \texttt{Department\_Account(\underline{account\_no}, dept\_no, details\_2)} & \texttt{account\_no} $\to$ \texttt{Account}, \texttt{dept\_no} $\to$ \texttt{Department} \\"
    )
    tex.append(
        r"Process\_Account & \texttt{Process\_Account(\underline{account\_no}, process\_id, details\_3)} & \texttt{account\_no} $\to$ \texttt{Account}, \texttt{process\_id} $\to$ \texttt{Process} \\"
    )
    tex.append(
        r"Cost\_Transaction & \texttt{Cost\_Transaction(\underline{trans\_no}, job\_no, sup\_cost)} & \texttt{job\_no} $\to$ \texttt{Job.job\_no} \\"
    )
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabularx}")
    tex.append(r"\end{table}")

    tex.append(r"\mysubsection{2. Normalization Analysis (BCNF / 3NF)}")
    tex.append(
        r"\noindent All schemas satisfy BCNF and 3NF because every non-trivial functional dependency $X \to Y$ has a candidate key for its determinant $X$, with zero partial or transitive dependencies:\\[0.2cm]"
    )
    tex.append(r"\begin{table}[H]")
    tex.append(r"\centering\small")
    tex.append(r"\renewcommand{\arraystretch}{1.15}")
    tex.append(r"\begin{tabular}{lll}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Relation} & \textbf{Functional Dependencies} & \textbf{Normal Form} \\")
    tex.append(r"\midrule")
    tex.append(r"Customer & name $\to$ address, category & BCNF / 3NF \\")
    tex.append(r"Assembly & assembly\_id $\to$ date\_ordered, details, customer\_name & BCNF / 3NF \\")
    tex.append(r"Department & dept\_no $\to$ dept\_data & BCNF / 3NF \\")
    tex.append(r"Process & process\_id $\to$ process\_data, dept\_no & BCNF / 3NF \\")
    tex.append(r"Job & job\_no $\to$ assembly\_id, process\_id, dates & BCNF / 3NF \\")
    tex.append(r"Manufacture & (assembly\_id, process\_id) $\to \emptyset$ (all-key relation) & BCNF / 3NF \\")
    tex.append(r"Accounts (all) & account\_no $\to$ balance, target\_id, details & BCNF / 3NF \\")
    tex.append(r"Cost\_Transaction & trans\_no $\to$ job\_no, sup\_cost & BCNF / 3NF \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}")
    tex.append(r"\end{table}")
    tex.append(r"\label{sec:task2_end}")
    tex.append(r"")

    # -------------------------------------------------------------------------
    # Task 3: Storage Structures
    # -------------------------------------------------------------------------
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task3}\addcontentsline{toc}{section}{Task 3. Physical Storage Structures}")
    tex.append(r"\mysection{Task 3. Physical Storage Structures}")
    tex.append(
        r"\phantomsection\label{sec:task3_1}\addcontentsline{toc}{subsection}{3.1. Discussion of Storage Structures for Tables (Lecture Topic 4)}"
    )
    tex.append(
        r"\mysubsection{3.1. Discussion of Storage Structures for Tables (Lecture Topic 4)}"
    )
    tex.append(
        r"\noindent Table access patterns and chosen file organizations based on Lecture Topic 4 (heap, sequential, B+ tree, hashing):\\[0.2cm]"
    )

    tex.append(r"\begin{table}[H]")
    tex.append(r"\centering\scriptsize")
    tex.append(r"\renewcommand{\arraystretch}{1.2}")
    tex.append(r"\begin{tabularx}{\textwidth}{p{2.0cm}p{2.2cm}p{1.8cm}p{1.5cm}p{2.5cm}X}")
    tex.append(r"\toprule")
    tex.append(
        r"\textbf{Table Name} & \textbf{Query\# and Type} & \textbf{Search Key} & \textbf{Frequency} & \textbf{Selected Organization} & \textbf{Justifications} \\"
    )
    tex.append(r"\midrule")
    tex.append(
        r"Customer & Q1 (Insert), Q4 (Lookup), Q12 (Range), Opt15 (Batch), Opt16 (Range) & name, category & 30/day (Q1), 100/day (Q12) & Indexed-Sequential File (Clustered on category, Secondary on name) & Q12 and Option 16 perform frequent category range scans. Clustering on category enables contiguous disk scans, while a secondary B+ tree on name supports point lookups. \\"
    )
    tex.append(r"\midrule")
    tex.append(
        r"Department & Q2 (Insert), Q3, Q10, Q11 (Lookup) & dept\_no & Infrequent (Q2), 100/day (Q11) & Static Hashing on dept\_no & Small, static relation accessed exclusively via equality lookups on dept\_no. Hashing achieves O(1) point retrieval. \\"
    )
    tex.append(r"\midrule")
    tex.append(
        r"Process & Q3 (Insert), Q4, Q6, Q11 (Lookup), Q10 (Join) & process\_id, dept\_no & 40/day (Q4), 100/day (Q11) & Indexed-Sequential File (Primary B+ Tree on process\_id, Secondary on dept\_no) & High-frequency point lookups on process\_id benefit from B+ tree search; secondary index on dept\_no accelerates Q10 joins without full table scan. \\"
    )
    tex.append(r"\midrule")
    tex.append(
        r"Assembly & Q4 (Insert), Q6 (Lookup), Q9 (Cost), Q11 (Range) & assembly\_id & 200/day (Q9), 100/day (Q11) & Indexed-Sequential File (Clustered B+ Tree on assembly\_id) & Highest read volume in system. Clustered index minimizes disk block accesses during cost retrieval and process trace. \\"
    )
    tex.append(r"\midrule")
    tex.append(
        r"Job & Q6 (Insert), Q7 (Update), Q8 (Lookup), Q11 (Range) & job\_no, assembly\_id, commence\_date & 50/day (Q6-8), 100/day (Q11) & Indexed-Sequential File (Clustered B+ on job\_no, Secondary on (assembly\_id, commence\_date)) & Primary B+ tree accelerates updates and deletions. Composite secondary index allows Q11 to retrieve jobs sorted in commence order without sort operations. \\"
    )
    tex.append(r"\midrule")
    tex.append(
        r"Cost\_Transaction & Q8 (Insert) & trans\_no, job\_no & 50/day & Heap File with Secondary B+ Tree on trans\_no & High write volume append-only log. Heap minimizes insert overhead; secondary index enforces primary key uniqueness. \\"
    )
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabularx}")
    tex.append(r"\end{table}")
    tex.append(r"\vspace{0.4cm}")

    tex.append(
        r"\phantomsection\label{sec:task3_2}\addcontentsline{toc}{subsection}{3.2. Discussion of Storage Structures for Tables (Azure SQL Database)}"
    )
    tex.append(
        r"\mysubsection{3.2. Discussion of Storage Structures for Tables (Azure SQL Database)}"
    )
    tex.append(
        r"\noindent Azure SQL organizes tables into 8KB data pages using clustered B-tree indexes on primary keys for direct lookups and foreign key joins across all base tables. To accelerate range scans and ordered lookups without runtime sorting, secondary indexes were created: a composite index on \texttt{Job(assembly\_id, commence\_date)} for chronological job tracking in Query 11, and a nonclustered index on \texttt{Customer(category)} for category range queries in Query 12. Cost transactions are clustered on \texttt{trans\_no} to prevent heap page fragmentation."
    )
    tex.append(r"\label{sec:task3_end}")
    tex.append(r"")

    # -------------------------------------------------------------------------
    # Task 4: DDL Table Creation
    # -------------------------------------------------------------------------
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task4}\addcontentsline{toc}{section}{Task 4. SQL Statements \& Azure SQL Table Creation}")
    tex.append(r"\mysection{Task 4. SQL Statements \& Azure SQL Table Creation}")
    tex.append(
        r"\noindent Table definitions, constraints, and indexes are in \texttt{Khor\_Arika\_IP\_Task4.sql}. Below is the Azure SQL terminal output confirming table creation."
    )
    tex.append(r"\\[0.3cm]")

    tex.append(r"\begin{figure}[H]")
    tex.append(r"\centering")
    tex.append(
        r"\includegraphics[width=0.98\textwidth]{../screenshots/task4_table_creation.png}"
    )
    tex.append(
        r"\caption{Verification of Table Creation \& Schema Deployment on Azure SQL Database.}\label{fig:task4}"
    )
    tex.append(r"\end{figure}")
    tex.append(r"\label{sec:task4_end}")
    tex.append(r"")

    # -------------------------------------------------------------------------
    # Task 5: Query Stored Procedures & Java Compilation Screenshot
    # -------------------------------------------------------------------------
    tex.append(r"\newpage")
    tex.append(
        r"\phantomsection\label{sec:task5}\addcontentsline{toc}{section}{Task 5. Query Implementation \& Java JDBC Program}"
    )
    tex.append(
        r"\mysection{Task 5. Query Implementation \& Java JDBC Program}"
    )
    tex.append(
        r"\phantomsection\label{sec:task5_1}\addcontentsline{toc}{subsection}{5.1. SQL Statements \& Transact-SQL Stored Procedures}"
    )
    tex.append(
        r"\mysubsection{5.1. SQL Statements \& Transact-SQL Stored Procedures}"
    )
    tex.append(
        r"\noindent Queries 1-14 are in \texttt{Khor\_Arika\_IP\_Task5a.sql}. Multi-account updates are wrapped in stored procedures with transaction rollback on error."
    )
    tex.append(r"\\[0.3cm]")
    tex.append(
        r"\phantomsection\label{sec:task5_2}\addcontentsline{toc}{subsection}{5.2. Java Source Program \& Successful Compilation}"
    )
    tex.append(
        r"\mysubsection{5.2. Java Source Program \& Successful Compilation}"
    )
    tex.append(
        r"\noindent Interactive console client in \texttt{Khor\_Arika\_IP\_Task5b.java} with 17 menu options. Terminal output below confirms clean compilation with \texttt{javac}."
    )
    tex.append(r"\\[0.3cm]")

    tex.append(r"\begin{figure}[H]")
    tex.append(r"\centering")
    tex.append(
        r"\includegraphics[width=0.98\textwidth]{../screenshots/task5b_compilation.png}"
    )
    tex.append(
        r"\caption{Verification of Java JDBC Application Compilation with javac.}\label{fig:task5b}"
    )
    tex.append(r"\end{figure}")
    tex.append(r"\label{sec:task5_end}")
    tex.append(r"")

    # -------------------------------------------------------------------------
    # Task 6: Execution Screenshots 6.1 - 6.17 (Minimal Student Headings)
    # -------------------------------------------------------------------------
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6}\addcontentsline{toc}{section}{Task 6. Java Program Execution Screenshots}")
    tex.append(r"\mysection{Task 6. Java Program Execution Screenshots}")

    # 6.1
    tex.append(r"\phantomsection\label{sec:task6_1}\addcontentsline{toc}{subsection}{6.1. Query 1}")
    tex.append(r"\mysubsection{Query 1}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_1_query1.png}\end{figure}"
    )

    # 6.2
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_2}\addcontentsline{toc}{subsection}{6.2. Query 2}")
    tex.append(r"\mysubsection{Query 2}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_2_query2.png}\end{figure}"
    )

    # 6.3
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_3}\addcontentsline{toc}{subsection}{6.3. Query 3}")
    tex.append(r"\mysubsection{Query 3}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_3_query3.png}\end{figure}"
    )

    # 6.4
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_4}\addcontentsline{toc}{subsection}{6.4. Query 4}")
    tex.append(r"\mysubsection{Query 4}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_4_query4.png}\end{figure}"
    )

    # 6.5
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_5}\addcontentsline{toc}{subsection}{6.5. Query 5}")
    tex.append(r"\mysubsection{Query 5}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_5_query5.png}\end{figure}"
    )

    # 6.6
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_6}\addcontentsline{toc}{subsection}{6.6. Query 6}")
    tex.append(r"\mysubsection{Query 6}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_6_query6.png}\end{figure}"
    )

    # 6.7
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_7}\addcontentsline{toc}{subsection}{6.7. Query 7}")
    tex.append(r"\mysubsection{Query 7}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_7_query7.png}\end{figure}"
    )

    # 6.8
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_8}\addcontentsline{toc}{subsection}{6.8. Query 8}")
    tex.append(r"\mysubsection{Query 8}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_8_query8.png}\end{figure}"
    )

    # 6.9 & 6.10
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_9}\addcontentsline{toc}{subsection}{6.9. Query 9}")
    tex.append(r"\mysubsection{Query 9}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_9_query9.png}\end{figure}"
    )

    tex.append(r"\phantomsection\label{sec:task6_10}\addcontentsline{toc}{subsection}{6.10. Query 10}")
    tex.append(r"\mysubsection{Query 10}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_10_query10.png}\end{figure}"
    )

    # 6.11 & 6.12
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_11}\addcontentsline{toc}{subsection}{6.11. Query 11}")
    tex.append(r"\mysubsection{Query 11}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_11_query11.png}\end{figure}"
    )

    tex.append(r"\phantomsection\label{sec:task6_12}\addcontentsline{toc}{subsection}{6.12. Query 12}")
    tex.append(r"\mysubsection{Query 12}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_12_query12.png}\end{figure}"
    )

    # 6.13 & 6.14
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_13}\addcontentsline{toc}{subsection}{6.13. Query 13}")
    tex.append(r"\mysubsection{Query 13}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_13_query13.png}\end{figure}"
    )

    tex.append(r"\phantomsection\label{sec:task6_14}\addcontentsline{toc}{subsection}{6.14. Query 14}")
    tex.append(r"\mysubsection{Query 14}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_14_query14.png}\end{figure}"
    )

    # 6.15
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_15}\addcontentsline{toc}{subsection}{6.15. Options 15 \& 16: Import and Export}")
    tex.append(r"\mysubsection{Options 15 \& 16: Import and Export}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_15_import_export.png}\end{figure}"
    )

    # 6.16 & 6.17
    tex.append(r"\newpage")
    tex.append(r"\phantomsection\label{sec:task6_16}\addcontentsline{toc}{subsection}{6.16. Error Testing}")
    tex.append(r"\mysubsection{Error Testing}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_16_error_detection.png}\end{figure}"
    )

    tex.append(r"\phantomsection\label{sec:task6_17}\addcontentsline{toc}{subsection}{6.17. Option 17: Exit}")
    tex.append(r"\mysubsection{Option 17: Exit}")
    tex.append(
        r"\begin{figure}[H]\centering\includegraphics[width=0.95\textwidth]{../screenshots/task6_17_quit.png}\end{figure}"
    )
    tex.append(r"\label{sec:task6_end}")

    tex.append(r"")
    tex.append(r"\end{document}")

    return "\n".join(tex)


def main():
    tex_file = os.path.join(REPORT_DIR, "report.tex")
    pdf_file = os.path.join(REPORT_DIR, "report.pdf")

    print("Writing LaTeX master report source (report.tex)...")
    content = generate_tex()
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(content)

    # Also keep Khor_Arika_IP_REPORT.tex in sync
    ip_tex = os.path.join(REPORT_DIR, "Khor_Arika_IP_REPORT.tex")
    with open(ip_tex, "w", encoding="utf-8") as f:
        f.write(content)

    print("Compiling XeLaTeX report (Pass 1)...")
    cmd1 = ["xelatex", "-interaction=nonstopmode", "report.tex"]
    res1 = subprocess.run(
        cmd1, check=False, cwd=REPORT_DIR, capture_output=True, text=True
    )
    if res1.returncode != 0:
        print("Pass 1 error log snippet:")
        print("\n".join(res1.stdout.splitlines()[-40:]))
        return False

    print("Compiling XeLaTeX report (Pass 2 - resolving page labels & TOC)...")
    cmd2 = ["xelatex", "-interaction=nonstopmode", "report.tex"]
    res2 = subprocess.run(
        cmd2, check=False, cwd=REPORT_DIR, capture_output=True, text=True
    )
    if res2.returncode != 0:
        print("Pass 2 error log snippet:")
        print("\n".join(res2.stdout.splitlines()[-40:]))
        return False

    if os.path.exists(pdf_file):
        print(f"SUCCESS: Report compiled successfully to {pdf_file}")
        # Copy to project root as report.pdf
        dest_pdf = os.path.join(PROJECT_DIR, "report.pdf")
        shutil.copyfile(pdf_file, dest_pdf)
        print(f"Copied deliverable to {dest_pdf}")

        # Also maintain Khor_Arika_IP_REPORT.pdf copy for Canvas assignment prompt compatibility
        canvas_pdf = os.path.join(PROJECT_DIR, "Khor_Arika_IP_REPORT.pdf")
        shutil.copyfile(pdf_file, canvas_pdf)
        print(f"Maintained Canvas compatibility copy at {canvas_pdf}")
        return True
    return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
