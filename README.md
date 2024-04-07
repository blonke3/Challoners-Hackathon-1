# Challoners-Hackathon-1
This is an electric circuit solver project.

In the front end a display is created of the circuit that the user can generate. This is done using sveltekit.

In the backend (python) there is some code that computes the voltages of the given circuit using some elementary graph theory.

I was inspired to do this project as we covered some of these ideas in our Applied Mathematics course and so I thought it would be a nice revision project!

To run this project yourself, make sure that all of the svelte and python dependencies are installed and then run the python script which will create the server with a backend URL.
Replace the backend URL in the front end in the file Challoners-Hackathon-1/FrontEnd/src/routes/graph/+page.svelte under the function 
