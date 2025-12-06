const { Customer } = require('../models');

async function createCustomer(req, res) {
  try {
    const { customer_code, name, dob, address, phone, email } = req.body;
    const c = await Customer.create({ customer_code, name, dob, address, phone, email });
    res.json(c);
  } catch (err) {
    res.status(500).json({ message: 'Create customer failed', detail: err.message });
  }
}

async function updateCustomer(req, res) {
  try {
    const id = req.params.id;
    const customer = await Customer.findByPk(id);
    if (!customer) return res.status(404).json({ message: 'Not found' });
    await customer.update(req.body);
    res.json(customer);
  } catch (err) {
    res.status(500).json({ message: 'Update failed', detail: err.message });
  }
}

async function getCustomer(req, res) {
  try {
    const id = req.params.id;
    const customer = await Customer.findByPk(id);
    if (!customer) return res.status(404).json({ message: 'Not found' });
    res.json(customer);
  } catch (err) {
    res.status(500).json({ message: 'Get failed', detail: err.message });
  }
}

async function listCustomers(req, res) {
  try {
    const { q, limit = 50, page = 1 } = req.query;
    const where = {};
    if (q) where.name = { [require('sequelize').Op.like]: `%${q}%` };
    const customers = await Customer.findAll({ where, limit: parseInt(limit), offset: (page-1)*limit, order: [['createdAt','DESC']]});
    res.json(customers);
  } catch (err) {
    res.status(500).json({ message: 'List failed', detail: err.message });
  }
}

module.exports = { createCustomer, updateCustomer, getCustomer, listCustomers };
