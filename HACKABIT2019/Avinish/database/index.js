const express = require("express")
require('./mongoose')
const blinkRouter = require('./routers/blink')
const timeRouter = require('./routers/time')
const userRouter = require('./routers/user')
const historyRouter = require('./routers/history')
const rabbitRouter = require('./routers/rabbit')
var amqp = require('amqplib/callback_api');

const port = process.env.PORT || 3001
const app = express()


app.use(express.json())
app.use(blinkRouter)
app.use(timeRouter)
app.use(userRouter)
app.use(historyRouter)



function send(queue,msg)
{
    amqp.connect('amqp://localhost', function(error0, connection) {
                if (error0) {
                throw error0;
                }

                connection.createChannel(function(error1, channel) {
                    if (error1) {
                        throw error1;
                    }

                    channel.assertQueue(queue, {
                    durable: false
                    });


                    channel.sendToQueue(queue, Buffer.from(msg));
                
                });

            });
}

app.get('/website',(req,res)=>{
    const domain = req.query.domain
    const bool = req.query.bool

    const message = {
        domain,
        bool
    }

    const msg= JSON.stringify(message)
    console.log(msg)
    send("website",msg)
    res.send()
})

app.get('/youtube',(req,res)=>{
    const title = req.query.title
    const bool = req.query.bool

    const message = {
        title,
        bool
    }

    const msg= JSON.stringify(message)
    console.log(msg)
    send("youtube",msg)
    res.send()

})


app.get('/process',(req,res)=>{
    const list = req.body
    const bool = req.query.bool

    const message = {
        list: JSON.parse(list),
        bool
    }

    const msg= JSON.stringify(message)
    console.log(msg)
    send("process",msg)
    res.send()

})




app.get('/',(req,res)=>{
    res.send("Hello")
})
app.listen(port, ()=>{
    console.log("Server running on "+port)
})