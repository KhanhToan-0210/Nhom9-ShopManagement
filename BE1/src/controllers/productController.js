const { Product } = require('../models');

async function createProduct(req, res) {
  try {
    const { sku, name, description, price } = req.body;
    const p = await Product.create({ sku, name, description, price });
    res.json(p);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Create product failed', detail: err.message });
  }
}

async function updateProduct(req, res) {
  try {
    const id = req.params.id;
    const product = await Product.findByPk(id);
    if (!product) return res.status(404).json({ message: 'Not found' });
    await product.update(req.body);
    res.json(product);
  } catch (err) {
    res.status(500).json({ message: 'Update failed', detail: err.message });
  }
}

async function getProduct(req, res) {
  try {
    const id = req.params.id;
    const product = await Product.findByPk(id);
    if (!product) return res.status(404).json({ message: 'Not found' });
    res.json(product);
  } catch (err) {
    res.status(500).json({ message: 'Get failed', detail: err.message });
  }
}

async function listProducts(req, res) {
  try {
    const { q, limit = 50, page = 1, includeHidden = false } = req.query;
    const where = {};
    if (q) where.name = { [require('sequelize').Op.like]: `%${q}%` };
    if (!JSON.parse(includeHidden ? 'true' : 'false')) where.is_hidden = false;

    const products = await Product.findAll({ where, limit: parseInt(limit), offset: (page-1)*limit, order: [['createdAt','DESC']]});
    res.json(products);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'List failed', detail: err.message });
  }
}

module.exports = { createProduct, updateProduct, getProduct, listProducts };
