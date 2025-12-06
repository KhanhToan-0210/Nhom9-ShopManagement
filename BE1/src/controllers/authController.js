const bcrypt = require('bcrypt');
const { User } = require('../models');
const tokenService = require('../services/tokenService');
const { verifyGoogleToken, verifyFacebookToken } = require('../utils/oauthVerify');

const SALT_ROUNDS = 12;

async function register(req, res) {
  try {
    const { username, password, email, role } = req.body;
    if (!username || !password) return res.status(400).json({ message: 'username/password required' });
    const hash = await bcrypt.hash(password, SALT_ROUNDS);
    const user = await User.create({ username, password_hash: hash, email, role: role || 'STAFF' });
    return res.json({ id: user.id, username: user.username, email: user.email });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ message: 'Registration failed', detail: err.message });
  }
}

async function login(req, res) {
  try {
    const { username, password } = req.body;
    if (!username || !password) return res.status(400).json({ message: 'username/password required' });
    const user = await User.findOne({ where: { username } });
    if (!user) return res.status(401).json({ message: 'Invalid credentials' });
    const ok = await bcrypt.compare(password, user.password_hash);
    if (!ok) return res.status(401).json({ message: 'Invalid credentials' });
    const token = tokenService.sign({ id: user.id, username: user.username, role: user.role });
    return res.json({ token, user: { id: user.id, username: user.username, role: user.role } });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Login failed', detail: err.message });
  }
}

async function oauthLogin(req, res) {
  // client sends { provider: 'GOOGLE'|'FACEBOOK', token: '...' }
  try {
    const { provider, token } = req.body;
    if (!provider || !token) return res.status(400).json({ message: 'provider and token required' });

    let profile;
    if (provider === 'GOOGLE') {
      profile = await verifyGoogleToken(token);
      // profile.sub is google id, profile.email
    } else if (provider === 'FACEBOOK') {
      profile = await verifyFacebookToken(token);
    } else {
      return res.status(400).json({ message: 'Unsupported provider' });
    }

    // find or create user
    const email = profile.email || null;
    const externalId = provider === 'GOOGLE' ? profile.sub : profile.id;
    const where = provider === 'GOOGLE' ? { google_id: externalId } : { facebook_id: externalId };

    let user = await User.findOne({ where });
    if (!user && email) {
      // try find by email
      user = await User.findOne({ where: { email } });
    }

    if (!user) {
      // create a user
      const newUser = {
        username: email || `${provider.toLowerCase()}_${externalId}`,
        email,
        role: 'STAFF'
      };
      if (provider === 'GOOGLE') newUser.google_id = externalId;
      if (provider === 'FACEBOOK') newUser.facebook_id = externalId;
      user = await User.create(newUser);
    } else {
      // if user existed by email but doesn't have provider id, set it
      const changes = {};
      if (provider === 'GOOGLE' && !user.google_id) changes.google_id = externalId;
      if (provider === 'FACEBOOK' && !user.facebook_id) changes.facebook_id = externalId;
      if (Object.keys(changes).length) await user.update(changes);
    }

    const jwtToken = tokenService.sign({ id: user.id, username: user.username, role: user.role });
    return res.json({ token: jwtToken, user: { id: user.id, username: user.username, role: user.role } });
  } catch (err) {
    console.error('oauthLogin error', err.message);
    return res.status(500).json({ message: 'OAuth login failed', detail: err.message });
  }
}

module.exports = { register, login, oauthLogin };
