const express = require('express')
const History = require('../models/history')
const auth = require('../middleware/auth')
const router = new express.Router()

router.post('/history', auth, async (req, res) => {
    const history = new History({
        ...req.body,
        owner: req.user._id
    })

    try {
        await history.save()
        res.status(201).send(history)
    } catch (e) {
        res.status(400).send(e)
    }
})


router.get('/allHistory', auth, async (req, res) => {
    console.log(req.user)
    try {
        await req.user.populate({
            path: 'history',
            options: {
                limit: parseInt(req.query.limit),
                skip: parseInt(req.query.skip),
            }
        }).execPopulate()
        res.send(req.user.history)
    } catch (e) {
        res.status(500).send(e)
    }
})

router.get('/history/:id', auth, async (req, res) => {
    const _id = req.params.id

    try {
        const history = await History.findOne({ _id, owner: req.user._id })

        if (!history) {
            return res.status(404).send()
        }

        res.send(history)
    } catch (e) {
        res.status(500).send()
    }
})


module.exports = router