const axios = require('axios');
require('dotenv').config();

async function verifyGoogleToken(idToken) {
  // Verify token via Google tokeninfo endpoint or Google OAuth2 tokeninfo.
  // https://oauth2.googleapis.com/tokeninfo?id_token=...
  const url = `https://oauth2.googleapis.com/tokeninfo?id_token=${idToken}`;
  const resp = await axios.get(url);
  // resp.data will contain 'aud' (client_id), 'sub' (google id), 'email', etc.
  if (resp.data.aud !== process.env.GOOGLE_CLIENT_ID) {
    throw new Error('Invalid Google client id');
  }
  return resp.data; // contains email, sub, name, picture...
}

async function verifyFacebookToken(accessToken) {
  // Validate token: call debug_token then /me?fields=email,name
  // https://graph.facebook.com/debug_token?input_token={token}&access_token={app_id}|{app_secret}
  const appAccess = `${process.env.FACEBOOK_APP_ID}|${process.env.FACEBOOK_APP_SECRET}`;
  const debugUrl = `https://graph.facebook.com/debug_token?input_token=${accessToken}&access_token=${appAccess}`;
  const dbg = await axios.get(debugUrl);
  if (!dbg.data || !dbg.data.data || !dbg.data.data.is_valid) {
    throw new Error('Invalid Facebook token');
  }
  // fetch profile
  const meUrl = `https://graph.facebook.com/me?fields=id,name,email&access_token=${accessToken}`;
  const me = await axios.get(meUrl);
  return me.data; // { id, name, email }
}

module.exports = { verifyGoogleToken, verifyFacebookToken };
