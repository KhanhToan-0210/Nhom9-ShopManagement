module.exports = (sequelize, DataTypes) => {
  const Customer = sequelize.define('Customer', {
    id: { type: DataTypes.BIGINT, primaryKey: true, autoIncrement: true },
    customer_code: { type: DataTypes.STRING, unique: true },
    name: { type: DataTypes.STRING, allowNull: false },
    dob: { type: DataTypes.DATEONLY, allowNull: true },
    address: { type: DataTypes.TEXT },
    phone: { type: DataTypes.STRING },
    email: { type: DataTypes.STRING }
  }, {
    tableName: 'customers',
    timestamps: true
  });
  return Customer;
};
