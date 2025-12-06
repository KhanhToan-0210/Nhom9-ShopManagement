const tokenService = require('../services/tokenService');

function authJwt(req, res, next) {
  const authHeader = req.headers['authorization'];
  if (!authHeader) return res.status(401).json({ message: 'Missing Authorization header' });
  const parts = authHeader.split(' ');
  if (parts.length !== 2 || parts[0] !== 'Bearer') return res.status(401).json({ message: 'Invalid Authorization header' });
  const token = parts[1];
  try {
    const payload = tokenService.verify(token);
    req.user = payload;
    next();
  } catch (err) {
    return res.status(401).json({ message: 'Invalid token', detail: err.message });
  }
}

module.exports = authJwt;
