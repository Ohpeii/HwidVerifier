const express = require('express');

const app = express();

const { join } = require("path");

const { readFileSync } = require("fs");

app.use(express.static('Public'))

app.use("/api", require("./Routes/api"))

app.get('/', (req, res) => {
  res.sendFile(join(process.cwd(), "./html/home.html"))
});


app.listen(JSON.parse(readFileSync("../config.json", "utf8"))["port"], () => console.log('server started'));