# HTB Write-Up: [Challenge/Box Name]

![BOX Screenshot](../files/phantomcheck.png)

## Table of Contents

1. [Challenge Overview](#challenge-overview)

2. [Answers](#answers)
    1. [Which WMI class did the attacker use to retrieve model and manufacturer information for virtualization detection?](#which-wmi-class-did-the-attacker-use-to-retrieve-model-and-manufacturer-information-for-virtualization-detection)
    2. [Which WMI query did the attacker execute to retrieve the current temperature value of the machine?](#which-wmi-query-did-the-attacker-execute-to-retrieve-the-current-temperature-value-of-the-machine)
    3. [The attacker loaded a PowerShell script to detect virtualization. What is the function name of the script?](#the-attacker-loaded-a-powershell-script-to-detect-virtualization-what-is-the-function-name-of-the-script)
    4. [Which registry key did the above script query to retrieve service details for virtualization detection?](#which-registry-key-did-the-above-script-query-to-retrieve-service-details-for-virtualization-detection)
    5. [The VM detection script can also identify VirtualBox. Which processes is it comparing to determine if the system is running VirtualBox?](#the-vm-detection-script-can-also-identify-virtualbox-which-processes-is-it-comparing-to-determine-if-the-system-is-running-virtualbox)
    6. [The VM detection script prints any detection with the prefix 'This is a'. Which two virtualization platforms did the script detect?](#the-vm-detection-script-prints-any-detection-with-the-prefix-this-is-a-which-two-virtualization-platforms-did-the-script-detect)
7. [Conclusion](#conclusion)

---

## Challenge Overview

- **Name**: OPhantom Check
- **Category**: Sherlock
- **Difficulty**: Very Easy
- **Description**: Talion suspects that the threat actor carried out anti-virtualization checks to avoid detection in sandboxed environments. Your task is to analyze the event logs and identify the specific techniques used for virtualization detection. Byte Doctor requires evidence of the registry checks or processes the attacker executed to perform these checks.
- **Created By**:  iamr007
- **Co-Authors**: [Tier]
- **Date**: [06/06/2025]

## Answers

1. Which WMI class did the attacker use to retrieve model and manufacturer information for virtualization detection?

2. Which WMI query did the attacker execute to retrieve the current temperature value of the machine?

3. The attacker loaded a PowerShell script to detect virtualization. What is the function name of the script?

4. Which registry key did the above script query to retrieve service details for virtualization detection?

5. The VM detection script can also identify VirtualBox. Which processes is it comparing to determine if the system is running VirtualBox?

6. The VM detection script prints any detection with the prefix 'This is a'. Which two virtualization platforms did the script detect?


## Conclusion

## Sample Table

| Name          | Age | Occupation        | Location      |
| ------------- | --- | ----------------- | ------------- |
| John Doe      | 29  | Software Engineer | New York      |
| Jane Smith    | 34  | Data Scientist    | San Francisco |
| Alice Johnson | 25  | UX Designer       | London        |
| Bob Brown     | 40  | Product Manager   | Berlin        |
