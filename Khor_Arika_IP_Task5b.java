import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Types;
import java.util.Scanner;

/**
 * CS/DSAI-4513 Database Management Systems - Fall 2026
 * Individual Project: A Job-Shop Accounting System
 * Task 5b: Interactive Java JDBC Console Application
 *
 * Student Name: Arika Khor
 * Student ID:   113540292
 * Email:        Arika.S.Khor-1@ou.edu
 *
 * Important Architecture Requirements:
 * 1. Data manipulation and error checking must be done by Azure SQL Database.
 *    The application program solely renders the menu, accepts user inputs,
 *    submits parameterized queries/stored procedures to Azure SQL Database,
 *    and displays execution results or database error messages.
 * 2. Terminating condition: The program loops continuously and terminates
 *    ONLY when Option 17 (Quit) is selected.
 * 3. In-line comments are provided for all methods and options.
 */
public class Khor_Arika_IP_Task5b {

    // Azure SQL Database Connection Parameters
    // Configurable via environment variables or default connection parameters
    private static final String DEFAULT_HOSTNAME = "db-course-hw2-73926.database.windows.net";
    private static final String DEFAULT_DBNAME = "free-sql-db-2392521";
    private static final String DEFAULT_USER = "<your4x4>";
    private static final String DEFAULT_PASS = "<your_password>";

    /**
     * Builds the JDBC connection string for Microsoft Azure SQL Database.
     * Uses TLS encryption with login timeout.
     */
    private static Connection getConnection() throws SQLException {
        String host = System.getenv("AZURE_SQL_HOST") != null ? System.getenv("AZURE_SQL_HOST") : DEFAULT_HOSTNAME;
        String db = System.getenv("AZURE_SQL_DB") != null ? System.getenv("AZURE_SQL_DB") : DEFAULT_DBNAME;
        String user = System.getenv("AZURE_SQL_USER") != null ? System.getenv("AZURE_SQL_USER") : DEFAULT_USER;
        String pass = System.getenv("AZURE_SQL_PASSWORD") != null ? System.getenv("AZURE_SQL_PASSWORD") : DEFAULT_PASS;

        String url = String.format(
            "jdbc:sqlserver://%s:1433;database=%s;user=%s;password=%s;encrypt=true;trustServerCertificate=false;loginTimeout=30;",
            host, db, user, pass
        );
        return DriverManager.getConnection(url);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("===============================================================================");
        System.out.println("            WELCOME TO THE JOB-SHOP ACCOUNTING DATABASE SYSTEM                ");
        System.out.println("===============================================================================");

        boolean running = true;

        while (running) {
            printMenu();
            System.out.print("\nPlease select an option (1-17): ");
            String inputLine = sc.nextLine().trim();

            if (inputLine.isEmpty()) {
                continue;
            }

            int option = -1;
            try {
                option = Integer.parseInt(inputLine);
            } catch (NumberFormatException e) {
                System.out.println("[Error]: Invalid input. Please enter an integer from 1 to 17.");
                continue;
            }

            try {
                switch (option) {
                    case 1:
                        handleQuery1(sc);
                        break;
                    case 2:
                        handleQuery2(sc);
                        break;
                    case 3:
                        handleQuery3(sc);
                        break;
                    case 4:
                        handleQuery4(sc);
                        break;
                    case 5:
                        handleQuery5(sc);
                        break;
                    case 6:
                        handleQuery6(sc);
                        break;
                    case 7:
                        handleQuery7(sc);
                        break;
                    case 8:
                        handleQuery8(sc);
                        break;
                    case 9:
                        handleQuery9(sc);
                        break;
                    case 10:
                        handleQuery10(sc);
                        break;
                    case 11:
                        handleQuery11(sc);
                        break;
                    case 12:
                        handleQuery12(sc);
                        break;
                    case 13:
                        handleQuery13(sc);
                        break;
                    case 14:
                        handleQuery14(sc);
                        break;
                    case 15:
                        handleOption15(sc);
                        break;
                    case 16:
                        handleOption16(sc);
                        break;
                    case 17:
                        System.out.println("\n[System]: Exiting Job-Shop Accounting System. Goodbye!");
                        running = false;
                        break;
                    default:
                        System.out.println("[Error]: Option " + option + " is out of range. Choose between 1 and 17.");
                }
            } catch (SQLException e) {
                // All database-level error checking and constraint violations are caught and reported directly
                System.err.println("\n[Azure SQL Error " + e.getErrorCode() + "]: " + e.getMessage());
            } catch (Exception e) {
                System.err.println("\n[Application Error]: " + e.getMessage());
            }
        }
        sc.close();
    }

