# Blockchain POC
# Providers-Node - API Service Management 🌐

## 📌 Description
Providers-Node is a **Node.js-powered API management tool** designed to streamline provider interactions, optimize request handling, and ensure efficient service integration.

## 🎯 Project Objectives
- **Simplify API provider management** for seamless integration.
- **Enhance request handling** with optimized workflows.
- **Improve service reliability** through structured interactions.

## 🔥 Key Features
- **Automated API request processing**.
- **Secure authentication** for provider access.
- **Optimized data handling** for improved performance.

## 🛠️ Technologies Used
- **Backend:** Node.js, Express.js
- **Database:** MongoDB or SQL-based storage
- **Authentication:** JWT, OAuth
- **Version Control:** GitHub

## 🏗️ Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/GJHR-6/Providers-node.git
## AWS Lambda function code

Under zventus_blockchain we have a poetry installable package that will be packaged and uploaded to the lambda function we will be using for poc V2.

## Packaging the lambda function

You need to go to the lambda folder like this:

```bash
cd zventus_blockchain 
```

then run

```bash
make install
```

and if you want to zip it

```bash
make zip_lambda
```

You can then upload this artifact.zip into AWS. Ideally you setup a GitHub action to do all the steps above and even uploading it to lambda automatically after passing some unit tests to make sure the new version is not broken.
