# capstone-project-3900-f16a-200forever
Follow the readme.txt to start servers.
Contact z5247487@ad.unsw.edu.au if you have any problem.

# Requirements and tools
1. python 3.8
2. pip (version 22.1.1)
3. nodejs (version v18.2.0)
4. npm (version 8.9.0)
5. redis (version 6.2.6)
		if you downloaded the source codes, run `make` under "redis-6.2.6" folder
6. python modules are listed in requirement.txt
		go to /backend folder and run 
			`pip3 install -r requirement.txt`
			OR
			`pip install -r requirement.txt`
7. react modules are listed under frontend folder
		go to /frontend folder and run
			`npm install`

# How to run the codes
You need 3 terminals

(1) If you install redis via other ways, please start the redis server in terminal. If you downloaded the source codes, go to "/redis-6.2.6/src" folder and run 
    `./redis-server`
   
(2) Under "/capstone-project-3900-f16a-200forever/backend" folder, to start the backend server, run
		`python3 run.py`

(3) Under "/capstone-project-3900-f16a-200forever/frontend" folder, to start the frontend pages, run
		`npm start`

# 3. The default port for frontend pages is 3000. You can access pages via the root path
`localhost:3000` or `127.0.0.1:3000`

Happy coding. Please contact me if you have any problem.
