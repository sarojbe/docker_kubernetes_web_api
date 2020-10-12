# docker_kubernetes_web_api
This project aimed at creating a web application that will connect to multiple other APIs( internal and external ) to render data to users.
Primary focus is to have containerized application and hosting the docker images in Google Cloud Registry. 
Both Web application and Api run on Kubernetes cluster 
Major parts to the project:
WebApplication build with Python Flask Framework Bootstrap
Database Mysql
WebAPI  Flask
External APIs
Webapp is intended to run on stanadlone node/vm/container
WebAPI will be hosted in Kubernetes clustered environment with auto scaling

# caveats and limitations
Not a SPA  . Angular/others can be used to redesign the web app part.
API may not be robust enough . No session validation, tokenization added
As the project was intended to have apps run in a containerzed env, the functionalities of the app is kept minimal.

