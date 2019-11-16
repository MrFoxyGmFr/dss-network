const utils = require("./utils");
const config = require("../conf/config");
const Router = require("express").Router;

const routes = Router();

routes.post("/connect/:code", async (req, resp) => {
    let code = req.params.code;
    let users = await utils.allClients();
    let user = users.find(user => user.uuid.split(":")[1] === code);

    if (user == null) {
        return resp.status(403).json({ error: "Connection code wrong" });
    }

    let uuid = user.uuid;
    user.uuid = user.uuid.split(":")[0];
    user.config = {
        fps: user.config.fps,
        video_size: [req.body.width, req.body.height]
    };

    await utils.editClient(uuid, user);

    return resp.json({
        uuid: user.uuid,
        url: config.url,
        rtmp_port: config.rtmp.port,
        ...user.config
    });
});

routes.use("/config/:uuid", async (req, resp) => {
    let user = (await utils.allClients()).find(user => user.uuid === req.params.uuid);

    if (user == null) {
        return resp.json({ error: `user with uuid ${req.params.uuid} not found`});
    }

    user.approved = Date.now();
    await utils.editClient(user.uuid, user);

    return resp.json({
        status: user.status === "online",
        setting: user.config
    });
});

module.exports = routes;