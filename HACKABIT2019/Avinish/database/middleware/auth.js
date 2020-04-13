const jwt = require('jsonwebtoken')
const User = require('../models/user')

const auth = async (req, res, next) => {
    // console.log(req.header('Authorization'))

    try {
        // const token = req.header('Authorization').replace('Bearer ', '')
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1ZGFiNmFlMDM3OTQ2ZjMzNmMxYThhMjQiLCJpYXQiOjE1NzE1MTkxNDl9.mg9ZiR__SB3mwq5YSR-CrJUm_m8ZTuXrHFT1JzxkKTU"
        const decoded = jwt.verify(token, "destello")
        // console.log(token)
        const user = await User.findOne({ _id: decoded._id, 'tokens.token': token })
        
        // console.log(user)
        if (!user) {
            throw new Error()
        }

        req.token = token
        req.user = user
        next()
    } catch (e) {
        res.status(401).send(e)
    }
}

module.exports = auth