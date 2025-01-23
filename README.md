# Revised Project Plans for IoT Solutions

## Integration of AWS S3 and Google Cloud Platform for Storing and Analyzing IoT Data

### Project Goals
- Ensure efficient storage of telemetry from IoT devices (Shelly EM) using AWS S3.
- Utilize Google Cloud Platform tools for scalable and efficient data analysis.
- Transition towards a fully integrated system that supports both real-time and batch processing.

### Implementation Stages

#### Stage 0: Sensor Setup and Configuration
1. **Physical Connection of the Sensor**
   - Install and safely connect the Shelly EM device to the power supply and network.
2. **Mobile App Setup**
   - Configure the mobile app for initial management of the sensor.
3. **MQTT Configuration**
   - Set up Shelly EM to transmit telemetry data to AWS IoT Core via MQTT, ensuring proper topic definitions and secure authentication.
4. **AWS IoT Core Rule Configuration**
   - Create rules in AWS IoT Core to forward telemetry data to Amazon S3 for storage.

#### Stage 1: Data Storage in Amazon S3
1. **S3 Bucket Setup**
   - Create and configure an S3 bucket with lifecycle management for cost optimization.
   - Secure the bucket with appropriate IAM policies to control access.
2. **Automated Data Transfer**
   - Configure AWS IoT Core rules to ensure seamless data transfer to the S3 bucket.

#### Stage 2: Integration with Google Cloud Platform
1. **Accessing AWS S3 Data from GCP**
   - Use Google Cloud Storage Transfer Service for regular imports from S3 to GCP.
   - Set up IAM roles and service accounts for secure cross-cloud access.
2. **Data Synchronization**
   - Automate the data synchronization process to ensure GCP receives daily aggregated JSONL files from AWS S3.

#### Stage 3: Data Processing and Analysis
1. **Data Aggregation**
   - Aggregate JSON objects into daily JSONL files using AWS Lambda and State Machines for efficient storage.
2. **BigQuery Analysis**
   - Import aggregated data into BigQuery and create SQL queries to analyze power consumption patterns.
3. **Data Visualization**
   - Use Looker Studio (Google Data Studio) to build dashboards that provide insights into household power usage and costs.

### Adjustments Based on Prior Work
- Emphasis on **data aggregation at AWS S3 level** to minimize operational costs in GCP.
- Utilization of **BigQuery external tables** to avoid redundant data replication.
- Introduction of **integral-based calculations** for energy consumption within non-uniform time intervals.

### Security Measures
- Ensure data encryption during storage and transmission.
- Regularly review and update access controls to align with best practices.

### Resource Optimization
- Optimize S3 storage and GCP processing costs based on historical usage patterns.
- Transition unused raw data to AWS Glacier for cost-effective archiving.

### Backup and Recovery
- Implement robust backup policies for both AWS and GCP to ensure data reliability.
- Test recovery plans periodically to confirm data availability during failures.

### Monitoring and Logging
- Set up CloudWatch (AWS) and Google Cloud Monitoring to track system performance.
- Log critical events in both clouds to enable troubleshooting and usage analysis.

### Versioning and Documentation
- Maintain detailed version control for infrastructure configurations and scripts.
- Document all configurations, workflows, and processes to ensure project scalability and maintenance.

### Future Plans
- Explore integration with solar energy generation data (e.g., Photovoltaic Geographical Information System).
- Investigate potential savings by shifting energy consumption patterns based on multi-zone tariff models.
- Develop more advanced analysis using PySpark or machine learning for predictive energy management.

### Final Measures
- Conduct thorough testing of the entire pipeline from sensor setup to data analysis.
- Deploy the system into a production environment with adequate training and support for users.
- Monitor and refine the system as more data is collected and analyzed.

### Key Takeaway
The updated plan leverages lessons learned from previous implementations to improve scalability, cost efficiency, and analytic capabilities, ensuring a robust and user-friendly IoT solution.
