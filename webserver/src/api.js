const utils = require("./utils");
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
    user.config.height = req.body.height;
    user.config.width = req.body.width;

    await utils.editClient(uuid, user);

    return resp.json({
        uuid: user.uuid,
        url: config.url,
        fps: user.config.fps,
        rtmp_port: config.rtmp.port,
        video_size: [user.config.width, user.config.height]
    });
});


module.exports = routes;