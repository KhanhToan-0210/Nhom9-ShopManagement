module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    id: { type: DataTypes.BIGINT, primaryKey: true, autoIncrement: true },
    username: { type: DataTypes.STRING, unique: true },
    password_hash: { type: DataTypes.STRING },
    email: { type: DataTypes.STRING, unique: true },
    google_id: { type: DataTypes.STRING, unique: true, allowNull: true },
    facebook_id: { type: DataTypes.STRING, unique: true, allowNull: true },
    role: { type: DataTypes.ENUM('ADMIN','STAFF','VIEWER'), defaultValue: 'STAFF' }
  }, {
    tableName: 'users',
    timestamps: true
  });
  return User;
};