    /**
     * Prints the required 17-option menu per project specification Section II.
     */
    private static void printMenu() {
        System.out.println("\n-------------------------------------------------------------------------------");
        System.out.println("                             MAIN MENU OPTIONS                                 ");
        System.out.println("-------------------------------------------------------------------------------");
        System.out.println(" (1)  Enter a new customer (30/day)");
        System.out.println(" (2)  Enter a new department (infrequent)");
        System.out.println(" (3)  Enter a new process with its type and details (infrequent)");
        System.out.println(" (4)  Enter a new assembly and associate with process (40/day)");
        System.out.println(" (5)  Create a new account (assembly, department, or process) (10/day)");
        System.out.println(" (6)  Enter a new job (job-no, assembly, process, commence date) (50/day)");
        System.out.println(" (7)  At job completion, enter completion date and job details (50/day)");
        System.out.println(" (8)  Enter cost transaction and update 3 affected accounts (50/day)");
        System.out.println(" (9)  Retrieve total cost incurred on an assembly-id (200/day)");
        System.out.println(" (10) Retrieve total labor time in department for completed jobs on date (20/day)");
        System.out.println(" (11) Retrieve processes passed through by assembly in commence order (100/day)");
        System.out.println(" (12) Retrieve customers in a given category range (100/day)");
        System.out.println(" (13) Delete cut-jobs whose job-no is in a given range (1/month)");
        System.out.println(" (14) Change the color of a given paint job (1/week)");
        System.out.println(" (15) Import: Enter new customers from data file until empty");
        System.out.println(" (16) Export: Retrieve customers in category range and save to file");
        System.out.println(" (17) Quit");
        System.out.println("-------------------------------------------------------------------------------");
    }

