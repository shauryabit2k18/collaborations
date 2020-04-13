const mongoose = require('mongoose')

const HistorySchema = new mongoose.Schema({
    date: {
        type: String,
        required: true,
        trim: true
    },
    domain: {
        type: String,
        required:true,
        default: false
    },
    bool: {
        type: Boolean,
        required:true,
        default: false
    },
    owner: {
        type: mongoose.Schema.Types.ObjectId,
        required: true,
        ref: 'User'
    }
}, {
    timestamps: true
})

const History = mongoose.model('History', HistorySchema)

module.exports = History