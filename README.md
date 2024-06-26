﻿# Challoners-Hackathon-1
This is an electric circuit solver project.

In the front end a display is created of the circuit that the user can generate. This is done using sveltekit.

In the backend (python) there is some code that computes the voltages of the given circuit using some elementary graph theory.

I was inspired to do this project as we covered some of these ideas in our Applied Mathematics course (taught by Professor Darren Crowdy) and so I thought it would be a nice revision project!

To run this project yourself, make sure that all of the svelte and python dependencies are installed and then run the python script which will create the server with a backend URL.
Replace the backend URL in the front end in the file Challoners-Hackathon-1/FrontEnd/src/routes/graph/+page.svelte under the function POST_data with the name of the server it gives you. Then you can run the svelte with npm run dev -- --open and a URL to a localhost should pop up. On that page, you *should* be able to use the project properly! 
Note that if the localhost URL isn't http://localhost:5173/ then you will need to change the URL name in Challoners-Hackathon-1/BackEnd/ under the function handle_options to allow requests to
pass through. 

Unfortunately, this project can only run locally although maybe future versions will be runnable on a proper website.

<img src="https://github.com/blonke3/Challoners-Hackathon-1/assets/93889351/fcfd48fc-f723-489b-b460-bb34997dfa20" width="400">


<img src="https://github.com/blonke3/Challoners-Hackathon-1/assets/93889351/edb5ec09-cac2-4d3a-a7f5-4a327baead94" width="400">
