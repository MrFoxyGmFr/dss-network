const utils = require("./utils");
const express = require("express");
const api_routes = require("./api");
const config = require("../conf/config");
const body_parser = require("body-parser");

const server = express();


server.use(body_parser.json());
server.use(body_parser.urlencoded());
server.use(express.static(__dirname + "/../static"));

server.use("/api", api_routes);

server.get("/users", async (req, resp) => {
    let users = await utils.allClients();
    resp.render(__dirname + "/templates/users.ejs", { users, config });
});


server.get("/user/add", async (req, resp) => {
    resp.render(__dirname + "/templates/add_user_get.ejs");
});

server.post("/user/add", async (req, resp) => {
    let name = req.body.name;
    let code = await utils.createClient(name);
    resp.render(__dirname + "/templates/add_user_post.ejs", { name, code });
});


server.get("/user/:uuid", async (req, resp) => {
    let uuid = req.params.uuid;
    let users = await utils.allClients();
    let user = users.find(user => user.uuid === uuid);

    if (user == null) {
        return resp.redirect("/users");
    }

    resp.render(__dirname + "/templates/edit_user.ejs", { user });
});

server.post("/user/:uuid", async (req, resp) => {
    let uuid = req.params.uuid;
    let users = await utils.allClients();
    let user = users.find(user => user.uuid === uuid);

    if (user == null) {
        return resp.redirect("/users");
    }

    resp.render(__dirname + "/templates/edit_user.ejs", { user });
});

server.use("/", (req, resp, next) => {
    if (req.url === "/") {
        return resp.redirect("/users")
    }

    next();
});
server.use("*", (req, resp) => resp.status(404).send("404"));

server.listen(config.express.port, (err) => {
    if (err) {
        return console.error(`Server start failed! Port: ${config.express.port} \n Verbose: ${err}`);
    }

    return console.log(`Server started successfully! Port: ${config.express.port}`);
});
