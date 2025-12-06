module.exports = (sequelize, DataTypes) => {
  const Product = sequelize.define('Product', {
    id: { type: DataTypes.BIGINT, primaryKey: true, autoIncrement: true },
    sku: { type: DataTypes.STRING, unique: true },
    name: { type: DataTypes.STRING, allowNull: false },
    description: { type: DataTypes.TEXT },
    price: { type: DataTypes.DECIMAL(13,2), defaultValue: 0 },
    is_hidden: { type: DataTypes.BOOLEAN, defaultValue: false }
  }, {
    tableName: 'products',
    timestamps: true
  });
  return Product;
};
