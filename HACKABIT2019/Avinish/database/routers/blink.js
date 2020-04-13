const express = require('express')
const Blink = require('../models/blink')
const auth = require('../middleware/auth')
const router = new express.Router()

router.post('/blink', auth, async (req, res) => {
    const blink = new Blink({
        ...req.body,
        owner: req.user._id
    })

    try {
        await blink.save()
        res.status(201).send(blink)
    } catch (e) {
        res.status(400).send(e)
    }
})


router.get('/blinks', auth, async (req, res) => {
    console.log(req.user)
    try {
        await req.user.populate({
            path: 'blink',
            options: {
                limit: parseInt(req.query.limit),
                skip: parseInt(req.query.skip),
            }
        }).execPopulate()
        res.send(req.user.blink)
    } catch (e) {
        res.status(500).send(e)
    }
})

router.get('/blink/:id', auth, async (req, res) => {
    const _id = req.params.id

    try {
        const blink = await Blink.findOne({ _id, owner: req.user._id })

        if (!blink) {
            return res.status(404).send()
        }

        res.send(blink)
    } catch (e) {
        res.status(500).send()
    }
})


module.exports = router