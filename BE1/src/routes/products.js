const express = require('express');
const router = express.Router();
const productCtrl = require('../controllers/productController');
const authJwt = require('../middleware/authJwt');
const roleCheck = require('../middleware/roleCheck');

router.get('/', authJwt, productCtrl.listProducts);
router.get('/:id', authJwt, productCtrl.getProduct);

// Admin/Staff allowed to create/update
router.post('/', authJwt, roleCheck(['ADMIN','STAFF']), productCtrl.createProduct);
router.put('/:id', authJwt, roleCheck(['ADMIN','STAFF']), productCtrl.updateProduct);

module.exports = router;
