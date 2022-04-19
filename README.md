# Recipe Generator and Nutrition App - Freestyle Project (Python)

# Installation/Setup 

Navigate to an appropriate space on your Desktop to store your code:
```sh
cd ~/Desktop/freestyle-project-2022/
```

Use Anaconda to create and activate a new virtual environment, perhaps called "freestyle-env":
```sh
conda create -n freestyle-env python=3.8
conda activate freestyle-env
```

Then, within an active virtual environment, install package dependencies:
```sh
pip install -r requirements.txt
```

# Configuration 

## SendGrid API Key Setup
First, [sign up for a SendGrid account](https://app.sendgrid.com/login?redirect_to=%2Fsettings%2Fapi_keys), then follow the instructions to complete your "Single Sender Verification", clicking the confirmation email to verify your account. 
NOTE: some users in the passed have reported issues with using yahoo-issued, university-issued, or work-issued emails in the past. Consequently, if you run into similar issues when attempt to set up your SendGrid account, perhaps consider using a personal Gmail account. 

Then, [create your SendGrid API Key with "full access" permissions](https://app.sendgrid.com/login?redirect_to=%2Fsettings%2Fapi_keys). Once you create your SendGrid API Key, we will want to store the API Key in an environment variable in the .env file called ```SENDGRID_API_KEY```. Also set an environment variable called ```SENDER_ADDRESS``` to be the same email address as the single sender address you just associated with your SendGrid account.

Use a ".env" file approach to manage these files, as mentioned in the ".env file approach" section below.


# Environment Variables - ".env" File Approach
You must set up a local file named ".env" that is outside the root directory of the project. In this file, you will be able to store the necessary environment variables to run the program. For the purposes of the shopping-cart program, the following code will suffice:
```sh
# this is the .env file

# for the sengrid email bonus assignment
SENDGRID_API_KEY="SENDGRID_API_KEY"
SENDER_ADDRESS="SENDER_ADDRESS"

# for the google sheet bonus assignment  -- Don't Know if this is necessary 
GOOGLE_SHEET_ID="1_hisQ9kNjmc-cafIasMue6IQG-ql_6TcqFGpVNOkUSE"
SHEET_NAME="shopping-clean"

#For Tax Rate
TAX_RATE=0.0875
```
Note that you will need to update the values of the SendGrid environment variables to meet your specific API key and email address that you created in your SendGrid account (instructions for that mentioned in the "SendGrid API Key Setup" Section)

