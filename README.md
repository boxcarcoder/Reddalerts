# Server-Side for Reddalerts

## Reddalerts

An application for users to monitor their favorite Subreddits from the website, Reddit, based on specified keywords.
![image](https://user-images.githubusercontent.com/5587071/130664603-e4625320-6d93-48c0-9c96-f37f4f5e998b.png)

<img width="1278" alt="Screen Shot 2022-01-31 at 8 42 26 AM" src="https://user-images.githubusercontent.com/5587071/151835460-74b140a0-5d34-4359-8da1-b76020dc81d4.png">

<img width="1279" alt="Screen Shot 2022-01-31 at 8 44 38 AM" src="https://user-images.githubusercontent.com/5587071/151835881-3cea68ee-d300-4bfa-88ab-34f94448c7fe.png">

<img width="1278" alt="Screen Shot 2022-01-31 at 8 47 21 AM" src="https://user-images.githubusercontent.com/5587071/151836281-c499d0b2-89d8-4004-ab4c-7dfb14337493.png">

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

## Thoughts and Overview
Learning how to design and implement a SQL database has been both challenging and rewarding. My initial design included a many-to-many relationship between `users` and `subreddits`, as well as a many-to-many relationship between `subreddits` and `keywords`. At first, it made sense since one user can have many subreddits while one subreddit can be monitored by many users. In addition, one subreddit can have many keywords while one keyword can belong to many subreddits.

However, problems arose when the combinations of `users`, `subreddits`, and `keywords` were not unique. If `user1` is monitoring `subreddit1` for `keyword1`, and `user2` is also monitoring `subreddit1` but decides to monitor the subreddit for `keyword2`, `keyword2` is appended to `subreddit1` despite `user1` not monitoring for `keyword2`. In order to maintain unique combinations, I had to change the design to use an `association object` that held all three foreign keys rather than `association tables`. Most of the API routes then query the association object table to find and use unique combinations.

The usage of Flask as a micro web framework gave me the tools to write a server that contains API routes, and to treat the server as an application that can create tables and access a database. During development, I used the Flask Shell to query the SQLite database and for production, I used MySQL workbench, which I found to be very useful for viewing the contents of tables in a convenient graphical interface.

Writing the server-side in Python and client-side in Javascript emphasized the usefulness of transferring data in a standard form. In my application, data is sent between the server-side and client-side using JSON. To serialize the response data of my API routes, I created a serializer class mixin for my database models that converts the data in each table into a dictionary of key-value pairs.

SQLAlchemy has been particularly helpful in writing an application that deals with SQL and a SQL database. The ability to achieve what SQL code should do while writing in Python has been a great learning experience for me who has done object-oriented design. The use of `classes` and `attributes` to create tables and columns, as well as the use of methods on these tables such as `querying, filtering, and join`, has been more intuitive than writing SQL commands such as `CREATE, SELECT, and JOIN`. Not to say I won't learn SQL, but rather, it has been a great beginning step as I dive more into the world of SQL and SQL databases.
