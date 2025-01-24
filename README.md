# Designing a Secure Database Architecture for Banking Firms

## Authors
- Saroj Baral
- Hirva Patel
- Chris Witt

## Overview
This project outlines the design of a secure database architecture tailored for banking firms. It highlights critical components necessary for securing sensitive data, ensuring data integrity, and implementing role-based access control policies.

---

## Key Components of the Security Architecture
1. **Access Control Policy**:
   - Implemented using a **Role-Based Access Control (RBAC)** model.
   - Defined roles include:
     - **Admin**: Highest access privileges.
     - **Employee**: Moderate access for managing operations.
     - **Advisor**: Restricted access based on advisory needs.
     - **Client**: Limited access to personal account information.

2. **Data Classification & Encryption**:
   - Sensitive fields (e.g., credit card numbers, passwords, SSNs) are encrypted to protect against unauthorized access.

3. **Data Integrity & Validation**:
   - Measures include:
     - Buffer overflow control.
     - Validation of input data to prevent corruption or malicious input.

---

## Security Features
- **Access Policy**:
  - A hierarchical RBAC model with layered permissions.
- **Encryption**:
  - Sensitive data fields are secured using robust encryption techniques.
- **Data Validation**:
  - Ensures all input data adheres to pre-defined formats and avoids vulnerabilities like buffer overflows.

---

## Future Work
- Enhance encryption methods with post-quantum cryptography.
- Implement automated auditing tools to monitor access logs and data integrity.
- Extend the schema to include multi-factor authentication (MFA) support.

---

## How to Use
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-name/secure-database-architecture.git
