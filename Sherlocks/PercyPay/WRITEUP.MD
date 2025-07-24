# HTB Write-Up: [Challenge/Box Name]

![BOX Screenshot](https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com/challenges/9232fe81225bcaef853ae32870a2b0fe.png)

## Table of Contents

1. [Challenge Overview](#challenge-overview)
3. [Guided Questions](#guided-questions)
    1. [Which S3 bucket was the affected file stored in?](#which-s3-bucket-was-the-affected-file-stored-in)
    2. [Which AWS IAM user interacted with the file?](#which-aws-iam-user-interacted-with-the-file)
    3. [What AWS Access Key should be revoked as part of the response action?](#what-aws-access-key-should-be-revoked-as-part-of-the-response-action)
    4. [What was the Threat Actor's (TA) IP address?](#what-was-the-threat-actors-ta-ip-address)
    5. [What was the blast radius, and how many files were impacted?](#what-was-the-blast-radius-and-how-many-files-were-impacted)
    6. [Which customer's data has been impacted?](#which-customers-data-has-been-impacted)
    7. [What date was the payment data from?](#what-date-was-the-payment-data-from)
    8. [What was the time for the initial event from this user?](#what-was-the-time-for-the-initial-event-from-this-user)
    9. [How many IP addresses did the TA use for this user?](#how-many-ip-addresses-did-the-ta-use-for-this-user)
    10. [What was the first action the TA performed?](#what-was-the-first-action-the-ta-performed)
    11. [What was the first IAM Policy the TA reviewed?](#what-was-the-first-iam-policy-the-ta-reviewed)
    12. [What operation did the TA perform to alter IAM Policy permissions available to the user?](#what-operation-did-the-ta-perform-to-alter-iam-policy-permissions-available-to-the-user)
    13. [Which IAM Policy was next utilized by the TA?](#which-iam-policy-was-next-utilized-by-the-ta)
    14. [What was the ARN of the next resource the TA created?](#what-was-the-arn-of-the-next-resource-the-ta-created)
    15. [Which user created the resource?](#which-user-created-the-resource)
    16. [The role given to the resource is different from that of the creating user; which IAM action has likely been used?](#the-role-given-to-the-resource-is-different-from-that-of-the-creating-user-which-iam-action-has-likely-been-used)
    17. [What action did the TA-created Lambda Function perform?](#what-action-did-the-ta-created-lambda-function-perform)
    18. [What Policy was assigned to which user?](#what-policy-was-assigned-to-which-user)
    19. [What AWS service did the user conduct discovery activity against next?](#what-aws-service-did-the-user-conduct-discovery-activity-against-next)
    20. [What was the ID of the detector the TA deleted?](#what-was-the-id-of-the-detector-the-ta-deleted)
    21. [Which AWS service did the user target next for discovery activities?](#which-aws-service-did-the-user-target-next-for-discovery-activities)
    22. [What is the ARN of the response to the aforementioned request by the TA?](#what-is-the-arn-of-the-response-to-the-aforementioned-request-by-the-ta)
    23. [What was the TA's first action with S3?](#what-was-the-tas-first-action-with-s3)
    24. [Immediately before exfiltration, what was the TA's final request?](#immediately-before-exfiltration-what-was-the-tas-final-request)
    25. [After the exfiltration, what Role did the TA create?](#after-the-exfiltration-what-role-did-the-ta-create)
    26. [What was the name of the Policy applied to that role?](#what-was-the-name-of-the-policy-applied-to-that-role)
    27. [The Policy allows `s3:ReplicateObject` action for what resource?](#the-policy-allows-s3replicateobject-action-for-what-resource)
    28. [The TA attempted the 'PutBucketReplication' action; what was the error message?](#the-ta-attempted-the-putbucketreplication-action-what-was-the-error-message)
    29. [What IAM User did the TA create?](#what-iam-user-did-the-ta-create)
    30. [When was the AdministratorAccess policy attached to the newly created user?](#when-was-the-administratoraccess-policy-attached-to-the-newly-created-user)
    31. [What was the Access Key ID for the new user?](#what-was-the-access-key-id-for-the-new-user)
    32. [What time was the new user first used?](#what-time-was-the-new-user-first-used)
    33. [For this user, what IP address was the TA using?](#for-this-user-what-ip-address-was-the-ta-using)
    34. [What Service did the TA stop?](#what-service-did-the-ta-stop)
    35. [What anomaly user event occurred before the original User was compromised?](#what-anomaly-user-event-occurred-before-the-original-user-was-compromised)
    36. [What was the ARN for the resource uploaded to `percypay-website-host`?](#what-was-the-arn-for-the-resource-uploaded-to-percypay-website-host)
    37. [What was the Access Key Secret for the original compromised user?](#what-was-the-access-key-secret-for-the-original-compromised-user)
4. [Conclusion](#conclusion)

---

## Challenge Overview

- **Name**: PercyPay
- **Category**: Sherlock
- **Difficulty**: Easy
- **Description**:  
    You are working for an innovative new payment provider, PercyPay, who are revolutionising the financial technology landscape with their cutting-edge solutions and customer-centric approach. There's a new Cyber Threat Intelligence Analyst as part of your team, and they're still finding their feet, understanding the business and our SecOps processes. They're just come across what appears to be some valuable information, but asking the wider team for support to help understand how real it is. And if real, what's the next steps and impact seen. On AlphaBay (a dark web marketplace), PercyPay customer data has been listed for sale. There is no further information about quantities, or what type of data, but a single sample file has been made available as proof. The filename is `CustomerB-2024-12-09-f97a1bcc-7.json`. 
- **Created By**: b3ngriffiths
- **Date**: [07/17/2025]

---

| Acronym     | Meaning                                                 |
| :---------- | :------------------------------------------------------ |
| TARGET_IP   | Spawned Target Machine IP Address                       |
| TARGET_PORT | Spawned Target Machine Port                             |
| PMN_BOX     | Personal Machine with a Connection to the Academy's VPN |
| PWN_IP      | Pwnbox IP Address (or PMVPN IP Address)                 |
| PWN_PORT    | Pwnbox Port (or PMVPN Port)                             |

---

## Initial Analysis :

## Guided Questions

1. Which S3 bucket was the affected file stored in?
2. Which AWS IAM user interacted with the file?
3. What AWS Access Key should be revoked as part of the response action?
4. What was the Threat Actor's (TA) IP address?
5. What was the blast radius, and how many files were impacted?
6. Which customer's data has been impacted?
7. What date was the payment data from?
8. What was the time for the initial event from this user?
9. How many IP addresses did the TA use for this user?
10. What was the first action the TA performed?
11. What was the first IAM Policy the TA reviewed?
12. What operation did the TA perform to alter IAM Policy permissions available to the user?
13. Which IAM Policy was next utilized by the TA?
14. What was the ARN of the next resource the TA created?
15. Which user created the resource?
16. The role given to the resource is different from that of the creating user; which IAM action has likely been used?
17. What action did the TA-created Lambda Function perform?
18. What Policy was assigned to which user?
19. What AWS service did the user conduct discovery activity against next?
20. What was the ID of the detector the TA deleted?
21. Which AWS service did the user target next for discovery activities?
22. What is the ARN of the response to the aforementioned request by the TA?
23. What was the TA's first action with S3?
24. Immediately before exfiltration, what was the TA's final request?
25. After the exfiltration, what Role did the TA create?
26. What was the name of the Policy applied to that role?
27. The Policy allows `s3:ReplicateObject` action for what resource?
28. The TA attempted the 'PutBucketReplication' action; what was the error message?
29. What IAM User did the TA create?
30. When was the AdministratorAccess policy attached to the newly created user?
31. What was the Access Key ID for the new user?
32. What time was the new user first used?
33. For this user, what IP address was the TA using?
34. What Service did the TA stop?
35. What anomaly user event occurred before the original User was compromised?
36. What was the ARN for the resource uploaded to `percypay-website-host`?
37. What was the Access Key Secret for the original compromised user?

## Conclusion
