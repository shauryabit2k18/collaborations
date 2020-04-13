const express = require('express')
const Time = require('../models/time')
const auth = require('../middleware/auth')
const router = new express.Router()

router.post('/time', auth, async (req, res) => {
    const time = new Time({
        ...req.body,
        owner: req.user._id
    })

    try {
        await time.save()
        res.status(201).send(time)
    } catch (e) {
        res.status(400).send(e)
    }
})


router.get('/times', auth, async (req, res) => {
    console.log(req.user)
    try {
        await req.user.populate({
            path: 'time',
            options: {
                limit: parseInt(req.query.limit),
                skip: parseInt(req.query.skip),
            }
        }).execPopulate()
        res.send(req.user.time)
    } catch (e) {
        res.status(500).send(e)
    }
})

router.get('/time/:id', auth, async (req, res) => {
    const _id = req.params.id

    try {
        const time = await Time.findOne({ _id, owner: req.user._id })

        if (!time) {
            return res.status(404).send()
        }

        res.send(time)
    } catch (e) {
        res.status(500).send()
    }
})


module.exports = router