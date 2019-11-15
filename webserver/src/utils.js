const fs = require("fs");
const uuidv4 = require("uuidv4").default;

const readJSON = (name) => new Promise((resolve) => {
    fs.readFile(`${__dirname}/../conf/${name}.json`, (err, data) => {
        if (err) {
            return resolve(null);
        }

        resolve(JSON.parse(data));
    });
});

const writeJSON = (name, data) => new Promise((resolve) => {
    fs.writeFile(`${__dirname}/../conf/${name}.json`, JSON.stringify(data, null, 4), (err) => {
        resolve(err);
    });
});

const allClients = async () => await readJSON("clients") || [];

const createClient = async (name) => {
    let users = await allClients();
    let code = Math.floor(Math.random() * 1000000);

    users.push({
        uuid: `${uuidv4.fromString(name)}:${code}`,
        name,
        status: "offline",
        config: {
            fps: "30"
        }
    });

    writeJSON("clients", users);
    return code;
};

const editClient = async (uuid, new_data) => {
    let users = await allClients();

    users = users.filter(user => user.uuid !== uuid);
    users.push(new_data);

    writeJSON("clients", users);
};

const deleteClient = async (uuid) => {
    let users = await allClients();

    users = users.filter(user => user.uuid !== uuid);

    writeJSON("users", users);
};



module.exports = { createClient, allClients, editClient, deleteClient };