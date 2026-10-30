# Primary-source register

Research checked: **2026-10-29**. Baseline: **OWASP ASVS 5.0.0**, **WSTG v4.2**, **API Security Top 10 2023**. ASVS supplies verification requirements; WSTG supplies test techniques; API/LLM Top 10 lists are awareness taxonomies, not complete audit standards. This catalog is a broad synthesis, not full conformance or every known exploit.

Source IDs below are used by each control in controls.json and the HTML. Living documentation may change; re-open the official material, choose the deployed version and record the access date during each audit. Require fresh vendor CVE/security-advisory and support-lifecycle checks for exact versions, lockfiles, images, modules and transitive dependencies. A source link does not mean the associated control was tested.

The Odoo entry uses official versioned documentation source because the rendered page timed out during research. Match the deployed Odoo version before applying it. Some URLs redirect to newer official project domains; the versioned baseline remains explicit. Source entries may repeat a publication under domain-specific IDs to preserve control references.

- **ID-ASVS** — [OWASP Application Security Verification Standard](https://github.com/OWASP/ASVS/releases/tag/v5.0.0_release). 5.0.0 (released 2025-05-30); verified stable baseline, not bleeding edge. Checked 2026-10-29.

- **ID-WSTG** — [OWASP Web Security Testing Guide](https://wstg.owasp.org/v4.2/). 4.2 (stable selector verified); use versioned links. Checked 2026-10-29.

- **ID-NIST-TEST** — [NIST SP 800-115: Technical Guide to Information Security Testing and Assessment](https://csrc.nist.gov/pubs/sp/800/115/final). Final, September 2008; planning/process reference, not current exploit catalog. Checked 2026-10-29.

- **ID-ATTACK-SURFACE** — [OWASP Attack Surface Analysis Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-THREAT-MODEL** — [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-API-AUTH** — [OWASP API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/). API Security Top 10, 2023 edition. Checked 2026-10-29.

- **ID-NIST-AUTH** — [NIST SP 800-63B-4: Authentication and Authenticator Management](https://pages.nist.gov/800-63-4/sp800-63b.html). Revision 4, final 2025; apply requirements for the selected assurance target. Checked 2026-10-29.

- **ID-AUTHENTICATION** — [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-PASSWORD-STORAGE** — [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html). Living documentation; recheck algorithm/cost guidance at audit. Checked 2026-10-29.

- **ID-MFA** — [OWASP Multifactor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-FORGOT** — [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-SESSION** — [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-JWT** — [IETF RFC 8725: JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725). RFC 8725 / BCP 225, February 2020; check errata and updates. Checked 2026-10-29.

- **ID-OAUTH-RFC** — [IETF RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700). RFC 9700 / BCP 240, January 2025; check errata and updates. Checked 2026-10-29.

- **ID-OAUTH** — [OWASP OAuth2 Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-SAML** — [OWASP SAML Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-PASSKEY** — [OWASP Passkey Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Passkey_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-AUTHORIZATION** — [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-API-BOLA** — [OWASP API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/). API Security Top 10, 2023 edition. Checked 2026-10-29.

- **ID-API-FUNCTION** — [OWASP API5:2023 Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/). API Security Top 10, 2023 edition. Checked 2026-10-29.

- **ID-API-PROPERTY** — [OWASP API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/). API Security Top 10, 2023 edition. Checked 2026-10-29.

- **ID-TENANT** — [OWASP Multi Tenant Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-MASS** — [OWASP Mass Assignment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-NEXT-AUTH** — [Next.js: How to implement authentication](https://nextjs.org/docs/app/guides/authentication). Living App Router documentation; match installed Next.js version at audit. Checked 2026-10-29.

- **ID-CSRF** — [OWASP Cross-Site Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-CORS** — [MDN: Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS). Living browser-platform documentation; recheck at audit. Checked 2026-10-29.

- **ID-CSP** — [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-CLICKJACK** — [OWASP Clickjacking Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-HEADERS** — [OWASP HTTP Security Response Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-REDIRECT** — [OWASP Unvalidated Redirects and Forwards Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-HTML5** — [OWASP HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-CACHE** — [OWASP Web Cache Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Web_Cache_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-PRIVACY** — [OWASP User Privacy Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-INPUT** — [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-SQL** — [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-NOSQL** — [OWASP NoSQL Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/NoSQL_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-CMD** — [OWASP OS Command Injection Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-JINJA** — [Jinja sandbox security considerations](https://jinja.palletsprojects.com/en/stable/sandbox/). 3.1.x documentation; match deployed version. Checked 2026-10-29.

- **APP-XXE** — [OWASP XML External Entity Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-DESER** — [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-PROTOTYPE** — [OWASP Prototype Pollution Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-XSS** — [OWASP Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-DOM** — [OWASP DOM based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-INJECT** — [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-CSV** — [OWASP CSV Injection](https://community.owasp.org/attacks/CSV_Injection). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-UPLOAD** — [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-WSTG-UPTYPE** — [OWASP WSTG: Test Upload of Unexpected File Types](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/10-Business_Logic_Testing/08-Test_Upload_of_Unexpected_File_Types/). WSTG v4.2, WSTG-BUSL-08. Checked 2026-10-29.

- **APP-WSTG-UPMAL** — [OWASP WSTG: Test Upload of Malicious Files](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/10-Business_Logic_Testing/09-Test_Upload_of_Malicious_Files/). WSTG v4.2, WSTG-BUSL-09; use this package's safer test policy. Checked 2026-10-29.

- **APP-PATH** — [OWASP WSTG: Testing Directory Traversal File Include](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/05-Authorization_Testing/01-Testing_Directory_Traversal_File_Include/). WSTG v4.2, WSTG-ATHZ-01. Checked 2026-10-29.

- **APP-TAR** — [Python tarfile extraction filters](https://docs.python.org/3/library/tarfile.html#extraction-filters). Python 3 documentation; match deployed interpreter and extraction-filter behavior. Checked 2026-10-29.

- **APP-REST** — [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-GQL** — [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-WS** — [OWASP WebSocket Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-SSRF** — [OWASP Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-SMUGGLE** — [OWASP WSTG: Testing for HTTP Splitting/Smuggling](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/07-Input_Validation_Testing/15-Testing_for_HTTP_Splitting_Smuggling/). WSTG v4.2, WSTG-INPV-15. Checked 2026-10-29.

- **APP-API4** — [OWASP API4:2023 Unrestricted Resource Consumption](https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption/). OWASP API Security Top 10, 2023. Checked 2026-10-29.

- **APP-API6** — [OWASP API6:2023 Unrestricted Access to Sensitive Business Flows](https://api-security.owasp.org/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/). OWASP API Security Top 10, 2023. Checked 2026-10-29.

- **APP-DOS** — [OWASP Denial of Service Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-AI1** — [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/). OWASP LLM Top 10, 2025. Checked 2026-10-29.

- **APP-AI2** — [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/). OWASP LLM Top 10, 2025. Checked 2026-10-29.

- **APP-AI5** — [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/). OWASP LLM Top 10, 2025. Checked 2026-10-29.

- **APP-AI6** — [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/). OWASP LLM Top 10, 2025. Checked 2026-10-29.

- **APP-AI10** — [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/). OWASP LLM Top 10, 2025. Checked 2026-10-29.

- **APP-NEXT** — [Next.js: How to think about data security](https://nextjs.org/docs/app/guides/data-security). App Router living documentation, page updated 2026-10-06; match deployed Next.js/React. Checked 2026-10-29.

- **APP-NODE** — [Node.js Security Best Practices](https://nodejs.org/learn/getting-started/security-best-practices). Living documentation; recheck at audit. Checked 2026-10-29.

- **APP-PYTHON** — [Python Security Considerations](https://docs.python.org/3/library/security_warnings.html). Python 3 documentation; match deployed interpreter. Checked 2026-10-29.

- **APP-DJANGO** — [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/). Django 5.2 documentation; match deployed framework version. Checked 2026-10-29.

- **APP-DOTNET** — [ASP.NET Core security topics](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-10.0). ASP.NET Core 10.0 documentation; match deployed version. Checked 2026-10-29.

- **APP-DOTNET-PROXY** — [Configure ASP.NET Core for proxy servers and load balancers](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/proxy-load-balancer?view=aspnetcore-10.0). ASP.NET Core 10.0 documentation; match deployed version. Checked 2026-10-29.

- **APP-BINARYFORMATTER** — [Microsoft: Deserialization risks in BinaryFormatter and related types](https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide). .NET Framework / .NET guidance; recheck at audit. Checked 2026-10-29.

- **OPS-PAYMENT** — [OWASP Third Party Payment Gateway Integration Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Payment_Gateway_Integration_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-TRANSACTION** — [OWASP Transaction Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-STATUS** — [Stripe Payment status updates](https://docs.stripe.com/payments/payment-intents/verifying-status). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-WEBHOOK** — [Stripe Receive events in your webhook endpoint](https://docs.stripe.com/webhooks). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-IDEMPOTENCY** — [Stripe Idempotent requests](https://docs.stripe.com/api/idempotent_requests). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-BUSINESS** — [OWASP Business Logic Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Business_Logic_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-ODOO** — [Odoo Security in Odoo (official documentation source)](https://raw.githubusercontent.com/odoo/documentation/19.0/content/developer/reference/backend/security.rst). Odoo documentation branch 19.0; use the deployed version's documentation. Checked 2026-10-29.

- **OPS-API10** — [OWASP API10 Unsafe Consumption of APIs](https://api-security.owasp.org/editions/2023/en/0xaa-unsafe-consumption-of-apis/). OWASP API Security Top 10 2023. Checked 2026-10-29.

- **OPS-THIRDJS** — [OWASP Third Party JavaScript Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-PRIVACY** — [OWASP User Privacy Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-SECRETS** — [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-CRYPTO** — [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-TLS** — [OWASP Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-SBOM** — [GitHub Exporting a software bill of materials](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/export-dependencies-as-sbom). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-SUPPLY** — [OWASP Software Supply Chain Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-NEXT** — [Next.js official security advisories](https://github.com/vercel/next.js/security/advisories). Live advisory index; exact deployed-version review required at every audit. Checked 2026-10-29.

- **OPS-NODE** — [Node.js security release announcements](https://nodejs.org/en/blog/vulnerability). Live advisory index; exact deployed-version review required at every audit. Checked 2026-10-29.

- **OPS-PYTHON** — [Python Security and vulnerability handling](https://www.python.org/dev/security/). Living security policy; follow current CPython and framework advisories at audit. Checked 2026-10-29.

- **OPS-DOTNET** — [Official .NET runtime security advisories](https://github.com/dotnet/runtime/security/advisories). Live advisory index; also check ASP.NET Core and deployed package advisories. Checked 2026-10-29.

- **OPS-GHA** — [GitHub Actions Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-OIDC** — [GitHub Actions OpenID Connect](https://docs.github.com/en/actions/concepts/security/openid-connect). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-DOCKER** — [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-IAM** — [AWS IAM security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-S3** — [AWS S3 Blocking public access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-SIGNED** — [AWS S3 Download and upload objects with presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-VPC** — [AWS VPC security best practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-ORIGIN** — [AWS CloudFront Restrict access to Application Load Balancers](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/restrict-access-to-load-balancer.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-IMDS** — [AWS EC2 Instance Metadata Service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-RDS** — [AWS Security in Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-CLOUDTRAIL** — [AWS CloudTrail security best practices](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/best-practices-security.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-LOGGING** — [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-VAULT** — [AWS Backup Vault Lock](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-BACKUP** — [AWS Backup Restore testing](https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **OPS-INCIDENT** — [AWS Well-Architected SEC10-BP02 Develop incident management plans](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_incident_response_develop_management_plans.html). Living documentation; recheck at audit. Checked 2026-10-29.

- **ID-HOST** — [OWASP WSTG: Testing for Host Header Injection](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/07-Input_Validation_Testing/17-Testing_for_Host_Header_Injection/). WSTG v4.2, WSTG-INPV-17. Checked 2026-10-29.
