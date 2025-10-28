# Debugging Login Issue

## Verified Working:
✅ Backend is running
✅ Direct API call works (test_login.py passed)
✅ Credentials are correct: reader_user / ReaderPass123!

## Possible Issues:

### 1. Check Browser Console
Open browser Developer Tools (F12) and check the Console tab for errors.
Look for:
- CORS errors (blocked by CORS policy)
- Network errors (failed to fetch)
- 401 Unauthorized
- 400 Bad Request

### 2. Check Network Tab
In Developer Tools, go to Network tab:
- Look for the request to `http://127.0.0.1:8000/api/token/`
- Check the Request Payload (what password is being sent)
- Check the Response

### 3. Common Causes:

#### A. CORS Issue
Frontend (localhost:3000) → Backend (127.0.0.1:8000)
**Solution:** Backend CORS is already configured for localhost:3000

#### B. Wrong Password
The password field might have extra spaces or wrong characters
**Test:** Try copy-pasting: `ReaderPass123!`

#### C. User Not Active
**Solution:** Run: `python setup_test_data.py` to ensure user is active

## Quick Fix Steps:

1. **Open Browser Console (F12)**
2. **Try to login**
3. **Check what error appears**
4. **Take a screenshot of the Console/Network tab**

## Manual Test:

Open browser console (F12) and paste:

```javascript
fetch('http://127.0.0.1:8000/api/token/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'reader_user',
    password: 'ReaderPass123!'
  })
})
.then(res => res.json())
.then(data => console.log('Success:', data))
.catch(err => console.error('Error:', err));
```

This will show the exact error.
