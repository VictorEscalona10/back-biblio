import { Router } from "express";
import { register, login } from "../controllers/auth.controller.js";
import { registerValidationRules } from "../middlewares/dataFilter.js";
import { validateRegister } from "../middlewares/dataValidation.js";

const router = Router();

router.post('/register', registerValidationRules, validateRegister, register);
router.post('/login', login);

export default router;
