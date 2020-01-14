//----- SOCKET IO ------
const app = require('express')();
const server = require('http').Server(app);
const io = require('socket.io')(server);

//----- SETUP ----
server.listen(3333, () => {
    console.log("Server listening on port: " + 3333 + ".");
});

io.on('connection', (socket) => {
    console.log(`Socket ${socket.id} connected`);

    socket.on("disconnect", () => {
        console.log(`Socket ${socket.id} disconnected`);
    });

    socket.on("mouse_delta", data => {
        console.log(data);
    });

});
