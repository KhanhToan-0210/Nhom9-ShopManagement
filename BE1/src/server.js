const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
require('dotenv').config();

const { sequelize } = require('./models');

const authRoutes = require('./routes/auth');
const productRoutes = require('./routes/products');
const customerRoutes = require('./routes/customers');
const searchRoutes = require('./routes/search');

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.use('/api/auth', authRoutes);
app.use('/api/products', productRoutes);
app.use('/api/customers', customerRoutes);
app.use('/api/search', searchRoutes);

app.get('/', (req, res) => res.json({ ok: true }));

const PORT = process.env.PORT || 4000;

async function start() {
  try {
    await sequelize.authenticate();
    console.log('DB connected');
    // sync models (be careful in production: use migrations)
    await sequelize.sync({ alter: true }); // for dev: sync
    app.listen(PORT, () => console.log(`BE1 running on port ${PORT}`));
  } catch (err) {
    console.error('Startup error', err);
    process.exit(1);
  }
}
start();
