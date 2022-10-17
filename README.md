## SEP_PROJECT
<h2>Face Biometrics in public transportation systems</h2>
Tools used: Python, Amazon Web Services (S3, Amazon Rekognition, RDS), AWS Python SDK(Boto3), OpenCV, MySQL<br><br>

## Setup
<p>
1. Setup AWS Credentials
  
  ```
  sudo apt install awscli
  ```

After installing AWSCLI, use your Secret Keys generated from IAM to config local system with AWS.
  
```
aws configure
```
  
Enter your Access Key ID, Secret Access key and default region name.<br>
<br>
2. Configure a MySQL server and edit the config-example.json file to update the server endpoint, database name, password and port. Rename the file to config.json
```
mv config-example.json config.json
```
<br>
3. Clone the repository and install the require packages.
  
```console
https://github.com/cr-trojan23/project3006.git
cd project3006
pip3 install -r requirements.txt
python3 main.py
```
  
</p>


## Infrastructure
![INFRA](https://raw.githubusercontent.com/cr-trojan23/project3006/cloud-based/infrastructure.png)

