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

const writeClients = async (users) => {
    let activated = users.filter(user => user.uuid.split(":")[1] == null).sort((a, b) => a.name > b.name);
    let not_activated = users.filter(user => user.uuid.split(":")[1] != null).sort((a, b) => a.name > b.name);

    await writeJSON("clients", activated.concat(not_activated));
};

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

    await writeClients(users);
    return code;
};

const editClient = async (uuid, new_data) => {
    let users = await allClients();

    users = users.filter(user => user.uuid !== uuid);
    users.push(new_data);

    await writeClients(users);
};

const deleteClient = async (uuid) => {
    let users = await allClients();

    users = users.filter(user => user.uuid !== uuid);

    await writeClients(users);
};

module.exports = { createClient, allClients, editClient, deleteClient };