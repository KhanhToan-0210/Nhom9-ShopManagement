const express = require('express');
const router = express.Router();
const customerCtrl = require('../controllers/customerController');
const authJwt = require('../middleware/authJwt');
const roleCheck = require('../middleware/roleCheck');

router.get('/', authJwt, customerCtrl.listCustomers);
router.get('/:id', authJwt, customerCtrl.getCustomer);

router.post('/', authJwt, roleCheck(['ADMIN','STAFF']), customerCtrl.createCustomer);
router.put('/:id', authJwt, roleCheck(['ADMIN','STAFF']), customerCtrl.updateCustomer);

module.exports = router;
