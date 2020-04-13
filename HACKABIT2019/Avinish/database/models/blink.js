const mongoose = require('mongoose')

const BlinkSchema = new mongoose.Schema({
    time:{
        type: Number,
        required:true
    },
    frequency:{
        type:Number,
        required: true
    },
    owner: {
        type: mongoose.Schema.Types.ObjectId,
        required: true,
        ref: 'User'
    }
}, {
    timestamps: true
})

const Blink = mongoose.model('Blink', BlinkSchema)

module.exports = Blink