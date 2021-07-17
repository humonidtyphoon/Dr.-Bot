const { spawn } = require('child_process');
const express = require('express')
const bodyParser = require('body-parser');
const app = express()
const port = 5000
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

 app.post("/api/world", (req, res) => {
  childPython = spawn('py', ['script.py', `${req.body.post}`]);
  childPython.stdout.on("data", (data) => {
    console.log(`stdout: ${data}`);
    res.send(`${data}`);
  });
  childPython.stderr.on('data', (data) => 
  {
      console.error(`sctderr: ${data}`);
  });
  childPython.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        });
      }
      );

// // app.post("/api/places", (req, res) => {
//   childPython = spawn('py', ['try.py', 1]);
//   childPython.stdout.on("data", (data) => {
//     console.log(`stdout: ${data}`);
//     // res.send(`${data}`);
//   });
//   childPython.stderr.on('data', (data) => 
//   {
//       console.error(`sctderr: ${data}`);
//   });
//   childPython.on('close', (code) => {
//         console.log(`child process close all stdio with code ${code}`);
//         // send data to browser
//         });



// // });
  
app.listen(port, () => console.log(`Listening on port ${port}`));