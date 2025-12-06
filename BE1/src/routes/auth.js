const express = require('express');
const router = express.Router();
const authCtrl = require('../controllers/authController');

router.post('/register', authCtrl.register); // for initial setup (admin creates users)
router.post('/login', authCtrl.login);
router.post('/oauth', authCtrl.oauthLogin); // { provider: 'GOOGLE'|'FACEBOOK', token: '...' }

module.exports = router;
