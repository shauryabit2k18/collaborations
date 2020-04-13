const mongoose = require('mongoose')

const TimeSchema = new mongoose.Schema({
    totalTime:{
        type: Number,
        required:true
    },
    usefulTime:{
        type: Number,
        required:true
    },
    wastedTime:{
        type: Number,
        required:true
    },
    owner: {
        type: mongoose.Schema.Types.ObjectId,
        required: true,
        ref: 'User'
    }
}, {
    timestamps: true
})

const Time = mongoose.model('Time', TimeSchema)

module.exports = Time