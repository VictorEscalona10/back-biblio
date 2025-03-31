import { validationResult } from 'express-validator';

export const validateRegister = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    const extractedErrors = errors.array().map(err => err.msg);
    return res.status(400).json({error: extractedErrors.join(', ')})
  }
  next();
};

export const validateBooks = (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      const extractedErrors = errors.array().map(err => err.msg);
      return res.status(400).json({error: extractedErrors.join(', ')})
    }
    next();
  };
