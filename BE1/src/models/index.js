const sequelize = require('../config/db');
const { DataTypes } = require('sequelize');

const User = require('./user')(sequelize, DataTypes);
const Product = require('./product')(sequelize, DataTypes);
const Customer = require('./customer')(sequelize, DataTypes);

// associations if needed (for BE1, minimal)
module.exports = {
  sequelize,
  User,
  Product,
  Customer
};
