# About:
This project is a simple API built using FastAPI to register and obtain basic information about users.

# API:
1. GET: /person/<id>
    - Returns `{id: <id>, email: <person_email}`
2. POST: /person/
    - Creates a Person (or user account)
    - Creates and sends a fake e-mail with first and last name in subject
    - Returns
    ```
    {
        'first_name': <first_name>,
        'last_name': <last_name>,
        'email': <user_email>,
        'id': <newly_created_id>
    }
    ```

2. PUT: /person/<id>
    - Updates a Person's data
    - Returns
    ```
    {
        'first_name': <first_name>,
        'last_name': <last_name>,
        'email': <user_email>,
        'id': <existing_id>
    }
    ```

# Prerequistes:
- Docker Desktop with Kubernetes enabled
- kubectl (k8s CLI tool)
- Python 3.8
- kubectl (`brew install kubectl`)

# How to run locally:
1. Pull the repo from Github.
2. While in `/src`, open a terminal tab and enter `uvicorn main:app --reload`.
3. To see the email messages, in a separate tab, create a local SMTP server: `python -m smtpd -n -c DebuggingServer localhost:1025`

# How to deploy
1. Have Docker Desktop running, and make sure there is a green dot next to Kubernetes when you click on the Docker icon in the Menu Bar.
2. Use kubectl to deploy the application `kubectl apply -f config.yaml`.
3. You can check the deployments and services by executing `kubectl get deployments`, or `kubectl get services`, respectively.
4. If step 3 is successful, you should be able to see the application at `localhost:30001`.

# Assumptions:
1. For simplicity, I have not required HTTPS for the app, nor SSL for email. Obviously, for an application that involves user data, both of these would have been implemented.
2. I chose SQL over NoSQL as user data tends to be highly relational. Additionally, we can have an async connection with our DB since we have async/await at our disposal, allowing the single thread to work on multiple tasks.
3. I am assuming all user input entered is valid. This includes only letters in names and e-mails being both properly formatted and verifiable.
4. For e-mails, I just wanted to create proof of concept. In production, a service such as mailgun or sendgrid should be used.
5. When I started the app, my goal was to getting a working application locally, so following the FastAPI tutorials seemed like the quickest route. However, when I factor in deploying a stateful application, using sqlite and a file as a db doesn't make much sense. In order to deploy a stateful app such as MySQL, one would use a Deployment object and connect it to a PersistentVolume, which live in separate nodes.
6. While testing, I initialized data in the `startup` function. For example: `await database.execute(persons.insert().values(first_name='Albert', last_name='Han', email='Albert@han.com'))`

# Comments
I realized doing this over the weekend was probably not the best idea as I didn't have a chance to ask questions. (Last week was a bit hectic for me.) However, had I had the opportunity to, a few questions I would have asked were:

1. How is rate-limiting being done at Reach? I have not found any popular Python rate-limting libraries/packages. Had my deployment via kubernetes been successful, I would have attempted rate-limiting using an Ingress object.
2. I noticed you recommended uvicorn-gunicorn-docker, but as Reach is using FastAPI, why not uvicorn-gunicorn-fastapi-docker?
3. What is the purpose of mixing FastAPI with Flask?

I found this project to be much more beneficial to my learning than completing algorithms on leetcode. Admittedly, I don't have as much exposure to deployment/containerization/orchestration as I would like, which is why I wanted to try to get this fully deployed. I don't regret trying to get the app deployed as it was still a good learning experience. If you know what I am missing, please do let me know.

Thanks for taking the time to view this!