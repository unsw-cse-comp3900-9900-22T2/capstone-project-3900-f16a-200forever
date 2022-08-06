# capstone-project-3900-f16a-200forever
Follow the readme.txt to start servers.
Contact z5247487@ad.unsw.edu.au if you have any problem.

# ENV
VirtualBox (version 6.1.22)

# Requirements
1. python 3.8.10
2. pip (version 22.1.1)
3. nodejs (version v18.2.0 or higher)
4. npm (version 8.9.0 or higher)
5. redis (version 6.2.6 or higher)
6. python modules are listed in requirement.txt
7. react modules are listed under frontend folder

# Installation in VM
(1) Backend setup
Open terminal and go to `/capstone-project-3900-f16a-200forever/backend` directory. Run these commands to install

`sudo apt-get update`

`sudo apt install python3-pip`

`sudo apt install redis-server`

`pip3 install -r requirement.txt`

(2) Frontend setup
Open another terminal and go to `/capstone-project-3900-f16a-200forever/frontend` folder. Run these commands to install

`sudo apt install curl`

`curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -`

`sudo apt-get install -y nodejs`

`npm install`


# How to run the codes
You need 2 terminals
   
(1) Under `/capstone-project-3900-f16a-200forever/backend` folder, to start the backend server, run

`python3 run.py`

(2) Under `/capstone-project-3900-f16a-200forever/frontend` folder, to start the frontend pages, run

`npm start`

# The default port for frontend pages is 3000. You can access pages via the root path
`localhost:3000` or `127.0.0.1:3000`

Happy coding. Please contact me if you have any problem.
