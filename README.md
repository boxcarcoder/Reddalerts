# Server-Side for Reddalerts

## Reddalerts

An application for users to monitor their favorite Subreddits from the website, Reddit, based on specified keywords.

![image](https://user-images.githubusercontent.com/5587071/130664603-e4625320-6d93-48c0-9c96-f37f4f5e998b.png)

![image](https://user-images.githubusercontent.com/5587071/130667161-b3c9538a-4227-49a1-b7ce-d828784c3625.png)

![image](https://user-images.githubusercontent.com/5587071/130664934-53a7342d-8870-4173-a5ec-a3c68e7f89dd.png)

## Installation And Set Up

Make sure `python3`, `pip`, and `pipenv` are installed in the current machine.
If the machine runs MacOS, make sure `GCC` is installed by running `xcode-select --install`.

1. Clone the repository: https://github.com/boxcarcoder/Reddalerts.git
2. Set up and activate a virtual environment for the repository's dependencies:
    - install the `venv` module: `python3 -m venv venv_name`
    - activate the virtual environment: `source venv_name/bin/activate`
3. Install all dependencies into the virtual environment: `pip3 install -r requirements.txt`
4. Start the server: 
    - confirm the virtual environment is activated.
    - run: `flask run`.

## Visit the Deployed Application

Link: https://reddalerts.com/

This application is deployed with the following configurations:
- Flask application is configured with CORS to allow requests from my client-side domains.
- Flask application is deployed to AWS Elastic Beanstalk. 
- The Elastic Beanstalk environment is configured with a load balancer to listen for domains listed on my client-side SSL certificate.
- My CloudFlare DNS server uses CNAME records to redirect API requests to the Elastic Beanstalk environment through domains listed on the SSL certificate.
- The MySQL database is hosted on AWS RDS.
