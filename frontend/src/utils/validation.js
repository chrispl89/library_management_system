// Form validation utilities

export const validateRequired = (value, fieldName) => {
  if (!value || value.trim() === '') {
    return `${fieldName} is required`;
  }
  return null;
};

export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email) {
    return 'Email is required';
  }
  if (!emailRegex.test(email)) {
    return 'Please enter a valid email address';
  }
  return null;
};

export const validatePassword = (password) => {
  if (!password) {
    return 'Password is required';
  }
  if (password.length < 6) {
    return 'Password must be at least 6 characters long';
  }
  return null;
};

export const validateUsername = (username) => {
  if (!username) {
    return 'Username is required';
  }
  if (username.length < 3) {
    return 'Username must be at least 3 characters long';
  }
  if (!/^[a-zA-Z0-9_]+$/.test(username)) {
    return 'Username can only contain letters, numbers, and underscores';
  }
  return null;
};

export const validateBookForm = (formData) => {
  const errors = {};
  
  const titleError = validateRequired(formData.title, 'Title');
  if (titleError) errors.title = titleError;
  
  const authorError = validateRequired(formData.author, 'Author');
  if (authorError) errors.author = authorError;
  
  const categoryError = validateRequired(formData.category, 'Category');
  if (categoryError) errors.category = categoryError;
  
  return errors;
};

export const validateLoginForm = (formData) => {
  const errors = {};
  
  const usernameError = validateRequired(formData.username, 'Username');
  if (usernameError) errors.username = usernameError;
  
  const passwordError = validateRequired(formData.password, 'Password');
  if (passwordError) errors.password = passwordError;
  
  return errors;
};

export const validateRegisterForm = (formData) => {
  const errors = {};
  
  const usernameError = validateUsername(formData.username);
  if (usernameError) errors.username = usernameError;
  
  const emailError = validateEmail(formData.email);
  if (emailError) errors.email = emailError;
  
  const passwordError = validatePassword(formData.password);
  if (passwordError) errors.password = passwordError;
  
  if (formData.password !== formData.password2) {
    errors.password2 = 'Passwords do not match';
  }
  
  return errors;
};

export const hasErrors = (errors) => {
  return Object.keys(errors).length > 0;
};