    // -------------------------------------------------------------------------
    // Option 1: Enter a new customer
    // -------------------------------------------------------------------------
    private static void handleQuery1(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 1: Enter a New Customer ---");
        System.out.print("Customer Name: ");
        String name = sc.nextLine().trim();
        System.out.print("Customer Address: ");
        String address = sc.nextLine().trim();
        System.out.print("Customer Category (1-10): ");
        int category = Integer.parseInt(sc.nextLine().trim());

        String sql = "INSERT INTO Customer (name, address, category) VALUES (?, ?, ?);";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, name);
            ps.setString(2, address);
            ps.setInt(3, category);
            int rows = ps.executeUpdate();
            System.out.println("[Success]: Customer '" + name + "' inserted successfully (" + rows + " row affected).");
        }
    }

    // -------------------------------------------------------------------------
    // Option 2: Enter a new department
    // -------------------------------------------------------------------------
    private static void handleQuery2(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 2: Enter a New Department ---");
        System.out.print("Department Number: ");
        int deptNo = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Department Data: ");
        String deptData = sc.nextLine().trim();

        String sql = "INSERT INTO Department (dept_no, dept_data) VALUES (?, ?);";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, deptNo);
            ps.setString(2, deptData);
            int rows = ps.executeUpdate();
            System.out.println("[Success]: Department " + deptNo + " inserted successfully (" + rows + " row affected).");
        }
    }

    // -------------------------------------------------------------------------
    // Option 3: Enter a new process
    // -------------------------------------------------------------------------
    private static void handleQuery3(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 3: Enter a New Process ---");
        System.out.print("Process ID: ");
        int procId = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Process Data: ");
        String procData = sc.nextLine().trim();
        System.out.print("Supervising Department Number: ");
        int deptNo = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Process Type (fit / paint / cut): ");
        String ptype = sc.nextLine().trim().toLowerCase();

        String param1 = null;
        String param2 = null;

        if (ptype.equals("fit")) {
            System.out.print("Fit Type: ");
            param1 = sc.nextLine().trim();
        } else if (ptype.equals("paint")) {
            System.out.print("Paint Type: ");
            param1 = sc.nextLine().trim();
            System.out.print("Painting Method: ");
            param2 = sc.nextLine().trim();
        } else if (ptype.equals("cut")) {
            System.out.print("Cutting Type: ");
            param1 = sc.nextLine().trim();
            System.out.print("Machine Type: ");
            param2 = sc.nextLine().trim();
        }

        String sql = "{CALL sp_insert_process(?, ?, ?, ?, ?, ?)}";
        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql)) {
            cs.setInt(1, procId);
            cs.setString(2, procData);
            cs.setInt(3, deptNo);
            cs.setString(4, ptype);
            cs.setString(5, param1);
            cs.setString(6, param2);
            cs.execute();
            System.out.println("[Success]: Process " + procId + " (" + ptype + ") inserted successfully.");
        }
    }

    // -------------------------------------------------------------------------
    // Option 4: Enter a new assembly and associate with processes
    // -------------------------------------------------------------------------
    private static void handleQuery4(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 4: Enter a New Assembly ---");
        System.out.print("Assembly ID: ");
        int asmId = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Date Ordered (YYYY-MM-DD): ");
        Date dateOrdered = Date.valueOf(sc.nextLine().trim());
        System.out.print("Assembly Details: ");
        String details = sc.nextLine().trim();
        System.out.print("Customer Name: ");
        String custName = sc.nextLine().trim();
        System.out.print("Process ID to Associate: ");
        int procId = Integer.parseInt(sc.nextLine().trim());

        String sql = "{CALL sp_insert_assembly(?, ?, ?, ?, ?)}";
        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql)) {
            cs.setInt(1, asmId);
            cs.setDate(2, dateOrdered);
            cs.setString(3, details);
            cs.setString(4, custName);
            cs.setInt(5, procId);
            cs.execute();
            System.out.println("[Success]: Assembly " + asmId + " registered and linked to process " + procId + ".");
        }
    }

    // -------------------------------------------------------------------------
    // Option 5: Create a new account
    // -------------------------------------------------------------------------
    private static void handleQuery5(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 5: Create a New Account ---");
        System.out.print("Account Number: ");
        int actNo = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Date Established (YYYY-MM-DD): ");
        Date estDate = Date.valueOf(sc.nextLine().trim());
        System.out.print("Account Type (assembly / department / process): ");
        String actType = sc.nextLine().trim().toLowerCase();
        System.out.print("Target Entity ID (assembly_id, dept_no, or process_id): ");
        int targetId = Integer.parseInt(sc.nextLine().trim());

        String sql = "{CALL sp_create_account(?, ?, ?, ?)}";
        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql)) {
            cs.setInt(1, actNo);
            cs.setDate(2, estDate);
            cs.setString(3, actType);
            cs.setInt(4, targetId);
            cs.execute();
            System.out.println("[Success]: Account " + actNo + " established for " + actType + " " + targetId + ".");
        }
    }

    // -------------------------------------------------------------------------
    // Option 6: Enter a new job
    // -------------------------------------------------------------------------
    private static void handleQuery6(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 6: Enter a New Job ---");
        System.out.print("Job Number: ");
        int jobNo = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Assembly ID: ");
        int asmId = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Process ID: ");
        int procId = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Commence Date (YYYY-MM-DD): ");
        Date commDate = Date.valueOf(sc.nextLine().trim());

        String sql = "INSERT INTO Job (job_no, assembly_id, process_id, commence_date, complete_date) VALUES (?, ?, ?, ?, NULL);";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, jobNo);
            ps.setInt(2, asmId);
            ps.setInt(3, procId);
            ps.setDate(4, commDate);
            int rows = ps.executeUpdate();
            System.out.println("[Success]: Job " + jobNo + " commenced on assembly " + asmId + " (" + rows + " row affected).");
        }
    }

    // -------------------------------------------------------------------------
    // Option 7: Complete a job
    // -------------------------------------------------------------------------
    private static void handleQuery7(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 7: Complete a Job ---");
        System.out.print("Job Number: ");
        int jobNo = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Completion Date (YYYY-MM-DD): ");
        Date compDate = Date.valueOf(sc.nextLine().trim());
        System.out.print("Job Type (cut / paint / fit): ");
        String jobType = sc.nextLine().trim().toLowerCase();

        String p1 = null;
        double p2 = 0.0;
        String p3 = null;
        double labor = 0.0;

        if (jobType.equals("cut")) {
            System.out.print("Machine Type Used: ");
            p1 = sc.nextLine().trim();
            System.out.print("Machine Time Used (hours): ");
            p2 = Double.parseDouble(sc.nextLine().trim());
            System.out.print("Material Used: ");
            p3 = sc.nextLine().trim();
            System.out.print("Labor Time (hours): ");
            labor = Double.parseDouble(sc.nextLine().trim());
        } else if (jobType.equals("paint")) {
            System.out.print("Color: ");
            p1 = sc.nextLine().trim();
            System.out.print("Volume (liters): ");
            p2 = Double.parseDouble(sc.nextLine().trim());
            System.out.print("Labor Time (hours): ");
            labor = Double.parseDouble(sc.nextLine().trim());
        } else if (jobType.equals("fit")) {
            System.out.print("Labor Time (hours): ");
            labor = Double.parseDouble(sc.nextLine().trim());
        }

        String sql = "{CALL sp_complete_job(?, ?, ?, ?, ?, ?, ?)}";
        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql)) {
            cs.setInt(1, jobNo);
            cs.setDate(2, compDate);
            cs.setString(3, jobType);
            cs.setString(4, p1);
            cs.setDouble(5, p2);
            cs.setString(6, p3);
            cs.setDouble(7, labor);
            cs.execute();
            System.out.println("[Success]: Job " + jobNo + " marked complete and specialized as " + jobType + " job.");
        }
    }

    // -------------------------------------------------------------------------
    // Option 8: Record transaction and update 3 accounts
    // -------------------------------------------------------------------------
    private static void handleQuery8(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 8: Enter Cost Transaction ---");
        System.out.print("Transaction Number: ");
        int transNo = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Job Number: ");
        int jobNo = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Supply Cost (sup-cost): ");
        double supCost = Double.parseDouble(sc.nextLine().trim());

        String sql = "{CALL sp_record_cost_transaction(?, ?, ?)}";
        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql)) {
            cs.setInt(1, transNo);
            cs.setInt(2, jobNo);
            cs.setDouble(3, supCost);
            cs.execute();
            System.out.println("[Success]: Transaction " + transNo + " recorded for Job " + jobNo +
                               "; atomically updated Process, Assembly, and Department accounts by +" + supCost + ".");
        }
    }

    // -------------------------------------------------------------------------
    // Option 9: Retrieve total cost incurred on an assembly-id
    // -------------------------------------------------------------------------
    private static void handleQuery9(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 9: Retrieve Total Assembly Cost ---");
        System.out.print("Assembly ID: ");
        int asmId = Integer.parseInt(sc.nextLine().trim());

        String sql = "{CALL sp_get_assembly_cost(?)}";
        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql)) {
            cs.setInt(1, asmId);
            try (ResultSet rs = cs.executeQuery()) {
                if (rs.next()) {
                    double totalCost = rs.getDouble("total_cost_incurred");
                    System.out.printf("[Result]: Total cost incurred on Assembly ID %d = $%.2f%n", asmId, totalCost);
                } else {
                    System.out.println("[Result]: No account records found for Assembly ID " + asmId + ".");
                }
            }
        }
    }

    // -------------------------------------------------------------------------
    // Option 10: Retrieve total labor time in department for date
    // -------------------------------------------------------------------------
    private static void handleQuery10(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 10: Retrieve Department Labor Time ---");
        System.out.print("Department Number: ");
        int deptNo = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Completion Date (YYYY-MM-DD): ");
        Date compDate = Date.valueOf(sc.nextLine().trim());

        String sql = "{CALL sp_get_dept_labor_time(?, ?)}";
        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql)) {
            cs.setInt(1, deptNo);
            cs.setDate(2, compDate);
            try (ResultSet rs = cs.executeQuery()) {
                if (rs.next()) {
                    double labor = rs.getDouble("total_labor_time");
                    System.out.printf("[Result]: Total labor time in Dept %d for jobs completed on %s = %.2f hours%n",
                                      deptNo, compDate.toString(), labor);
                }
            }
        }
    }

    // -------------------------------------------------------------------------
    // Option 11: Retrieve processes passed through for an assembly
    // -------------------------------------------------------------------------
    private static void handleQuery11(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 11: Retrieve Assembly Process History ---");
        System.out.print("Assembly ID: ");
        int asmId = Integer.parseInt(sc.nextLine().trim());

        String sql = "{CALL sp_get_assembly_process_history(?)}";
        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql)) {
            cs.setInt(1, asmId);
            try (ResultSet rs = cs.executeQuery()) {
                System.out.println("\nCommence Date | Job No | Process ID | Process Data       | Dept No | Department Data");
                System.out.println("---------------------------------------------------------------------------------------");
                boolean found = false;
                while (rs.next()) {
                    found = true;
                    Date cDate = rs.getDate("commence_date");
                    int jNo = rs.getInt("job_no");
                    int pId = rs.getInt("process_id");
                    String pData = rs.getString("process_data");
                    int dNo = rs.getInt("dept_no");
                    String dData = rs.getString("dept_data");
                    System.out.printf("%-13s | %-6d | %-10d | %-18s | %-7d | %s%n",
                                      cDate, jNo, pId, pData, dNo, dData);
                }
                if (!found) {
                    System.out.println("[Result]: No jobs or processes recorded yet for Assembly ID " + asmId + ".");
                }
            }
        }
    }

    // -------------------------------------------------------------------------
    // Option 12: Retrieve customers in category range
    // -------------------------------------------------------------------------
    private static void handleQuery12(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 12: Retrieve Customers in Category Range ---");
        System.out.print("Minimum Category (1-10): ");
        int minCat = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Maximum Category (1-10): ");
        int maxCat = Integer.parseInt(sc.nextLine().trim());

        String sql = "{CALL sp_get_customers_in_category_range(?, ?)}";
        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql)) {
            cs.setInt(1, minCat);
            cs.setInt(2, maxCat);
            try (ResultSet rs = cs.executeQuery()) {
                System.out.println("\nCustomer Name                  | Address                             | Category");
                System.out.println("-------------------------------------------------------------------------------");
                boolean found = false;
                while (rs.next()) {
                    found = true;
                    String cName = rs.getString("name");
                    String cAddr = rs.getString("address");
                    int cCat = rs.getInt("category");
                    System.out.printf("%-30s | %-35s | %d%n", cName, cAddr, cCat);
                }
                if (!found) {
                    System.out.println("[Result]: No customers found in category range [" + minCat + ", " + maxCat + "].");
                }
            }
        }
    }

    // -------------------------------------------------------------------------
    // Option 13: Delete cut-jobs in range
    // -------------------------------------------------------------------------
    private static void handleQuery13(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 13: Delete Cut-Jobs in Range ---");
        System.out.print("Minimum Job Number: ");
        int minJob = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Maximum Job Number: ");
        int maxJob = Integer.parseInt(sc.nextLine().trim());

        String sql = "{CALL sp_delete_cut_jobs_in_range(?, ?)}";
        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql)) {
            cs.setInt(1, minJob);
            cs.setInt(2, maxJob);
            try (ResultSet rs = cs.executeQuery()) {
                if (rs.next()) {
                    int count = rs.getInt("cut_jobs_deleted");
                    System.out.println("[Success]: " + count + " cut-job(s) deleted in job-no range [" + minJob + ", " + maxJob + "].");
                }
            }
        }
    }

    // -------------------------------------------------------------------------
    // Option 14: Change paint job color
    // -------------------------------------------------------------------------
    private static void handleQuery14(Scanner sc) throws SQLException {
        System.out.println("\n--- Query 14: Change Paint Job Color ---");
        System.out.print("Job Number: ");
        int jobNo = Integer.parseInt(sc.nextLine().trim());
        System.out.print("New Color: ");
        String newColor = sc.nextLine().trim();

        String sql = "{CALL sp_change_paint_job_color(?, ?)}";
        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql)) {
            cs.setInt(1, jobNo);
            cs.setString(2, newColor);
            cs.execute();
            System.out.println("[Success]: Paint Job " + jobNo + " color updated to '" + newColor + "'.");
        }
    }

    // -------------------------------------------------------------------------
    // Option 15: Import customers from data file until empty
    // -------------------------------------------------------------------------
    private static void handleOption15(Scanner sc) throws SQLException {
        System.out.println("\n--- Option 15: Import Customers from File ---");
        System.out.print("Enter Input File Path: ");
        String filePath = sc.nextLine().trim();
        File file = new File(filePath);

        if (!file.exists() || !file.isFile()) {
            System.out.println("[Error]: File not found: " + filePath);
            return;
        }

        String sql = "INSERT INTO Customer (name, address, category) VALUES (?, ?, ?);";
        int count = 0;

        try (BufferedReader br = new BufferedReader(new FileReader(file));
             Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            String line;
            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#")) {
                    continue; // Skip comments and empty lines
                }

                // Expecting CSV format: name, address, category
                String[] parts = line.split(",");
                if (parts.length >= 3) {
                    String name = parts[0].trim();
                    String address = parts[1].trim();
                    int category = Integer.parseInt(parts[2].trim());

                    ps.setString(1, name);
                    ps.setString(2, address);
                    ps.setInt(3, category);
                    ps.executeUpdate();
                    count++;
                }
            }
            System.out.println("[Success]: Successfully imported " + count + " customer(s) from " + filePath + ".");
        } catch (IOException e) {
            System.err.println("[File Read Error]: " + e.getMessage());
        }
    }

    // -------------------------------------------------------------------------
    // Option 16: Export customers in category range to file
    // -------------------------------------------------------------------------
    private static void handleOption16(Scanner sc) throws SQLException {
        System.out.println("\n--- Option 16: Export Customers to File ---");
        System.out.print("Minimum Category (1-10): ");
        int minCat = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Maximum Category (1-10): ");
        int maxCat = Integer.parseInt(sc.nextLine().trim());
        System.out.print("Enter Output File Path: ");
        String filePath = sc.nextLine().trim();

        String sql = "{CALL sp_get_customers_in_category_range(?, ?)}";
        int count = 0;

        try (Connection conn = getConnection();
             CallableStatement cs = conn.prepareCall(sql);
             BufferedWriter bw = new BufferedWriter(new FileWriter(filePath))) {

            cs.setInt(1, minCat);
            cs.setInt(2, maxCat);

            try (ResultSet rs = cs.executeQuery()) {
                bw.write("Name,Address,Category\n");
                while (rs.next()) {
                    String name = rs.getString("name");
                    String address = rs.getString("address");
                    int category = rs.getInt("category");

                    bw.write(String.format("\"%s\",\"%s\",%d%n", name, address, category));
                    count++;
                }
            }
            System.out.println("[Success]: Successfully exported " + count + " customer(s) to " + filePath + ".");
        } catch (IOException e) {
            System.err.println("[File Write Error]: " + e.getMessage());
        }
    }
}
