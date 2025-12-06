const express = require('express');
const router = express.Router();
const { Product, Customer } = require('../models');
const authJwt = require('../middleware/authJwt');

router.get('/', authJwt, async (req, res) => {
  try {
    const { q } = req.query;
    if (!q) return res.status(400).json({ message: 'q required' });
    const Op = require('sequelize').Op;
    const [products, customers] = await Promise.all([
      Product.findAll({ where: { name: { [Op.like]: `%${q}%` } }, limit: 20 }),
      Customer.findAll({ where: { name: { [Op.like]: `%${q}%` } }, limit: 20 })
    ]);
    res.json({ products, customers });
  } catch (err) {
    res.status(500).json({ message: 'Search failed', detail: err.message });
  }
});

module.exports = router;
